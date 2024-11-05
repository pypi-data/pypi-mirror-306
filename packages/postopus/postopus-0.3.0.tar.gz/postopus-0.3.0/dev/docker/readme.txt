Run Octopus in Docker
=====================

We assume docker is available.

1. Build docker image::

    sh build-docker-image.sh

2. Execute octopus from container: navigate to directory that contains the ``inp`` file, and then run::

    sh octopus-docker.sh

   You can also provide an integer as the first parameter to run multiple MPI processes for faster computation

    sh octopus-docker.sh 8          # 8 MPI processes



Developer notes
===============

After having handcrafted this Docker file, I noticed that Spack can create Dockerfiles. This might be the neater way to go: https://spack.readthedocs.io/en/latest/containers.html
