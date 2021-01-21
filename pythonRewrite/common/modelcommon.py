class Stat(object):
    def __init__(self,stat):
        self.flat = stat["flat"]
        self.percent = stat["percent"]
        self.per_level =stat["perLevel"]
        self.percent_per_level = stat["percentPerLevel"]
        if "percentBase" in list(stat.keys()):
            self.percent_base = stat["percentBase"]
        if "peercentBonus" in list(stat.keys()):
            self.percent_bonus = stat["percentBonus"]

class Zeros(Stat):
    def __init__(self):
        self.flat = 0
        self.percent = 0
        self.per_level = 0
        self.percent_per_level = 0
        self.percent_base = 0
        self.percent_bonus = 0

class Stats(object):
    def __init__(self,stat,simple):
        sta = ['abilityPower',
                'armor',
                'armorPenetration',
                'attackDamage',
                'attackSpeed',
                'cooldownReduction',
                'criticalStrikeChance',
                'goldPer_10',
                'healAndShieldPower',
                'health',
                'healthRegen',
                'lethality',
                'lifesteal',
                'magicPenetration',
                'magicResistance',
                'mana',
                'manaRegen',
                'movespeed',
                'abilityHaste',
                'omnivamp',
                'tenacity',
                'magicPenPer']
        for i in sta:
            if i in list(stat.keys()):
                setattr(self,i,Stat(stat[i]))
            else:
                setattr(self,i,Zeros())
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