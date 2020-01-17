import sys
import os

# Get macronized text
title = sys.argv[1]
author = sys.argv[2]
image = sys.argv[3]
path = sys.argv[4]
os.system("macronize -i %s > macronized.txt" % path)
macronized = open("macronized.txt", "r").read()

# Get in-dict/out-of-dict glossary
os.system("cat macronized.txt | gengloss > gloss.txt")
os.system("cat macronized.txt | genmissing > missing.txt")
gloss = open("gloss.txt", "r").read()

# Apply macronized text and glossary to template
template = open("/home/keegan/prog/ldict/blank_story.tex", "r").read()
template = template.replace("%%author%%", author)
template = template.replace("%%title_img%%", image)
template = template.replace("%%title%%", title)
template = template.replace("%%gloss%%",gloss)
template = template.replace("%%text%%",macronized)
with open("output.tex","w") as w:
    print(template, file=w)

# Generate PDF
os.system("pdflatex output.tex")
os.system("pdfbook output.pdf")
