#!/bin/bash
set -e

function log_info(){
	local msg=$1
	printf "INFO: ${msg}\n"
}

function log_error(){
	local msg=$1
	printf "ERROR: ${msg}\n"
}

# Check & Validate Required ENV VARS

## 
# TOMB_DOCKER_IMAGE
if [ -z "$TOMB_DOCKER_IMAGE" ]; then
	log_error "ENV VAR: TOMB_DOCKER_IMAGE is required!"
	exit 1
fi
if [ -z "$(docker images -q $TOMB_DOCKER_IMAGE)" ]; then
	log_error "TOMB_DOCKER_IMAGE not found: $TOMB_DOCKER_IMAGE"
	exit 1
fi

## 
# TOMB_VOLUME
if [ -z "$TOMB_VOLUME" ]; then
	log_error "ENV VAR: TOMB_VOLUME is required!"
	exit 1
fi
if [ ! -f "$TOMB_VOLUME" ]; then
	log_error "TOMB_VOLUME not found: $TOMB_VOLUME"
	exit 1
fi

## 
# TOMB_VOLUME_KEY
if [ -z "$TOMB_VOLUME_KEY" ]; then
	log_error "ENV VAR: TOMB_VOLUME_KEY is required!"
	exit 1
fi
if [ ! -f "$TOMB_VOLUME_KEY" ]; then
	log_error "TOMB_VOLUME_KEY not found: $TOMB_VOLUME_KEY"
	exit 1
fi

## 
# TOMB_OUTPUT_DIR
if [ -z "$TOMB_OUTPUT_DIR" ]; then
	log_error "ENV VAR: TOMB_OUTPUT_DIR is required!"
	exit 1
fi
if [ ! -d "$TOMB_OUTPUT_DIR" ]; then
	log_error "TOMB_OUTPUT_DIR not found: $TOMB_OUTPUT_DIR"
	exit 1
fi

# Internal Vars
I_TOMB_VOLUME=/tomb/volume
I_TOMB_VOLUME_KEY=/tomb/volume_key
I_TOMB_OUTPUT_DIR=/tomb/output_dir # Important: This must NOT end in a slash!
I_TOMB_MOUNT_DIR=/tomb/mount_dir # Important: This must NOT end in a slash!

# Parse command
cmd=$1

if [ -z "$cmd" ]; then
	log_error "A valid command is required! (eg: unpack, repack)"
	exit 1
fi

# Parse flags (right now there is only one possible flag so I'm being lazy about parsing it)
flags=$2

force_opt=""
if [ "$flags" = "-f" ]; then
	force_opt=$flags
fi

if [ $cmd = unpack ]; then

	if [ ! -z "$(ls -A $TOMB_OUTPUT_DIR)" ]; then
		log_error "Cannot unpack: TOMB_OUTPUT_DIR is not empty! $TOMB_OUTPUT_DIR"
		exit 1
	fi

	docker run -it --rm --privileged \
		--mount type=bind,source=${TOMB_VOLUME},target=${I_TOMB_VOLUME} \
		--mount type=bind,source=${TOMB_VOLUME_KEY},target=${I_TOMB_VOLUME_KEY} \
		--mount type=bind,source=${TOMB_OUTPUT_DIR},target=${I_TOMB_OUTPUT_DIR} \
		tomb /bin/bash -c "set -e; tomb open ${I_TOMB_VOLUME} ${I_TOMB_MOUNT_DIR} -k ${I_TOMB_VOLUME_KEY} ${force_opt}; rsync -azh --delete ${I_TOMB_MOUNT_DIR}/ ${I_TOMB_OUTPUT_DIR}; tomb close"

elif [ $cmd = repack ]; then

	if [ -z "$(ls -A $TOMB_OUTPUT_DIR)" ]; then
		log_error "Cannot repack: TOMB_OUTPUT_DIR is empty! $TOMB_OUTPUT_DIR"
		exit 1
	fi

	docker run -it --rm --privileged \
		--mount type=bind,source=${TOMB_VOLUME},target=${I_TOMB_VOLUME} \
		--mount type=bind,source=${TOMB_VOLUME_KEY},target=${I_TOMB_VOLUME_KEY} \
		--mount type=bind,source=${TOMB_OUTPUT_DIR},target=${I_TOMB_OUTPUT_DIR} \
		tomb /bin/bash -c "set -e; tomb open ${I_TOMB_VOLUME} ${I_TOMB_MOUNT_DIR} -k ${I_TOMB_VOLUME_KEY} ${force_opt}; rsync -azh --delete ${I_TOMB_OUTPUT_DIR}/ ${I_TOMB_MOUNT_DIR}; tomb close; rm -rf ${I_TOMB_OUTPUT_DIR}/..?* ${I_TOMB_OUTPUT_DIR}/* ${I_TOMB_OUTPUT_DIR}/.[!.]*"

elif [ $cmd = drop ]; then

	if [ -z "$(ls -A $TOMB_OUTPUT_DIR)" ]; then
		log_error "Cannot drop: TOMB_OUTPUT_DIR is empty! $TOMB_OUTPUT_DIR"
		exit 1
	fi

	docker run -it --rm --privileged \
		--mount type=bind,source=${TOMB_OUTPUT_DIR},target=${I_TOMB_OUTPUT_DIR} \
		tomb /bin/bash -c "set -e; rm -rf ${I_TOMB_OUTPUT_DIR}/..?* ${I_TOMB_OUTPUT_DIR}/* ${I_TOMB_OUTPUT_DIR}/.[!.]*"

else
	log_error "Invalid command: $cmd"
fi
