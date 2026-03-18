use pyo3::prelude::*;

mod json_handler;
mod text_parser;
mod memory_manager;
mod consciousness_core;

use json_handler::JsonHandler;
use text_parser::TextParser;
use memory_manager::MemoryManager;
use consciousness_core::ConsciousnessCore;

/// Python module for Lyra's core Rust-based features
#[pymodule]
fn lyra_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<JsonHandler>()?;
    m.add_class::<TextParser>()?;
    m.add_class::<MemoryManager>()?;
    m.add_class::<ConsciousnessCore>()?;
    Ok(())
}
