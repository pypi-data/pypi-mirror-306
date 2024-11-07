//! Definition for contextual entity
//!
//! Contextual entity can be thought of a data object that supplements the
//! metadata of a data entity

use crate::ro_crate::constraints::*;
use crate::ro_crate::modify::*;
use serde::{
    de::{self, MapAccess, Visitor},
    Deserialize, Deserializer, Serialize, Serializer,
};
use std::collections::HashMap;
use std::fmt;

/// Defines a contextual entity - an entity without a local
/// or remote data file that is essential for crate undestanding
#[derive(Debug)]
pub struct ContextualEntity {
    /// Can be a URI but must be some form of local unique identifier for the current
    /// crate. If a local, should prefix with # (e.g {"@id": "#alice"}) or a blank
    /// node (e.g {"@id" : "_alice"})
    pub id: String,
    /// Data type for current contextual entity
    pub type_: DataType,
    /// Optional additional metadata
    pub dynamic_entity: Option<HashMap<String, DynamicEntity>>,
}

impl DynamicEntityManipulation for ContextualEntity {
    /// Implements dynamic entity to allow sharing of modifications between data/ contextual
    fn dynamic_entity(&mut self) -> &mut Option<HashMap<String, DynamicEntity>> {
        &mut self.dynamic_entity
    }
    fn dynamic_entity_immut(&self) -> &Option<HashMap<String, DynamicEntity>> {
        &self.dynamic_entity
    }
}

impl fmt::Display for ContextualEntity {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "ContextualEntity: id={}, type_={:?}, dynamic_entity={:?}",
            self.id, self.type_, self.dynamic_entity
        )
    }
}

/// Enables custom serialisation of known struct fields
impl CustomSerialize for ContextualEntity {
    fn dynamic_entity(&self) -> Option<&HashMap<String, DynamicEntity>> {
        self.dynamic_entity.as_ref()
    }

    fn id(&self) -> &String {
        &self.id
    }

    fn type_(&self) -> &DataType {
        &self.type_
    }
}

/// Inherits serde serialisation and enables custom serialisation for crate creation
impl Serialize for ContextualEntity {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        self.custom_serialize(serializer)
    }
}

/// Custom deserialization implementation for `ContextualEntity`.
///
/// This method provides a tailored approach to convert serialized data
/// (like JSON) into a `ContextualEntity` instance. It employs a `ContextualEntityVisitor`
/// for map-based deserialization.
///
/// The method expects the serialized data to be in a map format (key-value pairs),
/// which is typical for formats like JSON. It specifically looks for `@id` and `@type`
/// keys to fill the corresponding fields of `ContextualEntity`. All other keys are treated
/// as dynamic properties and are stored in a `HashMap`.
impl<'de> Deserialize<'de> for ContextualEntity {
    fn deserialize<D>(deserializer: D) -> Result<Self, D::Error>
    where
        D: Deserializer<'de>,
    {
        struct ContextualEntityVisitor;

        impl<'de> Visitor<'de> for ContextualEntityVisitor {
            type Value = ContextualEntity;

            fn expecting(&self, formatter: &mut fmt::Formatter) -> std::fmt::Result {
                formatter.write_str("a map representing a ContextualEntity")
            }

            fn visit_map<A>(self, mut map: A) -> Result<ContextualEntity, A::Error>
            where
                A: MapAccess<'de>,
            {
                let mut id = None;
                let mut type_ = None;
                let mut dynamic_entity: HashMap<String, DynamicEntity> = HashMap::new();

                while let Some(key) = map.next_key::<String>()? {
                    match key.as_str() {
                        "@id" => id = Some(map.next_value()?),
                        "@type" => type_ = Some(map.next_value()?),
                        _ => {
                            let value: DynamicEntity = map.next_value()?;
                            dynamic_entity.insert(key, value);
                        }
                    }
                }

                let id = id.ok_or_else(|| de::Error::missing_field("@id"))?;
                let type_ = type_.ok_or_else(|| de::Error::missing_field("@type"))?;

                Ok(ContextualEntity {
                    id,
                    type_,
                    dynamic_entity: Some(dynamic_entity),
                })
            }
        }

        deserializer.deserialize_map(ContextualEntityVisitor)
    }
}

/// Tests
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_contextual_entity_creation() {
        let entity = ContextualEntity {
            id: "entity_id".to_string(),
            type_: DataType::Term("ExampleType".to_string()),
            dynamic_entity: Some(HashMap::new()),
        };
        assert_eq!(entity.id, "entity_id");
        assert!(matches!(entity.type_, DataType::Term(ref t) if t == "ExampleType"));
        assert!(entity.dynamic_entity.is_some());
    }

    #[test]
    fn test_add_and_remove_dynamic_entity() {
        let mut entity = ContextualEntity {
            id: "entity_id".to_string(),
            type_: DataType::Term("ExampleType".to_string()),
            dynamic_entity: None,
        };

        // Adding a dynamic entity
        entity.add_string_value("key".to_string(), "value".to_string());
        assert_eq!(
            entity.dynamic_entity().unwrap().get("key"),
            Some(&DynamicEntity::EntityString("value".to_string()))
        );

        // Removing a dynamic entity
        entity.remove_field("key");
        assert!(entity.dynamic_entity().unwrap().get("key").is_none());
    }

    #[test]
    fn test_serialization() {
        let entity = ContextualEntity {
            id: "entity_id".to_string(),
            type_: DataType::Term("ExampleType".to_string()),
            dynamic_entity: None,
        };

        let serialized = serde_json::to_string(&entity).unwrap();
        assert!(serialized.contains("entity_id"));
        assert!(serialized.contains("ExampleType"));
    }

    #[test]
    fn test_deserialization() {
        let json_data = r#"
            {
                "@id": "entity_id",
                "@type": "ExampleType"
            }
        "#;
        let deserialized: ContextualEntity = serde_json::from_str(json_data).unwrap();
        assert_eq!(deserialized.id, "entity_id");
        assert!(matches!(deserialized.type_, DataType::Term(ref t) if t == "ExampleType"));
    }

    #[test]
    fn test_dynamic_entity_serialization() {
        let mut entity = ContextualEntity {
            id: "entity_id".to_string(),
            type_: DataType::Term("ExampleType".to_string()),
            dynamic_entity: None,
        };
        entity.add_string_value("key".to_string(), "value".to_string());

        let serialized = serde_json::to_string(&entity).unwrap();
        assert!(serialized.contains("\"key\":\"value\""));
    }

    #[test]
    fn test_dynamic_entity_deserialization() {
        let json_data = r#"
            {
                "@id": "entity_id",
                "@type": "ExampleType",
                "key": "value"
            }
        "#;
        let deserialized: ContextualEntity = serde_json::from_str(json_data).unwrap();
        assert_eq!(
            deserialized.dynamic_entity.unwrap().get("key"),
            Some(&DynamicEntity::EntityString("value".to_string()))
        );
    }

    #[test]
    fn test_deserialization_with_missing_fields() {
        let json_data = r#"
            {
                "@id": "entity_id"
            }
        "#;
        let result: Result<ContextualEntity, _> = serde_json::from_str(json_data);
        assert!(result.is_err()); // Expecting an error due to missing @type field
    }
}
