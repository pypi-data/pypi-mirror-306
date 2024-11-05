#!/bin/bash

# Check if number of MPI processes was passed as an argument, otherwise set 1
# also check if $1 is an integer (cast to string and match regex) [src:
# https://stackoverflow.com/questions/806906/how-do-i-test-if-a-variable-is-a-number-in-bash/806923#806923]
re='^[0-9]+$'
if [ -z ${1} ]; then
    PROCS=1
else
    if ! [[ $1 =~ $re ]]; then
        echo "First parameter needs to be an INTEGER (number of MPI processes for octopus)!"
        exit -1
    fi
    PROCS=$1
fi

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    # check if ran as root (assume sudo) or as user
    if [[ "$USER" == "root" ]]; then
        # Get uid of user that ran sudo ./thisscript.sh
        OPTS="--user `id -u ${SUDO_USER}`"
    else
        # Get root uid
        OPTS="--user `id -u ${USER}`"
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    # Nothing needed here
    OPTS=""
fi

docker run ${OPTS} --env MPIPROCS=$PROCS -v `pwd`:/io -ti --rm octopus
