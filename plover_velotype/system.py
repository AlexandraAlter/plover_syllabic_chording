from plover.system import english_stenotype

# ZFSPTCKJR LN H Y IOE'UA [# - #] 'UAOIE Y LN KJRPTCFSZ _ 

KEYS = (
    # LHS consonants fingers
    'Z-', 'F-', 'S-', 'P-', 'T-', 'C-', 'K-', 'J-', 'R-',
    # LHS consonants thumb
    'L-', 'N-',
    # LHS heel
    'H-',
    # LHS vowels thumb
    'Y-',
    # LHS vowels fingers
    'I-', 'O-', 'E-', "'-", 'U-', 'A-',
    # LHS syms thumb
    '[-', '#-',
    # RHS syms thumb
    '-#', '-]',
    # RHS vowels fingers
    "-'", '-U', '-A', '-O', '-I', '-E',
    # RHS vowels thumb
    '-Y',
    # RHS consonants thumb
    '-L', '-N',
    # RHS consonants fingers
    '-K', '-J', '-R', '-P', '-T', '-C', '-F', '-S', '-Z',
    # RHS heel
    '-_',
)

INIT_CON_KEYS = 'ZFSPTCKJRLNH'
VOWEL_KEYS = 'YIOE\'UA[#-#]\'UAOIEY'
FINAL_CON_KEYS = 'LNKJRPTCFSZ_'

IMPLICIT_HYPHEN_KEYS = ()

SUFFIX_KEYS = ('-_',)

NUMBER_KEY = '#'

NUMBERS = {}

UNDO_STROKE_STENO = 'SN-NS'

ORTHOGRAPHY_RULES = english_stenotype.ORTHOGRAPHY_RULES
ORTHOGRAPHY_RULES_ALIASES = english_stenotype.ORTHOGRAPHY_RULES_ALIASES

ORTHOGRAPHY_WORDLIST = None

KEYMAPS = {
    'Keyboard': {
      'L-': 'c',
      'N-': 'v',
      'Y-': 'b',
      '[-': 'z',
      '#-': 'x',
      'Z-': 'Tab',
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
      'H-': '[',
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
      '-L': ',',
      '-N': 'm',
      '-Y': 'n',
      '-#': '.',
      '-]': '/',
      '-_': ']',
      'arpeggiate': 'space',
      # Suppress adjacent keys to prevent miss-strokes.
      'no-op': (),
    },
}

DICTIONARIES_ROOT = 'asset:plover_velotype:assets'
DEFAULT_DICTIONARIES = (
    'velo_user.json',
    'velo_commands.json',
    'velo_initial_consonants.json',
    'velo_vowels.json',
    'velo_final_consonants.json',
    'velo_combinations.json',
    'velo_special.json',
)

