import os

class Config:

    def __init__(self, path='/secrets'):
        self.path=path

    def get_value(self, key, default=None):
        if key not in os.listdir(self.path):
            return default
        return open(os.path.join(self.path, key), 'r').read()
