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
    itemdata = json.load(f) #load the json file into a dict
        
class Item(object):
    def __init__(self,key):
        if not key in list(itemdata.keys()):
            print('Invalid item key')
            return
        self.name = itemdata[key]["name"] 
        self.key = itemdata[key]["id"]
        self.rank = itemdata[key]["rank"]
        self.removed = itemdata[key]["removed"]
        self.icon = itemdata[key]["icon"]
        self.simple_description = itemdata[key]["simpleDescription"]
        self.nicknames = itemdata[key]["nicknames"]
        self.passives = ['']*len(itemdata[key]["passives"])
        for i in range(len(itemdata[key]["passives"])):
            self.passives[i] = Passive(itemdata[key]["passives"][i])
        if itemdata[key]["active"]:
            self.active = Active(itemdata[key]["active"][0])
        else:
            self.active = []
        self.stats = Stats(itemdata[key]["stats"],0)
