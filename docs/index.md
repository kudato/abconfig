## ABConfig helps you easily create great configurations

Import and create class:

```python
from abconfig import ABConfig

class MyConfig(ABConfig):
    host = str
    port = int

```
and create config:
```python
config = MyConfig()
config
{'host': None, 'port': None}
```
[read more.](usage.md)


## Dependencies

**Python 3.6+** and optional:

- pyyaml>=5.1;
- toml>=0.10.0;
- hvac>=0.9.6 - for reading Vault;
- boto3>=1.11.15 - for supports Vault IAM auth.


## Сode and License

- It's [**MIT**](https://github.com/kudato/abconfig/blob/master/LICENSE) licensed and freely [available on github](https://github.com/kudato/abconfig/).

- Please feel free to file an issue on the [bug tracker](https://github.com/kudato/abconfig/issues) if you have found a bug or have some suggestion in order to improve the library.
