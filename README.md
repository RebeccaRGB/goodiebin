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
