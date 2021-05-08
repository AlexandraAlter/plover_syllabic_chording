
from plover_velotype.dictionary import VeloDictionaryCollection

class VeloExtension:
    def __init__(self, engine):
        self.engine = engine
        self.dictionaries = None
        self.origin_dictionaries = None
        self.engine.hook_connect('dictionaries_loaded', self.proxy_dictionaries)

    def proxy_dictionaries(self, dictionaries):
        print('attaching the dict')
        self.origin_dictionaries = self.engine.dictionaries
        self.dictionaries = VeloDictionaryCollection(self.origin_dictionaries)

        self.engine._dictionaries = self.dictionaries
        self.engine._translator.set_dictionary(self.dictionaries)

    def start(self):
        pass

    def stop(self):
        pass

