import numpy as np
import os
import json
import random
import argparse

from absaproc.config import FileConfig, TaskConfig
from absaproc.dataset import ABSADataset


fileconfigs = {
    "laptop14": FileConfig("14", "laptop", "Laptop_Train_v2.xml", "Laptops_Test_Gold.xml"),
    "rest14": FileConfig("14", "rest", "Restaurants_Train_v2.xml", "Restaurants_Test_Gold.xml"),
    "laptop15": FileConfig("15", "laptop", "ABSA-15_Laptops_Train_Data.xml", "ABSA15_Laptops_Test.xml"),
    "rest15": FileConfig("15", "rest", "ABSA-15_Restaurants_Train_Final.xml", "ABSA15_Restaurants_Test.xml"),
    "laptop16": FileConfig("16", "laptop", "ABSA16_Laptops_Train_SB1_v2.xml", "EN_LAPT_SB1_TEST_.xml.gold"),
    "rest16": FileConfig("16", "rest", "ABSA16_Restaurants_Train_SB1_v2.xml", "EN_REST_SB1_TEST.xml.gold"),
}

taskconfigs = [
    TaskConfig("ae", fileconfigs["laptop14"]),
    TaskConfig("ae", fileconfigs["rest14"]),
    
    TaskConfig("ae", fileconfigs["rest15"]),
    TaskConfig("ae", fileconfigs["rest16"]),

    TaskConfig("asc", fileconfigs["laptop14"]),
    TaskConfig("asc", fileconfigs["rest14"]),

    TaskConfig("asc", fileconfigs["rest15"]),
    TaskConfig("asc", fileconfigs["rest16"]),

    TaskConfig("e2e", fileconfigs["laptop14"]),
    TaskConfig("e2e", fileconfigs["rest14"]),
    TaskConfig("e2e", fileconfigs["rest15"]),
    TaskConfig("e2e", fileconfigs["rest16"]),
]


def main():
    random.seed(1337)
    np.random.seed(1337)
    
    for taskconfig in taskconfigs:
        dataset = ABSADataset(taskconfig)
        dataset.build()


if __name__ == "__main__":
    main()
