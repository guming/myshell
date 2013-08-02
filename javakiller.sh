#!/bin/sh
export LANG=en_US.UTF-8
javaprocess=`ps -ef | grep java | grep tomcat | awk -F ' ' '{print $2}'`
for p2 in $javaprocess
do 
 jstack $p2 >> /opt/$filename-$p2  
 echo "kill process $p2"
   kill -9 $p2
done
