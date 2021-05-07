"""

"""

import codecs

try:
    import simplejson as json
except ImportError:
    import json

from plover.steno_dictionary import StenoDictionary, StenoDictionaryCollection
from plover.steno import normalize_steno, normalize_stroke

from plover_velotype.system import INIT_CON_KEYS, VOWEL_KEYS, FINAL_CON_KEYS


class VeloDictionaryCollection:
    def __init__(self, proxy):
        if not isinstance(proxy, StenoDictionaryCollection):
            raise RuntimeError(
                'Trying to proxy something that isn\'t a StenoDictionaryCollection'
            )
        self.proxy = proxy

    def __getattr__(self, attr):
        return getattr(self.proxy, attr)

    def _split_stroke(self, key):
        # TODO this is definitely the wrong way to do this, but for now it'll do
        key = key[-1]

        found_vowels = False
        found_finals = False
        point1 = len(key)
        point2 = len(key)

        for i, c in enumerate(key):
            if not found_vowels and c not in INIT_CON_KEYS:
                found_vowels = True
                point1 = i
            elif found_vowels and c not in VOWEL_KEYS:
                point2 = i
                break

        init_cons, vowels, final_cons = key[:point1], key[point1:point2], key[point2:]

        norm_init_cons = normalize_steno(init_cons) if len(init_cons) > 0 else None
        norm_vowels = normalize_steno(vowels) if len(vowels) > 0 and vowels != '-' else None
        norm_final_cons = normalize_steno('-' + final_cons) if len(final_cons) > 0 else None

        return (norm_init_cons, norm_vowels, norm_final_cons)

    def _lookup(self, key, dicts=None, filters=()):
        def real_lookup(v):
            return self.proxy._lookup(v, dicts=dicts, filters=filters)

        full_match = real_lookup(key)
        if full_match is not None:
            return full_match

        split_stroke = self._split_stroke(key)
        split_stroke_matches = list(real_lookup(s) if s else '{}' for s in split_stroke)

        print(key, split_stroke, split_stroke_matches)
        if all(split_stroke_matches):
            return ''.join(split_stroke_matches)

    def _lookup_from_all(self, key, dicts=None, filters=()):
        def real_lookup(v):
            return self.proxy._lookup_from_all(v, dicts=dicts, filters=filters)

        full_match = real_lookup(key)
        if full_match is not None:
            return full_match

        split_stroke = self._split_stroke(key)
        split_stroke_matches = list(real_lookup(s) if s else '{}' for s in split_stroke)

        print(key, split_stroke, split_stroke_matches)
        if all(split_stroke_matches):
            return ''.join(split_stroke_matches)

    def lookup(self, key):
        return self._lookup(key, filters=self.filters)

    def raw_lookup(self, key):
        return self._lookup(key)
    
    def lookup_from_all(self, key):
        return self._lookup_from_all(key, filters=self.filters)

    def raw_lookup_from_all(self, key):
        return self._lookup_from_all(key)
