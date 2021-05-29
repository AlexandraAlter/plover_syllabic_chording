from plover import log

from plover_velotype.dictionary import VeloDictionaryCollection


class VeloExtension:
    def __init__(self, engine):
        self.engine = engine

    def proxy_dicts(self, dictionaries):
        log.info('velotype extension: proxying the dictionary')

        if not isinstance(self.engine.dictionaries, VeloDictionaryCollection):
            new_dicts = VeloDictionaryCollection(self.engine.dictionaries)
            self.engine._dictionaries = new_dicts
            self.engine._translator.set_dictionary(new_dicts)

    def unproxy_dicts(self):
        log.info('velotype extension: unproxying the dictionary')

        if isinstance(self.engine.dictionaries, VeloDictionaryCollection):
            new_dicts = self.engine.dictionaries._proxy
            self.engine._dictionaries = new_dicts
            self.engine._translator.set_dictionary(new_dicts)

    def start(self):
        log.info('velotype extension: connecting dictionary hook')
        self.engine.hook_connect('dictionaries_loaded', self.proxy_dicts)

    def stop(self):
        log.info('velotype extension: disconnecting dictionary hook')
        self.engine.hook_disconnect('dictionaries_loaded', self.proxy_dicts)
        self.unproxy_dicts()
