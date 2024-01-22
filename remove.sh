#!/bin/bash

read -p "Are you sure? (this will remove the entire tests folder) " -n 1 -r
echo
if [[ $REPLY =~ ^[YyOo]$ ]]
then
    #DANGEROUS
    rm -rf tests
fi
