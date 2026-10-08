# Error Handling

> Existential Birds, LLC wrote the original of this file in [beagle](https://github.com/existential-birds/beagle), under the [Apache-2.0 license](../../licenses/beagle-LICENSE.txt). The user changed this file.

`logger` below means the logger the module already uses. Never name a logging package in a finding.

## Defects

### 1. A bare `except:` clause

A bare clause also catches `KeyboardInterrupt` and `SystemExit`.

```python
# BAD
try:
    process()
except:
    pass

# GOOD - the specific type
try:
    process()
except ValueError as error:
    logger.error("invalid value: %s", error)
    raise

# ACCEPTABLE - a boundary that must catch everything
try:
    process()
except Exception as error:
    logger.exception("unexpected error")
    raise
```

### 2. A swallowed exception

```python
# BAD
try:
    result = risky_operation()
except Exception:
    pass

# GOOD - handle it, and record why the default applies
try:
    result = risky_operation()
except OperationError as error:
    logger.warning("operation failed, using default: %s", error)
    result = default_value
```

Teardown and cleanup code is the exception. A handler that logs and continues during shutdown is correct, so never flag it.

### 3. A lost exception chain

```python
# BAD
try:
    parse_config()
except ValueError:
    raise ConfigError("invalid config")

# GOOD
try:
    parse_config()
except ValueError as error:
    raise ConfigError("invalid config") from error
```

### 4. An error message with no context

```python
# BAD
except KeyError:
    raise ValueError("missing key")

# GOOD
except KeyError as error:
    raise ValueError(f"missing required key: {error.args[0]}") from error
```

Context means the identifier, the operation, or the value that failed. It never means a sensitive field. See [house-rules.md](house-rules.md).

## Observation, Not a Defect

### A bare `raise` with no log line

```python
try:
    process(item)
except ProcessError:
    raise
```

A log line here records the failure at this layer. It also duplicates the record when a caller logs the same failure, and duplicate records make a log harder to read. Log once, at the layer that decides what happens. Raise anything else as an observation.

## Review Questions

1. Does any bare `except:` clause exist?
2. Does every re-raise preserve the chain with `raise ... from`?
3. Does every error message carry enough context to diagnose the failure?
4. Does any message or log line carry a sensitive field?
