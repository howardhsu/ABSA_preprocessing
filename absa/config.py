
import os
import json
import copy

class Config(object):
    """
    Base class for all configurations.
    """
    def __init__(self, **kwargs):
        self.config_cls = self.__class__.__name__

    @classmethod
    def from_json_file(cls, json_file):
        with open(json_file) as f:
            config_dict = json.load(f)
        return cls.from_dict(config_dict)

    @classmethod
    def from_dict(cls, config_dict):
        config = cls(**config_dict)
        return config

    def to_dict(self):
        return copy.deepcopy(self.__dict__)

    def to_json_file(self, json_file):
        with open(json_file, "w") as fw:
            json.dump(self.to_dict, fw)


class FileConfig(Config):
    def __init__(self, year, domain, mode, source, **kwargs):
        super().__init__(**kwargs)
        self.year = year
        self.domain = domain
        self.mode = mode
        self.source = source


class TaskConfig(FileConfig):
    def __init__(self, task, **kwargs):
        super().__init__(**kwargs)
        self.task = task
        self.data_dir = os.path.join("data/generated", self.task, self.year, self.domain)


file_config = {
    '14': {
        'laptop': {
            'train': 'Laptop_Train_v2.xml', 
            'test': 'Laptops_Test_Gold.xml'
        },
        'rest': {
            'train': 'Restaurants_Train_v2.xml',
            'test': 'Restaurants_Test_Gold.xml'
        }
    },

    '15': {
        'laptop': {
            'train': 'ABSA-15_Laptops_Train_Data.xml', 
            'test': 'ABSA15_Laptops_Test.xml'
        },
        'rest': {
            'train': 'ABSA-15_Restaurants_Train_Final.xml',
            'test': 'ABSA15_Restaurants_Test.xml'
        }
    },

    '16': {
        'laptop': {
            'train': 'ABSA16_Laptops_Train_SB1_v2.xml', 
            'test': 'EN_LAPT_SB1_TEST_.xml.gold'
        },
        'rest': {
            'train': 'ABSA16_Restaurants_Train_SB1_v2.xml',
            'test': 'EN_REST_SB1_TEST.xml.gold'
        }
    }
}
