#! /usr/bin/python

import sys

def make_dict(lines):
    defs = map(lambda s: s.replace("\n",""), lines)
    defs = map(lambda s: s.split(":")[:2], defs)
    defs = filter(lambda l: len(l) == 2, defs)
    res = {}
    for d in defs:
        res[d[0]] = d[1].strip()

    return res

defs = open("/home/keegan/prog/ldict/wordlist.txt").readlines()
defs = make_dict(defs)

gen_glossary = len(sys.argv) > 1 and sys.argv[1] == "-g"

not_in_dict = []
for word in sys.stdin.readlines():
    w = word.strip()
    if w in defs:
        if gen_glossary:
            #print("%s: %s" % (w, defs[w]))
            print('\\textbf{%s:} %s\\\\' %(w, defs[w]))
    else:
        not_in_dict.append(w)

if not gen_glossary:
    for word in not_in_dict:
        print(word)
