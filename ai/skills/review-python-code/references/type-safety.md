# Type Safety

> Existential Birds, LLC wrote the original of this file in [beagle](https://github.com/existential-birds/beagle), under the [Apache-2.0 license](../../licenses/beagle-LICENSE.txt). The user changed this file.

## Defects

### 1. Missing return type

A caller cannot tell what the function gives back.

```python
# BAD
def get_user(user_id: int):
    return User.query.get(user_id)

# GOOD
def get_user(user_id: int) -> User | None:
    return User.query.get(user_id)
```

### 2. `Any` with no forcing reason

`Any` removes the checker from the call site. Keep it only where an untyped boundary forces it.

```python
# BAD
def process(data: Any) -> Any:
    return data

# ACCEPTABLE - the external package ships no stubs
def process(data: Any) -> dict:
    return json.loads(data)

# GOOD - the real types are known
def process(data: str | bytes) -> dict:
    return json.loads(data)
```

A comment on `Any` is welcome when a reader cannot infer the reason. It is not mandatory. The house default is no comment.

### 3. `Optional[T]` instead of `T | None`

```python
# BAD
from typing import Optional, Union
def find(user_id: int) -> Optional[User]: ...
def parse(value: Union[str, int]) -> str: ...

# GOOD
def find(user_id: int) -> User | None: ...
def parse(value: str | int) -> str: ...
```

### 4. A bare collection type

A bare `list` or `dict` loses the element type.

```python
# BAD
def get_items() -> list:
    return [Item(...)]

# GOOD
def get_items() -> list[Item]:
    return [Item(...)]

# BAD
def get_config() -> dict:
    return {"key": "value"}

# GOOD
def get_config() -> dict[str, str]:
    return {"key": "value"}
```

## Observation, Not a Defect

### A plain `dict` that a `TypedDict` could describe

```python
def get_user_data() -> dict[str, str | int]:
    return {"name": "Alice", "age": 30}
```

A `TypedDict` class states the keys, and it helps once several call sites share the shape. For one caller it is speculative structure. Raise it as an observation, and let the author decide.

## Review Questions

1. Does every parameter carry a type?
2. Does every return value carry a type?
3. Does each `Any` sit at a boundary that forces it?
4. Is every collection type generic?
5. Does the code use `T | None` everywhere?
