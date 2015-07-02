#!/usr/bin/env bash
function canonicalize {
	cd -P -- "$(dirname -- "$1")" 2> /dev/null &&
	printf '%s\n' "$(pwd -P)/$(basename -- "$1")" | sed 's/^\/\/*/\//' ||
	printf '%s\n' "$1"
}
if [ "$#" -lt 1 ]
then echo "usage: canonicalize <path> [<path> [...]]"
else
	for i in "$@"
	do canonicalize "$i"
	done
fi
