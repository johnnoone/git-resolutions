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

# prepare some conflicting commits

cat <<EOF > helloworld.ru
#! /usr/bin/env ruby

def hello
  puts 'hello world'
end
EOF
git add helloworld.ru
git commit -m "first commit"

git checkout -b i18n-world
cat <<EOF > helloworld.ru
#! /usr/bin/env ruby

def hello
  puts 'hola world'
end
EOF
git commit -m "hello -> hola"  helloworld.ru

git checkout master
cat <<EOF > helloworld.ru
#! /usr/bin/env ruby

def hello
  puts 'hello mundo'
end
EOF
git commit -m "world -> mundo"  helloworld.ru
