#!/usr/bin/env bash
function install {
	cp "$1" "/usr/local/bin/${1%.*}" 2> /dev/null
	chmod a+rx "/usr/local/bin/${1%.*}" 2> /dev/null
}
function die {
	echo "This script must be run as root."
	exit
}

mkdir -p /usr/local/bin/ 2> /dev/null || die
install approximate.py || die
install bci.py || die
install bcr.py || die
install canonicalize.sh || die
install chargen.py || die
install dechex.sh || die
install factor.py || die
install harden.sh || die
install hexdec.sh || die
install simplify.py || die
install soften.sh || die
