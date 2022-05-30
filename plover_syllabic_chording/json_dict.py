"""
"""

try:
  import simplejson as json
except ImportError:
  import json

from plover_syllabic_chording.strokes import Stroke, bits_to_keys
from plover_syllabic_chording.base_dict import BaseDictionary


class SyllabicJSONEncoder(json.JSONEncoder):
  def encode(self, o):
    assert isinstance(o, list), 'this encoder must take a list'

    strokes = []
    for stroke in o:
      chunks = self.iterencode(stroke, _one_shot=False)
      if not isinstance(chunks, (list, tuple)):
        chunks = list(chunks)
      strokes.append(''.join(chunks))
    return '[\n  ' + ',\n  '.join(strokes) + '\n]'


class JsonDictionary(BaseDictionary):
  def __init__(self):
    super().__init__()

  def _load(self, filename):
    with open(filename, 'rb') as fp:
      contents = fp.read()
    contents = contents.decode('utf-8')

    obj = json.loads(contents)
    strokes = (Stroke.from_json(s, n=i) for i, s in enumerate(obj))
    filtered = (s for s in strokes if s is not None)
    self._strokes = list(filtered)

