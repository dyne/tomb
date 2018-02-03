#!/usr/bin/env zsh

error=0

check_kdf() {
	while read line; do
		pass=`cut -f1 <<<$line`
		salt=`cut -f2 <<<$line`
		iter=`cut -f3 <<<$line`
		keylen=`cut -f4 <<<$line`
		expected=`cut -f5 <<<$line`
		hexsalt=`cut -f6 <<<$line`
		#TODO: check!
		derived=`./tomb-kdb-pbkdf2 $hexsalt $iter $keylen <<<$pass`
		if [[ $derived != $expected ]]; then
			echo "Expected $expected, got $derived" >&2
			error=$((error + 1))
		fi
	done < test.txt
}	

check_white_spaces() {
	hexsalt="73616c74"
	iter=4096
	keylen=20
	typeset -a results
	passwords=('one two three' 'one two' 'one')
	for pwd in $passwords; do
		results+=`./tomb-kdb-pbkdf2 $hexsalt $iter $keylen <<<$pwd`
	done
	for ((i=1;i<=3;i++)); do
		d1=$results[$i]
		i1=$passwords[$i]
		for ((j=(($i+1));j<=3;j++)); do
			d2=$results[$j]
			i2=$passwords[$j]
			if [[ $d1 == $d2 ]]; then
				echo "Inputs \"$i1\" and \"$i2\" produce the same output $d1" >&2
				error=$((error + 1))
			fi
		done
	done
}

check_kdf
check_white_spaces

if [[ $error == 1 ]]; then
	exit $error
fi
