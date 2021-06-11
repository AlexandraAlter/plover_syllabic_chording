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

from plover_velotype.system import UNDO_STROKE_STENO
from plover_velotype.strokes import VeloLang, keys_to_bits, bits_to_keys


class VeloDictionary(StenoDictionary):
    readonly = True

    def __init__(self):
        super().__init__()
        del self._dict
        self._lang = None

    def _load(self, filename):
        with open(filename, 'rb') as fp:
            contents = fp.read()
        contents = contents.decode('utf-8')
        self._lang = VeloLang.from_json(json.loads(contents))

    def __iter__(self):
        return self._lang.__iter__()

    def items(self):
        return list(self._lang.as_key_to_stroke())

    def get(self, key, fallback=None):
        if 0 <= key < len(self._lang):
            return self._lang[key]
        return fallback

    def __contains__(self, key):
        return self.get(key) is not None

    def reverse_lookup(self, value):
        raise NotImplementedError()

    def casereverse_lookup(self, value):
        raise NotImplementedError()


class VeloDictionaryCollection:
    def __init__(self, proxy):
        if not isinstance(proxy, StenoDictionaryCollection):
            raise RuntimeError('Must proxy StenoDictionaryCollection')
        self._proxy = proxy

    def __getattr__(self, attr):
        return getattr(self._proxy, attr)

    @property
    def velo_dicts(self):
        return list(d for d in self.dicts if isinstance(d, VeloDictionary))

    def _generic_lookup(self, lookup_fn, strokes, dicts, filters):
        if strokes[-1] == UNDO_STROKE_STENO:
            # ignore the undo stroke
            return None

        # TODO look up the full stroke in non-velo dictionaries?

        if len(strokes) > 1:
            return None

        stroke = strokes[0]
        stroke_bits = keys_to_bits(stroke)

        matches = []

        for d in self.velo_dicts:
            skip_counter = 0
            for s in d:
                if skip_counter > 0:
                    skip_counter -= 1
                    print('Skipping', s)
                    continue

                matched, new_stroke_bits, branch = s.matches(stroke_bits)

                if matched:
                    print(f'Matched {s}, new_stroke={bits_to_keys(new_stroke_bits)}')
                else:
                    print(f'Failed {s}')

                if matched and s.output:
                    matches.append(s)

                if branch is not None:
                    skip_counter = branch.jump
                    if branch.consume:
                        stroke_bits = new_stroke_bits
                else:
                    stroke_bits = new_stroke_bits

        print(matches)
        print(stroke)

        if stroke is not None:
            return None

        matches.sort(key=lambda m: m.order)

        return ''.join(m.output for m in matches)

    def _lookup(self, strokes, dicts=None, filters=()):
        def lookup_fn(v):
            return self._proxy._lookup(v, dicts=dicts, filters=filters)

        return self._generic_lookup(lookup_fn, strokes, dicts, filters)

    def _lookup_from_all(self, strokes, dicts=None, filters=()):
        def lookup_fn(v):
            return self._proxy._lookup_from_all(v,
                                                dicts=dicts,
                                                filters=filters)

        return self._generic_lookup(lookup_fn, strokes, dicts, filters)

    def lookup(self, strokes):
        return self._lookup(strokes, filters=self._proxy.filters)

    def raw_lookup(self, strokes):
        return self._lookup(strokes)

    def lookup_from_all(self, strokes):
        return self._lookup_from_all(strokes, filters=self._proxy.filters)

    def raw_lookup_from_all(self, strokes):
        return self._lookup_from_all(strokes)
