# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置文件类，使用方法：
ConfigMgr.init(path1, path2, path3) # 初始化， 可提供path1, path2, path3其中1个至3个，不提供默认为../etc/config.json
获取某个json值：ConfigMgr.get("p1","p2", "p3")
存在p1,p2,p3为key的字典，返回字典值，否则返回None
"""
import json
import os
import threading


class JsonConf(object):
    def __init__(self, file_name):
        self.file_name = file_name
        self._data = self.load_file(file_name)

    def get(self):
        return self._data

    def load_file(self, file_name):
        if not os.path.exists(file_name):
            return {}
        with open(file_name, encoding="utf-8") as json_file:
            try:
                data = json.load(json_file)
            except Exception as e:
                print(e)
                data = {}

        return data


class ConfigMgr(object):
    _instance_lock = threading.Lock()

    def __init__(self, path1, path2, path3):
        self.path1 = path1
        self.path2 = path2
        self.path3 = path3

    @classmethod
    def init(self, path1="../etc/config.json", path2="../../etc/config.json", path3="../../../etc/global_config.json"):
        ConfigMgr(path1, path2, path3)

    def __new__(cls, *args, **kwargs):
        if not hasattr(ConfigMgr, "_instance"):
            with ConfigMgr._instance_lock:
                if not hasattr(ConfigMgr, "_instance"):
                    ConfigMgr._instance = object.__new__(cls)
                    ConfigMgr._instance.load_conf(args[0], args[1], args[2])

        return ConfigMgr._instance

    def load_conf(self, path1, path2, path3):
        a0 = JsonConf(path3)
        a = JsonConf(path2)
        b = JsonConf(path1) # path1是最重要的，所有的都会被path1覆盖
        # 不能放在init中，原因是每调用一次ConfigMgr._instance就会调用一次init
        tmp = dict(a0.get(), **a.get())
        self._data = dict(tmp, **b.get())

    @staticmethod
    def get(*args):
        length = len(args)
        try:
            if length == 1:
                return ConfigMgr._instance._data[args[0]]
            elif length == 2:
                return ConfigMgr._instance._data[args[0]][args[1]]
            elif length == 3:
                return ConfigMgr._instance._data[args[0]][args[1]][args[2]]
            elif length == 4:
                return ConfigMgr._instance._data[args[0]][args[1]][args[2]][args[3]]
        except:
            return None

    @staticmethod
    def has_key(*args):
        length = len(args)
        data = ConfigMgr._instance._data
        if length == 1:
            return args[0] in data
        elif length == 2:
            return args[0] in data and args[1] in data[args[0]]
        elif length == 3:
            return args[0] in data and args[1] in data[args[0]] and args[2] in data[args[0]][args[1]]


if __name__ == "__main__":
    ConfigMgr.init("../etc/config.json")
    print(ConfigMgr.get("all_capital_ratio"))
