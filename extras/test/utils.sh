sanity_tomb() {
	tombsize=`stat $1 -c '%s'`
	if [[ $tombsize -ge 12000000 ]] || [[ $tombsize -le 9000000 ]]; then
		echo "Error: tomb size is wrong: $tombsize"
		return 1
	fi
	keysize=`stat ${1}.key -c '%s'`
	if [[ $keysize -le 400 ]]; then
		echo "Error: key size is wrong: $keysize"
		return 2
	fi
	keytype=`file =(egrep -v '^_' ${1}.key) -bi`
	if ! [[ $keytype =~ application/pgp ]]; then
		echo "Wrong type for keyfile"
		return 3
	fi
}
