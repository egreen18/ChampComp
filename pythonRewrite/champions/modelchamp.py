from common.modelcommon import (Stats, Abilities, Stack, Effect)
import json
import re

with open(r"../version/latest/champions.json",encoding="utf8") as f:
    data = json.load(f) #load the json file into a dict
    
class Champ(object):
    def __init__(self,name):
        if not name in list(data.keys()):
            print('Invalid champion name')
            return 
        self.level = 1
        self.name = name
        self.inv = ['']*6
        self.inv_id = ['']*6
        self.stats = Stats(data[name]["stats"],1)
        self.abilities = Abilities(data[name]["abilities"])
        self.stats.healthCurrent = self.stats.health
        self.stats.manaCurrent = self.stats.mana
        self.stats_base = self.stats
        stackChamp = ('Thresh','Senna','Nasus','Kindred','Chogath')
        stacks = ('Souls', 'Mist', 'Siphon', 'Marks', 'Feast')
        if self.name in stackChamp:
            self.stack = Stack(stacks[stackChamp.index(self.name)])
    
ratio = re.compile(r"^%\s+|.*:Rscale|.*Soul|.*Mist|.*Siphon|.*Mark|.*Feast")
priscale = re.compile(r"(AP|AD)")
def val(champ1,champ2,abi):
    #Takes input primary champion object champ1, target champion object champ2, 
    #and identiying ability string abi
    
    def translate(match):
       if re.match(r"AP",match):
           return champ1.stats.abilityPower
       elif re.match(r"AD",match):
           return champ1.stats.attackDamage
       
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
    
    for idx,i in enumerate(e):
        for jdx,j in enumerate(i.effects):
            for kdx,k in enumerate(j.leveling):
                lvl = e[0].level-1
                #Rlvl = champ1.abilities.R[0].l
                eff = getattr(effect[idx],'value')[(jdx+1)*(kdx+1)-1]
                for l in k.modifiers:
                    if not ratio.match(l.units[lvl]):
                        eff = eff + float(l.values[lvl])
                    elif priscale.match(ratio.split(l.units[lvl])[1]):
                        eff = eff + float(l.values[lvl])*float(translate(
                            priscale.match(ratio.split(l.units[lvl])[1]).group()))/100
                effect[idx].value[(jdx+1)*(kdx+1)-1] = eff
    return effect
    