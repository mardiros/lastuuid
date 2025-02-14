use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::types::{timezone_utc_bound, PyBytes, PyDateTime, PyModule, PyTzInfo};

use ::uuid7::uuid7 as uuid7gen;

#[pyfunction]
fn uuid7<'py>(py: Python<'py>) -> PyResult<Py<PyAny>> {
    let uuid_module = PyModule::import_bound(py, "uuid")?;
    let uuid_class = uuid_module.getattr("UUID")?;

    let myuuid = uuid7gen();
    let args = ((), PyBytes::new_bound(py, myuuid.as_bytes()));
    let pyuuid = uuid_class.call1(args)?;

    Ok(pyuuid.into())
}

#[pyfunction]
#[pyo3(signature = (uuid, tz=None))]
fn uuid7_to_datetime<'py>(
    py: Python<'py>,
    uuid: Py<PyAny>,
    tz: Option<&Bound<'py, PyTzInfo>>,
) -> PyResult<PyObject> {
    let py_version: Py<PyAny> = uuid.getattr(py, "version")?.into();
    let version: u8 = py_version.extract(py)?;
    if version != 7 {
        return Err(PyValueError::new_err(format!(
            "UUIDv7 expected, received UUIDv{:?}",
            version
        )));
    }

    let py_bytes: Py<PyAny> = uuid.getattr(py, "bytes")?.into();
    let as_bytes: &[u8] = py_bytes.extract(py)?;

    // Extract the first 6 bytes (48 bits) as the timestamp (milliseconds)
    let ms_since_epoch = ((as_bytes[0] as u64) << 40)
        | ((as_bytes[1] as u64) << 32)
        | ((as_bytes[2] as u64) << 24)
        | ((as_bytes[3] as u64) << 16)
        | ((as_bytes[4] as u64) << 8)
        | (as_bytes[5] as u64);

    let datetime = PyDateTime::from_timestamp_bound(
        py,
        ms_since_epoch as f64 / 1000.,
        tz.or(Some(&timezone_utc_bound(py))),
    )?;

    Ok(datetime.into())
}

#[pymodule]
fn lastuuid(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(crate::uuid7, m)?)?;
    m.add_function(wrap_pyfunction!(crate::uuid7_to_datetime, m)?)?;
    Ok(())
}
