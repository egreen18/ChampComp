import json

from common.modelcommon import Stats

class Passive(object):
    def __init__(self,passive):
        self.unique = passive["unique"]
        self.mythic = passive["mythic"]
        self.name = passive["name"]
        self.effects = passive["effects"]
        self.range = passive["range"]
        self.stats = Stats(passive["stats"],0)
    
class Active(object):
    def __init__(self,active):
        self.unique = active["unique"]
        self.name = active["name"]
        self.effects = active["effects"]
        self.range = active["range"]
        self.cooldown = active["cooldown"]

with open(r"../version/latest/Items.json",encoding="utf8") as f:
    data = json.load(f) #load the json file into a dict
        
class Item(object):
    def __init__(self,key):
        if not key in list(data.keys()):
            print('Invalid item key')
            return
        self.name = data[key]["name"] 
        self.id = data[key]["id"]
        self.rank = data[key]["rank"]
        self.removed = data[key]["removed"]
        self.icon = data[key]["icon"]
        self.simple_description = data[key]["simpleDescription"]
        self.nicknames = data[key]["nicknames"]
        self.passives = ['']*len(data[key]["passives"])
        for i in range(len(data[key]["passives"])):
            self.passives[i] = Passive(data[key]["passives"][i])
        if data[key]["active"]:
            self.active = Active(data[key]["active"][0])
        else:
            self.active = []
        self.stats = Stats(data[key]["stats"],0)
