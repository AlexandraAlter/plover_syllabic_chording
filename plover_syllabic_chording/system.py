"""
"""

from dataclasses import dataclass

from plover.system import english_stenotype

KEYS = (
    '#-', # shifts
    # left consonants
    'Z-', 'F-', 'S-', 'P-', 'T-', 'C-', 'K-', 'J-', 'R-',
    'L-', 'N-',
    '´-', # accents
    'H-', # caps
    # vowels
    'Y-',
    'I-', 'O-', 'E-',
    "'-", # symbols
    'U-', 'A-',
    '-A', '-U',
    "-'", # symbols
    '-O', '-I', '-E',
    '-Y',
    # right consonants
    '-_', # spacing
    '-`', # accents
    '-N', '-L',
    '-K', '-J', '-R', '-P', '-T', '-C', '-F', '-S', '-Z',
) # yapf: disable


# this is intentionally left empty
IMPLICIT_HYPHEN_KEYS = ()

# this is intentionally left empty
SUFFIX_KEYS = ()

# this is intentionally unused
# there are far too many keys and strokes
NUMBER_KEY = None

# this is intentionally unused
NUMBERS = {}

# this is intentionally unused
FERAL_NUMBER_KEY = False

UNDO_STROKE_STENO = 'SN-NS'

ORTHOGRAPHY_RULES = english_stenotype.ORTHOGRAPHY_RULES
ORTHOGRAPHY_RULES_ALIASES = english_stenotype.ORTHOGRAPHY_RULES_ALIASES

ORTHOGRAPHY_WORDLIST = None

KEYMAPS = {
    'Keyboard': {
                                       'P-': '3',  'K-': '4',  'I-': '5',  "'-": '6',
                           'F-': 'w',  'T-': 'e',  'J-': 'r',  'O-': 't',  'U-': 'y',
        'Z-': ('q', 'a'),  'S-': 's',  'C-': 'd',  'R-': 'f',  'E-': 'g',  'A-': 'h',
                                                   'L-': 'v',  'N-': 'b',  'Y-': 'n',

        "-'": '7',  '-O': '8',  '-K': '9',  '-P': '0',
        '-U': 'u',  '-I': 'i',  '-J': 'o',  '-T': 'p',  '-F': '\\',
        '-A': 'j',  '-E': 'k',  '-R': 'l',  '-C': ';',  '-S': '[',  '-Z': (']', "'"),
        '-Y': 'm',  '-N': ',',  '-L': '.',

        '´-': 'z',  '#-': 'x',  '-`': '/',
        'H-': 'c',  '-_': 'space',

        'arpeggiate': 'Return',
        'no-op': ('`', '1', '2', '-', '='),
    },

    'Gemini PR': {
                                    'P-': '#3',   'K-': '#4',   'I-': '#5',   "'-": '#6',
                      'F-': 'S1-',  'T-': 'T-',   'J-': 'P-',   'O-': 'H-',   'U-': '*1',
        'Z-': 'Fn',   'S-': 'S2-',  'C-': 'K-',   'R-': 'W-',   'E-': 'R-',   'A-': '*2',
                                                  'L-': 'A-',   'N-': 'O-',   'Y-': '#1',

        "-'": '#7',   '-O': '#8',   '-K': '#9',   '-P': '#A',
        '-U': '*3',   '-I': '-F',   '-J': '-P',   '-T': '-L',   '-F': '-T',
        '-A': '*4',   '-E': '-R',   '-R': '-B',   '-C': '-G',   '-S': '-S',   '-Z': '-Z',
        '-Y': '#C',   '-N': '-E',   '-L': '-U',

        '#-': '-D',
        'H-': 'res1', '-_': 'res2',
        '´-': '#2',   '-`': '#B',

        'no-op': (),
    },
} # yapf: disable


DICTIONARIES_ROOT = 'asset:plover_syllabic_chording:assets'
DEFAULT_DICTIONARIES = (
    'syc_user.jsyc',
    'syc_modifiers.jsyc',
    'syc_commands.jsyc',
    'syc_symbols.jsyc',
    'syc_dutch_basic.jsyc',
    'syc_dutch_pro.jsyc',
    'syc_english_basic.jsyc',
    'syc_english_pro.jsyc',
)
