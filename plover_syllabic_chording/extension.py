from plover import log, system

from plover_syllabic_chording import system as syllabic_sys
from plover_syllabic_chording.dictionary import SyllabicDictCollection


class SyllabicExt:
    def __init__(self, engine):
        self.engine = engine

    def proxy_dicts(self, dictionaries):
        if system is syllabic_sys:
            log.info('syllabic chording extension: ignoring non-syllabic system')
            return

        log.info('syllabic chording extension: proxying the dictionary')

        if not isinstance(self.engine.dictionaries, SyllabicDictCollection):
            new_dicts = SyllabicDictCollection(self.engine.dictionaries)
            self.engine._dictionaries = new_dicts
            self.engine._translator.set_dictionary(new_dicts)

    def unproxy_dicts(self):
        if system is syllabic_sys:
            log.info('syllabic chording extension: ignoring non-syllabic system')
            return

        log.info('syllabic chording extension: unproxying the dictionary')

        if isinstance(self.engine.dictionaries, SyllabicDictCollection):
            new_dicts = self.engine.dictionaries._proxy
            self.engine._dictionaries = new_dicts
            self.engine._translator.set_dictionary(new_dicts)

    def start(self):
        log.info('syllabic chording extension: connecting dictionary hook')
        self.engine.hook_connect('dictionaries_loaded', self.proxy_dicts)

    def stop(self):
        log.info('syllabic chording extension: disconnecting dictionary hook')
        self.engine.hook_disconnect('dictionaries_loaded', self.proxy_dicts)
        self.unproxy_dicts()
