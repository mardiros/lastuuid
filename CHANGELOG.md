## 0.4.1  -  2025-12-27

* Readd python3.10 compatibility (downgrade pyo3 to 0.26) 

## 0.4.0  -  2025-12-26

* Create new module for factories. See {mod}`lastuuid.factories`.
* Remove {class}`lastuuid.dummies.LastUUID7Factory`, replaced by
  {class}`lastuuid.factories.LastUUIDFactory`.

## 0.3.3  -  2025-12-24
* Add new dummy helpers for UUID7.
See {func}`lastuuid.dummies.uuid7gen` and {class}`lastuuid.dummies.LastUUID7Factory`
* Drop python 3.9 and 3.10 support
* Update pyo3, and uuid7 rust libraries.

## 0.2.2  -  2025-02-16

* Only improve the documentation. The API of the library does not change. 

## 0.2.1  -  2025-02-15

* Add more utilities in the API, such as {func}`lastuuid.uuid7_to_datetime`,
{func}`lastuuid.utils.uuid7_bounds_from_date`,
{func}`lastuuid.utils.uuid7_bounds_from_datetime`
* Build a documentation available at https://mardiros.github.io/lastuuid/

## 0.1.2  -  2024-12-14

* Build library for windows / python 3.10 for x64 and i686 architecture
* Update readme

## 0.1.1  -  2024-11-10

* Initial release
