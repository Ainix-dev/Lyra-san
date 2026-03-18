use pyo3::prelude::*;
use serde_json::Value;
use std::fs;

/// Fast JSON handler for Lyra's memory and configuration files
#[pyclass]
pub struct JsonHandler;

#[pymethods]
impl JsonHandler {
    /// Load JSON from file with fallback to default
    #[staticmethod]
    fn load(filepath: String, default_data: String) -> PyResult<String> {
        match fs::read_to_string(&filepath) {
            Ok(content) => {
                match serde_json::from_str::<Value>(&content) {
                    Ok(_) => Ok(content),
                    Err(_) => Ok(default_data),
                }
            }
            Err(_) => Ok(default_data),
        }
    }

    /// Save JSON to file with validation
    #[staticmethod]
    fn save(filepath: String, data: String) -> PyResult<bool> {
        match serde_json::from_str::<Value>(&data) {
            Ok(json_value) => {
                let formatted = serde_json::to_string_pretty(&json_value)
                    .unwrap_or(data);
                match fs::write(&filepath, formatted) {
                    Ok(_) => Ok(true),
                    Err(_) => Ok(false),
                }
            }
            Err(_) => Ok(false),
        }
    }

    /// Fast JSON merge operation
    #[staticmethod]
    fn merge(base: String, updates: String) -> PyResult<String> {
        match (
            serde_json::from_str::<Value>(&base),
            serde_json::from_str::<Value>(&updates),
        ) {
            (Ok(mut base_val), Ok(updates_val)) => {
                merge_json(&mut base_val, &updates_val);
                Ok(base_val.to_string())
            }
            _ => Ok(base),
        }
    }

    /// Extract nested JSON values efficiently
    #[staticmethod]
    fn get_path(json_str: String, path: String) -> PyResult<Option<String>> {
        match serde_json::from_str::<Value>(&json_str) {
            Ok(val) => {
                let keys: Vec<&str> = path.split('.').collect();
                let result = keys.iter().fold(Some(&val), |current, key| {
                    current.and_then(|v| v.get(key))
                });
                Ok(result.map(|v| v.to_string()))
            }
            Err(_) => Ok(None),
        }
    }
}

fn merge_json(target: &mut Value, source: &Value) {
    if let Value::Object(ref mut target_map) = target {
        if let Value::Object(source_map) = source {
            for (k, v) in source_map.iter() {
                merge_json(target_map.entry(k.clone()).or_insert(Value::Null), v);
            }
            return;
        }
    }
    *target = source.clone();
}
