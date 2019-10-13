#!/usr/bin/env bash
function install {
	cp "$1" "/usr/local/bin/${1%.*}" 2> /dev/null
	chmod a+rx "/usr/local/bin/${1%.*}" 2> /dev/null
}
function compile {
	gcc -o "/usr/local/bin/${1%.*}" "$1" 2> /dev/null
}
function die {
	echo "This script must be run as root."
	exit
}

mkdir -p /usr/local/bin/ 2> /dev/null || die
install approximate.py || die
install bci.py || die
install bcr.py || die
install bec.py || die
install canonicalize.sh || die
install chargen.py || die
install dechex.sh || die
compile erdrcr.c || die
install factor.py || die
install harden.sh || die
install hexdec.sh || die
install scon.py || die
install simplify.py || die
install soften.sh || die
install sread.py || die
install ssff.py || die
install swrite.py || die
