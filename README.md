# Plover Syllabic Chording

A syllabic chording system for Plover, reminiscent of how the Veyboard and Velotype keyboards operate.

## Development Status

This project is largely for personal use, and no gurantees of function, form or sanity can be given.
While every attempt will be made to fix any bugs found in this project, nothing is guranteed.

## Affiliation

This project is not affiliated with the makers of the Veyboard or Velotype keyboard in any way,
it's just a crude approximation of the keyboard's functioning onto Plover, made by an ameteur.

## Installation

This package provides a Plover System and an Extension.
Without the extension active, strokes will not be processed correctly, and the keyboard will not work.
If the system is changed, the extension will not interfere with normal operation.

## Recommended Keyboard

The default layouts and dictionaries are very much personalized, and may be inappropriate for any other user.
I use a ZSA Moonlander Mark I alongside [custom firmware](https://github.com/AlexandraAlter/qmk_firmware/tree/master/keyboards/moonlander/keymaps/AlexandraAlter).

## Technical Details

To be rewritten following a large redesign.

Plover is certainly not meant to work this way.
This extension works by proxying Plover's `DictionaryCollection` system.

This custom dictionary collection acts in the same way as the default Plover dictionary collection,
but if the lookup fails, the stroke is then searched as a syllabic chord.

