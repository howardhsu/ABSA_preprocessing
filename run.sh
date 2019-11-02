#!/bin/bash

export PYTHONPATH=.:$PYTHONPATH

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task acsc --year 16 --domain laptop

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/SemEval_gen \
        --task acsc --year 16 --domain rest

