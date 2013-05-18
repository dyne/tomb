#!/usr/bin/env zsh

test_file() {
	t=$1
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
		return 1
	fi
	return 0
}

source utils.sh
if [[ -z $sudo_pwd ]]; then
	echo "WARNING: sudo_pwd is probably needed by some test"
fi
rm /tmp/tomb_test_errorlog -f &> /dev/null
has_err=0
autoload colors
colors
if [[ $# == 0 ]]; then
	for t in *.test.sh; do
		test_file $t
		if [[ $? != 0 ]]; then
			has_err=$?
		fi
	done
else
	for t in "$@"; do
		test_file $t
		if [[ $? != 0 ]]; then
			has_err=$?
		fi
	done
fi
exit $has_err


