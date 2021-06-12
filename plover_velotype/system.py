"""
"""

from dataclasses import dataclass

from plover.system import english_stenotype

KEYS = (
    # LHS consonants fingers
    'Z-', 'F-', 'S-', 'P-', 'T-', 'C-', 'K-', 'J-', 'R-',
    # LHS consonants thumb
    'L-', 'N-',
    # LHS heel
    'H-',
    # Shared vowels thumbs
    'Y-', '-Y',
    # LHS vowels fingers
    'I-', 'O-', 'E-',
    # Shared vowels fingers
    'U-', '-U', 'A-', '-A',
    # RHS vowels fingers
    '-O', '-I', '-E',
    # RHS consonants thumb
    '-N', '-L',
    # RHS consonants fingers
    '-K', '-J', '-R', '-P', '-T', '-C', '-F', '-S', '-Z',
    # Finger syms
    "'-", "-'",
    # thumb syms
    '´-', '-`',
    # shifts
    '-#',
    # RHS heel
    '-_',
    # Function Keys
    '-¹', '-²', '-³', '-⁴', '-⁵', '-⁶', '-⁷', '-⁸', '-⁹', '-ᵃ', '-ᵇ', '-ᶜ',
    # Modifier Keys
    '-✦', '-◆', '-⎈', '-❖',
    # Arrow Keys
    '-↓', '-↑', '-←', '-→',
) # yapf: disable


# this is intentionally left empty
IMPLICIT_HYPHEN_KEYS = ()

# this is intentionally left empty
SUFFIX_KEYS = ()

# this is intentionally unused
# there are far too many keys and strokes
NUMBER_KEY = ''

# this is intentionally unused
NUMBERS = {}

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

        "-'": '6',  '-O': '7',  '-K': '8',  '-P': '9',
        '-U': 'y',  '-I': 'u',  '-J': 'i',  '-T': 'o',  '-F': 'p',
        '-A': 'h',  '-E': 'j',  '-R': 'k',  '-C': 'l',  '-S': ';',  '-Z': ('[', "'"),
        '-Y': 'n',  '-N': 'm',  '-L': ',',

        '´-': 'c',  '-#': ('x', '/'),  '-`': '.',
        'H-': 'z',  '-_': 'space',

        'arpeggiate': 'Return',
        'no-op': ('`', '1', '2', '0', '-', '=', ']', '\\'),
    },

    'Gemini PR': {
                                    'P-': '#3',   'K-': '#4',   'I-': '#5',   "'-": '#6',
                      'F-': 'S1-',  'T-': 'T-',   'J-': 'P-',   'O-': 'H-',   'U-': '*1',
        'Z-': 'res2', 'S-': 'S2-',  'C-': 'K-',   'R-': 'W-',   'E-': 'R-',   'A-': '*2',
                                                  'L-': 'A-',   'N-': 'O-',   'Y-': '#2',

        "-'": '#7',   '-O': '#8',   '-K': '#9',   '-P': '#A',
        '-U': '*3',   '-I': '-F',   '-J': '-P',   '-T': '-L',   '-F': '-T',
        '-A': '*4',   '-E': '-R',   '-R': '-B',   '-C': '-G',   '-S': '-S',   '-Z': '-Z',
        '-Y': '#B',   '-N': '-E',   '-L': '-U',

        '´-': '#1',   '-#': 'Fn', '-`': '#C',
        'H-': 'res1', '-_': '-D',

        'no-op': ('pwr'),
    },
} # yapf: disable

# Normally this kind of duplication would be handled using KEYMAP_MACHINE_TYPE,
#   but due to the way the keymap fallback is done, these layouts would lose their
#   extra keys, so this exists as a patch for that issue.
KEYMAPS_EXTRAS = {
    '-¹': 'F1',
    '-²': 'F2',
    '-³': 'F3',
    '-⁴': 'F4',
    '-⁵': 'F5',
    '-⁶': 'F6',
    '-⁷': 'F7',
    '-⁸': 'F8',
    '-⁹': 'F9',
    '-ᵃ': 'F10',
    '-ᵇ': 'F11',
    '-ᶜ': 'F12',
    'H-': 'F14',
    '-_': 'F15',
    '-#': 'F16',
    '-✦': 'F17',
    '-◆': 'F18',
    '-⎈': 'F19',
    '-❖': 'F20',
    '-↓': 'F21',
    '-↑': 'F22',
    '-←': 'F23',
    '-→': 'F24',
    'no-op': ('F13', ),
}

KEYMAPS['Gemini PR Footpedal'] = KEYMAPS['Gemini PR'].copy()
KEYMAPS['Keyboard Plus'] = KEYMAPS['Keyboard'].copy()

for m in ('Gemini PR Footpedal', 'Keyboard Plus'):
  for k, v in KEYMAPS_EXTRAS.items():
    orig = KEYMAPS[m].get(k)

    if isinstance(v, str):
      v = (v, )
    elif not isinstance(v, tuple):
      raise ValueError('KEYMAP_EXTRAS value was not str or tuple')

    if orig is None:
      KEYMAPS[m][k] = v
    elif isinstance(orig, str):
      KEYMAPS[m][k] = (orig, ) + v
    elif isinstance(orig, tuple):
      KEYMAPS[m][k] = orig + v
    else:
      raise ValueError('KEYMAPS value was not None, str, or tuple')

DICTIONARIES_ROOT = 'asset:plover_velotype:assets'
DEFAULT_DICTIONARIES = (
    'velo_user.velo',
    'velo_english_basic.velo',
)
