import pickle
from tqdm import tqdm
import argparse


def sim_tree(word, theasarus):
    top_40 = theasarus[word][:40]
    top_40_words = [w[0] for w in theasarus[word][:40]]
    nesting = {top_40[0][0]: 1}

    seen_words = [top_40[0][0]]
    for w in tqdm(top_40[1:]):
        for pair in theasarus[w[0]]:
            if pair[0] in seen_words:
                index = seen_words.index(pair[0])
                seen_words.insert(index + 1, w[0])
                nesting[w[0]] = nesting[pair[0]] + 1
                break

    print(word)
    for x, y in zip(top_40_words, seen_words):
        print(" |   " * (nesting[y] - 1), "|___", y)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--word")
    args = parser.parse_args()

    with open("thesauri/results_sim.pkl", "rb") as f:
        lin = pickle.load(f)

    sim_tree(args.word, lin)
