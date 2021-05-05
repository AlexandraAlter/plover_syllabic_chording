from plover.system import english_stenotype

KEYS = (
  'Z-', 'F-', 'S-', 'P-', 'T-', 'C-', 'K-', 'J-', 'R-', 'I-', 'O-', 'E-', "'-", 'U-', 'A-',
  'L-', 'N-', 'Y-', '`-', # shift
  'CAPS',
  'NOSPACE',
  '-L', '-N', '-Y', '-`', # shift
  "'-", 'U-', 'A-', '-O', '-I', '-E', '-K', '-J', '-R', '-P', '-T', '-C', '-F', '-S', '-Z', 
)

IMPLICIT_HYPHEN_KEYS = (,)

SUFFIX_KEYS = (,)

NUMBER_KEY = None

NUMBERS = {}

UNDO_STROKE_STENO = 'SN-NS'

ORTHOGRAPHY_RULES = english_stenotype.ORTHOGRAPHY_RULES
ORTHOGRAPHY_RULES_ALIASES = english_stenotype.ORTHOGRAPHY_RULES_ALIASES

ORTHOGRAPHY_WORDLIST = None

KEYMAPS = {
  'Keyboard': {
    'Z-': 'tab',
    'F-': 'q',
    'S-': 'a',
    'P-': '2',
    'T-': 'w',
    'C-': 's',
    'K-': '3',
    'J-': 'e',
    'R-': 'd',
    'I-': '4',
    'O-': 'r',
    'E-': 'f',
    "'-": '5',
    'U-': 't',
    'A-': 'g',
    'L-': 'c',
    'N-': 'v',
    'Y-': 'b',
    '`-': 'z',
    # shift
    'CAPS': 'alt',
    'NOSPACE': 'space',
    '-L': ',',
    '-N': 'm',
    '-Y': 'n',
    '-`': '/',
    # shift
    "-'": '6',
    '-U': 'y',
    '-A': 'h',
    '-O': '7',
    '-I': 'u',
    '-E': 'j',
    '-K': '8',
    '-J': 'i',
    '-R': 'k',
    '-P': '9',
    '-T': 'o',
    '-C': 'l',
    '-F': 'p',
    '-S': ';',
    '-Z': "'",
    'arpeggiate': 'ralt',
    # Suppress adjacent keys to prevent miss-strokes.
    'no-op': (,),
  },
}

DICTIONARIES_ROOT = 'asset:plover_velotype:assets'
DEFAULT_DICTIONARIES = ('user.json', 'commands.json', 'main.json')
