# {py:mod}`lastuuid.utils`

```{py:module} lastuuid.utils
```

```{autodoc2-docstring} lastuuid.utils
:parser: myst
:allowtitles:
```

## Module Contents

### Functions

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`uuid7_bounds_from_date <lastuuid.utils.uuid7_bounds_from_date>`
  - ```{autodoc2-docstring} lastuuid.utils.uuid7_bounds_from_date
    :parser: myst
    :summary:
    ```
* - {py:obj}`uuid7_bounds_from_datetime <lastuuid.utils.uuid7_bounds_from_datetime>`
  - ```{autodoc2-docstring} lastuuid.utils.uuid7_bounds_from_datetime
    :parser: myst
    :summary:
    ```
````

### API

````{py:function} uuid7_bounds_from_date(dt: datetime.date, tz=UTC) -> tuple[uuid.UUID, uuid.UUID]
:canonical: lastuuid.utils.uuid7_bounds_from_date

```{autodoc2-docstring} lastuuid.utils.uuid7_bounds_from_date
:parser: myst
```
````

````{py:function} uuid7_bounds_from_datetime(dt_lower: datetime.datetime, dt_upper: datetime.datetime | None = None) -> tuple[uuid.UUID, uuid.UUID]
:canonical: lastuuid.utils.uuid7_bounds_from_datetime

```{autodoc2-docstring} lastuuid.utils.uuid7_bounds_from_datetime
:parser: myst
```
````
