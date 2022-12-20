# Generate secure pin tumbler key codes

* Generates a plain text file containing all of the secure key codes.
* Filters out codes outside Maximum Adjacent Cut Specification (MACS).
* Filters out codes that aren't aggressive; the key cut would be too flat.
* Filters out codes where the second to last pin is at the maximum length to make picking the deepest pin difficult.

## Examples

| program | pins | num_pins | macs | aggressiveness | outfile |
| :--- | ---: | ---: | ---: | ---: | :--- |
| ./secure-pin-tumbler.py | 0123456789 | 5 | 7 | 20 | schlage_5.txt |
| ./secure-pin-tumbler.py | 1234567 | 5 | 4 | 8 | kwikset_5.txt |

`./secure-pin-tumbler.py 0123456789 5 7 20 schlage_5.txt`

`./secure-pin-tumbler.py 1234567 5 4 8 kwikset_5.txt`
