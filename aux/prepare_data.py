"""
This scripts extracts 10,000 sentences with adjectives and 10,000 sentences
with adverbs. In all cases, adjectives and adverbs modify a verb.

The input data is The Blog Authorship Corpus available at
http://u.cs.biu.ac.il/~koppel/BlogCorpus.htm.
"""

import argparse
import json
import os
import en_core_web_md

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="Path to the blogs corpus.")
    args = parser.parse_args()

    # Transform adjectives to adverbs and vice versa

    with open("../data/adjectives.txt", "r") as f:
        ADJ = set(line.strip() for line in f.readlines())

    with open("../data/adverbs.txt", "r") as f:
        ADV = set(line.strip() for line in f.readlines())


    def transform_adj_to_adv(adjective):
        """
        Convert an adjective to the corresponding adverb.
        :param adjective: string (adjective)
        :return: string (adverb) or None
        """
        # friendly
        if adjective.endswith("ly"):
            return None
        # hard
        if adjective in ADV:
            return adjective
        # exceptions
        elif adjective == "good":
            return "well"
        elif adjective in ["whole", "true"]:
            return adjective[:-1] + "ly"
        # responsible => responsibly
        elif adjective.endswith("le") and adjective != "sole":
            adverb = adjective[:-1] + "y"
        # angry => angrily
        elif adjective.endswith("y") and adjective != "shy":
            adverb = adjective[:-1] + "ily"
        # idiotic => idiotically
        elif adjective.endswith("ic"):
            adverb = adjective + "ally"
        # full => fully
        elif adjective.endswith("ll"):
            adverb = adjective + "y"
        # free => freely
        else:
            adverb = adjective + "ly"
        # check for validity
        return adverb if adverb in ADV else None

    adj_to_adv, adv_to_adj = dict(), dict()

    for adj in ADJ:
        adv = transform_adj_to_adv(adj)
        if adv and adv != adj:
            adj_to_adv[adj] = adv
            adv_to_adj[adv] = adj

    # Extract sentences

    nlp = en_core_web_md.load(disable=['ner'])

    adj, adv = [], []
    for filename in os.listdir(args.input_dir)[:55]:
        print(filename)
        with open(args.input_dir + filename, "r", encoding="utf-8",
                  errors='ignore') as f:
            for line in f.readlines():
                line = line.strip()
                if len(line) > 0 and not line.startswith("<"):
                    for sent in nlp(line).sents:
                        for i in range(len(sent)):
                            token = sent[i]
                            if token.tag_ == "JJ" and \
                                    token.head.tag_.startswith("VB") and \
                                    adj_to_adv.get(token.text, None):
                                adj.append({"sentence": [token.text
                                                         for token in sent],
                                            "ind": i, "label": "ADJ"})
                            elif token.tag_ == "RB" and \
                                    token.head.tag_.startswith("VB") and \
                                    adv_to_adj.get(token.text, None):
                                adv.append({"sentence": [token.text
                                                         for token in sent],
                                            "ind": i, "label": "ADV"})

    print("Total number of sentences with adjectives:", len(adj))
    print("Total number of sentences with adverbs:", len(adv))

    with open("../data/adj_vs_adv_data.json", "w") as f:
        json.dump(adj[:10000] + adv[:10000], f, indent=4)

    print("Wrote 10,000 samples with adjectives and 10,000 samples with adverbs"
          " to ../data/adj_vs_adv_data.json.")
