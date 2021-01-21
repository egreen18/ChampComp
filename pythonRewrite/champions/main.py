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
from common.utils import (
    download_soup,
    parse_top_level_parentheses,
    grouper,
    to_enum_like,
    download_json,
)
from champions.modelchampion import (
    Champion,
    Stats,
    Ability,
    Cooldown,
    Cost,
    Effect,
    Resource,
    Modifier,
    Leveling,
)

class jsonToObject:


    def render_champ_data(self,data) -> Champion:
        champion = data["name"] #champion == champion name
        abilities = dict() #create an ability dictionary
        for ab in data["abilities"]: #for ability in ability
            abil = [] #Every ability is a list of abilities so we create a list to match that
            #print(ab) #print the ability key (this was for testing), it will be either  P Q W E or R
            for a in data["abilities"][ab]: #for each ability in the list of abilities
                abil.append(self._render_ability(a)) #send the ability to _render_ability and append it to abil list
            abilities[ab] = abil #set abilities[key"] == ability list
        champ = Champion(
            name=champion,
            icon=data["icon"],
            resource=data["resource"],
            stats=Stats(#create a stat object from the stats)
                health=Health(
                    flat=data["stats"]["health"]["flat"],
                    per_level=data["stats"]["health"]["perLevel"],
                ),
                health_regen=HealthRegen(
                    flat=data["stats"]["healthRegen"]["flat"],
                    per_level=data["stats"]["healthRegen"]["perLevel"],
                ),
                mana=Mana(
                    flat=data["stats"]["mana"]["flat"],
                    per_level=data["stats"]["mana"]["perLevel"],
                ),
                mana_regen=ManaRegen(
                    flat=data["stats"]["manaRegen"]["flat"],
                    per_level=data["stats"]["mana"]["perLevel"],
                ),
                armor=Armor(
                    flat=data["stats"]["armor"]["flat"],
                    per_level=data["stats"]["armor"]["perLevel"],
                ),
                magic_resistance=MagicResistance(
                    flat=data["stats"]["magicResistance"]["flat"],
                    per_level=data["stats"]["magicResistance"]["perLevel"],
                ),
                attack_damage=AttackDamage(
                    flat=data["stats"]["attackDamage"]["flat"],
                    per_level=data["stats"]["attackDamage"]["perLevel"],
                ),
                attack_speed=AttackSpeed(
                    flat=data["stats"]["attackSpeed"]["flat"],
                    per_level=data["stats"]["attackSpeed"]["perLevel"],
                ),
                attack_speed_ratio=Stat(flat=data["stats"]["attackSpeedRatio"]["flat"]),
                attack_cast_time=Stat(
                    flat=data["stats"]["attackCastTime"]["flat"]
                ),
                attack_total_time=Stat(flat=data["stats"]["attackTotalTime"]["flat"]),
                attack_delay_offset=Stat(flat=data["stats"]["attackDelayOffset"]["flat"]),
                attack_range=AttackRange(
                    flat=data["stats"]["attackRange"]["flat"],
                    per_level=data["stats"]["attackRange"]["perLevel"],
                ),
                critical_strike_damage=Stat(flat=data["stats"]["criticalStrikeDamage"]["flat"]),
                critical_strike_damage_modifier=Stat(
                    flat=data["stats"]["criticalStrikeDamageModifier"]["flat"]),
                movespeed=Movespeed(flat=data["stats"]["movespeed"]["flat"]),
                acquisition_radius=Stat(flat=data["stats"]["acquisitionRadius"]["flat"]),
                selection_radius=Stat(flat=data["stats"]["selectionRadius"]["flat"]),
                pathing_radius=Stat(flat=data["stats"]["pathingRadius"]["flat"]),
                gameplay_radius=Stat(flat=data["stats"]["gameplayRadius"]["flat"]),
            ),
            abilities=abilities,
        )
        return champ

    def _render_ability(self,data):
        effects = [] #empty list for effects

        if data["cost"]: # if cost is not none
            modifiers_Cost=[]
            for m in data["cost"]["modifiers"]:
                #print(m)
                modifier_cost = Modifier(# create a modifier object and add that to list
                    values=m["values"],
                    units=m["units"],
                )
                modifiers_Cost.append(modifier_cost)
            cost = Cost(modifiers=modifiers_Cost) #set cost == Cost object
        else:
            cost = None
        if data["cooldown"]:
            modifiers_CD = []
            for m in data["cooldown"]["modifiers"]:
                #print(m)
                modifier = Modifier(
                    values=m["values"],
                    units=m["units"],
                )
                modifiers_CD.append(modifier)
            cd = Cooldown(modifiers=modifiers_CD, affected_by_cdr=data["cooldown"]["affectedByCdr"])
        else:
            cd = None

        for effect in data["effects"]: #create list of effect objects
            effects.append(Effect(description=effect["description"],leveling=effect["leveling"]))
        ability = Ability(#create Ability object with all the data from the json
            name=data["name"],
            icon=data["icon"],
            effects=effects,
            cost=cost,
            cooldown=cd,
            targeting=data["targeting"],
            affects=data["affects"],
            spellshieldable=data["spellshieldable"],
            resource=data["resource"],
            damage_type=data["damageType"],
            spell_effects=data["spellEffects"],
            projectile=data["projectile"],
            on_hit_effects=data["onHitEffects"],
            occurrence=data["occurrence"],
            blurb=data["blurb"],
            notes=data["occurrence"],
            missile_speed=data["missileSpeed"],
            recharge_rate=data["rechargeRate"],
            collision_radius=data["collisionRadius"],
            tether_radius=data["tetherRadius"],
            on_target_cd_static=data["onTargetCdStatic"],
            inner_radius=data["innerRadius"],
            speed=data["speed"],
            width=data["width"],
            angle=data["angle"],
            cast_time=data["castTime"],
            effect_radius=data["effectRadius"],
            target_range=data["targetRange"],
        )
        return ability #return the ability object to the main function




def gen_origin(new_champ):

    with open(r"../champions.json",encoding="utf8") as f:

        data = json.load(f) #load the json file into a dict
        stuff = jsonToObject() #initialize the jsonToObject clash
        if new_champ in list(data.keys()):
            champ_origin = stuff.render_champ_data(data[new_champ]) #send the champion data to the render_champ_data class
            return champ_origin
        else:
            return "Invalid champion name"