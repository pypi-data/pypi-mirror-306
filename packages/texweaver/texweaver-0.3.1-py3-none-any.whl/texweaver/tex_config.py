import yaml
import importlib.resources as pkg_resources
class TexConfig:
    def __init__(self, config_file = None):
        self.config = {}
        if config_file is not None:
            self.load(config_file)
        else:
            self.load_default()
            
    def load(self, config_file):
        with open(config_file, 'r') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
    
    def load_default(self):
        with pkg_resources.open_text('texweaver', 'default.yaml') as f:
            self.config = yaml.load(f, Loader=yaml.FullLoader)
    
    def apply(self, key, **kwargs):
        if key in self.config:
            return self.config[key].format(**kwargs)
        elif 'content' in kwargs:
            return kwargs['content']
        else:
            return ''
        

DefaultConfig = TexConfig()