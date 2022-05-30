from plover import log, system
from plover.steno_dictionary import StenoDictionaryCollection

from plover_syllabic_chording import system as syllabic_sys
from plover_syllabic_chording.system import UNDO_STROKE_STENO
from plover_syllabic_chording.strokes import keys_to_bits, bits_to_keys


class SyllabicDictCollection:
  def __init__(self, proxy):
    if not isinstance(proxy, StenoDictionaryCollection):
      raise RuntimeError('Must proxy StenoDictionaryCollection')
    self._proxy = proxy

  def __getattr__(self, attr):
    return getattr(self._proxy, attr)

  def _generic_lookup(self, lookup_fn, strokes, dicts, filters):
    if dicts is None:
      dicts = self.dicts
    stroke_len = len(strokes)
    if stroke_len > self.longest_key:
      return None

    if strokes[-1] == UNDO_STROKE_STENO:
      # ignore the undo stroke
      return None

    # TODO look up the full stroke in non-syllabic dictionaries?

    if len(strokes) > 1:
      return None

    stroke = keys_to_bits(strokes[0])

    matches = []

    for d in dicts:
      if not d.enabled:
        continue
      if stroke_len > d.longest_key:
        continue
      if not isinstance(d, SyllabicDict):
        continue

      skip_counter = 0
      for s in d:
        if skip_counter > 0:
          skip_counter -= 1
          print('Skipping', s)
          continue

        matched, new_stroke, branch = s.matches(stroke)

        if matched:
          print(f'Matched {s}, new_stroke={bits_to_keys(new_stroke)}')
        else:
          print(f'Failed {s}')

        # TODO implement filters here?

        if matched and s.output:
          matches.append(s)

        if branch is not None:
          skip_counter = branch.jump or 0
          if branch.consume:
            stroke = new_stroke
        elif s.output:
          # this is a bit of a shortcut to stop output-less,
          # branch-less strokes from eating input.
          stroke = new_stroke
        else:
          pass

    if stroke and not matches:
      # we did not clear any bit of the stroke
      return None

    matches.sort(key=lambda m: m.output.order)
    value = ''.join(m.output.string for m in matches)

    if stroke and matches:
      # we found some matches, but did not clear every bit of the stroke
      value += bits_to_keys(stroke)

    return value

  def _lookup(self, strokes, dicts=None, filters=()):
    def lookup_fn(v):
      return self._proxy._lookup(v, dicts=dicts, filters=filters)

    return self._generic_lookup(lookup_fn, strokes, dicts, filters)

  def _lookup_from_all(self, strokes, dicts=None, filters=()):
    def lookup_fn(v):
      return self._proxy._lookup_from_all(v, dicts=dicts, filters=filters)

    return self._generic_lookup(lookup_fn, strokes, dicts, filters)

  def lookup(self, strokes):
    return self._lookup(strokes, filters=self._proxy.filters)

  def raw_lookup(self, strokes):
    return self._lookup(strokes)

  def lookup_from_all(self, strokes):
    return self._lookup_from_all(strokes, filters=self._proxy.filters)

  def raw_lookup_from_all(self, strokes):
    return self._lookup_from_all(strokes)


class SyllabicExtension:
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
