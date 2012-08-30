#!/usr/bin/env zsh

source utils.sh
if [[ -z $sudo_pwd ]]; then
	echo "WARNING: sudo_pwd is probably needed by some test"
fi
rm /tmp/tomb_test_errorlog -f &> /dev/null
has_err=0
autoload colors
colors
for t in *.test.sh; do
	echo -n "$fg[yellow]$t start test... $fg[default]"
	sudo_pwd=$sudo_pwd source $t 3> /tmp/tomb_test_errorlog 4> /tmp/tomb_test_fulllog
	ret=$?
	if [[ `stat -c '%s' /tmp/tomb_test_errorlog` == 0 ]]; then
		echo "$fg[green] OK$fg[default]"
	else
		echo "$fg[red] ERRORS$fg[default]"
		< /tmp/tomb_test_errorlog
		rm /tmp/tomb_test_errorlog
#TODO: make it optional!
echo "\n--- Full log (for $t) ---\n"
		< /tmp/tomb_test_fulllog
		rm /tmp/tomb_test_fulllog
		has_err=1
	fi
done
exit $has_err


