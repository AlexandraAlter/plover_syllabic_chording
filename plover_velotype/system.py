"""
    Some abbreviations are used in this source file:
      ic=initial consonants
      fc=final consonants
      v=vowels
"""

from plover.system import english_stenotype

# ZFSPTCKJR LN H ´ IOE 'UAY# OIE ` NL KJRPTCFSZ _

KEYS = (
    # Modifier keys
    '⇧-', '⎈-', '◆-', '❖-', '✦-',
    # RHS heel
    '_-',
    # LHS consonants fingers
    'Z-', 'F-', 'S-', 'P-', 'T-', 'C-', 'K-', 'J-', 'R-',
    # LHS consonants thumb
    'L-', 'N-',
    # LHS heel
    'H-',
    # LHS syms thumb
    '´-',
    # LHS vowels fingers
    'I-', 'O-', 'E-',
    # Shared vowels fingers
    "'", 'U', 'A',
    # Shared vowels thumb
    'Y',
    # shifts
    '#',
    # RHS vowels fingers
    '-O', '-I', '-E',
    # RHS syms thumb
    '-`',
    # RHS consonants thumb
    '-N', '-L',
    # RHS consonants fingers
    '-K', '-J', '-R', '-P', '-T', '-C', '-F', '-S', '-Z',
)

# not part of the system definition, used in the Velotype Extension
META_KEYS = '«<=>»' # these should not be used, as they mark special strokes

# these MUST be in steno order because of assumptions made in the extension
PREFIX_KEYS = '⇧⎈◆❖✦_'
PREFIX_META = '«'
IC_KEYS = 'ZFSPTCKJRLNH'
IC_META = '<'
V_KEYS = "´IOE-'UAY#OIE`"
V_META = '='
FC_KEYS = 'NLKJRPTCFSZ'
FC_META = '>'
SUFFIX_KEYS = ''
SUFFIX_META = '»'

IC_V_KEYS = IC_KEYS + V_KEYS
IC_V_META = IC_META + V_META
V_FC_KEYS = V_KEYS + FC_KEYS
V_FC_META = V_META + FC_META
# end of custom section

# this is intentionally left empty, as it might break the dictionary
IMPLICIT_HYPHEN_KEYS = ()

# this is intentionally left empty
SUFFIX_KEYS = ()

NUMBER_KEY = '#'

NUMBERS = {
    'Z-': '@-',
    'F-': '£-',
    'S-': '$-',
    'P-': '%-',
    'T-': 's-', # should be '/', but that is an invalid stroke
    'C-': '(-',
    'K-': '&-',
    'J-': '*-',
    'R-': '+-',
    'L-': '€-',
    'N-': ',-',
    '´-': '~-',
    'I-': '7-',
    'O-': '4-',
    'E-': '1-',
    "'": '8',
    'U': '5',
    'A': '2',
    'Y': '0',
    '-O': '-9',
    '-I': '-6',
    '-E': '-3',
    '-`': '-¨',
    '-N': '-.',
    '-L': '-_',
    '-K': '-?',
    '-J': '-e', # should be '=', but that is used for special purposes
    '-R': '-d', # should be '-', but that is an invalid stroke
    '-P': '-!',
    '-T': '-;',
    '-C': '-)',
    '-F': "-'",
    '-S': '-:',
    '-Z': '-h', # should be '#', but that is already a stroke
}

UNDO_STROKE_STENO = 'SN-NS'

ORTHOGRAPHY_RULES = english_stenotype.ORTHOGRAPHY_RULES
ORTHOGRAPHY_RULES_ALIASES = english_stenotype.ORTHOGRAPHY_RULES_ALIASES

ORTHOGRAPHY_WORDLIST = None

KEYMAPS = {
    'Keyboard': {
        '⇧-': 'F4',
        '⎈-': 'F5',
        '◆-': 'F6',
        '❖-': 'F7',
        '✦-': 'F8',
        '_-': 'space',
        'Z-': 'a',
        'F-': 'w',
        'S-': 's',
        'P-': '3',
        'T-': 'e',
        'C-': 'd',
        '´-': 'c',
        'K-': '4',
        'J-': 'r',
        'R-': 'f',
        'L-': 'v',
        'I-': '5',
        'O-': 't',
        'E-': 'g',
        'N-': 'b',
        'H-': 'z',
        "'": '6',
        'U': 'y',
        'A': 'h',
        'Y': 'n',
        '#': 'x',
        '-O': '7',
        '-I': 'u',
        '-E': 'j',
        '-N': 'm',
        '-K': '8',
        '-J': 'i',
        '-R': 'k',
        '-L': ',',
        '-P': '9',
        '-T': 'o',
        '-C': 'l',
        '-`': '.',
        '-F': 'p',
        '-S': ';',
        '-Z': "'",
        'arpeggiate': 'Return',
        'no-op': ('`', '1', '2', '0', '-', '=', 'q', '[', ']', '/', '\\'),
    },
}

# mostly for plover_keyboardplus, but harmless otherwise
# the higher F-keys are useful for binding to other devices, such as footpedals
KEYMAPS['KeyboardPlus'] = KEYMAPS['Keyboard']
KEYMAPS['KeyboardPlus'].update({
    '⇧-': 'F13',
    '⎈-': 'F17',
    '◆-': 'F18',
    '❖-': 'F19',
    '✦-': 'F20',
    'H-': ('z', 'F14'),
    '_-': ('space', 'F15'),
    '#': ('x', 'F16'),
})

DICTIONARIES_ROOT = 'asset:plover_velotype:assets'
DEFAULT_DICTIONARIES = (
    'velo_user.json',
    'velo_commands.json',
    'velo_english_basic.json',
    'velo_base.json',
)

