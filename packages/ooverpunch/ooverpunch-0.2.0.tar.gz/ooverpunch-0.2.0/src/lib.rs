use overpunch::{
    convert_from_signed_format as convert_from_signed_format_rs,
    convert_to_signed_format as convert_to_signed_format_rs, extract as extract_rs,
    format as format_rs,
};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use rust_decimal::Decimal;

#[pyfunction]
fn convert_from_signed_format(value: &str, field_format: &str) -> PyResult<Decimal> {
    convert_from_signed_format_rs(value, field_format).ok_or_else(|| {
        PyValueError::new_err(format!(
            "received None, but expected value when converting {:?} from signed format {:?}",
            value, field_format
        ))
    })
}

#[pyfunction]
fn convert_to_signed_format(value: Decimal, field_format: &str) -> PyResult<String> {
    convert_to_signed_format_rs(value, field_format).ok_or_else(|| {
        PyValueError::new_err(format!(
            "received None, but expected value when converting {:?} to signed format {:?}",
            value, field_format
        ))
    })
}

#[pyfunction]
fn extract(raw: &str, decimals: usize) -> PyResult<Decimal> {
    extract_rs(raw, decimals).map_err(|e| PyValueError::new_err(e.to_string()))
}

#[pyfunction]
fn format(value: Decimal, decimals: usize) -> PyResult<String> {
    format_rs(value, decimals).map_err(|e| PyValueError::new_err(e.to_string()))
}

#[pymodule]
fn ooverpunch(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(convert_from_signed_format, m)?)?;
    m.add_function(wrap_pyfunction!(convert_to_signed_format, m)?)?;
    m.add_function(wrap_pyfunction!(extract, m)?)?;
    m.add_function(wrap_pyfunction!(format, m)?)?;
    Ok(())
}
