# Plover Velotype

Velotype-esque typing for Plover.

## Development Status

This project is largely for personal use, and no gurantees of function, form or sanity can be given.
While every attempt will be made to fix any bugs found in this project, nothing is guranteed.

## Affiliation

This project is not affiliated with the makers of the Velotype keyboard in any way,
it's just a crude approximation of the keyboard's functioning onto Plover.

## Installation

This package provides a Plover System and and Extension.
Without the extension active, strokes will not be split up correctly, and the keyboard will not work.
If the system is set to anything other than Velotype, the extension will not interfere with normal operation.

## Velotype Theory

A full discussion of the theory behind the Velotype would be too big to fit in this readme, but an outline will do.

The keyboard works via chords. Multiple letters are output by holding down a sequence of keys, then releasing them.

The keyboard is divided crudely into three areas, with consonants on the left and right, and vowels in the middle.
When letters are output, they are broadly output from left to right.

Symbols and numbers are output by chording a shift key with the relevant other key.

When the Velotype resolves a chord into a sequence of keys, it looks up the keys of each area independantly of each other, then appends the results of each lookup together to form the final output.

## Technical Details

Plover is certainly not meant to work this way.
This extension works by proxying Plover's `DictionaryCollection` system.

This custom dictionary collection acts in the same way as the default Plover dictionary collection,
but if the lookup fails, the stroke is split according tho the Velotype rules and the lookup is retried.

These split strokes are looked up as if they were each a sequence of two strokes.
The first stroke is a 'meta' stroke made out of characters that cannot be stroked orginarily,
protecting Velotype-specific sequences from being matched by accident.

Currently the characters '+«<=>»' are used for these meta-strokes.
In order, they represent the stroke prefixes (+, used for the NoSpace button or _),
the leading consonants («, used for ZFSPTCKJRLNH),
the leading vowels (<, used for Y),
the main vowels (=, used for IOE-UAOIE),
the symbol keys (>, used for ´'`),
and the ending consonants (», used for -NLKJRPTCFSZ).

Five different permutations of these split strokes are tried against the dictionary,
with the exception of the prefix, which is looked up on its own.

There's a preferential order to matching. If a stroke '«<=>»/' exists in the dictionary,
it will be matched before any other stroke.
(Of course, if a bare stroke without any meta-prefix exists, this will avoid the splitting process altogether.)
The last combination to be checked is each sub-section, independantly of the others.
These rules apply to entries made in the velo_user.json dictionary too.
It's best to ensure that the meta-stroke each entry is prefixed with exactly matches the keys that make up the stroke,
else some keys may mysteriously go missing.


