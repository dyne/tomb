rm /tmp/asd.tomb{,.key} -f || exit 1
sudo -k
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd --tomb-pwd f00za --use-urandom create /tmp/asd -s 10 >&4 2>&4 || echo error creating: $? >&3
sanity_tomb /tmp/asd.tomb || echo error sanity checks: $? >&3
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd --tomb-pwd wrongpassword open /tmp/asd.tomb >&4 2>&4 && echo error: open with wrong password is successful >&3
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd --tomb-pwd f00za open /tmp/asd.tomb >&4 2>&4 || echo error opening: $? >&3
../tomb --no-color list >&4 2>&4 || echo error listing: $? >&3
../tomb --no-color list --get-mountpoint asd >&4 || echo error listing specific: $? >&3
mountpoint=`../tomb --no-color list --get-mountpoint asd`
df $mountpoint >&4 || echo error df: $? >&3

../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd close asd >&4 2>&4 || echo error closing: $? >&3

rm /tmp/asd.tomb{,.key} -f


