#!/bin/bash

# windows users recommended to use anaconda prompt or windows bash environment
# mac users can use bash in their terminal
# linux users and servers generally use bash

mkdir data_camp18
cd data_camp18
pwd
ls
mkdir tmp
ls
cd tmp
pwd
cd ..
pwd
ls
rmdir tmp
ls
touch tmp.txt
ls
rm tmp.txt
ls
uname -a
!!
top
htop
echo "hello world!"
echo "hello world!" > hello_world.txt
ls
cat hello_world.txt
echo "hello again world" > hello_world.txt
cat hello_world.txt
echo "yet another thing" >> hello_world.txt
cat hello_world.txt
echo "\nlet's start on a new line this time." >> hello_world.txt
cat hello_world.txt
ls
wget bbc.co.uk
cat index.html
head index.html
tail index.html
tail -n 30 index.html
wc hello_world.txt
wc index.html
wc *
wc *.html
wc -l *.html
cp hello_world.txt hi.txt
ls
ls -l
ls -lh
mv hello_world.txt hello.txt
ls
ls | wc -l
find . -size +100k
find . -size -100k
find . name ".txt" -size +50k
grep "world" *
sed 's/world/universe/g' index.html > grand.html
head index.html
head grand.html
diff index.html grand.html







