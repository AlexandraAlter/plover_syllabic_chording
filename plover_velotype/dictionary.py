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

    # abbreviations: ic=initial consonants, fc=final consonants, v=vowels
    def _split_stroke(self, stroke):
        found_vowels = False
        found_finals = False
        point1 = len(stroke)
        point2 = len(stroke)

        for i, c in enumerate(stroke):
            if not found_vowels and c not in INIT_CON_KEYS:
                found_vowels = True
                point1 = i
            elif found_vowels and c not in VOWEL_KEYS:
                point2 = i
                break

        ic, v, fc = stroke[:point1], stroke[point1:point2], stroke[point2:]

        norm_ic = ('<',) + normalize_steno(ic) if ic else None
        norm_v = ('=',) + normalize_steno(v) if v and v != '-' else None
        norm_fc = ('>',) + normalize_steno('-' + fc) if fc else None
        norm_ic_v = ('<=',) + normalize_steno(ic + v) if ic and v else None
        norm_v_fc = ('=>',) + normalize_steno(v + fc) if v and fc else None

        group_l = (norm_ic_v, norm_fc) if norm_ic_v else None
        group_r = (norm_ic, norm_v_fc) if norm_v_fc else None
        group_a = (norm_ic, norm_v, norm_fc)

        return (group_l, group_r, group_a)

    def _lookup(self, key, dicts=None, filters=()):
        def real_lookup(v):
            return self.proxy._lookup(v, dicts=dicts, filters=filters)

        if full_match := real_lookup(key):
            return full_match

        if len(key) == 1:
            stroke_groups = self._split_stroke(key[0])

            for stroke_group in stroke_groups:
                if not stroke_group or not any(stroke_group):
                    continue
                matches = list(real_lookup(s) if s else '{}' for s in stroke_group)
                print(key, stroke_group, matches)
                if all(matches):
                    return ''.join(matches)

    def _lookup_from_all(self, key, dicts=None, filters=()):
        def real_lookup(v):
            return self.proxy._lookup_from_all(v, dicts=dicts, filters=filters)

        if full_match := real_lookup(key):
            return full_match

        if len(key) == 1:
            stroke_groups = self._split_stroke(key[0])

            for stroke_group in stroke_groups:
                if not stroke_group or not any(stroke_group):
                    continue
                matches = list(real_lookup(s) if s else '{}' for s in stroke_group)
                print(key, stroke_group, matches)
                if all(matches):
                    return ''.join(matches)

    def lookup(self, key):
        return self._lookup(key, filters=self.proxy.filters)

    def raw_lookup(self, key):
        return self._lookup(key)

    def lookup_from_all(self, key):
        return self._lookup_from_all(key, filters=self.proxy.filters)

    def raw_lookup_from_all(self, key):
        return self._lookup_from_all(key)
