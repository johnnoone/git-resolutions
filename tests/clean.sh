#!/bin/sh

mkdir repo-a
cd repo-a
git init
touch foo.txt
git add foo.txt
git commit -m "commited foo"
cd ..

mkdir repo-b
cd repo-b
git init
git remote add origin ../repo-a
