import copy
import json

class Struct:
    def __init__(self, data):
        self.data=data
    def dumps(self, indent=None):
        return json.dumps(self.data, indent=indent)
    @staticmethod
    def loads(string):
        return Struct(json.loads(string))
    def dump(self, file, indent=None):
        json.dump(self, file,indent=indent)
    @staticmethod
    def load(file):
        return  Struct(json.load(file))
    def __repr__(self):
        return self.dumps(indent=4)
    def __setitem__(self, path, value):
        if type(path)==str:
            path=[path]
        modifyStruct(self.data, list(path)+[value])
    def __delitem__(self, path):
        self[path]=None
    def __contains__(self, key):
        return isKeyIn(self.data, key)
    def __getitem__(self, path):
        if type(path)==str:
            path=[path]
        return getItem(self.data, list(path))
    def __iter__(self):
        if type(self.data)==dict:
            return [(k, self.data[k]) for k in self.data].__iter__()
        elif type(self.data)==list:
            return self.data.__iter__()
        else:
            return [self.data].__iter__()
    def __len__(self):
        n=0
        for x in self.data:
            n+=1
        return n
    def sorted(self, path=None):
        if type(self.data)==list:
            if path==None:
                return Struct(sorted(self.data))
            else:
                return Struct(sorted(self.data, key=lambda x:Struct(x)[path]))
        else:
            result = Struct({})
            if path==None:
                for e in sorted(self):
                    result[e[0]]=e[1]
            else:
                for e in sorted(self, key=lambda x: Struct(x[1])[path]):
                    result[e[0]] = e[1]
            return result
    def sort(self, path=None):
        self=self.sort(path)

    def isValueIn(self, value):
        return isValueIn(self.data, value)
    def pathToValue(self, value):
        return pathToValue(self.data, value)
    def getAll(self, key):
        return getAll(self.data, key)
    def replace(self, old, new):
        result=copy.deepcopy(self)
        if (path:=result.pathToValue(old))!=None:
            del path[-1]
            result[path]=new
        return result
    def replaceAll(self, old, new):
        result = copy.deepcopy(self)
        while (path := result.pathToValue(old)) != None:
            del path[-1]
            result[path] = new
        return result


def getItem(data, path):
    if path==[]:
        return data
    return getItem(data[path[0]], path[1:])

def modifyStruct(data, path):
    if len(path) == 2:
        data[path[0]] = path[1]
        if path[1] == None:
            del data[path[0]]
        return data
    if type(data)==dict:
        data.setdefault(path[0], {})
    data[path[0]] = modifyStruct(data[path[0]], path[1:])
    if data[path[0]] == {}:
        del data[path[0]]
    return data

def isValueIn(data, value):
    if data == value:
        return True

    elif type(data) == list:
        for x in data:
            if isValueIn(x, value):
                return True
        return False
    elif type(data) == dict:
        for k in data:
            if isValueIn(data[k], value):
                return True
    return False


def pathToValue(data, value):
    if data == value:
        return [value]

    if type(data) == dict:
        sequence = data.keys()
    else:
        sequence = range(len(data))

    for k in sequence:
        if isValueIn((sub := data[k]), value):
            return [k] + pathToValue(sub, value)

def isKeyIn(data, key):
    sequence = []
    if type(data) == list:
        sequence = range(len(data))
    elif type(data) == dict:
        sequence = data.keys()
    for k in sequence:
        if k == key:
            return True
        elif isKeyIn(data[k], key):
            return True
    return False


def getAll(data, key):
    sequence = []
    if type(data) == list:
        sequence = range(len(data))
    elif type(data) == dict:
        sequence = data.keys()
    values = []
    for k in sequence:
        if k == key:
            values.append(data[k])
        else:
            values += getAll(data[k], key)
    return values