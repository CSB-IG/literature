#!/bin/bash

##
# shortcut for building install_env.sh
# e.g.:
# ./dump_env.sh > install_env.sh
##

for LIB in `pip freeze`
do
    echo "pip install $LIB" 
done
