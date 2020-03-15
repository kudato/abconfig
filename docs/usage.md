# Usage

## Create

Import **ABConfig** and create a your config class:

```python
from abconfig import ABConfig

class MyConfig(ABConfig):
   host = str
   port = int

```
Get instance:

```python
config = MyConfig()
config
{'host': None, 'port': None}
```
or you can set default values:
```python
class MyConfig(ABConfig):
   host = '127.0.0.1'
   port = 8000

config = MyConfig()
config
{'host': '127.0.0.1', 'port': 8000}
```

## It's [Dict](https://github.com/kudato/abconfig/blob/dff872a15541deefc34b4db36ae9e5d0165b7e7d/abconfig/common.py#L57)

```config``` is a python ```dict```-like instance:
```python
config['host']
None
config.get('port', 8000)
8000
config.items()
ItemsView({'host': None, 'port': None})
```
and by attrs:
```python
config.host
None
```
______

## Supported sources

- [**Environment**](env.md)
- [**File**](file.md)
- [**Vault**](vault.md)

______

## Multiple sources

You can define multiple sources, their values ​​will be use by priority:

1. Default;
2. File;
3. Environment;
4. Vault.


## Common settings

Default values:

- ```__hidesettings__``` - hide ABConfig settings from result;
- ```__hidesettings_exclude__``` - list of settings that need to be shown anyway.

```python
class MyConfig(ABConfig):
    __hidesettings__ = True
    __hidesettings_exclude__ = []

```
