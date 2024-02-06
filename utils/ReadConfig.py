import json
from utils.singleton import Singleton
import os
#from logpkg.log_decorator import setup_logger,log_to_file
#logger = setup_logger("my_app", log_file="app.log")
class _ReadConfig:
    def __init__(self,base_dir='config/'):
        #BASE_DIR = 'config/'
        self.base_dir=base_dir
        self.file_path = os.path.join(self.base_dir, 'config.json')
        #self.file_path = file_path
        self._config_data = None
        self.load_config()
        print(f"Initializing ReadConfig once {self.file_path}")

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
