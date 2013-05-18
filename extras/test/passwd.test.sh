rm /tmp/asd.tomb{,.key} -f || exit 1
{
sudo -k
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd --tomb-pwd f00za --use-urandom create /tmp/asd -s 10 >&4 2>&4 || echo error creating: $? >&3
sanity_tomb /tmp/asd.tomb || echo error sanity checks: $? >&3
#checking wrong&correct password
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd --tomb-pwd wrongpassword open /tmp/asd.tomb >&4 2>&4 && echo error: open with wrong password is successful >&3
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd --tomb-pwd f00za open /tmp/asd.tomb >&4 2>&4 || echo error opening: $? >&3
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd close asd >&4 2>&4 || echo error closing1 $? >&3
#now changing password
../tomb --no-color --unsecure-dev-mode --tomb-old-pwd f00za --tomb-pwd n3w passwd /tmp/asd.tomb.key >&4 2>&4 || echo error changing password: $? >&3
#checking it all
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd --tomb-pwd wrongpassword open /tmp/asd.tomb >&4 2>&4 && echo error: open with wrong password is successful after passwd >&3
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd --tomb-pwd f00za open /tmp/asd.tomb >&4 2>&4 && echo error: open with old password is successful >&3
../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd --tomb-pwd n3w open /tmp/asd.tomb >&4 2>&4 || echo error opening after new password: $? >&3

../tomb --no-color list >&4 2>&4 || echo error listing: $? >&3
../tomb --no-color list --get-mountpoint asd >&4 || echo error listing specific: $? >&3
mountpoint=`../tomb --no-color list --get-mountpoint asd`
df $mountpoint >&4 || echo error df: $? >&3

../tomb --no-color --unsecure-dev-mode --sudo-pwd $sudo_pwd close asd >&4 2>&4 || echo error closing2: $? >&3
} always {
	rm /tmp/asd.tomb{,.key} -f
}


