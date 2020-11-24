##
# gregtzar/tomb
#
# This creates an Ubuntu derived base image and installs the tomb libarary
# along with it's dependencies.

FROM ubuntu:bionic

ARG DEBIAN_FRONTEND=noninteractive
ARG TOMB_VERSION=2.5

# Install dependencies
RUN apt-get update -y && \
	apt-get install -y \
	sudo \
	curl \
	rsync \
	build-essential \
	gettext \
	zsh \
	gnupg \
	cryptsetup \
	pinentry-curses \
	steghide

# Build and install Tomb from remote repo
RUN curl https://files.dyne.org/tomb/Tomb-$TOMB_VERSION.tar.gz -o /tmp/Tomb-$TOMB_VERSION.tar.gz && \
	cd /tmp && \
	tar -zxvf /tmp/Tomb-$TOMB_VERSION.tar.gz && \
	cd /tmp/Tomb-$TOMB_VERSION && \
	make install