# Adjective vs. adverb

Code for ODSC Ukraine 2018 workshop Feature Engineering for NLP.

## Prerequisites

Make sure you have the following installed:
- Python 3
- spacy>=2.0.9
```
pip install -U spacy
```
- spacy models for the English language
```
python -m spacy download en_core_web_md
```
- scikit-learn==0.15.2, numpy>=1.8.2, scipy>=0.13.3
```
pip install -U scikit-learn
```
- jupyter
```
pip install jupyter
```

## Contents

The [data](data/) folder contains:
- lists of adjectives and adverbs extracted from the English Wiktionary (see http://dumps.wikimedia.your.org/enwiki/20180401/)
- a data set of 20,000 sentences extracted from [The Blog Authorship Corpus](http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm)

The [aux](aux/) folder contains a script for extracting the data set from [The Blog Authorship Corpus](http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm).

[adjective-vs-adverb.ipynb](adjective-vs-adverb.ipynb) contains a simple prototype for the task of correcting confused adjectives and adverbs:
- How do we change adjectives to adverbs and vice versa?
- What features distinguish adjectives from adverbs?
- Where do we get data?
