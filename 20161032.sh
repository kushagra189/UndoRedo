#!/bin/sh
if [ "$#" -ne 1 ]; then
    python 20161032_1.py $1 $2
else 
    python 20161032_2.py $1
fi