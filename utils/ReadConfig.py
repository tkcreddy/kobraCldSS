import json
from utils.singleton import Singleton
import os

class _ReadConfig:

    def __init__(self,base_dir=None):
        if base_dir != None:
            self.base_dir=base_dir
        else:
            self.base_dir='config/'
        self.file_path = os.path.join(self.base_dir, 'config.json')
        self._config_data = None
        self.load_config()
        print(f"Initializing ReadConfig once {self.file_path}")
    @property
    def set_config_dir(self):
        return self.base_dir
    def load_config(self):
        try:
            with open(self.file_path, 'r') as file:
                self._config_data = json.load(file)
        except Exception as e:
            print(f"file open error {e}")

    @property
    def logging_config(self):
        return self._config_data['logging']

    @property
    def kakfa_config(self):
        return self._config_data['kafka']

    @property
    def encryption_config(self):
        return self._config_data['encryption']

class ReadConfig(_ReadConfig,metaclass=Singleton):
        pass
