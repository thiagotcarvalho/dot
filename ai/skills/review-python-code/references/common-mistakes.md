# Common Mistakes

> Existential Birds, LLC wrote the original of this file in [beagle](https://github.com/existential-birds/beagle), under the [Apache-2.0 license](../../licenses/beagle-LICENSE.txt). The user changed this file.

Import order, whitespace, and line length are absent from this file on purpose. The formatter owns them.

## Contents

1. A mutable default argument
2. `print()` for output
3. A magic number
4. A deep conditional pyramid
5. A dead name
6. Review questions

## Defects

### 1. A mutable default argument

The default object is created once, and every call shares it.

```python
# BAD - the same list serves every call
def add_item(item, items=[]):
    items.append(item)
    return items

add_item("a")  # ["a"]
add_item("b")  # ["a", "b"]

# GOOD
def add_item(item: str, items: list[str] | None = None) -> list[str]:
    if items is None:
        items = []
    items.append(item)
    return items

# GOOD - a dataclass field
@dataclass
class Container:
    items: list[str] = field(default_factory=list)
```

### 2. `print()` for output

`print()` carries no level, no timestamp, and no filter.

```python
# BAD
print(f"processing {order_id}")

# GOOD - the logger the module already uses
logger.info("processing %s", order_id)
```

Use the logger that the module already imports. A review never asks for a new logging package.

### 3. A magic number

```python
# BAD
if len(items) > 100:
    paginate()

# GOOD
MAX_PAGE_SIZE = 100

if len(items) > MAX_PAGE_SIZE:
    paginate()
```

One named constant is also the single authoritative representation of that number. A second copy of the literal is the defect this rule prevents.

### 4. A deep conditional pyramid

```python
# BAD
def process(user):
    if user:
        if user.active:
            if user.verified:
                return do_work(user)
    return None

# GOOD - early returns
def process(user: User | None) -> Result | None:
    if user is None:
        return None
    if not user.active:
        return None
    if not user.verified:
        return None
    return do_work(user)
```

### 5. A dead name

A name that nothing reads is dead code. Delete it.

```python
# BAD
result = process()  # nothing reads result

# GOOD
process()

# GOOD - an ignored element carries the underscore
_, second, _ = get_triple()
```

Run a workspace-wide search first. A decorator, an entry point, or a registry can call a name that no direct caller mentions.

## Review Questions

1. Does any mutable default argument exist?
2. Does `print()` appear where the module has a logger?
3. Does any literal need a named constant?
4. Does an early return flatten a deep pyramid?
5. Does the workspace search confirm that a dead name is truly dead?
