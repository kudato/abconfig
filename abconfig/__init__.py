__version__ = '1.0.7'

from collections import UserDict

from abconfig.common import Dict
from abconfig.file import File
from abconfig.env import Env


class Settings:
    __list__ = (
        '__hidesettings__',
        '__file_required__',
        '__file__',
        '__env__',
        '__prefix__',
        '__vault__',
    )

    __hidesettings__ = True
    __file_required__ = False
    __file__ = False
    __env__ = True
    __prefix__ = None
    __vault__ = False


class HideSettings(Dict):
    def __init__(self, obj:Dict):
        if obj.get('__hidesettings__'):
            for k,_ in dict(obj).items():
                if k in Settings.__list__:
                    obj.pop(k)
        super().__init__(obj)


class GetAttrs(Dict):
    def __init__(self, obj: Dict):
        super().__init__({
            str(k): v for k,v in type(obj).__dict__.items()
            if k[:1] != '_' or k in Settings.__list__
        })


class ABConfig(UserDict, Settings):
    __sources__ = (File, Env)

    def __init__(self, obj=None):
        if str(type(self).__name__) == 'ABConfig':
            raise NotImplementedError

        super().__init__(
            GetAttrs(obj if obj else self)
                .do(*self.__sources__)
                .bind(HideSettings)
                .items()
        )
        self.__dict__.update(self)
