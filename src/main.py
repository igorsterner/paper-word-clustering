import cProfile
import io
import pickle
import pstats
from collections import Counter

# from plogger.info import plogger.info
import os
import sys

import numpy as np
from tqdm import tqdm

import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter

log_path = "logging"

logger = logging.getLogger(__name__)

max_freq = 400
debug = False


class word_clustering:
    def __init__(self) -> None:
        pass

    def load_data(self):
        logger.info("Opening dependency triplets...")
        # dependency_triples = []

        # for i in range(1,4):
        #     with open(f'data/dependencies_{i}00000.pkl', 'rb') as f:
        #         dependency_triples += pickle.load(f)

        pos_data = []
        for i in tqdm(range(1, 3)):
            with open(f"data/dependencies_{i}00000_pos.pkl", "rb") as f:
                pos_data += pickle.load(f)

        dependency_triples = [(t[0], t[2], t[3]) for t in pos_data]
        noun_vocab = []

        for trip in pos_data:
            if trip[1] == "NOUN":
                noun_vocab.append(trip[0])

        c = Counter(noun_vocab)
        noun_vocab = [w for w, freq in c.items() if freq > max_freq]
        logger.info(len(noun_vocab))
        logger.info("Generating vocab lists")

        word_vocab = []
        depd_vocab = []
        cont_vocab = []

        for trip in dependency_triples:
            word_vocab.append(trip[0])
            depd_vocab.append(trip[1])
            cont_vocab.append(trip[2])

        c = Counter(word_vocab)
        word_vocab = [w for w, freq in c.items() if freq > max_freq]

        c = Counter(depd_vocab)
        depd_vocab = [i[0] for i in c.most_common(8)]

        c = Counter(cont_vocab)
        cont_vocab = [w for w, freq in c.items() if freq > max_freq]

        if debug:
            logger.info(f"Length of word vocab = {len(word_vocab)}")
            logger.info(f"Number of dependency types = {len(depd_vocab)}")
            logger.info(f"Length of context vocab = {len(cont_vocab)}")

        a = {}
        b = {triplet[1]: {} for triplet in dependency_triples}
        c = {triplet[1]: {} for triplet in dependency_triples}
        d = {triplet[1]: {} for triplet in dependency_triples}

        for triplet in tqdm(dependency_triples):
            if triplet[1] in a:
                a[triplet[1]] += 1
            else:
                a[triplet[1]] = 1

            if triplet[2] in b[triplet[1]]:
                b[triplet[1]][triplet[2]] += 1
            else:
                b[triplet[1]][triplet[2]] = 1

            if triplet[0] in c[triplet[1]]:
                c[triplet[1]][triplet[0]] += 1
            else:
                c[triplet[1]][triplet[0]] = 1

            if (triplet[0], triplet[2]) in d[triplet[1]]:
                d[triplet[1]][(triplet[0], triplet[2])] += 1
            else:
                d[triplet[1]][(triplet[0], triplet[2])] = 1

        self.a = a
        self.b = b
        self.c = c
        self.d = d

        self.num_xxx = len(dependency_triples)

        self.depd_vocab = depd_vocab
        self.cont_vocab = cont_vocab
        self.noun_vocab = noun_vocab

    def I(self, w, r, wp, debug=False):
        num_xrx = self.a[r]
        num_xrw = self.b[r].get(wp, 0)
        num_wrx = self.c[r].get(w, 0)
        num_wrw = self.d[r].get((w, wp), 0)

        if not all([self.num_xxx, num_xrx, num_wrx, num_xrw, num_wrw]):
            return None

        P_MLE_B = num_xrx / self.num_xxx
        P_MLE_A_B = num_wrx / num_xrx
        P_MLE_C_B = num_xrw / num_xrx
        P_MLE_ABC = num_wrw / self.num_xxx

        I_wrwp = -np.log(P_MLE_B * P_MLE_A_B * P_MLE_C_B) - (-np.log(P_MLE_ABC))

        if debug:
            logger.info(f"p(B) = {P_MLE_B}")
            logger.info(f"p(A|B) = {P_MLE_A_B}")
            logger.info(f"p(C|B) = {P_MLE_C_B}")

            logger.info(f"p(A,B,C) = {P_MLE_ABC}")

            assert round(I_wrwp, 3) == round(
                np.log((num_wrw * num_xrx) / (num_wrx * num_xrw)), 3
            )

        return I_wrwp

    def T(self, w):
        T = []
        for r in self.depd_vocab:
            for wp in self.cont_vocab:
                mi = self.I(w, r, wp)
                if not mi:
                    continue
                elif mi > 0:
                    T.append((r, wp))
                else:
                    continue
        return set(T)

    def sim(self, w1, w2, debug=False):
        T1 = self.T(w1)
        T2 = self.T(w2)

        T12 = list(T1.intersection(T2))

        if debug:
            logger.info(f"Length T1: {len(T1)}")
            logger.info(f"Length T2: {len(T2)}")
            logger.info(f"Length T12: {len(T12)}")

        numerator = 0
        denominator = 0

        for pair in T12:
            numerator += self.I(w1, pair[0], pair[1])
            numerator += self.I(w2, pair[0], pair[1])

        for pair in T1:
            denominator += self.I(w1, pair[0], pair[1])

        for pair in T2:
            denominator += self.I(w2, pair[0], pair[1])

        return numerator / denominator

    def simHindle(self, w1, w2):
        T1 = self.T(w1)
        T2 = self.T(w2)

        T12 = list(T1.intersection(T2))

        keep = [
            "dobj-of",
            "pobj-of",
            "nsubjpass-of",
            "csubjpass-of",
            "nsubj-of",
            "csubj-of",
        ]

        T12 = [p for p in T12 if p[0] in keep]

        output = 0

        for pair in T12:
            output += min(self.I(w1, pair[0], pair[1]), self.I(w2, pair[0], pair[1]))

        return output

    def simHindle_r(self, w1, w2):
        T1 = self.T(w1)
        T2 = self.T(w2)

        T12 = list(T1.intersection(T2))

        output = 0

        for pair in T12:
            output += min(self.I(w1, pair[0], pair[1]), self.I(w2, pair[0], pair[1]))

        return output

    def simCosine(self, w1, w2):
        T1 = self.T(w1)
        T2 = self.T(w2)

        T12 = list(T1.intersection(T2))

        return len(T12) / (np.sqrt(len(T1) * len(T2)))

    def simDice(self, w1, w2):
        T1 = self.T(w1)
        T2 = self.T(w2)

        T12 = list(T1.intersection(T2))

        return 2 * len(T12) / (len(T1) + len(T2))

    def simJacard(self, w1, w2):
        T1 = self.T(w1)
        T2 = self.T(w2)

        T12 = list(T1.intersection(T2))

        return len(T12) / (len(T1) + len(T2) - len(T12))

    def evalulate(self, w1, sim_metric):
        theas = []

        for w2 in self.noun_vocab:
            if w1 == w2:
                continue
            elif w1 == w2[:-1] or w2 == w1[:-1]:
                continue
            theas.append((w2, getattr(self, sim_metric)(w1, w2)))

        theas.sort(key=lambda x: x[1], reverse=True)

        # logger.info(f"Original word was: {w1}")
        # theas = [(t[0], round(t[1],2)) for t in theas[:10]]
        # logger.info(theas)
        return theas


def initialization():
    # ====== Set Logger =====
    log_file_format = "[%(levelname)s] - %(asctime)s - %(name)s : %(message)s (in %(pathname)s:%(lineno)d)"
    log_console_format = "[%(levelname)s] - %(name)s : %(message)s"

    # Main logger
    main_logger = logging.getLogger()
    main_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(Formatter(log_console_format))
    from utils.color_logging import CustomFormatter

    custom_output_formatter = CustomFormatter(custom_format=log_console_format)
    console_handler.setFormatter(custom_output_formatter)

    info_file_handler = RotatingFileHandler(
        os.path.join(log_path, "info.log"),
        maxBytes=10**6,
        backupCount=5,
    )

    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(Formatter(log_file_format))

    exp_file_handler = RotatingFileHandler(
        os.path.join(log_path, "debug.log"),
        maxBytes=10**6,
        backupCount=5,
    )

    exp_file_handler.setLevel(logging.DEBUG)
    exp_file_handler.setFormatter(Formatter(log_file_format))

    exp_errors_file_handler = RotatingFileHandler(
        os.path.join(log_path, "error.log"),
        maxBytes=10**6,
        backupCount=5,
    )
    exp_errors_file_handler.setLevel(logging.WARNING)
    exp_errors_file_handler.setFormatter(Formatter(log_file_format))

    main_logger.addHandler(console_handler)
    main_logger.addHandler(info_file_handler)
    main_logger.addHandler(exp_file_handler)
    main_logger.addHandler(exp_errors_file_handler)

    # setup a hook to log unhandled exceptions
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)

        logger.error(
            f"Uncaught exception: {exc_type} --> {exc_value}",
            exc_info=(exc_type, exc_value, exc_traceback),
        )


if __name__ == "__main__":
    initialization()
    sims = ["sim", "simHindle", "simHindle_r", "simCosine", "simDice", "simJacard"]
    WC = word_clustering()
    WC.load_data()
    for sim_metric in sims:
        logger.info(sim_metric)
        results = {}
        for w1 in tqdm(WC.noun_vocab):
            results[w1] = WC.evalulate(w1, sim_metric)

        with open(f"results_{sim_metric}.pkl", "wb") as f:
            pickle.dump(results, f)
