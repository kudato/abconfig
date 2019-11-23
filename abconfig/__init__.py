__version__ = '1.0.3'

from abconfig.common import Dict
from abconfig.file import File
from abconfig.env import Env


class GetAttrs(Dict):
    """ Class attribute reader. """

    __settings__ = ('__prefix__','__env__','__file__')

    def __init__(self, obj: Dict):
        super().__init__({
            str(k): v for k,v in type(obj).__dict__.items()
            if k[:1] != '_' or k in self.__settings__
        })


class ABConfig(Dict):
    """ Abstract base class. """

    __prefix__  = None
    __env__     = True
    __file__    = False

    __sources__ = (GetAttrs, File, Env)

    def __init__(self):
        if str(type(self).__name__) == 'ABConfig':
            raise NotImplementedError

        super().__init__(self.do(*self.__sources__))
        self.__dict__.update(self)
