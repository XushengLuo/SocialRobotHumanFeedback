#!/bin/bash

# for k in 60
# do
#     echo "---------------------------k = ${k}-------------------------"
#     # for((i=1; i<=20;i++))
#     # do
#     /usr/local/Cellar/python/3.6.3/Frameworks/Python.framework/Versions/3.6/bin/python3.6 /Users/chrislaw/Github/SocialRobotHumanFeedback/main.py ${k}
#     #done
#     echo "------------------"
# done


for k in 5
do
    for r in 0.3 1
    do
        for((i=1; i<=5;i++))
        do
            echo "max_iter = ${k}, radius = ${r}, repeat = ${i}"
            /usr/local/Cellar/python/3.6.3/Frameworks/Python.framework/Versions/3.6/bin/python3.6 /Users/chrislaw/Github/SocialRobotHumanFeedback/main_online.py ${k} ${r} ${i}
        done
    done
done
