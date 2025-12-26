# {py:mod}`lastuuid.factories`

```{py:module} lastuuid.factories
```

```{autodoc2-docstring} lastuuid.factories
:parser: myst
:allowtitles:
```

## Module Contents

### Classes

````{list-table}
:class: autosummary longtable
:align: left

* - {py:obj}`LastUUIDFactory <lastuuid.factories.LastUUIDFactory>`
  - ```{autodoc2-docstring} lastuuid.factories.LastUUIDFactory
    :parser: myst
    :summary:
    ```
* - {py:obj}`NewTypeFactory <lastuuid.factories.NewTypeFactory>`
  - ```{autodoc2-docstring} lastuuid.factories.NewTypeFactory
    :parser: myst
    :summary:
    ```
````

### API

`````{py:class} LastUUIDFactory(newtype: typing.Any, id_factory: collections.abc.Callable[[], uuid.UUID] = uuid7, cache_size: int = 10)
:canonical: lastuuid.factories.LastUUIDFactory

Bases: {py:obj}`lastuuid.factories.NewTypeFactory`\[{py:obj}`lastuuid.factories.T`\]

```{autodoc2-docstring} lastuuid.factories.LastUUIDFactory
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} lastuuid.factories.LastUUIDFactory.__init__
:parser: myst
```

````{py:method} __call__(*args: typing.Any, **kwargs: typing.Any) -> lastuuid.factories.T
:canonical: lastuuid.factories.LastUUIDFactory.__call__

```{autodoc2-docstring} lastuuid.factories.LastUUIDFactory.__call__
:parser: myst
```

````

````{py:property} last
:canonical: lastuuid.factories.LastUUIDFactory.last
:type: lastuuid.factories.T

```{autodoc2-docstring} lastuuid.factories.LastUUIDFactory.last
:parser: myst
```

````

````{py:property} lasts
:canonical: lastuuid.factories.LastUUIDFactory.lasts
:type: list[lastuuid.factories.T]

```{autodoc2-docstring} lastuuid.factories.LastUUIDFactory.lasts
:parser: myst
```

````

`````

`````{py:class} NewTypeFactory(newtype: typing.Any, id_factory: collections.abc.Callable[[], uuid.UUID] = uuid7)
:canonical: lastuuid.factories.NewTypeFactory

Bases: {py:obj}`typing.Generic`\[{py:obj}`lastuuid.factories.T`\]

```{autodoc2-docstring} lastuuid.factories.NewTypeFactory
:parser: myst
```

```{rubric} Initialization
```

```{autodoc2-docstring} lastuuid.factories.NewTypeFactory.__init__
:parser: myst
```

````{py:method} __call__(*args: typing.Any, **kwargs: typing.Any) -> lastuuid.factories.T
:canonical: lastuuid.factories.NewTypeFactory.__call__

```{autodoc2-docstring} lastuuid.factories.NewTypeFactory.__call__
:parser: myst
```

````

`````
