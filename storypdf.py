import sys
import os

# Get macronized text
os.system("macronize -i %s > macronized.txt" % sys.argv[1])
macronized = open("macronized.txt", "r").read()

# Get in-dict/out-of-dict glossary
os.system("cat macronized.txt | gengloss > gloss.txt")
os.system("cat macronized.txt | genmissing > missing.txt")
gloss = open("gloss.txt", "r").read()

# Apply macronized text and glossary to template
template = open("/home/keegan/prog/ldict/blank_story.tex", "r").read()
template = template.replace("%%gloss%%",gloss)
template = template.replace("%%text%%",macronized)
with open("output.tex","w") as w:
    print(template, file=w)

# Generate PDF
os.system("pdflatex output.tex")
