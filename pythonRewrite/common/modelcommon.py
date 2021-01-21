class Stat:
    def __init__(self,stat):
        self.flat = stat["flat"]
        self.percent = stat["percent"]
        self.per_level =stat["perLevel"]
        self.percent_per_level = stat["percentPerLevel"]
        self.percent_base = stat["percentBase"]
        self.percent_bonus = stat["percentBonus"]
    
class Health(Stat):
    pass

class HealthRegen(Stat):
    pass

class Mana(Stat):
    pass

class ManaRegen(Stat):
    pass

class Armor(Stat):
    pass

class MagicResistance(Stat):
    pass

class AttackDamage(Stat):
    pass

class AbilityPower(Stat):
    pass

class Movespeed(Stat):
    pass

class CriticalStrikeChance(Stat):
    pass

class AttackSpeed(Stat):
    pass

class Lethality(Stat):
    pass

class AttackRange(Stat):
    pass

class CooldownReduction(Stat):
    pass

class GoldPer10(Stat):
    pass

class HealAndShieldPower(Stat):
    pass

class Lifesteal(Stat):
    pass

class MagicPenetration(Stat):
    pass

class ArmorPenetration(Stat):
    pass

class AbilityHaste(Stat):
    pass

class OmniVamp(Stat):
    pass

class Tenacity(Stat):
    pass

class Stats(object):
    def __init__(self,stat):
        self.ability_power = AbilityPower(stat["abilityPower"])
        self.armor = Armor(stat["armor"])
        self.armor_penetration = ArmorPenetration(stat["armorPenetration"])
        self.attack_damage = AttackDamage(stat["attackDamage"])
        self.attack_speed = AttackSpeed(stat["attackSpeed"])
        self.cooldown_reduction = CooldownReduction(stat["cooldownReduction"])
        self.critical_strike_chance = CriticalStrikeChance(stat["criticalStrikeChance"])
        self.gold_per_10 = GoldPer10(stat["goldPer_10"])
        self.heal_and_shield_power = HealAndShieldPower(stat["healAndShieldPower"])
        self.health = Health(stat["health"])
        self.health_regen = HealthRegen(stat["healthRegen"])
        self.lethality = Lethality(stat["lethality"])
        self.lifesteal = Lifesteal(stat["lifesteal"])
        self.magic_penetration = MagicPenetration(stat["magicPenetration"])
        self.magic_resistance = MagicResistance(stat["magicResistance"])
        self.mana = Mana(stat["mana"])
        self.mana_regen = ManaRegen(stat["manaRegen"])
        self.movespeed = Movespeed(stat["movespeed"])
        self.ability_haste = AbilityHaste(stat["abilityHaste"])
        self.omnivamp = OmniVamp(stat["omnivamp"])
        self.tenacity = Tenacity(stat["tenacity"])