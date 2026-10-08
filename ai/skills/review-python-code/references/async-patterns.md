# Async Patterns

> Existential Birds, LLC wrote the original of this file in [beagle](https://github.com/existential-birds/beagle), under the [Apache-2.0 license](../../licenses/beagle-LICENSE.txt). The user changed this file.

Name no replacement package. Use the client, the file API, and the driver that the module already imports. Reach for the standard library before a new dependency.

## Defects

### 1. A blocking call inside `async def`

A blocking call holds the event loop, so every other task waits.

```python
# BAD
async def fetch_data(url: str) -> dict:
    response = requests.get(url)
    time.sleep(1)
    return response.json()

# GOOD - the module's own async client, and the async sleep
async def fetch_data(url: str) -> dict:
    response = await client.get(url)
    await asyncio.sleep(1)
    return response.json()
```

### 2. A coroutine with no `await`

The coroutine object is created, and the body never runs.

```python
# BAD
async def process() -> None:
    fetch_data(url)

# GOOD
async def process() -> None:
    await fetch_data(url)
```

### 3. An async context manager entered with `with`

```python
# BAD
async def query(sql: str) -> Rows:
    session = connect(database)
    return await session.execute(sql)

# GOOD
async def query(sql: str) -> Rows:
    async with connect(database) as session:
        return await session.execute(sql)
```

### 4. Sync file I/O inside `async def`

The read blocks the event loop. The standard library answers this first.

```python
# BAD
async def read_config() -> dict:
    with open("config.json") as handle:
        return json.load(handle)

# GOOD - standard library, no new dependency
async def read_config() -> dict:
    return await asyncio.to_thread(load_config_sync)
```

An async file package is a valid alternative when the module already depends on one. Never introduce that dependency from a review.

## Observation, Not a Defect

### Sequential awaits that could run together

```python
async def get_all() -> tuple[User, Posts, Comments]:
    user = await get_user()
    posts = await get_posts()
    comments = await get_comments()
    return user, posts, comments
```

`asyncio.gather` would overlap these three calls. That is a latency optimisation, and it is correct only when the latency is a stated requirement. Concurrency adds failure modes: partial results, harder cancellation, and interleaved logs. Raise it as an observation.

## Review Questions

1. Does any blocking call sit inside an `async def`?
2. Does every coroutine call have an `await`?
3. Does every async context manager use `async with`?
4. Does any suggested fix add a dependency the module does not already have?
