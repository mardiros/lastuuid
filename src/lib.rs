use pyo3::prelude::*;
use pyo3::types::{PyModule, PyBytes};

use ::uuid7::{uuid7 as uuid7gen};

#[pyfunction]
fn uuid7<'py>(py: Python<'py>) -> PyResult<Py<PyAny>> {

    let uuid_module = PyModule::import_bound(py, "uuid")?;
    let uuid_class = uuid_module.getattr("UUID")?;

    let myuuid = uuid7gen();
    let args = ((), PyBytes::new_bound(py, myuuid.as_bytes()));
    let pyuuid = uuid_class.call1(args)?;

    Ok(pyuuid.into())
}

#[pymodule]
fn lastuuid(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(crate::uuid7, m)?)?;
    Ok(())
}
