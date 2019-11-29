#!/bin/bash

export PYTHONPATH=.:$PYTHONPATH


python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task ae --year 14 --domain laptop

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task ae --year 14 --domain rest

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task ae --year 15 --domain rest

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task ae --year 16 --domain rest

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task asc --year 14 --domain laptop

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task asc --year 14 --domain rest

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task asc --year 15 --domain rest

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task asc --year 16 --domain rest


python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task e2e --year 14 --domain laptop

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task e2e --year 14 --domain rest

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task e2e --year 15 --domain rest

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task e2e --year 16 --domain rest


python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task scc --year 14 --domain rest

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task scc --year 15 --domain laptop

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task scc --year 15 --domain rest

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task scc --year 16 --domain laptop

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task scc --year 16 --domain rest


python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task acc --year 15 --domain rest


python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task acc --year 16 --domain rest


python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task acsc --year 14 --domain rest

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task acsc --year 15 --domain laptop

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task acsc --year 15 --domain rest

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task acsc --year 16 --domain laptop

python3 script/build.py --in_dir dataset/SemEval \
        --out_dir dataset/generated \
        --task acsc --year 16 --domain rest

