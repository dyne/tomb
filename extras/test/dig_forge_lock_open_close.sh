#/usr/bin/env zsh 

T="../../tomb"
source utils.sh

rm /tmp/test.tomb{,.key} -f || exit 1

sudo -k

${T} dig -s 10 /tmp/test.tomb

sudo losetup -a

${T} --ignore-swap --unsecure-dev-mode --tomb-pwd f00za --use-urandom \
	forge /tmp/test.tomb.key

sudo losetup -a

${T} --ignore-swap --unsecure-dev-mode --tomb-pwd f00za \
	lock /tmp/test.tomb -k /tmp/test.tomb.key

sudo losetup -a

# sanity_tomb /tmp/asd.tomb
echo
echo trying to open with wrong password
echo

${T} --unsecure-dev-mode --tomb-pwd wrongpassword \
	open /tmp/test.tomb

sudo losetup -a

echo
echo trying to open with good password
echo

${T} --unsecure-dev-mode --tomb-pwd f00za \
	open /tmp/test.tomb

sudo losetup -a

${T} --unsecure-dev-mode close test 

sudo losetup -a

rm /tmp/test.tomb{,.key} -f || exit 1

