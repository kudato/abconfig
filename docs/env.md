# Environment

## Create

By default, reads only environment variables:

```python
from abconfig import ABConfig

class MyConfig(ABConfig):
    host = str
    port = int

```

define env

```python
import os

os.environ['HOST'] = '127.0.0.1'
os.environ['PORT'] = '8000'
# recreate
config = MyConfig()
config
{'host': '127.0.0.1', 'port': 8000}
```

## Names

Capitalized attribute names are used to search for environment variables, you can also add your own prefix for all variables in the class:

```python
class MyConfig(ABConfig):
    __prefix__ = 'app'
    host = str
    port = int

config = MyConfig()
config
{'host': None, 'port': None}
```

define new env

```python
os.environ['APP_HOST'] = '0.0.0.0'
os.environ['APP_PORT'] = '8000'

config = MyConfig()
config
{'host': '0.0.0.0', 'port': 8000}
```
or
```python
class MyConfig(ABConfig):
    app = {
        'host': str,
        'port': int
    }

config = MyConfig()
config.app
{'host': None, 'port': None}

os.environ['APP_HOST'] = '0.0.0.0'
os.environ['APP_PORT'] = '8000'

config = MyConfig() # recreate
config.app
{'host': '0.0.0.0', 'port': 8000}
```

## Nested dict's

Will also be processed:

```python
class MyConfig(ABConfig):
    db = {
        'host': {
            'master': str
        }
    }

config = MyConfig() # recreate
config.db
{'host': {'master': None}}

os.environ['APP_HOST'] = '0.0.0.0'
os.environ['APP_PORT'] = '8000'

config = MyConfig() # recreate
config
{'host': '0.0.0.0', 'port': 8000}
```

## Settings

- ```__env__``` - on/off bool value;

- ```__prefix__``` - prefix to each attribute in the class.

Default:

```python
class MyConfig(ABConfig):
    __env__ = True
    __prefix__ = None

```
______

## Also read

- [**File**](file.md)
- [**Vault**](vault.md)

