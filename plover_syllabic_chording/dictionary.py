"""
"""

import codecs
import collections
import itertools
import os
from dataclasses import dataclass
from typing import Optional

try:
  import simplejson as json
except ImportError:
  import json

from plover import log
from plover.steno_dictionary import StenoDictionary, StenoDictionaryCollection

from plover_syllabic_chording.system import UNDO_STROKE_STENO
from plover_syllabic_chording.strokes import Stroke, keys_to_bits, bits_to_keys


class SyllabicDict(StenoDictionary):
  readonly = True

  def __init__(self):
    super().__init__()
    del self._dict
    self._strokes = None
    self._longest_key = 1

  def _load(self, filename):
    with open(filename, 'rb') as fp:
      contents = fp.read()
    contents = contents.decode('utf-8')

    obj = json.loads(contents)
    strokes = (Stroke.from_json(s, n=i) for i, s in enumerate(obj))
    filtered = (s for s in strokes if s is not None)
    self._strokes = list(filtered)

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
