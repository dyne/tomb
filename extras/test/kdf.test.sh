rm /tmp/kdf.tomb{,.key} -f || echo error removing previous files >&3
sudo -k
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd --tomb-pwd f00za --use-urandom create /tmp/kdf -s 10 --kdf pbkdf2 >&4 2>&4 || echo error creating: $? >&3
egrep '^_KDF_pbkdf2sha1_' /tmp/kdf.tomb.key >&4 2>&4 || echo error tomb kdf header >&3
sanity_tomb /tmp/kdf.tomb || echo error sanity checks: $? >&3
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd --tomb-pwd f00za open /tmp/kdf.tomb >&4 2>&4 || echo error creating: $? >&3
../tomb --no-color list >&4 2>&4 || echo error listing: $? >&3
../tomb --no-color list --get-mountpoint kdf >&4 || echo error listing specific: $? >&3
mountpoint=`../tomb --no-color list --get-mountpoint kdf`
df $mountpoint >&4 || echo error df: $? >&3

../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd close kdf >&4 2>&4 || echo error closing: $? >&3

