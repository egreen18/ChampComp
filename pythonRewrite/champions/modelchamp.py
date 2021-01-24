from common.modelcommon import (Stats, Abilities, Stack, Effect, StatChange)
from items.modelitem import (Item, itemdata)
import json
import re

with open(r"../version/latest/champions.json",encoding="utf8") as f:
    champdata = json.load(f) #load the json file into a dict
    
class Champ(object):
    def __init__(self,name):
        if not name in list(champdata.keys()):
            print('Invalid champion name')
            return 
        self.level = 1
        self.name = name
        self.inv = ['']*6
        self.inv_id = ['']*6
        self.stats = Stats(champdata[name]["stats"],1)
        self.stats_base = Stats(champdata[name]["stats"],1)
        self.stats_myth = Stats(dict(null=0),0)
        self.abilities = Abilities(champdata[name]["abilities"])
        self.healthCurrent = self.stats.health
        self.manaCurrent = self.stats.mana
        stackChamp = ('Thresh','Senna','Nasus','Kindred','Chogath')
        stacks = ('Souls', 'Mist', 'Siphon', 'Marks', 'Feast')
        if self.name in stackChamp:
            self.stack = Stack(stacks[stackChamp.index(self.name)])
            
    def level_change(self,level):
        self.level = level
        self.stats = StatChange(self,self.stats_base,'remove',1)
        statComplex = Stats(champdata[self.name]["stats"],0)
        for i in list(self.stats_base.__dict__.keys()):
            statTemp = getattr(statComplex,i)
            g = statTemp.perLevel
            if i == "attackSpeed":
                b = statComplex.attackSpeedRatio.flat
                staInd = b*(100+g*(level-1)*(0.7025+0.0175*(level-1)))/100
            else:
                b = statTemp.flat
                staInd = b + g*(level-1)*(0.7025+0.0175*(level-1))
            setattr(self.stats_base,i,staInd)
        self.stats = StatChange(self,self.stats_base,'add',1)
        self.healthCurrent = self.stats.health
        self.manaCurrent = self.stats.mana
        
    def quick_level(self):
        self.level_change(6)
        for i in ['Q','W','E','R']:
            abi = getattr(self.abilities,i)
            abi[0].level = 1
            
    def passive_up(self):
        m = 0; mdx = ''
        l = 0; b = 0; g = 0
        for idx,i in enumerate(self.inv):
            if i:
                if i.rank[0] == 'MYTHIC':
                    m += 1
                    mdx = idx
                    for jdx,j in enumerate(i.passives):
                        if j.mythic:
                            mloc = jdx
                elif i.rank[0] == 'BOOTS':
                    b += 1
                elif i.key == 3041 or i.key == 1082: #Counting glory items
                    g += 1
                elif i.rank[0] == 'LEGENDARY':
                    l += 1
        if m > 1 or b > 1 or g > 1:
            return 1
        if not type(mdx) == str:
            self.stats = StatChange(self,self.stats_myth,'remove',0)
            self.stats_myth = Stats(dict(null=0),0)
            for i in list(self.stats_myth.__dict__.keys()):
                for j in list(getattr(self.stats_myth,i).__dict__.keys()):
                    setattr(getattr(self.stats_myth,i),j,getattr(
                            getattr(self.inv[mdx].passives[mloc].stats,i),j)*l)
            self.stats = StatChange(self,self.stats_myth,'add',0)
            
        return 0 
        
    def item(self,item,slot):
        if not item:
            pass
        elif not item in list(itemdata.keys()):
            print('Invalid item key')
            return
        if self.inv[slot]:
                self.stats = StatChange(self,self.inv[slot].stats,'remove',0)
        if not item:
            self.inv[slot] = item
        if item:
            self.inv[slot] = Item(item)
            self.stats = StatChange(self,self.inv[slot].stats,'add',0)
        dup = self.passive_up()
        if dup:
            self.item('',slot)
            print('Rejected item because of unique repition')
        self.healthCurrent = self.stats.health
        self.manaCurrent = self.stats.mana
        
    
def val(champ1,champ2,abi):
    #Takes input primary champion object champ1, target champion object champ2, 
    #and identiying ability string abi
    
    #Translating regex matches to stats
    def translate(match):
       if re.match(r"AP",match):
           return champ1.stats.abilityPower
       elif re.match(r"AD",match):
           return champ1.stats.attackDamage
       
   #Investigating required size of effect list for predefinition
    e = getattr(champ1.abilities,abi)
    imax = len(e)
    jmax = 0
    kmax = 0
    for i in e:
        if len(i.effects) > jmax:
            jmax = len(i.effects)
            for j in i.effects:
                if len(j.leveling) > kmax:
                    kmax = len(j.leveling)
    effect = [Effect(jmax,kmax)]*imax
    
    #Defining regex patterns
    ratio = re.compile(r"^%\s+|.*:Rscale|.*Soul|.*Mist|.*Siphon|.*Mark|.*Feast")
    priscale = re.compile(r"(AP|AD)")
    
    #Parsing units and calculating damage values
    for idx,i in enumerate(e):
        for jdx,j in enumerate(i.effects):
            for kdx,k in enumerate(j.leveling):
                lvl = e[0].level-1
                #Rlvl = champ1.abilities.R[0].l
                effect[idx].att[(jdx+1)*(kdx+1)-1] = k.attribute
                eff = getattr(effect[idx],'value')[(jdx+1)*(kdx+1)-1]
                for l in k.modifiers:
                    if not ratio.match(l.units[lvl]):
                        eff = eff + float(l.values[lvl])
                    elif priscale.match(ratio.split(l.units[lvl])[1]):
                        eff = eff + float(l.values[lvl])*float(translate(
                            priscale.match(ratio.split(l.units[lvl])[1]).group()))/100
                effect[idx].value[(jdx+1)*(kdx+1)-1] = eff
    #Removing extraneous elements of effect structure
    for idx, i in enumerate(effect):
        for jdx in range(len(i.att)):
            if jdx in range(len(i.att)):
                while not i.att[jdx]:
                    del effect[idx].att[jdx]
                    del effect[idx].value[jdx]
                    if not jdx in range(len(i.att)):
                        break
            
    return effect
    