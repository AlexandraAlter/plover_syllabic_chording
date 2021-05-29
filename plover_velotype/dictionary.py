"""
    Some abbreviations are used in this source file:
      pref=prefixes
      suff=suffixes
      chars=non-prefix and non-suffix keys
      ic=initial consonants
      fc=final consonants
      v=vowels
"""

from plover import log
from plover.steno_dictionary import StenoDictionaryCollection
from plover_velotype.system import (
    PREFIX_G,
    IC_G,
    ACC_V_G,
    FC_G,
    TV_G,
    V_G,
    SYM_G,
    L_COMB_G,
    R_COMB_G,
    ALL_G,
    IMPLICIT_HYPHEN_KEYS,
    UNDO_STROKE_STENO,
)


class VeloDictionaryCollection:
    def __init__(self, proxy):
        if not isinstance(proxy, StenoDictionaryCollection):
            raise RuntimeError('Must proxy StenoDictionaryCollection')
        self._proxy = proxy

    def __getattr__(self, attr):
        return getattr(self._proxy, attr)

    def _drop_prefixes(self, stroke):
        """Remove prefixes (NoSpace) from the stroke"""
        s1 = stroke[-1].replace('_', '')
        return (s1, )

    def _split_stroke(self, stroke):
        def normalize(stroke):
            if stroke.endswith('-'):
                stroke = stroke[:-1]
            if not stroke:
                return None
            return stroke

        def qualify(stroke, group):
            norm = normalize(stroke)
            return (group.meta, norm) if norm else None

        def find_midpoint(stroke):
            midpoint_l = None
            midpoint_r = None
            for i, c in enumerate(stroke):
                if (midpoint_l is None
                        and (c in IMPLICIT_HYPHEN_KEYS or c == '-')):
                    midpoint_l = i
                elif (midpoint_l is not None and c not in IMPLICIT_HYPHEN_KEYS
                      and c != '-'):
                    midpoint_r = i
                    break

            if midpoint_l is None:
                midpoint_l = len(stroke)
            if midpoint_r is None:
                midpoint_r = len(stroke)

            return (midpoint_l, midpoint_r)

        def extract(stroke, group, mid_l, mid_r):
            """Extract a sub-stroke according to a group.
            Return a qualified sub-stroke."""
            if not group or not stroke:
                return None

            if group.rhs_only:
                stroke = '-' + stroke[mid_r:]
            elif group.lhs_only:
                stroke = stroke[:mid_l]
            elif not any(c == '-' for c in stroke):
                stroke = stroke[:mid_l] + '-' + stroke[mid_l:]

            filtered = ''.join(c for c in stroke if c in group.keys)

            if filtered == '-':
                return None

            if any(c in IMPLICIT_HYPHEN_KEYS for c in filtered):
                filtered = ''.join(c for c in filtered if c != '-')

            return qualify(filtered, group)

        mid_l, mid_r = find_midpoint(stroke)

        # filtered and qualified keys

        # extracted sections
        pref = extract(stroke, PREFIX_G, mid_l, mid_r)
        ic = extract(stroke, IC_G, mid_l, mid_r)
        acc_v = extract(stroke, ACC_V_G, mid_l, mid_r)
        fc = extract(stroke, FC_G, mid_l, mid_r)

        tv = extract(stroke, TV_G, mid_l, mid_r)
        v = extract(stroke, V_G, mid_l, mid_r)
        sym = extract(stroke, SYM_G, mid_l, mid_r)

        l_comb = extract(stroke, L_COMB_G, mid_l, mid_r)
        r_comb = extract(stroke, R_COMB_G, mid_l, mid_r)
        keys = extract(stroke, ALL_G, mid_l, mid_r)

        # grouped keys
        group_1 = (keys, ) if keys else None
        group_2 = (l_comb, sym, fc) if l_comb else None
        group_3 = (ic, sym, r_comb) if r_comb else None
        group_4 = (ic, acc_v, fc) if ic or acc_v or fc else None
        group_5 = (ic, tv, v, sym, fc) if ic or tv or v or sym or fc else None
        groups = (group_1, group_2, group_3, group_4, group_5)

        log.debug('split stroke %s into prefix %s and groups %s', stroke, pref,
                  groups)
        return (pref, groups)

    def _generic_lookup(self, lookup_fn, strokes, dicts, filters):
        if strokes[-1] == UNDO_STROKE_STENO:
            # ignore the undo stroke
            return None

        if full_match := lookup_fn(strokes):
            return full_match

        # TODO remove this once multi-stroke support has been added below
        # or, remove this notice to force split strokes to never use history
        if len(strokes) > 1:
            return None

        if full_match := lookup_fn(self._drop_prefixes(strokes)):
            return full_match

        pref, stroke_groups = self._split_stroke(strokes[-1])

        pref_match = lookup_fn(pref) if pref else ''
        if pref_match is None:
            log.debug('failed to match prefix %s', pref)
            return None

        for stroke_group in stroke_groups:
            if not stroke_group:
                continue
            matches = list(lookup_fn(s) for s in stroke_group if s)
            if all(matches):
                return pref_match + ''.join(matches)

        log.debug(f'failed to match split stroke')

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
