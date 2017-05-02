###########################################################################
#######                                                             #######
#######                          DUA                                #######
#######                                                             #######
###########################################################################

# FROM: Set base image to construct this image

# Get ubuntu 16.04 (latest stable version)
FROM ubuntu:latest


# Freeling files
ADD Docker/FreeLing-4.0 /FreeLing

# Patches
ADD Docker/Patches /Patches

# RUN: Run commands in the intermediate layers when building the image

# Install freeling dependencies
RUN apt update && apt install -y \
    dh-autoreconf \
    libboost-dev \
    libboost-filesystem1.58.0 \
    libboost-program-options-dev \
    libboost-regex-dev \
    libboost-system-dev \
    libboost-thread-dev \
    libicu-dev \
    swig \
    zlib1g-dev 

# Install python
RUN apt update && apt install -y \
    python2.7-dev 

# Install FreeLing
RUN cd FreeLing && autoreconf --install
RUN cd FreeLing && ./configure
RUN cd FreeLing && make
RUN cd FreeLing && make install

# Make python APIs
RUN export LD_LIBRARY_PATH=/usr/local/lib/libfreeling.so
### Patch the Makefile in python's API to work in this environment.
RUN patch /FreeLing/APIs/python/Makefile -i Patches/Makefile.patch || true
RUN cd /FreeLing/APIs/python && make
### Create symbolics links of _freeling.so and freeling.py in
### the python lib folder.
RUN ln -s /FreeLing/APIs/python/_freeling.so /usr/lib/python2.7/_freeling.so 
RUN ln -s /FreeLing/APIs/python/freeling.py /usr/lib/python2.7/freeling.py
RUN ln -s /usr/bin/python2.7 /usr/bin/python

# Install python dependencies for DUA

RUN apt update && apt install -y \
    python-nltk 

RUN python -c 'import nltk; nltk.download("wordnet")'
RUN python -c 'import nltk; nltk.download("punkt")'

RUN export PYTHONPATH=/ProyGrado/apps/utilities/

## No estoy seguro de que lo necesitemos ##
RUN apt install locales
RUN locale-gen "en_US.UTF-8"
###########################################

# Add Files
RUN mkdir ProyGrado
ADD apps ProyGrado/apps 
ADD tools ProyGrado/tools
ADD corpus ProyGrado/corpus
# CMD: Run command when the container is created.

# Run bash
CMD /bin/bash
