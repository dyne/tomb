#!/usr/bin/zsh

T="../../tomb"
source utils.sh
source ${T} source

notice() { print; yes "${@}"; print; }
error() { _warning "     ${@}"; }
tt() {
	start_loops=(`sudo losetup -a |cut -d: -f1`)
	${T} ${=@}
	res=$?
	loops=(`sudo losetup -a |cut -d: -f1`)
	{ test "${#start_loops}" = "${#loops}" } || { error "loop device limit change to ${#loops}" }
	print "     Tomb command returns $res"
	return $res
}



rm /tmp/test.tomb{,.key} -f || exit 1

notice "Testing creation"

tt dig -s 10 /tmp/test.tomb

tt --ignore-swap --unsecure-dev-mode --tomb-pwd f00za --use-urandom forge /tmp/test.tomb.key


tt --ignore-swap --unsecure-dev-mode --tomb-pwd f00za lock /tmp/test.tomb -k /tmp/test.tomb.key

# sanity_tomb /tmp/asd.tomb
notice "Testing open with wrong password"

tt --unsecure-dev-mode --tomb-pwd wrongpassword open /tmp/test.tomb

notice "Testing open with good password"

tt --unsecure-dev-mode --tomb-pwd f00za open /tmp/test.tomb

tt --unsecure-dev-mode close test

notice "Testing resize to 20MiB"
tt --unsecure-dev-mode --tomb-pwd f00za -k /tmp/test.tomb.key resize /tmp/test.tomb -s 20

# rm /tmp/test.tomb{,.key} -f || exit 1
