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
    AttackType,
    AttributeRatings,
    Cooldown,
    Cost,
    Effect,
    Price,
    Resource,
    Modifier,
    Role,
    Leveling,
    Skin,
    Chroma,
    Description,
    Rarities,
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
            id=data["id"],
            key=data["key"],
            name=champion,
            title=data["title"],
            full_name=data["fullName"],
            icon=data["icon"],
            resource=data["resource"],
            attack_type=data["attackType"],
            adaptive_type=data["adaptiveType"],

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
                aram_damage_taken=Stat(flat=data["stats"]["aramDamageTaken"]["flat"]),
                aram_damage_dealt=Stat(flat=data["stats"]["aramDamageDealt"]["flat"]),
                aram_healing=Stat(flat=data["stats"]["aramHealing"]["flat"]),
                aram_shielding=Stat(flat=data["stats"]["aramShielding"]["flat"]),
                urf_damage_taken=Stat(flat=data["stats"]["urfDamageTaken"]["flat"]),
                urf_damage_dealt=Stat(flat=data["stats"]["urfDamageDealt"]["flat"]),
                urf_healing=Stat(flat=data["stats"]["urfHealing"]["flat"]),
                urf_shielding=Stat(flat=data["stats"]["urfShielding"]["flat"]),
            ),
            roles=data["roles"],
            attribute_ratings=AttributeRatings(
                damage=data["attributeRatings"]["damage"],
                toughness=data["attributeRatings"]["toughness"],
                control=data["attributeRatings"]["control"],
                mobility=data["attributeRatings"]["mobility"],
                utility=data["attributeRatings"]["utility"],
                ability_reliance=data["attributeRatings"]["abilityReliance"],
                attack=data["attributeRatings"]["attack"],
                defense=data["attributeRatings"]["defense"],
                magic=data["attributeRatings"]["magic"],
                difficulty=data["attributeRatings"]["difficulty"],
            ),
            abilities=abilities,
            release_date=data["releaseDate"],
            release_patch=data["releasePatch"],
            patch_last_changed=data["patchLastChanged"],
            price=data["price"],
            lore=data["lore"],
            skins= None



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




def main():

    champions = []#create an empty list that is used to hold the champions
    with open(r"../champions.json",encoding="utf8") as f:

        data = json.load(f) #load the json file into a dict
        stuff = jsonToObject() #initialize the jsonToObject clash

        for champion in data: #create a for loop for each champion in the json file
            #in this loop, champion == champion name
            champ = stuff.render_champ_data(data[champion]) #send the champion data to the render_champ_data class
            champions.append(champ) # add the champion object to the champions list




        # how to use the data



        for x in champions:
            #x is the champion object, if you have an ide that can show objects it will help explore it
            #but the gist is that you can explore the object by using the keys above
            # ie x.name would give you the name of every champion in the list

            if x.name == "Katarina":

                # if you want to access abilities, you have to either make a for loop and access every ability
                # like this
                for abil_key in x.abilities:
                    for abil_object in x.abilities[abil_key]:
                        print(abil_object)

                    #or you can access individual ability keys like this
                for abil in x.abilities["R"]:
                    #the keys are P Q W E R for abilities
                    #so it would be x.abilities["Q"] if you want a champion's Q

                    print(abil.name)
                    print(abil.cast_time)

                #to access stats, you just put x.stats.{insert_stat}
                print(x.stats.attack_speed)
                return x





if __name__ == '__main__':# if the file is called directly, run main()
    champ = main()
