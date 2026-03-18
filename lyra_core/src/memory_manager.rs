use pyo3::prelude::*;
use std::collections::VecDeque;

/// Efficient in-memory chat history and context management
#[pyclass]
pub struct MemoryManager {
    #[pyo3(get)]
    max_history: usize,
    history: VecDeque<(String, String)>,
}

#[pymethods]
impl MemoryManager {
    #[new]
    fn new(max_size: usize) -> Self {
        MemoryManager {
            max_history: max_size,
            history: VecDeque::with_capacity(max_size),
        }
    }

    /// Add a message pair to history
    fn add(&mut self, role: String, content: String) -> PyResult<()> {
        self.history.push_back((role, content));
        if self.history.len() > self.max_history {
            self.history.pop_front();
        }
        Ok(())
    }

    /// Get formatted chat history for LLM
    fn get_history(&self) -> PyResult<Vec<(String, String)>> {
        Ok(self.history.iter().cloned().collect())
    }

    /// Get last N messages efficiently
    fn get_last(&self, n: usize) -> PyResult<Vec<(String, String)>> {
        Ok(self.history
            .iter()
            .rev()
            .take(n)
            .cloned()
            .collect::<Vec<_>>()
            .into_iter()
            .rev()
            .collect())
    }

    /// Clear history
    fn clear(&mut self) -> PyResult<()> {
        self.history.clear();
        Ok(())
    }

    /// Get history size
    fn size(&self) -> PyResult<usize> {
        Ok(self.history.len())
    }

    /// Check if history exceeds threshold
    fn should_trim(&self, threshold: usize) -> PyResult<bool> {
        Ok(self.history.len() > threshold)
    }

    /// Trim history to last N items
    fn trim(&mut self, keep_count: usize) -> PyResult<()> {
        while self.history.len() > keep_count {
            self.history.pop_front();
        }
        Ok(())
    }

    /// Search history for keyword
    fn search(&self, keyword: &str) -> PyResult<Vec<String>> {
        let keyword_lower = keyword.to_lowercase();
        Ok(self.history
            .iter()
            .filter(|(_, content)| content.to_lowercase().contains(&keyword_lower))
            .map(|(_, content)| content.clone())
            .collect())
    }
}
