"""
    Some abbreviations are used in this source file:
      pref=prefixes
      suff=suffixes
      chars=non-prefix and non-suffix keys
      ic=initial consonants
      fc=final consonants
      v=vowels
"""

import codecs
import collections
import os

try:
    import simplejson as json
except ImportError:
    import json

from dataclasses import dataclass, field
from typing import Optional

from plover import log
from plover.steno_dictionary import StenoDictionary, StenoDictionaryCollection
from plover.steno import normalize_steno
from plover.resource import ASSET_SCHEME, resource_filename, resource_timestamp, resource_update

from plover_velotype.system import (
    PREFIX_G, IC_G, ACC_V_G, FC_G, TV_G, V_G, SYM_G,
    L_COMB_G, R_COMB_G, ALL_G,
    IMPLICIT_HYPHEN_KEYS, UNDO_STROKE_STENO,
) # yapf: disable


def normalize(stroke):
    if not stroke:
        return None
    if stroke.endswith('-'):
        stroke = stroke[:-1]
    if not stroke:
        return None
    return stroke


def extract(template, stroke):
    extracted = []
    stroke_right = False
    templ_right = False
    templ_i = 0

    for k in stroke:
        t = template[templ_i]

        if not stroke_right and (k in IMPLICIT_HYPHEN_KEYS or k == '-'):
            stroke_right = True

        if not templ_right and (t in IMPLICIT_HYPHEN_KEYS or t == '-'):
            templ_right = True

        if stroke_right == templ_right and k == t:
            extracted.append(k)
            templ_i += 1
            if templ_i >= len(template):
                break

    return normalize(''.join(extracted))


def subtract(template, stroke):
    extracted = []
    stroke_right = False
    templ_right = False
    templ_i = 0

    for k in stroke:
        if templ_i < len(template):
            t = template[templ_i]
        else:
            t = None

        if not stroke_right and (k in IMPLICIT_HYPHEN_KEYS or k == '-'):
            stroke_right = True

        if not templ_right and (t in IMPLICIT_HYPHEN_KEYS or t == '-'):
            templ_right = True

        if stroke_right == templ_right and k == t:
            templ_i += 1
        else:
            extracted.append(k)

    return normalize(''.join(extracted))


@dataclass
class VeloBranch:
    keyless: bool
    consuming: bool
    true_skip: int
    unknown1: bool
    unknown2: bool
    false_skip: int

    @classmethod
    def from_velo(cls, d):
        if d is None:
            return None
        return VeloBranch(
            d['keyless'],
            d['consuming'],
            d['true_skip'],
            d['unknown1'],
            d['unknown2'],
            d['false_skip'],
        )


@dataclass
class VeloStroke:
    n: int
    order: int
    keys: str
    mask: Optional[str]
    branch: Optional[VeloBranch]
    output: str

    def __post_init__(self):
        keys_split = self.keys.split('-', 1)
        self.left_keys = keys_split[0]
        self.right_keys = keys_split[1] if len(keys_split) > 1 else ''

    def matches(self, stroke):
        if not stroke:
            return (False, stroke)

        mask = self.mask if self.mask else self.keys
        masked_stroke = extract(mask, stroke)

        if self.keys == masked_stroke:
            new_stroke = subtract(masked_stroke, stroke)
            return (True, new_stroke)

        return (False, stroke)

    @classmethod
    def from_velo(cls, d):
        return VeloStroke(
            d['n'],
            d['ord'],
            normalize(d['keys']),
            normalize(d['mask']),
            VeloBranch.from_velo(d['branch']),
            d['out'],
        )


class VeloDictionary(StenoDictionary):
    readonly = True

    def __init__(self):
        super().__init__()
        del self._dict
        self._list = []

    def _load(self, filename):
        with open(filename, 'rb') as fp:
            contents = fp.read()
        contents = contents.decode('utf-8')
        l = list(json.loads(contents))
        for s in l:
            self._list.append(VeloStroke.from_velo(s))

    def __iter__(self):
        return self._list.__iter__()

    def items(self):
        return list(((s.keys, ), s.output) for s in self._list)

    def get(self, key, fallback=None):
        if 0 <= key < len(self._list):
            return self._list[key]
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

        # if full_match := lookup_fn(strokes):
        #     return full_match

        if len(strokes) > 1:
            return None

        stroke = strokes[0]

        matches = []

        for d in self.velo_dicts:
            skip_counter = 0
            for s in d:
                if skip_counter > 0:
                    skip_counter -= 1
                    continue

                matched, new_stroke = s.matches(stroke)

                if matched:
                    matches.append(s)

                if s.branch is not None:
                    if matched and s.branch.consuming:
                        stroke = new_stroke

                    if matched:
                        skip_counter = s.branch.true_skip
                    else:
                        skip_counter = s.branch.false_skip
                elif matched:
                    stroke = new_stroke

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

