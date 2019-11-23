import json

try:
    import yaml
except ImportError:
    pass

try:
    import toml
except ImportError:
    pass

from abconfig.common import Dict


class Reader(Dict):
    def __init__(self, obj: Dict):
        self._obj = obj
        path = obj.get('__file__', False)
        if path != False:
            super().__init__(obj + self._read(path))
        else:
            super().__init__(obj)

    def _read(self, path: str) -> dict:
        try:
            with open(path, 'r') as fd:
                result = self._reader(fd)
                if not isinstance(result, (dict, Dict)):
                    raise IOError
                self._obj.pop('__file__', False)
                return result
        except Exception:
            return self.__mempty__

    def _driver(self, fd) -> dict:
        raise NotImplementedError

# Drivers:

class Yaml(Reader):
    def _driver(self, fd) -> dict:
        return yaml.load(fd, Loader=yaml.FullLoader)


class Json(Reader):
    def _driver(self, fd) -> dict:
        return json.load(fd)


class Toml(Reader):
    def _driver(self, fd) -> dict:
        return toml.load(fd)


class File(Dict):
    __formats__ = (Json, Yaml, Toml)

    def __init__(self, obj: Dict):
        super().__init__(obj.do(*self.__formats__))
