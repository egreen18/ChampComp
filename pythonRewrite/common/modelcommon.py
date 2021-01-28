class Stat(object):
    def __init__(self,stat):
        self.flat = stat["flat"]
        self.percent = stat["percent"]
        self.perLevel =stat["perLevel"]
        self.percentPerLevel = stat["percentPerLevel"]
        if "percentBase" in list(stat.keys()):
            self.percentBase = stat["percentBase"]
        if "percentBonus" in list(stat.keys()):
            self.percentBonus = stat["percentBonus"]

class Zeros(Stat):
    def __init__(self):
        self.flat = 0
        self.percent = 0
        self.perLevel = 0
        self.percentPerLevel = 0
        self.percentBase = 0
        self.percentBonus = 0

class Stats(object):
    def __init__(self,stat,simple):
        sta = ['abilityPower',
                'armor',
                'armorPenetration',
                'attackDamage',
                'attackSpeed',
                'attackSpeedRatio',
                'cooldownReduction',
                'criticalStrikeChance',
                'goldPer_10',
                'healAndShieldPower',
                'health',
                'healthRegen',
                'lethality',
                'lifesteal',
                'magicPenPer',
                'magicPenetration',
                'magicResistance',
                'mana',
                'manaRegen',
                'movespeed',
                'abilityHaste',
                'omnivamp',
                'tenacity']
        for i in sta:
            if not i in list(stat.keys()):
                setattr(self,i,Zeros())
            else:
                setattr(self,i,Stat(stat[i]))
                if i == "magicPenetration" and self.magicPenetration.percent != 0:
                    self.magicPenPer.flat = self.magicPenetration.percent
                    print('test')
                    # self.magicPenetration.percent = 0
                elif i == "criticalStrikeChance" and self.criticalStrikeChance.percent != 0:
                    self.criticalStrikeChance.flat = self.criticalStrikeChance.percent
                    self.criticalStrikeChance.percent = 0
                elif i == "armorPenetration" and self.armorPenetration.percent != 0:
                    self.armorPenetration.flat = self.armorPenetration.percent
                    self.armorPenetration.percent = 0
        if simple == 1:
            for i in list(self.__dict__.keys()):
                if i == 'magic_pen_per':
                    setattr(self,i,getattr(self,'magic_penetration').percent)
                else:
                    setattr(self,i,getattr(self,i).flat)
            
class Modifiers(object):
    def __init__(self, modifiers):
        self.values = modifiers["values"]
        self.units = modifiers["units"]
        
class Leveling(object):
    def __init__(self, leveling):
        self.attribute = leveling["attribute"]
        self.modifiers = ['']*len(leveling["modifiers"])
        for i in range(len(leveling["modifiers"])):
            self.modifiers[i] = Modifiers(leveling["modifiers"][i])
    
class Effects(object):
    def __init__(self, effects):
        self.description = effects["description"]
        self.leveling = ['']*len(effects["leveling"])
        for i in range(len(effects["leveling"])):
            self.leveling[i] = Leveling(effects["leveling"][i])
        
class Cost(object):
    def __init__(self):
        self.modifiers = Modifiers()
        
class Cooldown(object):
    def __init__(self):
        self.modifiers = Modifiers()
        self.affectedByCdr
        
class Ability(object):
    def __init__(self, abi):
        self.name = abi["name"]
        self.level = 0
        self.effects = ['']*len(abi["effects"])
        for i in range(len(abi["effects"])):
            self.effects[i] = Effects(abi["effects"][i])
        # self.cost = Cost(abi["cost"])
        # self.cooldown = Cooldown(abi["cooldown"])
        self.damageType = abi["damageType"]
        self.blurb = abi["blurb"]
        
class Abilities(object):
    def __init__(self, abilities):
        keys = ['Q','W','E','R']
        for i in keys:
            setattr(self,i,['']*len(abilities[i]))
            l = getattr(self,i)
            for j in range(len(abilities[i])):
                l[j] = Ability(abilities[i][j])
                
class Stack(object):
    def __init__(self,name):
        self.name = name
        self.count = 0
        self.stats = Stats(dict(null=0),0)
        
class Effect(object):
    def __init__(self,j,k):
        self.name = ''
        self.value = [0]*((j+1)*(k+1)-1)
        self.dealt = [0]*((j+1)*(k+1)-1)
        self.att = ['']*((j+1)*(k+1)-1)
        self.type = ''

class EffectList(object):
    def __init__(self,i,j,k):
        self.effect = ['']*i
        for x  in range(i):
            self.effect[x] = Effect(j,k)

def StatChange(champ,statin,mod,simple):
    if mod == 'add':
        mod = 1
    elif mod == 'remove':
        mod = -1
    if simple == 1:
        for i in list(statin.__dict__.keys()):
            statTemp = getattr(champ.stats,i)
            statinTemp = getattr(statin,i)
            if i == "attackSpeed":
                statTemp = statTemp + mod*statinTemp*champ.stats_base.attackSpeedRatio/100
            else:
                statTemp = statTemp + mod*statinTemp
            setattr(champ.stats,i,statTemp)
    else:
        for i in list(statin.__dict__.keys()):
            statTemp = getattr(champ.stats,i)
            baseTemp = getattr(champ.stats_base,i)
            statinTemp = getattr(statin,i)
            if i == "attackSpeed":
                statTemp = statTemp + mod*(statinTemp.flat*champ.stats_base.attackSpeedRatio/100)
            else:
                statTemp = statTemp + mod*(statinTemp.flat + statinTemp.percent*statTemp
                                   /100 + statinTemp.percentBase*baseTemp/100)
            setattr(champ.stats,i,statTemp)
    return champ.stats