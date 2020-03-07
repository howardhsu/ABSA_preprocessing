import numpy as np
import os
import json
import random

from . import task


class ABSADataset(object):
    # TODO: add a function to report dataset statistics.
    def __init__(self, taskconfig):
        self.taskconfig = taskconfig
        self.task = getattr(task, self.taskconfig.task_name.upper()+"Task")(taskconfig)

    def _write_json(self, fn, corpus, meta=None):
        path = os.path.join(self.taskconfig.target_dir, fn)
        with open(path, "w") as fw:
            json.dump({"data": {rec["id"]: rec for rec in corpus}, "meta": meta}, fw)


    def build(self):
        
        os.makedirs(self.taskconfig.target_dir, exist_ok=True)

        # each file config has a input path.
        corpus, meta = self.task.parseTrain()
        train_corpus = corpus[:-self.taskconfig.dev_split]
        dev_corpus = corpus[-self.taskconfig.dev_split:]
        
        self._write_json("train.json", train_corpus, meta)        
        self._write_json("dev.json", dev_corpus, meta)

        test_corpus, test_meta = self.task.parseTest()
        self._write_json("test.json", test_corpus, meta)
