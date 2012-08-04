#!/usr/bin/env zsh

error=0
while read line; do
	pass=`cut -f1 <<<$line`
	salt=`cut -f2 <<<$line`
	iter=`cut -f3 <<<$line`
	keylen=`cut -f4 <<<$line`
	expected=`cut -f5 <<<$line`
	hexsalt=`cut -f6 <<<$line`
	#TODO: check!
	derived=`./pbkdf2 $hexsalt $iter $keylen <<<$pass`
	if [[ $derived != $expected ]]; then
		echo ./pbkdf2 $hexsalt $iter $keylen "<<<$pass"
		echo "Expected $expected, got $derived" >&2
		error=$((error + 1))
	fi
done < test.txt

if [[ $error == 1 ]]; then
	exit $error
fi
