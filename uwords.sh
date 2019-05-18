#! /bin/sh
tr '[:punct:]' ' ' | tr '[:upper:]' '[:lower:]' | tr '[:space:]' '[\n*]' | grep -v "^\s*$" | sort | uniq | ./glossify.py
