# File

**Attention**: the source File has lower priority than environment variables so any founded environment vars will be used

## Create

Sample config class of the reading file:

```python
class MyConfig(ABConfig):
    __file__ = 'path/to/file'

    auth = {
        'username': str,
        'password': str
    }

    address = str
    port = int

```

## Formats

**ABConfig** will try to determine the format by the file extension.

**Supported:**

<details>
  <summary>Json</summary>
```json
{
	"auth": {
		"username": "user",
		"password": "pass"
	},
	"address": "0.0.0.0",
	"port": 8000
}
```
</details>


<details>
  <summary>Yaml</summary>
```yaml
auth:
  username: user
  password: pass
address: 0.0.0.0
port: 8000
```
</details>

<details>
  <summary>Toml</summary>
```toml
address = "0.0.0.0"
port = 8000

[auth]
username = "user"
password = "pass"
```
</details>

## Settings

- ```__file__``` - the path to the file;

- ```__file_required__``` - require file, otherwise an exception.

Default:

```python
class MyConfig(ABConfig):
    __file__ = False
    __file_required__ = False

```
______

## Also read

- [**Environment**](env.md)
- [**Vault**](vault.md)
