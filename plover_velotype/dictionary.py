"""
    Some abbreviations are used in this source file:
      pref=prefixes
      suff=suffixes
      chars=non-prefix and non-suffix keys
      ic=initial consonants
      fc=final consonants
      v=vowels
"""


from plover import log, system
from plover.steno_dictionary import StenoDictionaryCollection
# from plover.steno import normalize_steno, normalize_stroke
from plover_velotype.system import (
    META_KEYS,
    PREFIX_KEYS, PREFIX_META,
    IC_KEYS, IC_META,
    V_KEYS, V_META,
    FC_KEYS, FC_META,
    SUFFIX_KEYS, SUFFIX_META,
    IC_V_KEYS, IC_V_META,
    V_FC_KEYS, V_FC_META,
    UNDO_STROKE_STENO,
)


class VeloDictionaryCollection:
    def __init__(self, proxy):
        if not isinstance(proxy, StenoDictionaryCollection):
            raise RuntimeError(
                "Trying to proxy something that isn't a StenoDictionaryCollection"
            )
        self.proxy = proxy

    def __getattr__(self, attr):
        return getattr(self.proxy, attr)

    def _extract_space(self, strokes):
        space_state = SPACE_KEY in strokes[-1]
        strokes = strokes[:-1] + (strokes[-1].replace(SPACE_KEY, ''),)
        return strokes, space_state

    def _split_stroke(self, stroke):
        def normalize(stroke):
            if stroke.endswith('-'):
                stroke = stroke[:-1]
            if not stroke:
                return None
            return stroke

        def slice(stroke, start=0, filter=''):
            if len(filter) == 0:
                return None, start
            f_index = 0
            for i, c in enumerate(stroke):
                if i < start:
                    continue
                while c != filter[f_index]:
                    f_index += 1
                    if f_index >= len(filter):
                        return normalize(stroke[start:i]), i
            return normalize(stroke[start:]), len(stroke)

        # filtered keys
        # i_* variables represent the end of sections
        pref, i_pref = slice(stroke, filter=PREFIX_KEYS)
        ic, i_ic = slice(stroke, start=i_pref, filter=IC_KEYS)
        v, i_v = slice(stroke, start=i_ic, filter=V_KEYS)
        fc, i_fc = slice(stroke, start=i_v, filter=FC_KEYS)
        suff, i_suff = slice(stroke, start=i_fc, filter=SUFFIX_KEYS)
        ic_v, i_ic_v = slice(stroke, start=i_pref, filter=IC_V_KEYS)
        v_fc, i_v_fc = slice(stroke, start=i_ic, filter=V_FC_KEYS)
        keys = normalize(stroke[i_pref:i_fc])
        # pref = ''.join(k for k in stroke if k in PREFIX_KEYS)
        # suff = ''.join(k for k in stroke if k in SUFFIX_KEYS)
        # keys = ''.join(k for k in stroke if k not in PREFIX_KEYS or k not in SUFFIX_KEYS)
        # ic = ''.join(k for k in left if k in IC_KEYS)
        # v = ''.join(k for k in keys if k in V_KEYS)
        # fc = ''.join(k for k in dash + right if k in FC_KEYS)

        # qualified keys
        # blank strokes are also filtered out
        q_pref = (PREFIX_META, pref) if pref else None
        q_suff = (SUFFIX_META, suff) if suff else None
        q_keys = (keys,) if keys else None
        q_ic = (IC_META, ic) if ic else None
        q_v = (V_META, v) if v else None
        q_fc = (FC_META, '-' + fc) if fc else None
        q_ic_v = (IC_V_META, ic_v) if ic_v else None
        q_v_fc = (V_FC_META, v_fc) if v_fc else None

        # norm_ic = (META_IC,) + normalize_steno(ic) if ic else None
        # norm_v = (META_V,) + normalize_steno(v) if v and v != '-' else None
        # norm_fc = (META_FC,) + normalize_steno('-' + fc) if fc else None
        # norm_ic_v = (META_ICV,) + normalize_steno(ic + v) if ic and v else None
        # norm_v_fc = (META_VFC,) + normalize_steno(v + fc) if v and fc else None

        # grouped keys
        # all, left, right, each
        group_a = (q_keys,) if q_keys else None
        group_l = (q_ic_v, q_fc) if q_ic_v else None
        group_r = (q_ic, q_v_fc) if q_v_fc else None
        group_e = (q_ic, q_v, q_fc) if q_ic or q_v or q_fc else None

        return (q_pref, q_suff, (group_a, group_l, group_r, group_e))

    def _generic_lookup(self, lookup_fn, strokes, dicts, filters):
        if strokes[-1] == UNDO_STROKE_STENO:
            log.stroke(f'ignoring undo stroke')
            return None

        if full_match := lookup_fn(strokes):
            return full_match

        # TODO remove this once multi-stroke support has been added below
        # or, remove this notice to force split strokes to never use history
        if len(strokes) > 1:
            return None

        pref, suff, stroke_groups = self._split_stroke(strokes[-1])

        pref_match = lookup_fn(pref) if pref else ''
        suff_match = lookup_fn(suff) if suff else ''
        if pref_match is None or suff_match is None:
            log.stroke(f'failed to match prefixes {pref} or suffixes {suff}')
            return None

        for stroke_group in stroke_groups:
            if not stroke_group:
                continue
            matches = list(lookup_fn(s) for s in stroke_group if s)
            if all(matches):
                log.stroke(f'split stroke {strokes} into {stroke_group} and matched {matches}')
                return pref_match + ''.join(matches) + suff_match

        log.stroke(f'failed to split stroke {strokes}')


    def _lookup(self, strokes, dicts=None, filters=()):
        def lookup_fn(v):
            return self.proxy._lookup(v, dicts=dicts, filters=filters)

        return self._generic_lookup(lookup_fn, strokes, dicts, filters)

    def _lookup_from_all(self, strokes, dicts=None, filters=()):
        def lookup_fn(v):
            return self.proxy._lookup_from_all(v, dicts=dicts, filters=filters)

        return self._generic_lookup(lookup_fn, strokes, dicts, filters)

    def lookup(self, strokes):
        return self._lookup(strokes, filters=self.proxy.filters)

    def raw_lookup(self, strokes):
        return self._lookup(strokes)

    def lookup_from_all(self, strokes):
        return self._lookup_from_all(strokes, filters=self.proxy.filters)

    def raw_lookup_from_all(self, strokes):
        return self._lookup_from_all(strokes)
