.PHONY: test

system := $(shell uname -s)
# if [ ${system} == "FreeBSD" ]; then sudo kldload fusefs; fi

TOMB ?= test.tomb

#########
## BUILD
#########
test: create-open-close check-random-data

########
## TEST
########
create-open-close:
	TOMB=${TOMB} ./test/bats/bin/bats ./test/create_open_close.bats
	chmod a+r ${TOMB}

# arg: TOMB='path to tomb containing random.data'
# assumes $TOMB.hash is the pre-calculated hash on creation
check-random-data:
	TOMB=${TOMB} ./test/bats/bin/bats test/check-random-data.bats

########
## LINT
########
shellcheck:
	shellcheck -s sh tomb -e SC2006,SC2059,SC2034

########
## DEPS
########
download-deps-ubuntu22:
	curl https://files.dyne.org/tomb3/third-party/veracrypt-ubuntu22-amd64 -o /usr/local/bin/veracrypt && chmod +x /usr/local/bin/veracrypt
	curl https://files.dyne.org/zenroom/nightly/zenroom-linux-amd64 -o /usr/local/bin/zenroom && chmod +x /usr/local/bin/zenroom

download-deps-ubuntu20:
	curl https://files.dyne.org/tomb3/third-party/veracrypt-ubuntu20-amd64 -o /usr/local/bin/veracrypt && chmod +x /usr/local/bin/veracrypt
	curl https://files.dyne.org/zenroom/nightly/zenroom-linux-amd64 -o /usr/local/bin/zenroom && chmod +x /usr/local/bin/zenroom

download-deps-freebsd13:
	curl https://files.dyne.org/tomb3/third-party/veracrypt-freebsd13-amd64 -o /usr/local/bin/veracrypt && chmod +x /usr/local/bin/veracrypt
	curl https://files.dyne.org/tomb3/third-party/zenroom-freebsd13-amd64 -o /usr/local/bin/zenroom && chmod +x /usr/local/bin/zenroom

#curl https://files.dyne.org/zenroom/nightly/zenroom-freebsd13-amd64 -o /usr/local/bin/zenroom && chmod +x /usr/local/bin/zenroom
