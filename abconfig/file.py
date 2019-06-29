import yaml
import json

from abconfig.common import Dict
from typing import IO, Type


class Reader(Dict):
    def __init__(self, x: Type[Dict]):
        self.x = x
        file_path = self.x.get('load_file', None)
        if file_path != None:
            super().__init__(x + self._read(file_path))
        else:
            super().__init__(x)

    def _read(self, file_path: str):
        try:
            with open(file_path, 'r') as fd:
                read = self._reader(fd)
                if not isinstance(read, (dict, Dict)):
                    raise IOError
                self.x.pop('load_file', None)
                return read
        except Exception:
            return self.mempty

    def _reader(self, fd: IO[str]):
        raise NotImplementedError


class Yaml(Reader):
    def _reader(self, fd: IO[str]):
        return yaml.load(fd, Loader=yaml.FullLoader)


class Json(Reader):
    def _reader(self, fd: IO[str]):
        return json.load(fd)
