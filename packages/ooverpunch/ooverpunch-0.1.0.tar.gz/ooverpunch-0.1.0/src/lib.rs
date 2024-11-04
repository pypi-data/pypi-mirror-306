use overpunch::{
    convert_from_signed_format as convert_from_signed_format_rs,
    convert_to_signed_format as convert_to_signed_format_rs, extract as extract_rs,
    format as format_rs, OverpunchError as _OverpunchError,
};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use rust_decimal::Decimal;

struct OverpunchError(_OverpunchError);

impl From<OverpunchError> for PyErr {
    fn from(err: OverpunchError) -> PyErr {
        PyValueError::new_err(format!("{}", err.0))
    }
}

impl From<_OverpunchError> for OverpunchError {
    fn from(other: _OverpunchError) -> Self {
        Self(other)
    }
}

#[pyfunction]
fn convert_from_signed_format(value: &str, format: &str) -> Result<Decimal, OverpunchError> {
    Ok(convert_from_signed_format_rs(value, format).unwrap())
}

#[pyfunction]
fn convert_to_signed_format(value: Decimal, format: &str) -> Result<String, OverpunchError> {
    Ok(convert_to_signed_format_rs(value, format).unwrap())
}

#[pyfunction]
fn extract(value: &str, decimals: usize) -> Result<Decimal, OverpunchError> {
    Ok(extract_rs(value, decimals)?)
}

#[pyfunction]
fn format(value: Decimal, decimals: usize) -> Result<String, OverpunchError> {
    Ok(format_rs(value, decimals)?)
}

#[pymodule]
fn ooverpunch(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(convert_from_signed_format, m)?)?;
    m.add_function(wrap_pyfunction!(convert_to_signed_format, m)?)?;
    m.add_function(wrap_pyfunction!(extract, m)?)?;
    m.add_function(wrap_pyfunction!(format, m)?)?;
    Ok(())
}
