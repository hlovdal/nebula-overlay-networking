#!/bin/bash

set -e

if [ $# -ne 2 ]
then
	echo "Usage: $0 <spec-file> <sources-dir>" >&2
	exit 1
fi

# Version:        1.4.0
VER=$(sed -n '/^Version:\s*/s///p' "$1")
#echo $VER

# Source0:        https://github.com/slackhq/nebula/releases/download/v%{version}/nebula-linux-amd64.tar.gz
for url in $(sed -n "/^Source.*:\s*https:..github.com.slackhq/{s/%{version}/$VER/g; s/.*https/https/; p}" "$1")
do
	pushd "$2"
	curl -Lo $(basename $url) $url
	popd
done
