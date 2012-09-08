rm /tmp/kdf.tomb{,.key} -f || echo error removing previous files >&3
sudo -k
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd --tomb-pwd f00za --use-urandom create /tmp/kdf -s 10 --kdf null >&4 2>&4 || echo "error creating (with --kdf null): $?" >&3
egrep '^_KDF_' /tmp/kdf.tomb.key >&4 2>&4 && echo "error tomb kdf header present (--kdf=null), shouldn't" >&3
sanity_tomb /tmp/kdf.tomb || echo error sanity checks: $? >&3
rm /tmp/kdf.tomb{,.key} -f || echo error removing previous files >&3
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd --tomb-pwd f00za --use-urandom create /tmp/kdf -s 10 >&4 2>&4 || echo "error creating (without --kdf): $?" >&3
egrep '^_KDF_' /tmp/kdf.tomb.key >&4 2>&4 && echo "error tomb kdf header present (no --kdf), shouldn't" >&3
sanity_tomb /tmp/kdf.tomb || echo error sanity checks: $? >&3
