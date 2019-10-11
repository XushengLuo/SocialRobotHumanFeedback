#!/bin/bash

for ((i=1; i<=10;i++))
do
    for j in 0 1
    do
        /usr/local/Cellar/python/3.6.3/Frameworks/Python.framework/Versions/3.6/bin/python3.6 /Users//chrislaw/Documents/GitHub/zero_opt/main.py ${j}
    done
done
