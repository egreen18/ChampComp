from typing import Mapping, List, Union
from dataclasses import dataclass
import dataclasses_json
import json

from common.modelcommon import (
    DamageType,
    Health,
    HealthRegen,
    Mana,
    ManaRegen,
    Armor,
    MagicResistance,
    AttackDamage,
    AbilityPower,
    AttackSpeed,
    AttackRange,
    Movespeed,
    Lethality,
    CooldownReduction,
    GoldPer10,
    HealAndShieldPower,
    Lifesteal,
    MagicPenetration,
    Stat,
)
from common.utils import OrderedEnum, ExtendedEncoder


class Resource(OrderedEnum):
    NO_COST = "NO_COST"
    BLOODTHIRST = "BLOODTHIRST"
    MANA = "MANA"
    ENERGY = "ENERGY"
    RAGE = "RAGE"
    FURY = "FURY"
    FEROCITY = "FEROCITY"
    HEALTH = "HEALTH"
    MAXIMUM_HEALTH = "MAXIMUM_HEALTH"
    CURRENT_HEALTH = "CURRENT_HEALTH"
    HEALTH_PER_SECOND = "HEALTH_PER_SECOND"
    MANA_PER_SECOND = "MANA_PER_SECOND"
    CHARGE = "CHARGE"
    COURAGE = "COURAGE"
    HEAT = "HEAT"
    GRIT = "GRIT"
    FLOW = "FLOW"
    SHIELD = "SHIELD"
    OTHER = "OTHER"
    NONE = "NONE"
    SOUL_UNBOUND = "SOUL_UNBOUND"
    BLOOD_WELL = "BLOOD_WELL"


@dataclasses_json.dataclass_json(letter_case=dataclasses_json.LetterCase.CAMEL)
@dataclass
class Stats(object):
    health: Health
    health_regen: HealthRegen
    mana: Mana
    mana_regen: ManaRegen
    armor: Armor
    magic_resistance: MagicResistance
    attack_damage: AttackDamage
    movespeed: Movespeed
    acquisition_radius: Stat
    selection_radius: Stat
    pathing_radius: Stat
    gameplay_radius: Stat
    critical_strike_damage: Stat
    critical_strike_damage_modifier: Stat
    attack_speed: AttackSpeed
    attack_speed_ratio: Stat
    attack_cast_time: Stat
    attack_total_time: Stat
    attack_delay_offset: Stat
    attack_range: AttackRange


@dataclasses_json.dataclass_json(letter_case=dataclasses_json.LetterCase.CAMEL)
@dataclass
class Modifier(object):
    values: List[Union[int, float]]
    units: List[str]


@dataclasses_json.dataclass_json(letter_case=dataclasses_json.LetterCase.CAMEL)
@dataclass
class Cooldown(object):
    modifiers: List[Modifier]
    affected_by_cdr: bool


@dataclasses_json.dataclass_json(letter_case=dataclasses_json.LetterCase.CAMEL)
@dataclass
class Cost(object):
    modifiers: List[Modifier]


@dataclasses_json.dataclass_json(letter_case=dataclasses_json.LetterCase.CAMEL)
@dataclass
class Leveling(object):
    attribute: str
    modifiers: List[Modifier]


@dataclasses_json.dataclass_json(letter_case=dataclasses_json.LetterCase.CAMEL)
@dataclass
class Effect(object):
    description: str
    leveling: List[Leveling]


@dataclasses_json.dataclass_json(letter_case=dataclasses_json.LetterCase.CAMEL)
@dataclass
class Ability(object):
    name: str
    icon: str
    effects: List[Effect]
    cost: Cost
    cooldown: Cooldown
    targeting: str
    affects: str
    spellshieldable: str
    resource: Resource
    damage_type: DamageType
    spell_effects: str
    projectile: str
    on_hit_effects: str
    occurrence: str
    notes: str
    blurb: str
    missile_speed: str
    recharge_rate: str
    collision_radius: str
    tether_radius: str
    on_target_cd_static: str
    inner_radius: str
    speed: str
    width: str
    angle: str
    cast_time: str
    effect_radius: str
    target_range: str

@dataclasses_json.dataclass_json(letter_case=dataclasses_json.LetterCase.CAMEL)
@dataclass
class Champion(object):
    name: str
    icon: str
    resource: Resource
    stats: Stats
    abilities: Mapping[str, List[Ability]]

    def __json__(self, *args, **kwargs):
        # Use dataclasses_json to get the dict
        d = self.to_dict()
        # Delete the two stat objects that don't apply to champions
        for name, stat in d["stats"].items():
            if isinstance(stat, dict):
                del stat["percentBase"]
                del stat["percentBonus"]
        # Return the (un)modified dict
        return json.dumps(d, cls=ExtendedEncoder, *args, **kwargs)
