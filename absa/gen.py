import numpy as np
import os
import json
import random
import argparse

from .config import polar_idx, idx_polar, file_config
from .parser import parser_config

def gen_dataset(parser, in_dir, out_dir, task, year, domain, dev_split = 150):
    os.makedirs(os.path.join(out_dir, task, year, domain), exist_ok=True)
    corpus, cat2id = parser(os.path.join(in_dir, year, domain, file_config[year][domain]['train']))
    train_corpus = corpus[:-dev_split]
    dev_corpus = corpus[-dev_split:]
    path = os.path.join(out_dir, task, year, domain, "train.json")
    with open(path, "w") as fw:
        json.dump({"data": {rec["id"]: rec for rec in train_corpus}, "cat2id": cat2id}, fw)
    path = os.path.join(out_dir, task, year, domain, "dev.json")
    with open(path, "w") as fw:
        json.dump({"data": {rec["id"]: rec for rec in dev_corpus}, "cat2id": cat2id}, fw)

    test_corpus, test_cat2id = parser(os.path.join(in_dir, year, domain, file_config[year][domain]['test']))
    if not set(test_cat2id).issubset(cat2id):
        print(task, year, domain, ":", "testing set has novel classes.")
    path = os.path.join(out_dir, task, year, domain, "test.json")
    with open(path, "w") as fw:
        json.dump({"data": {rec["id"]: rec for rec in test_corpus}, "cat2id": cat2id}, fw)        
