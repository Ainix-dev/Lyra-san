use pyo3::prelude::*;
use regex::Regex;
use std::collections::HashMap;

/// Ultra-fast text parsing and regex operations for Lyra
#[pyclass]
pub struct TextParser {
    #[pyo3(get)]
    monologue_pattern: String,
    #[pyo3(get)]
    response_pattern: String,
}

#[pymethods]
impl TextParser {
    #[new]
    fn new() -> Self {
        TextParser {
            monologue_pattern: r"\[✦ Internal Monologue\](.*?)\[💬 Response\]".to_string(),
            response_pattern: r"\[💬 Response\](.*?)$".to_string(),
        }
    }

    /// Extract monologue from AI output (fast parallel patterns)
    fn extract_monologue(&self, ai_output: &str) -> PyResult<Option<String>> {
        let patterns = vec![
            r"\[✦ Internal Monologue\](.*?)\[💬 Response\]",
            r"\[Internal Monologue\](.*?)\[Response\]",
            r"✦(.*?)\[💬 Response\]",
        ];

        for pattern_str in patterns {
            if let Ok(regex) = Regex::new(pattern_str) {
                if let Some(caps) = regex.captures(ai_output) {
                    if let Some(m) = caps.get(1) {
                        return Ok(Some(m.as_str().trim().to_string()));
                    }
                }
            }
        }
        Ok(None)
    }

    /// Extract response from AI output (fast parallel patterns)
    fn extract_response(&self, ai_output: &str) -> PyResult<String> {
        let patterns = vec![
            r"\[💬 Response\](.*?)$",
            r"\[Response\](.*?)$",
        ];

        for pattern_str in patterns {
            if let Ok(regex) = Regex::new(pattern_str) {
                if let Some(caps) = regex.captures(ai_output) {
                    if let Some(m) = caps.get(1) {
                        return Ok(m.as_str().trim().to_string());
                    }
                }
            }
        }
        Ok(ai_output.to_string())
    }

    /// Parse multiple patterns at once (optimized)
    fn multi_extract(&self, ai_output: &str) -> PyResult<HashMap<String, Option<String>>> {
        let mut results = HashMap::new();

        // Extract monologue
        if let Ok(Some(mono)) = self.extract_monologue(ai_output) {
            results.insert("monologue".to_string(), Some(mono));
        } else {
            results.insert("monologue".to_string(), None);
        }

        // Extract response
        if let Ok(resp) = self.extract_response(ai_output) {
            results.insert("response".to_string(), Some(resp));
        }

        Ok(results)
    }

    /// Split text at tag boundaries efficiently
    fn split_by_tags(&self, text: &str, tag: &str) -> PyResult<Vec<String>> {
        Ok(text.split(tag)
            .map(|s| s.trim().to_string())
            .filter(|s| !s.is_empty())
            .collect())
    }

    /// Clean and normalize text for processing
    fn normalize(&self, text: &str) -> PyResult<String> {
        let cleaned = text
            .chars()
            .filter(|c| !c.is_control() || c.is_whitespace())
            .collect::<String>()
            .lines()
            .map(|l| l.trim())
            .filter(|l| !l.is_empty())
            .collect::<Vec<_>>()
            .join("\n");
        Ok(cleaned)
    }
}
