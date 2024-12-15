# docker-tomb

A [docker](https://www.docker.com) wrapper for the the Linux-based [Tomb encryption library](https://www.dyne.org/software/tomb) aimed at enabling functional cross platform support for the [Tomb library](https://github.com/dyne/Tomb) and container format.

**This is a work in progress and while functional it is not yet fully stable or secure.**

# Requirements

This strategy should work on MacOS, Windows, Linux, and any host OS where Docker is available. The only requirement is that you must have Docker running on your machine. My recommendation for first time users is to install [Docker Desktop](https://www.docker.com/products/docker-desktop).

# Container Setup

You can build the container by running the following command from the root directory of this repo:

```bash
docker build -t tomb .
```

Although building it yourself is preferred, you could also pull the container from my [dockerhub repo](https://hub.docker.com/r/gregtzar/tomb).

You can confirm the setup by first opening an interactive bash prompt in the new container and from there confirm the tomb version and exit the container.

```bash
docker run -it --rm tomb /bin/bash
tomb -v
exit
```

### Security Notes

You will see by examining the `Dockerfile` that I am using Docker's official Ubuntu Bionic container as the base, and that the latest Tomb library is downloaded directly from the [official tomb filestore](https://files.dyne.org/tomb). The `TOMB_VERSION` arg near the top of the `Dockerfile` will allow you to configure which Tomb version you want.

Be aware that because of the way the filestore is currently organized, the curl path will break unless the version is set to the most current. I am filing a request with them to address this.

Optionally if you wanted to store the tomb code in the repo, for example inside of a `src` folder, then you could install it alternatively like this:

```
ADD src/Tomb-$TOMB_VERSION.tar.gz /tmp/
RUN cd /tmp/Tomb-$TOMB_VERSION && \
	make install
```

# Container Usage

The thing which allows this container strategy to be really functional is the use of Docker's [bind mounts](https://docs.docker.com/storage/bind-mounts/) to give the dockerized tomb instance the ability to read an encrypted/closed tomb volume **from** the host and to then mount the decrypted/open tomb volume **back** to the host where it can be accessed as normal.

## Usage Examples

Once you understand the concept of docker bind mounts you will be able to run tomb commands from the host in any way you need. Here are a few examples to get you started.

### Create a Tomb Volume

First launch an interactive bash prompt in a temporary instance of the container, and bind-mount a working directory from the host machine where we can output the new tomb volume.

This will mount the `/tmp/tomb-gen` directory on the host to the location of `/tomb-gen` inside the docker container instance. **Note**: The `/tmp/tomb-gen` directory must already exist on the host.

```bash
docker run -it --rm --privileged \
	--mount type=bind,source=/tmp/tomb-gen,target=/tomb-gen \
	tomb /bin/bash
```

Now from the interactive prompt inside the docker container instance creating a new tomb volume is textbook. **Note**: If you get an error about swap partitions during the `forge` command, this is a host issue and not a container issue. You need to disable swapping on the host if you want to fix it, or use `-f` to forge ahead anyways.

```bash
cd /tomb-gen
tomb dig -s 100 secret.tomb
tomb forge secret.tomb.key
tomb lock secret.tomb -k secret.tomb.key
```

Now the host `/tmp/tomb-gen` directory contains a new `secret.tomb` volume and `secret.tomb.key` key. Use `exit` to close the tomb container and the new files will remain on the host.

### Direct Mount a Tomb Volume

This example will use the volume and key we created in the previous example but can be modified to suite your needs. First, launch another interactive bash prompt in a temporary instance of the container.

This will mount the host `/tmp/tomb-gen` directory as well as a new `/tmp/tomb-mount` directory where the container can mount the open tomb volume back to so the host can access it.

```bash
docker run -it --rm --privileged \
	--mount type=bind,source=/tmp/tomb-gen,target=/tomb-gen \
	--mount type=bind,source=/tmp/tomb-mount,target=/tomb-mount,bind-propagation=shared \
	tomb /bin/bash
```

Now from the interactive prompt inside the docker container instance we can open the tomb volume as usual, referencing the tomb volume, key, and mount destinations bind-mounted to the host:

```bash
tomb open /tomb-gen/secret.tomb /tomb-mount -k /tomb-gen/secret.tomb.key
```

The contents of the tomb volume are now accessible via `/tmp/tomb-mount` on the host. Be sure to successfully close the tomb volume before you exit the docker container:

```bash
tomb close
```

### Unpack and Repack a Tomb Volume

This workflow was created as a workaround for the MacOS lack of support for bind propagation which prevents us from directly mounting a tomb volume back to the host OS. The workaround is to use an additional bash script layer to copy and synchronize the tomb volume contents between a bind mounted host directory and the mounted tomb volume accessible only from inside the docker container.

The `tomb.sh` script is designed to run from the host and requires the following ENV VARS to be available to it:

* `TOMB_DOCKER_IMAGE`: The name of the docker image on the host. In the examples we named it `tomb`.
* `TOMB_VOLUME`: The full path of the tomb volume file on the host. In the example it is `/tmp/tomb-gen/secret.tomb`.
* `TOMB_VOLUME_KEY`: The full path of the tomb volume key file on the host. In the examples it is `/tmp/tomb-gen/secret.tomb.key`.
* `TOMB_OUTPUT_DIR`: The full path of the directory where we will unpack the tomb volume contents to on the host. In the examples it is `/tmp/tomb-out`.

#### tomb.sh unpack

This command will launch a new docker container, open the tomb volume internally, and copy it's contents to the host `TOMB_OUTPUT_DIR` directory which it expects to be empty. It will then close the tomb volume and exit the docker container.

```bash
export TOMB_DOCKER_IMAGE=tomb
export TOMB_VOLUME=/tmp/tomb-gen/secret.tomb
export TOMB_VOLUME_KEY=/tmp/tomb-gen/secret.tomb.key
export TOMB_OUTPUT_DIR=/tmp/tomb-out
./tomb.sh unpack
```

If needed, the `-f` flag can be forwarded through to tomb by passing it to the `unpack` command.

```bash
./tomb.sh unpack -f
```

#### tomb.sh repack

This command will launch a new docker container, open the tomb volume internally, and copy the current contents of the host `TOMB_OUTPUT_DIR` directory back into the open tomb volume. Copying uses `rsync` with `--delete` any files which were removed from `TOMB_OUTPUT_DIR` will also be removed from the open tomb volume contents. It will then close the tomb volume, delete the contents of `TOMB_OUTPUT_DIR`, and exit the docker container. This way all changes are persisted back to the tomb volume. Each step is performed sequentially and an error will cause the entire sequence to bail, so for example if we are unable to successfully close the tomb volume the the contents of `TOMB_OUTPUT_DIR` will not be deleted.

```bash
export TOMB_DOCKER_IMAGE=tomb
export TOMB_VOLUME=/tmp/tomb-gen/secret.tomb
export TOMB_VOLUME_KEY=/tmp/tomb-gen/secret.tomb.key
export TOMB_OUTPUT_DIR=/tmp/tomb-out
./tomb.sh repack
```

If needed, the `-f` flag can be forwarded through to tomb by passing it to the `repack` command.

```bash
./tomb.sh repack -f
```

# Known Issues and Workarounds

## Swap partitions

The user may get a security error from Tomb regarding the swap partitions and is prompted to either disable them or force an override. While the swap error is reported by tomb, it actually pertains to the state of the host OS and not the container OS. So the recommended `swapoff -a` command will obviously work on a Linux host but won't work on a MacOS or Windows host. In these later cases it is up to the user to disable swapping (either temporarily or permanently) on their host os should they choose to, or use the `-f` flag with tomb.

## Privileged access containers

The docker container must be launched in privileged mode, otherwise the tomb library cannot mount loopback devices which it depends. Launching a docker container in privileged mode removes some of the container security sandboxing and grants anything in the container access to parts of your host system. Until docker can support loopback mounting for unprivileged users this may be the only option.

## Bind propagation in MacOS

MacOS does not supported bind propagation for bind mounts, which means we cannot set the `bind-propagation=shared` option on the `--mount` flag for the docker instance. So even though we can mount the tomb volume back to the bind-mounted host directory, the mount will not recurse and the directory will appear empty from the hosts point of view. I have attempted to overcome this a variety of ways including FUSE `bindfs` and symlinks and cannot find a way to expose the mounted tomb volume directory back to the host of MacOS. As a workaround I created the `tomb unpack` and `tomb repack` commands which use `rsync` to recursively copy the contents between the tomb volume mounted inside the docker container and the bind-mounted directory from the host.

## Loop device mount ghost

If the docker container instance is shut down before the tomb volume is successfully closed then the the mounted volume and it's contents may remain attached and available from the host. Obviously any changes made to the contents at this point will not be persisted back to the tomb volume. The ghosted device mount and it's contents will disappear the host system is restarted or the node is manually cleaned up (which I don't know how to do properly), and you will be able to mount the real tomb volume again.

## Filesystem permissions

Since the docker container needs to run as root, anything it creates will have root permissions and may not be accessible from the host user without additional privileges.
