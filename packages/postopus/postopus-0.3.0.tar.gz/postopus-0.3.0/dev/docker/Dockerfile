FROM debian:bullseye
RUN apt-get -y update
# install essentials to allow spack to compile (plus some editors)
RUN apt-get install -y make sudo emacs git gcc python3 vim cpp xz-utils bzip2 g++ gfortran

# Create working directory for mounting host file system
RUN mkdir /io

# Run spack compilation as user
RUN useradd -ms /bin/bash user
USER user
WORKDIR /home/user

# Get spack and compile Octopus with it
RUN git clone https://github.com/fangohr/spack.git
WORKDIR /home/user/spack
RUN git checkout octopus-review-2021-08
RUN bin/spack install octopus@develop+netcdf

# Get octopus into path: create executable file in /home/user
RUN echo "#!/bin/bash" > ../octopus
RUN bin/spack load --sh octopus >> ../octopus
RUN echo "mpirun -np \$MPIPROCS octopus \$@" >> ../octopus
RUN echo "echo \$MPIPROCS"
RUN chmod a+x ../octopus
# put /home/user into PATH
env PATH=$PATH:/home/user

# change into mount point directory (io=input output)
WORKDIR /io

# for debugging purposes when building image (with one mpi process)
#RUN octopus 1 --version

# entry point
CMD /bin/bash /home/user/octopus

# Run with 'docker run --env MPIPROCS=2 -v `pwd`:/io -ti --rm octopus '
