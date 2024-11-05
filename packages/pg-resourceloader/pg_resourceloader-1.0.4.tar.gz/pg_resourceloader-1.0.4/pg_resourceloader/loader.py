from pg_common import log_info
from pg_objectserialization import loads
from pg_environment import config
from pg_resourceloader.define import *
from pydantic import BaseModel


__all__ = ("Loader", )


class Loader(object):

    def __init__(self, name: str, clazz: BaseModel):
        self.name = name
        self.clazz = clazz
        self.bin_dir = "cfg_bin"
        self.data = {}
        _cfg = config.get_conf(KEY_RESOURCE_LOADER)

        if _cfg:
            if KEY_RESOURCE_LOADER_BIN_DIR in _cfg and _cfg[KEY_RESOURCE_LOADER_BIN_DIR]:
                self.bin_dir = _cfg[KEY_RESOURCE_LOADER_BIN_DIR]

        if not self.bin_dir.startswith("/"):
            self.bin_dir = "%s/%s" % (config.get_pwd(), self.bin_dir)

        self._load()

    def get_by_id(self, _id):
        return self.data[_id] if _id in self.data else None

    def _load(self):
        _name = "%s/%s.bin" % (self.bin_dir, self.name)
        with open(_name, "rb") as _bin:
            _bytes = _bin.read()
            _data = loads(_bytes)
            for _d in _data:
                self.data[_d['id']] = self.clazz(**_d)
                self.load_one(self.data[_d['id']])

        log_info(f"loading cfg {_name} success.")

    def load_one(self, data: BaseModel):
        pass
