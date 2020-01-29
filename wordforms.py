import sys
import regex #type: ignore
from copy import copy #type: ignore
from functools import reduce #type: ignore
from jellyfish import jaro_winkler #type: ignore
from typing import Callable, List, Dict, Iterator

def count_unique(words: List[str]) -> Dict[str, int]:
    results = {} # type: Dict[str,int]
    for w in words:
        if w in results:
            results[w] += 1
        else:
            results[w] = 1
    return results

def partition(f, l):
    r1 = list(filter(f, l))
    r2 = list(filter(lambda x: not f(x), l))
    return r1,r2

pt,pt2 = partition(lambda x: x < 10, [2,5,7,12,20])
assert(pt == [2,5,7])
assert(pt2 == [12,20])

def merge_dicts(d1,d2,f):
    merged = copy(d2)
    for k,v in d1.items():
        if k in d2:
            merged[k] = f(d1[k],d2[k])
        else:
            merged[k] = d1[k]
    return merged

def to_clean_words(s: str) -> List[str]:
    s = s.replace("...", " ")
    s = s.replace("-", "")
    s = regex.sub("[\*\.,!:\"'`\?]","", s)
    results = list(s.split())
    results = list(filter(lambda x: x.strip() != "", results))
    results = list(map(lambda w: w.upper(), results))
    return sorted(results)

def get_word_usage_counts(s: str) -> Dict[str,int]:
    words = to_clean_words(s)
    return count_unique(words)

def is_similar_enough(w: str, ws: List[str]) -> bool:
    min_similarity = 0.9
    for r in ws:
        s = jaro_winkler(w,r)
        are_similar = (s >= min_similarity and r[0] == w[0])
        start_with_same_letters = r[:4] == w[:4]
        if are_similar: # or start_with_same_letters:
            return True
    return False


def to_similarity_list(words: List[str]) -> List[str]:
    results = [] #type: List[str]
    for w in words:
        if not is_similar_enough(w,results):
            results.append(w)
    return results

def paragraphs(s: str) -> List[str]:
    paragraph_split = "\n"
    paragraphs = regex.split(paragraph_split, s)
    return list(filter(lambda x: x.strip() != "", paragraphs))

def dictionary_intersect(d1,d2,join_func=lambda a,b: a):
    result = {}
    for k,v in d1.items():
        if k in d2.keys():
            result[k] = join_func(d1[k],d2[k])
    return result

path = sys.argv[1]
file_text = open(path,"r").read()
word_usages = get_word_usage_counts(file_text)
word_count = len(to_clean_words(file_text))

most_text = " ".join(paragraphs(file_text)[:-1]) # most = "all but last paragraph"
most_usages = get_word_usage_counts(most_text)

last_paragraph_text = paragraphs(file_text)[-1]
last_paragraph_words = to_clean_words(last_paragraph_text)
last_paragraph_usages = get_word_usage_counts(last_paragraph_text)

only_end_words = dictionary_intersect(word_usages, last_paragraph_usages)
endmulti, endsingle = partition(lambda kv: kv[1] > 1, only_end_words.items())
endsingle = list(map(lambda x: x[0], endsingle))
end_similar, end_newfangled = partition(lambda w: is_similar_enough(w, list(most_usages.keys())), endsingle)

similar_words = to_similarity_list(list(word_usages.keys()))
total_similar_words = len(similar_words)

# Output results
kvstr = lambda kv: "%s(%d)" % (kv[0],kv[1])
multiresults = map(kvstr, endmulti)
singleresults = map(kvstr, endsingle)

print("MULTI-USE WORDS:")
print(",".join(multiresults))
print("")
print("NEW BUT SIMILAR WORDS:")
print(",".join(list(end_similar)))
print("")
print("NEWFANGLED WORDS:")
print(",".join(list(end_newfangled)))
print("")
print("%d unique word forms" % len(word_usages))
print("%d similar word forms (roughly)" % total_similar_words)
print("%d total words" % word_count)
