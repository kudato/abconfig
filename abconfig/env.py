from os import environ

try:
    import hvac
except ImportError:
    pass

from abconfig.common import Dict


class Environment(Dict):
    def __init__(self, obj: Dict):
        self.__list_separator__ = ','
        super().__init__(obj + self.read(obj, obj.get('__prefix__', None)))

    def read(self, obj: Dict, prefix: str) -> Dict:
        return Dict([self.env(prefix,k,v) for k,v in obj.items()])

    def env(self, prefix: str, k: str, v: any) -> tuple:
        if self.is_dict(v):
            return (k, self.read(v, self.concat(prefix,k)))

        var = environ.get(self.concat(prefix, k).upper(), None)
        if not var: return (k,v)
        if self.is_list(v):
            return (k, self.is_type(v)(var.split(self.__list_separator__)))
        else:
            return (k, self.is_type(v)(var))


    @staticmethod
    def enabled(obj: Dict):
        return obj.get('__env__', True)

    @staticmethod
    def concat(*args: [str], **kwargs):
        s = kwargs.get('space', '_')
        return s.join(filter(lambda x: True if x else False, args))


class Vault(Environment):
    __config = Dict(
        type='json',
        kv_version=2,
        addr='127.0.0.1:8200',
        token=str,
        path=str
    )

    def __init__(self, obj: Dict):
        self._config = self.__config + obj.get('__vault__')
        self._cache = self._request
        if self._config['type'] == 'kv':
            super().__init__(obj + self.read(obj, obj.get('__prefix__')))
        elif self._config['type'] == 'json':
            super().__init__(obj + self._cache)
        else:
            raise ValueError(f'only supported "kv" or "json"')

    def env(self, prefix: str, k: str, v: any) -> tuple:
        key = k if k != '__vault__' else 'vault'
        if self.is_dict(v):
            return (key, self.read(v, self.concat(prefix,key)))
        else:
            return (key, self._cache.get(self.concat(prefix, key).upper(), None))

    @property
    def _request(self) -> dict:
        client = hvac.Client(
            url=self._config['addr'],
            token=self._config['token']
        ).secrets.kv

        if self._config['kv_version'] == 2:
            return client.v2read_secret_version(
                path=self._config['path']
            )['data']['data']
        elif self._config['kv_version'] == 1:
            return client.v1read_secret(
                path=self._config['path']
            )['data']
        else:
            return dict()

    @staticmethod
    def enabled(obj: Dict):
        return Dict.is_dict(obj.get('__vault__'))


class Close(Dict):
    def __init__(self, obj: Dict):
        super().__init__(obj.fmap(self.set_default_type))

    @staticmethod
    def set_default_type(k, v):
        if Dict.is_dict(v):
            return (k, Close(v))
        elif Dict.is_list(v):
            return (k, Dict.is_type(v)([None if isinstance(i, type) else i for i in v]))
        else:
            return (k, None if isinstance(v, type) else v)


class Switch(type):
    def __call__(cls, obj: Dict) -> Dict:
        do = [s for s in cls.__sources__ if s.enabled(obj)]
        return (obj.do(*do) if do else obj).bind(Close)


class Env(metaclass=Switch):
    __sources__ = (Environment, Vault)
