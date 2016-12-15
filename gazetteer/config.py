__author__ = 'Stefan Schweer'

import yaml

class YamlConfig(object):
    def __init__(self, config='gazetteer.yml'):
        try:
            with open(config) as f:
                entries = yaml.load(f)
            f.close()
        except:
            entries = dict(foo='bar')
        finally:
            self.__dict__.update(entries)
            self.entries = entries

