# The Goodie `/bin/`

This repository contains a random assortment of command line utilities that I have personally written and found very useful.

## `approximate`

Calculates the best fractional approximation of a real number. The first argument is the highest denominator to use. The remaining arguments are the values to approximate.

    $ approximate 10 3.1415926535
    3.1415926535 ≈ 22 / 7 = 3.14285714286
    Delta: 0.00126448935714
    Error: 0.0402499463364%
    $ approximate 100 3.1415926535
    3.1415926535 ≈ 311 / 99 = 3.14141414141
    Delta: 0.000178512085859
    Error: 0.00568221617337%
    $ approximate 1000 3.1415926535
    3.1415926535 ≈ 355 / 113 = 3.14159292035
    Delta: 2.66853982467e-07
    Error: 8.49422607891e-06%

## `bci`

Converts integers from one base (binary, octal, decimal, hexadecimal, etc.) to another. The first argument is the input base. The second argument is the output base. The remaining arguments are the values to convert.

    $ bci 10 16 255 65535 42
    FF
    FFFF
    2A
    $ bci 16 10 ff ffff 42
    255
    65535
    66

## `bcr`

Like `bci`, only working on real numbers. (This may be less precise than `bci` for integer values.)

    $ bcr 10 16 3.1415926535
    3.243F6A8822E88
    $ bcr 16 10 3.243F6A8822E88
    3.1415926535000000541231202078051865100860595703125

## `canonicalize`

Prints the canonical file path for every file path given as an argument. Removes symlinks and redundant dots and slashes from the directory path.

    $ canonicalize /
    /
    $ canonicalize /tmp/
    /tmp
    $ canonicalize /tmp/aprc9YXQU 
    /private/tmp/aprc9YXQU
    $ canonicalize /usr/local/bin/../../local/bin/../bin/canonicalize
    /usr/local/bin/canonicalize
    $ canonicalize /this/file/does/not/exist
    /this/file/does/not/exist

## `chargen`

Generates characters.

    $ chargen -n 5
    !"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefgh
    "#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghi
    #$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghij
    $%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijk
    %&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijkl
    $ chargen -f A -l Z -n 5
    ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRST
    BCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTU
    CDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUV
    DEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVW
    EFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWX
    $ chargen -f 0x30 -l 0x39 -o 1 -w 80 -n 1
    12345678901234567890123456789012345678901234567890123456789012345678901234567890
    $ chargen -v
     !"#$%&'()*+,-./
    0123456789:;<=>?
    @ABCDEFGHIJKLMNO
    PQRSTUVWXYZ[\]^_
    `abcdefghijklmno
    pqrstuvwxyz{|}~ 
    $ chargen -f 0x100 -l 0x17F -v -t ' '
    Ā ā Ă ă Ą ą Ć ć Ĉ ĉ Ċ ċ Č č Ď ď
    Đ đ Ē ē Ĕ ĕ Ė ė Ę ę Ě ě Ĝ ĝ Ğ ğ
    Ġ ġ Ģ ģ Ĥ ĥ Ħ ħ Ĩ ĩ Ī ī Ĭ ĭ Į į
    İ ı Ĳ ĳ Ĵ ĵ Ķ ķ ĸ Ĺ ĺ Ļ ļ Ľ ľ Ŀ
    ŀ Ł ł Ń ń Ņ ņ Ň ň ŉ Ŋ ŋ Ō ō Ŏ ŏ
    Ő ő Œ œ Ŕ ŕ Ŗ ŗ Ř ř Ś ś Ŝ ŝ Ş ş
    Š š Ţ ţ Ť ť Ŧ ŧ Ũ ũ Ū ū Ŭ ŭ Ů ů
    Ű ű Ų ų Ŵ ŵ Ŷ ŷ Ÿ Ź ź Ż ż Ž ž ſ

## `dechex`

An alias for `bci 10 16`.

    $ dechex 15 255 65535
    F
    FF
    FFFF

## `erdrcr`

ErroR DetectoR and CorrectoR. Compares multiple binary files for bit-for-bit equality. Reports which bits differ and how much of the files differ. Can also output an error-corrected binary file.

    $ erdrcr 1.bin 2.bin 3.bin
    Address.Mask	0's	1's	Correction
    00000015.02:	2	1	0
    0000001C.08:	1	2	1
    2 out of 320 bits mismatched (0.625% error rate)
    all errors correctable
    $ erdrcr 1.bin 2.bin 3.bin -o 4.bin
    Address.Mask	0's	1's	Correction
    00000015.02:	2	1	0
    0000001C.08:	1	2	1
    2 out of 320 bits mismatched (0.625% error rate)
    all errors correctable
    $ erdrcr 1.bin 4.bin
    no differences found
    $ erdrcr 1.bin trunc.bin 
    Address.Mask	0's	1's	Correction
    00000024.20:	1	1	?
    00000024.10:	1	1	?
    00000024.02:	1	1	?
    00000025.20:	1	1	?
    00000025.10:	1	1	?
    00000025.04:	1	1	?
    00000026.20:	1	1	?
    00000026.10:	1	1	?
    00000026.02:	1	1	?
    00000026.01:	1	1	?
    00000027.20:	1	1	?
    00000027.02:	1	1	?
    12 out of 320 bits mismatched (3.75% error rate)
    12 out of 320 bits unrecoverable (3.75% error rate)

## `factor`

Calculates the prime factorization of an integer and its divisors, and other related properties.

    $ factor 360
    360 = 2^3 * 3^2 * 5
    360 = 2 * 2 * 2 * 3 * 3 * 5
    
    Divisors: 1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 60, 72, 90, 120, 180, 360
    sigma_0(n) = 24
    sigma_1(n) = 1170
    sigma_1(n)-n = 810
    sigma_1(n)-2n = 450
    360 is abundant.
    
    Pairs:
    1*360	2*180	3*120	4*90	5*72	6*60	8*45	9*40	10*36	12*30	15*24	18*20

## `harden`

Recursively removes write permissions and sets the user immutable flag (also known as the "locked" property of a file under Mac OS X). Useful for creating an unwriteable backup.

## `hexdec`

An alias for `bci 16 10`.

    $ hexdec f ff ffff
    15
    255
    65535

## `scon`

Connects to a serial port and continually sends stdin to serial input and prints serial output to stdout. (Requires pySerial.)

    $ scon /dev/tty.usbmodemfd121 -b 9600 -d 8 -p none -s 1 -r -w 1
    !Hello
    Hello
    ^C
    $ scon --help
    usage: scon [<options>] <device>
       -u <path>   serial device to read from and write to
       -b <int>    baud rate
       -d <int>    data bits (5, 6, 7, 8)
       -p <str>    parity (none, even, odd, mark, space)
       -s <num>    stop bits (1, 1.5, 2)
       -t <num>    timeout (seconds)
       -x          enable XON/XOFF
       -r          enable RTS/CTS
       -h          enable DSR/DTR
       -w <num>    delay before reading or writing (seconds)

## `simplify`

Calculates and divides out the largest common factor / greatest common divisor from a list of integers.

    $ simplify 2 4 6 8
    GCD: 2
    Sim: 1 2 3 4
    $ simplify 36 72 96
    GCD: 12
    Sim: 3 6 8

## `soften`

Recursively clears the user immutable flag (also known as the "locked" property of a file under Mac OS X). A partial reversal of `harden`.

## `sread`

Reads from a serial port and writes to stdout or a file. (Requires pySerial.)

    $ sread -u /dev/tty.usbmodemfa131 -b 9600 -d 8 -p none -s 1 -r -o output.txt -w 1
    $ sread --help
    usage: sread [<options>] <device> [<output>]
       -u <path>   serial device to read from
       -b <int>    baud rate
       -d <int>    data bits (5, 6, 7, 8)
       -p <str>    parity (none, even, odd, mark, space)
       -s <num>    stop bits (1, 1.5, 2)
       -t <num>    timeout (seconds)
       -x          enable XON/XOFF
       -r          enable RTS/CTS
       -h          enable DSR/DTR
       -o <path>   path to write to
       -w <num>    delay before reading (seconds)
       -l <int>    number of bytes to read

## `ssff`

Extracts file paths from svn status lines with the specified statuses. Statuses may be specified in either uppercase or lowercase. `' '`, `'?'`, `'!'`, `'~'` may be specified as `'S'`, `'Q'`, `'E'`, `'T'`, respectively. `'Z'` specifies all possible statuses.

    $ svn status
    A       added/file
    D       deleted/file
    M       modified/file
    ?       unversioned/file
    !       missing/file
    $ svn status | ssff m
    modified/file
    $ svn status | ssff ad
    added/file
    deleted/file
    $ svn status | ssff \?
    unversioned/file
    $ svn status | ssff q
    unversioned/file
    $ svn status | ssff \!
    missing/file
    $ svn status | ssff e
    missing/file
    $ svn status | ssff z
    added/file
    deleted/file
    modified/file
    unversioned/file
    missing/file
    $ svn diff `svn st | ssff m` # diff modified files, but not added or deleted files
    --- modified/file       (revision 123)
    +++ modified/file       (working copy)
    @@ -1,3 +1,3 @@
     unmodified line
    -removed line
    +added line
     unmodified line
    $ svn add `svn st | ssff q` # add all unversioned files
    A         unversioned/file
    $ svn revert `svn st | ssff m` # revert all modified files
    Reverted 'modified/file'
    $ svn revert `svn st | ssff e` # restore all missing files
    Reverted 'missing/file'
    $ svn status
    A       added/file
    D       deleted/file
    A       unversioned/file

## `swrite`

Reads from stdin or a file and writes to a serial port. (Requires pySerial.)

    $ swrite -u /dev/tty.usbmodemfa131 -b 9600 -d 8 -p none -s 1 -r -i input.txt -w 10
    $ swrite --help
    usage: swrite [<options>] <device> [<input>]
       -u <path>   serial device to write to
       -b <int>    baud rate
       -d <int>    data bits (5, 6, 7, 8)
       -p <str>    parity (none, even, odd, mark, space)
       -s <num>    stop bits (1, 1.5, 2)
       -t <num>    timeout (seconds)
       -x          enable XON/XOFF
       -r          enable RTS/CTS
       -h          enable DSR/DTR
       -i <path>   path to read from
       -w <num>    delay before writing (seconds)
       -l <int>    number of bytes to write
