"""
"""

from plover.steno_dictionary import StenoDictionary

from plover_syllabic_chording.strokes import Stroke, bits_to_keys


class BaseDictionary(StenoDictionary):
  readonly = True

  def __init__(self):
    super().__init__()
    del self._dict
    self._strokes = None
    self._longest_key = 1

  def _load(self, filename):
    raise NotImplementedError()

  def __iter__(self):
    return self._strokes.__iter__()

  def items_iter(self):
    for s in self._strokes:
      yield ((bits_to_keys(s.keys), ), s.output.string if s.output else '')

  def items(self):
    return list(self.items_iter())

  def get(self, key, fallback=None):
    if 0 <= key < len(self._strokes):
      return self._strokes[key]
    return fallback

  def __contains__(self, key):
    return self.get(key) is not None

  def reverse_lookup(self, value):
    raise NotImplementedError()

  def casereverse_lookup(self, value):
    raise NotImplementedError()

