import numpy as np
import os
import json
import random
import argparse

from absa import gen_dataset, polar_idx, idx_polar, file_config, parser_config

# TODO: add all config here.


def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--in_dir", default=None, type=str, required=True, help="input folder.")

    parser.add_argument("--out_dir",
                        default=None,
                        type=str,
                        required=True,
                        help="output folder.")
    
    parser.add_argument("--task",
                        default=None,
                        type=str,
                        required=True,
                        help="name of the task.")

    parser.add_argument("--year",
                        default=None,
                        type=str,
                        required=True,
                        help="year of the dataset.")
    
    parser.add_argument("--domain",
                        default=None,
                        type=str,
                        required=True,
                        help="domain of the dataset.")

    args = parser.parse_args()

    random.seed(1337)
    np.random.seed(1337)
    
    gen_dataset(parser_config[args.task][args.year], 
            args.in_dir, args.out_dir, args.task, args.year, args.domain)


if __name__ == "__main__":
    main()
