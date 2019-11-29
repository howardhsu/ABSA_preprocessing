import numpy as np
import os
import json
import random
import argparse

from .config import file_config
from .parser import polar_idx, idx_polar, parser_config

def gen_dataset(parser, in_dir, out_dir, task, year, domain, dev_split = 150):
    os.makedirs(os.path.join(out_dir, task, year, domain), exist_ok=True)
    corpus, meta = parser(os.path.join(in_dir, year, domain, file_config[year][domain]['train']))
    train_corpus = corpus[:-dev_split]
    dev_corpus = corpus[-dev_split:]
    path = os.path.join(out_dir, task, year, domain, "train.json")
    with open(path, "w") as fw:
        json.dump({"data": {rec["id"]: rec for rec in train_corpus}, "meta": meta}, fw)
    path = os.path.join(out_dir, task, year, domain, "dev.json")
    with open(path, "w") as fw:
        json.dump({"data": {rec["id"]: rec for rec in dev_corpus}, "meta": meta}, fw)

    test_corpus, test_meta = parser(os.path.join(in_dir, year, domain, file_config[year][domain]['test']))
    if test_meta and not set(test_meta['label_list']).issubset(meta['label_list']):
        print(task, year, domain, ":", "testing set has novel classes.")
    path = os.path.join(out_dir, task, year, domain, "test.json")
    with open(path, "w") as fw:
        json.dump({"data": {rec["id"]: rec for rec in test_corpus}, "meta": meta}, fw)        
