from plover.system import english_stenotype

# ZFSPTCKJR LN H ´ IOE 'UAY# OIE ` NL KJRPTCFSZ _

KEYS = (
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
    # RHS heel
    '-_',
)

# not part of the system definition, used in the Velotype Extension
INIT_CON_KEYS = 'ZFSPTCKJRLNH'
VOWEL_KEYS = '´IOE-\'UAY#OIE`'
FINAL_CON_KEYS = 'NLKJRPTCFSZ_'
META_KEYS = ('<', '=', '>') # these should not be used, as they mark special strokes
# end of custom section

IMPLICIT_HYPHEN_KEYS = ("'", 'U', 'A', 'Y', '#', '8', '5', '2', '0')

SUFFIX_KEYS = ('-_',)

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
        'Z-': 'a',
        'F-': 'w',
        'S-': 's',
        '#': 'x',
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
        '-_': 'space',
        'arpeggiate': 'Return',
        'no-op': ('`', '1', '2', '0', '-', '=', 'q', '[', ']', '/'),
    },
}

DICTIONARIES_ROOT = 'asset:plover_velotype:assets'
DEFAULT_DICTIONARIES = (
    'velo_user.json',
    'velo_commands.json',
    'velo_english_basic.json',
    'velo_base.json',
)

