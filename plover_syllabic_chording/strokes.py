from dataclasses import dataclass, field
from typing import Optional, Union
from bitstring import BitArray
from enum import Enum

from plover import log

from plover_syllabic_chording.system import KEYS

ALL_KEYS_MASK = '*'


def split_stroke(stroke: str) -> tuple[str]:
  if stroke is None:
    return ('', '')
  split = stroke.split('-', 1)
  return (split[0], split[1] if len(split) > 1 else '')


def normalize(stroke: Optional[str]) -> Optional[str]:
  if not stroke:
    return None
  if stroke.endswith('-'):
    stroke = stroke[:-1]
  if not stroke:
    return None
  return stroke


def is_left_key(key: str) -> bool:
  return len(key) == 2 and key[1] == '-'


def is_right_key(key: str) -> bool:
  return len(key) == 2 and key[0] == '-'


def is_mid_key(key: str) -> bool:
  return len(key) == 1


def keys_to_bits(keys: Optional[str]) -> Optional[BitArray]:
  if keys is None:
    return None

  if keys == ALL_KEYS_MASK:
    return BitArray(int=-1, length=len(KEYS))

  bits = []

  keys_l, keys_r = split_stroke(keys)
  for key in KEYS:
    if is_left_key(key):
      found = key[:1] in keys_l
    elif is_right_key(key):
      found = key[1:] in keys_r
    elif is_mid_key(key):
      raise RuntimeError('unable to handle middle keys')
    else:
      raise RuntimeError('unknown key')

    if found:
      bits.append(BitArray(bin='1'))
    else:
      bits.append(BitArray(bin='0'))

  assert len(bits) == len(KEYS)

  return BitArray().join(bits)


def bits_to_keys(bits: Optional[BitArray]) -> Optional[str]:
  if bits is None:
    return None

  assert len(bits) == len(KEYS)

  l_keys = []
  r_keys = ['-']

  for bit, key in zip(bits, KEYS):
    if bit:
      if is_left_key(key):
        l_keys.append(key[:1])
      elif is_right_key(key):
        r_keys.append(key[1:])
      elif is_mid_key(key):
        raise RuntimeError('unable to handle middle keys')
      else:
        raise RuntimeError('unknown key')

  return ''.join(l_keys + r_keys)


@dataclass
class Branch:
  jump: Optional[int]
  consume: Optional[bool]

  def __post_init__(self):
    assert isinstance(self.jump, (type(None), int))
    assert isinstance(self.consume, (type(None), bool))
    if self.jump is not None:
      assert self.jump > 0

  def __format__(self, spec):
    consume = 'consumes' if self.consume else None
    jump = f'jump={self.jump}' if self.jump else None
    args = ' '.join(a for a in (consume, jump) if a is not None)
    if spec == 'short':
      return args
    else:
      return 'Branch(' + args + ')'

  def __repr__(self):
    return self.__format__(None)

  def to_json(self):
    return {}

  @classmethod
  def from_json(cls, obj):
    if obj is None:
      return None
    return Branch(jump=obj.get('jump'), consume=obj.get('consume'))


VALID_MODS = ['shift', 'ctrl', 'alt', 'altgr', 'super']
MODS_TO_PLOVER = {
    'shift': 'Shift',
    'ctrl': 'Control',
    'alt': 'Alt',
    'altgr': 'Alt_R',
    'super': 'Super',
}


@dataclass
class String:
  order: int
  mods: Optional[list[str]]
  string: Optional[str]

  @property
  def string_with_mods(self):
    if self.mods is None:
      return self.string

    if self.string is None:
      return None

    start = '#' + ''.join(MODS_TO_PLOVER[m] + '(' for m in self.mods)
    end = ')' * len(self.mods)

    if '#' in self.string:
      return self.string.replace('#', start, 1) + end
    else:
      return '{' + start + self.string + end + '}'

  def __post_init__(self):
    assert isinstance(self.order, int), 'output.order was not int'
    assert isinstance(self.mods, (type(None), list)), 'output.mods was not None/list'
    assert isinstance(self.string, (type(None), str)), 'output.string was not str'
    assert self.order >= 0, 'order must not be negative'
    if self.mods:
      for m in self.mods:
        assert m in VALID_MODS, 'output.mods invalid'

  def __format__(self, spec):
    mods = f' mods={self.mods}' if self.mods else ''
    string = f' string={repr(self.string)}' if self.string else ''
    args = f'order={self.order}{mods}{string}'
    if spec == 'short':
      return args
    else:
      return 'String(' + args + ')'

  def __repr__(self):
    return self.__format__(None)

  def to_json(self):
    obj = {'order': self.order}
    if self.mods:
      obj['mods'] = self.mods
    if self.string:
      obj['string'] = self.string
    return obj

  @classmethod
  def from_json(cls, obj):
    if obj is None:
      return None

    if isinstance(obj, list):
      return list(String.from_json(s) for s in obj)

    return String(order=obj['order'], mods=obj.get('mods'), string=obj.get('string'))


@dataclass
class Stroke:
  n: int
  keys: Optional[str]
  key_bits: Optional[BitArray] = field(init=False)
  wildcard: Optional[str]
  wildcard_bits: Optional[BitArray] = field(init=False)
  mask: Optional[str]
  mask_bits: Optional[BitArray] = field(init=False)
  output: Union[None, String, list[String]]
  if_true: Optional[Branch]
  if_false: Optional[Branch]

  def __post_init__(self):
    assert isinstance(self.n, int), 'n was not int'
    assert isinstance(self.keys, (type(None), str)), 'keys was not None/str'
    assert isinstance(self.wildcard, (type(None), str)), 'wildcard was not None/str'
    assert self.keys is not None or self.wildcard is not None, 'needs keys or wildcard'
    assert isinstance(self.mask, (type(None), str)), 'mask was not None/str'
    assert isinstance(self.output, (type(None), String, list)), 'output was not None/String/list'
    assert isinstance(self.if_true, (type(None), Branch)), 'if_true was not None/Branch'
    assert isinstance(self.if_false, (type(None), Branch)), 'if_false was not None/Branch'
    self.key_bits = keys_to_bits(self.keys)
    self.wildcard_bits = keys_to_bits(self.wildcard)
    self.mask_bits = keys_to_bits(self.mask)
    for field in ['key_bits', 'wildcard_bits', 'mask_bits']:
      value = getattr(self, field)
      assert isinstance(value, (type(None), BitArray)), f'{field} were not None/BitArray'
      assert not value or len(value) == len(KEYS), f'{field} was the wrong length'

  def __format__(self, spec):
    keys = ' keys=' + self.keys if self.keys is not None else ''
    wild = ' wild=' + self.wildcard if self.wildcard is not None else ''

    if self.mask is None:
      mask = ''
    else:
      # output a star if all bits are set
      mask = ' mask=' + (self.mask if (~self.mask_bits) else '*')

    if isinstance(self.output, list):
      outputs = ', '.join(format(o, 'short') for o in self.output)
      string = f' output=[{outputs}]'
    else:
      string = f' output=({self.output:short})' if self.output else ''

    if_true = f' if_true=({self.if_true:short})' if self.if_true else ''
    if_false = f' if_false=({self.if_false:short})' if self.if_false else ''
    args = f'n={self.n}{keys}{wild}{mask}{string}{if_true}{if_false}'

    if spec is None or spec == '':
      return 'Stroke(' + args + ')'
    elif spec == 'short':
      return args
    else:
      raise TypeError('unsupported format string')

  def __repr__(self):
    return self.__format__(None)

  def matches(self, keys: Optional[BitArray]) -> tuple[bool, Optional[BitArray]]:
    if keys is None:
      return (False, keys, self.if_false)

    mask = self.mask or self.keys or self.wildcard
    masked_keys = keys & mask

    if self.keys is not None:
      match = bool(self.keys == masked_keys)
      new_keys = keys & (~mask) if match else keys
    elif self.wildcard is not None:
      matched_keys = self.wildcard & masked_keys
      match = bool(matched_keys)
      new_keys = keys & (~matched_keys) if match else keys
    else:
      raise RuntimeError(f'unsure what to do with stroke {self}')

    branch = self.if_true if match else self.if_false

    return (match, new_keys, branch)

  def to_json(self):
    obj = {}
    if self.keys:
      obj['keys'] = self.keys
    if self.wildcard:
      obj['wildcard'] = self.wildcard
    if self.mask:
      obj['mask'] = self.mask
    if self.output:
      obj['output'] = self.output.to_json()
    if self.if_true:
      obj['if_true'] = self.if_true.to_json()
    if self.if_false:
      obj['if_false'] = self.if_false.to_json()
    return obj

  @classmethod
  def from_json(cls, obj, n=0):
    if obj is None:
      return None

    return Stroke(
        n=n,
        keys=obj.get('keys'),
        wildcard=obj.get('wildcard'),
        mask=obj.get('mask'),
        output=String.from_json(obj.get('output')),
        if_true=Branch.from_json(obj.get('if_true')),
        if_false=Branch.from_json(obj.get('if_false')),
    )


@dataclass
class Lang:
  strokes: list[Stroke]

  def __len__(self):
    return len(self.strokes)

  def to_json(self):
    return list(stroke.to_json() for stroke in self.strokes)

  @classmethod
  def from_json(cls, obj):
    if obj is None:
      return None
    assert isinstance(obj, list)

    strokes = (Stroke.from_json(s, n=i) for i, s in enumerate(obj))
    filtered = (s for s in strokes if s is not None)

    return Lang(strokes)
