
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
    def __init__(self, year, domain, train_file, test_file, in_dir="dataset/SemEval", **kwargs):
        super().__init__(**kwargs)
        self.year = year
        self.domain = domain
        self.train_file = os.path.join(in_dir, self.year, self.domain, train_file) 
        self.test_file = os.path.join(in_dir, self.year, self.domain, test_file) 


class TaskConfig(Config):
    """
    A task is about an ABSA task with its dataset configuration.
    """

    def __init__(self, 
        task_name, 
        fileconfig,
        out_dir="dataset/generated", 
        dev_split=150, 
        **kwargs):
        
        super().__init__(**kwargs)
        self.task_name = task_name
        self.fileconfig = fileconfig
        self.dev_split = dev_split
        self.target_dir = os.path.join(out_dir, self.task_name, self.fileconfig.year, self.fileconfig.domain)
