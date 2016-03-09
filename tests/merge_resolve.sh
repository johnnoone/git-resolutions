#!/bin/sh

cat <<EOF > helloworld.ru
#! /usr/bin/env ruby

def hello
  puts 'hola mundo'
end
EOF
git commit -m "fix merge"  helloworld.ru
