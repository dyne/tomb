#!/bin/sh
set -ex
wget https://github.com/TryCatchHCF/Cloakify/archive/v1.0.3.tar.gz -O /tmp/cloakify.tar.gz
mkdir -p extras/cloakify
tar -xvf /tmp/cloakify.tar.gz --strip-components=1 -C $PWD/extras/cloakify
echo "#!/bin/sh
python2 $PWD/extras/cloakify/cloakify.py $@" > /usr/bin/cloakify
echo "#!/bin/sh
python2 $PWD/extras/cloakify/decloakify.py $@" > /usr/bin/decloakify
chmod +x /usr/bin/cloakify
chmod +x /usr/bin/decloakify