#! encoding = utf-8

""" System configuration files """

import json


def to_json(obj, filename):
    """ Serialize an object to json and save on disk
    :argument
        obj: plan object
        filename: str           filename to be saved
    """

    with open(filename, 'w') as fp:
        json.dump(_obj2dict(obj), fp, indent=2)


def from_json_(obj, filename):
    """ Load data from json. Mutable functiona and replace obj in place
    :argument
        obj: the object to write value in
        f: str          filename to load
    """
    with open(filename, 'r') as fp:
        dict_ = json.load(fp)
        _dict2obj_(obj, dict_)


class Config:
    """ PSE Global preferences """

    def __init__(self):

        self.enabled_tm_idx = [0, ]
        self.lang = 'English'
        self.nft = 0
        self.nfc = 0
        self.nbt = 0
        self.nbc = 0
        self.retry_intvl = 10


def _obj2dict(obj):
    """ Convert plain object to dictionary (for json dump) """
    d = {}
    for attr in dir(obj):
        if not attr.startswith('__'):
            d[attr] = getattr(obj, attr)
    return d


def _dict2obj_(obj, dict_):
    """ Convert dictionary values back to plain obj. Mutable function
    :argument
        obj: object to be updated
        dict_: dictionary
    """

    for key, value in dict_.items():
        if isinstance(value, dict):
            for k, v in value.items():
                if isinstance(v, list):
                    # convert list to tuple
                    if len(v) > 0 and isinstance(v[0], list):
                        # convert list in list to tuple as well
                        value[k] = (tuple(vv) for vv in v)
                    else:
                        value[k] = tuple(v)
        setattr(obj, key, value)

