from common.modelcommon import (Stats, Abilities, Stack, Effect, StatChange)
from items.modelitem import (Item, itemdata)
import json
import os

#Stepping into directory to avoid path issues across OS differences
os.chdir(os.path.join('version','latest'))
with open(r"champions.json",encoding="utf8") as f:
    champdata = json.load(f) #load the json file into a dict
os.chdir('..')
os.chdir('..')

#This object will be used when generating a new champion
class Champ(object):
    #Initializing champion attributes
    def __init__(self,name):
        #Name is a valid string, can find list of these by calling champdata.__dict__.keys()
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
    
    #Method for leveling up or down a champion, changing their base stats accordingly
    def level_change(self,level):
        #level is a numeric value between 1 and 18
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
    
    #A method used in testing and development for quickly levelling a champ & abilities
    def quick_level(self):
        self.level_change(6)
        for i in ['Q','W','E','R']:
            abi = getattr(self.abilities,i)
            abi[0].level = 1
    
    #Method for updating the passives associated with items after adding an item to champ inventory
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
    
    #Method for adding an item to champoion inventory    
    def item(self,item,slot):
        #item is a string containing a 4 digit item key
        #slot is an index between 0 and 5 indicating the inventory slot for the new item
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
        
#magi an phys are evaluative functions for use in val and valMix
def magi(value,champ1,champ2):
        #Value is a damage float input from the effect object
        #champ1 and chmap2 are champion objects
        MR = champ2.stats.magicResistance
        MR = MR*(100-champ1.stats.magicPenPer)/100
        MR = MR - champ1.stats.magicPenetration
        if MR < 0:
            MR = 0
        if MR >= 0:
            dm = 100/(100+MR)
            dealt = value*dm
        else:
            dm = 2-100/(100-MR)
            dealt = value*dm
        return dealt

def phys(value,champ1,champ2):
    #Value is a damage float input from the effect structure
    #champ1 and chmap2 are champion structures
    AR = champ2.stats.armor
    AR = AR*(100-champ1.stats.armorPenetration)/100
    AR = AR - champ1.stats.lethality*(0.6+0.4*champ1.level/18)
    if AR >= 0:
        dm = 100/(100+AR)
        dealt = value*dm
    else:
        dm = 2-100/(100-AR)
        dealt = value*dm
    return dealt

#Evaluative function for handling mixed damage calculations, called in val()    
def valMix(effect,champ1,champ2,abi):
    #Effect is an object generated by val
    #champ1 and champ2 are champions objects
    #Abi is a string ['Q','W','E','R'] indicating ability of choice
    chkey = champ1.name + abi
    if chkey == 'AhriQ':
        effect.dealt[0] = magi(effect.value[0],champ1,champ2);
        effect.dealt[1] = effect.dealt[0] + effect.value[0];
        
    #Currently in the process of translating from MATLAB into pythonic    
        
    # elif chkey == 'AkaliR':
    #     eff(2,3).dealt = magi(eff(2,3).value,champ,champ2);
    #     eff(1,3).dealt = magi(eff(1,3).value,champ,champ2);
    #     eff(1,1).dealt = phys(eff(1,1).value,champ,champ2);
    # elif chkey == 'CamilleQ':
    #     eff(1,1).dealt = phys(eff(1,1).value,champ,champ2);
    #     if champ.l <= 16:
    #         mod = 0.36 + 0.04*champ.l;
    #     elif champ.l > 16:
    #         mod = 1;
    #     eff(1,3).dealt = phys((1-mod)*eff(1,3).value,champ,champ2);
    #     eff(1,3).dealt = eff(1,3).dealt + mod*eff(1,3).value;
    # elif chkey == 'CorkiE':
    #     eff(1).dealt = phys(0.5*eff(1).value,champ,champ2);
    #     eff(1).dealt = eff(1).dealt + magi(0.5*eff(1).value,champ,champ2);
    #     eff(2).dealt = phys(0.5*eff(2).value,champ,champ2);
    #     eff(2).dealt = eff(2).dealt + magi(0.5*eff(2).value,champ,champ2);
    # elif chkey == 'FizzQ':
    #     eff.dealt = magi(eff.value,champ,champ2);
    #     eff.dealt = eff.dealt + phys(champ.stats.attackDamage,champ,champ2);
    # elif chkey == 'IllaoiE':
    #     pass
    # elif chkey == 'KatarinaR':
    #     eff(1).dealt = phys(eff(1).value,champ,champ2);
    #     eff(2).dealt = phys(eff(2).value,champ,champ2);
    #     eff(3).dealt = magi(eff(3).value,champ,champ2);
    #     eff(4).dealt = magi(eff(4).value,champ,champ2);
    # elif chkey == 'LilliaQ':
    #     eff(1,2).dealt = magi(eff(1,2).value,champ,champ2);
    #     eff(2,2).dealt = eff(1,2).dealt + eff(1,2).value;
    # elif chkey == 'NunuQ':
    #     eff(1,1).dealt = magi(eff(1,1).value,champ,champ2);
    #     eff(1,2).dealt = eff(1,2).value;
    # elif chkey == 'RekSaiE':
    #     eff(1).dealt = phys(eff(1).value,champ,champ2);
    #     eff(2).dealt = eff(2).value;
    # elif chkey == 'SettW':
    #     eff(2).dealt = eff(2).value;
    #     eff(3).dealt = phys(eff(3).value,champ,champ2);
    # elif chkey == 'SkarnerQ':
    #     eff(1,1).dealt = phys(eff(1,1).value,champ,champ2);
    #     eff(1,2).dealt = magi(eff(1,2).value,champ,champ2);
    #     eff(2,2).dealt = eff(1,2).dealt + eff(1,1).dealt;
    # elif chkey == 'SkarnerE':
    #     eff(1,2).dealt = magi(eff(1,2).value,champ,champ2);
    #     eff(1,3).dealt = phys(eff(1,3).value,champ,champ2);
    # elif chkey == 'SkarnerR':
    #     eff(1).dealt = magi(eff(1).value,champ,champ2);
    #     eff(2).dealt = 2*eff(1).dealt + phys(1.2*champ.stats.attackDamage,champ,champ2);
    # elif chkey == 'UrgotR':
    #     eff.dealt = phys(eff.value,champ,champ2);
    # elif chkey == 'VelkozR':
    #     eff(1,3).dealt = magi(eff(1,3).value,champ,champ2);
    #     eff(2,3).dealt = magi(eff(2,3).value,champ,champ2);
    # elif chkey == 'YoneW':
    #     eff(2).dealt = phys(eff(2).value,champ,champ2);
    #     eff(3).dealt = magi(eff(3).value,champ,champ2);
    #     eff(1).dealt = eff(2).dealt + eff(3).dealt;
    # elif chkey == 'YoneR':
    #     eff(3,2).dealt = magi(eff(3,2).value,champ,champ2);
    #     eff(2,2).dealt = phys(eff(2,2).value,champ,champ2);
    #     eff(1,2).dealt = eff(3,2).dealt + eff(2,2).dealt;
    # elif chkey == 'PantheonR':
    #     eff(1,4).dealt = magi(eff(1,4).value,champ,champ2);
    #     eff(2,4).dealt = magi(eff(2,4).value,champ,champ2);
    else:
        print(champ1.name+"'s "+abi+" has mixed damage and needs to be reviewed!")
    return effect
    
#Function which evaluates the ability of champ1 performed on champ2    
def val(champ1,champ2,abi):
    #Takes input primary champion object champ1, target champion object champ2, 
    #and identiying ability string abi
       
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
    effect = ['']*imax
    for i in range(imax):
        effect[i] = Effect(jmax,kmax)
    
    #Parsing units and calculating damage values - needs to be redone in Regex
    lvl = e[0].level-1
    for idx,i in enumerate(e):
        effect[idx].name = i.name
        for jdx,j in enumerate(i.effects):
            for kdx,k in enumerate(j.leveling):
                effect[idx].att[(jdx+1)*(kdx+1)-1] = k.attribute
                eff = getattr(effect[idx],'value')[(jdx+1)*(kdx+1)-1]
                for l in k.modifiers:
                    if l.units[0] == '': #Base damage
                        eff= eff + float(l.values[lvl])
                    elif l.units[lvl] == '%':  #Unique champion stat or effect modifier
                        eff = eff + float(l.values[lvl])
                    elif l.units[lvl] == ' soldiers':  #Azir R width
                        eff = eff + float(l.values[lvl])
                    elif l.units[lvl] == ':Rscale':  #Karma abilities scaling with R
                        eff = eff + float(l.values[champ1.abilities.R[0].level-1])
                    elif l.units[lvl] == '%:Rscale':  #Percent based R scaling
                        eff = eff + float(l.values[champ1.abilities.R[0].level-1])
                    elif l.units[lvl] == '% AD:Rscale':  #R scaling, percent AD
                        eff = eff + float(l.values[champ1.abilities.R[0].level-1])*champ1.stats.attackDamage/100
                    elif l.units[lvl] == '% AP:Rscale':  #R scaling, percent AP
                        eff = eff + float(l.values[champ1.abilities.R[0].level-1])*champ1.stats.abilityPower/100
                    elif l.units[lvl] == ' AD':  #Tryndamere flat damage reduction
                        eff = eff + float(l.values[lvl])
                    elif l.units[lvl] == ' bonus health':  #Chogath flat stats from R
                        eff = eff + float(l.values[lvl])
                    elif l.units[lvl] == '% transmission per 100 AD':  #Illaoi E soul transmission
                        eff = eff +float(l.values[lvl])/100*champ1.stats.attackDamage
                    elif l.units[lvl] == '% (based on level) MS':
                        if champ1.l < 10:
                            eff = eff + float(l.values[1])
                        elif champ1.l >= 10:
                            eff = eff + float(l.values[2])
                    elif l.units[lvl] == '% per 100 AP':  #Unique champion stat or effect modifier scaling with AP
                        eff = eff + float(l.values[lvl])*champ1.stats.abilityPower/100
                    elif l.units[lvl] == '% AD':  #AD ratio
                        eff = eff + float(l.values[lvl])*champ1.stats.attackDamage/100
                    elif l.units[lvl] == '% AP':  #AP ratio
                        eff = eff + float(l.values[lvl])*champ1.stats.abilityPower/100
                    elif l.units[lvl] == '% bonus AD':  #Bonus AD ratio
                        eff = eff + float(l.values[lvl])*(champ1.stats.attackDamage
                            - champ1.stats_base.attackDamage)/100
                    elif l.units[lvl] == '% attack speed':  #Total AS ratio - modifier of AD ratio
                        eff = eff + float(l.values[lvl])*champ1.stats.attackSpeed*(champ1.stats.attackDamage - champ1.stats_base.attackDamage)/100
                    elif l.units[lvl] == '% bonus armor':  #Bonus Armor ratio
                        eff = eff + float(l.values[lvl])*(champ1.stats.armor
                            - champ1.stats_base.armor)/100
                    elif l.units[lvl] == '% total armor':  #Armor ratio
                        eff = eff + float(l.values[lvl])*champ1.stats.armor/100
                    elif l.units[lvl] == '% total magic resistance':
                        eff = eff + float(l.values[lvl])*champ1.stats.magicResistance/100
                    elif l.units[lvl] == '% bonus magic resistance':  #Bonus MR ratio
                        eff = eff + float(l.values[lvl])*(champ1.stats.magicResistance
                            - champ1.stats_base.magicResistance)/100
                    elif l.units[lvl] == '% of turret''s maximum health':  #Ziggs demolition
                        eff = eff + float(l.values[lvl])
                    elif l.units[lvl] == '% of damage dealt':  #Zedd - Percent of damage dealt
                        eff = eff + float(l.values[lvl])
                    elif l.units[lvl] == '% of maximum health':  #Percent self max health
                        eff = eff + float(l.values[lvl])*champ1.stats.health/100
                    elif l.units[lvl] == '% (+ 2% per 100 AP) of target''s maximum health':  #Zac W/Shen Q scaling
                        eff = eff + (float(l.values[lvl])+0.02*champ1.stats.abilityPower)*champ2.stats.health/100
                    elif l.units[lvl] == '% of target''s current health':  #Percent target current HP
                        eff = eff + float(l.values[lvl])*champ2.healthCurrent/100
                    elif l.units[lvl] == '% of target''s maximum health':  #Percent target max HP
                        eff = eff + float(l.values[lvl])*champ2.stats.health/100
                    elif l.units[lvl] == '% of target''s armor':  #Percent target armor
                        eff = eff + float(l.values[lvl])*champ2.stats.armor/100
                    elif l.units[lvl] == '% of bonus health':  #Percent of self bonus health
                        eff = eff + float(l.values[lvl])*(champ1.stats.health 
                            - champ1.stats_base.health)/100
                    elif l.units[lvl] == '% of target bonus health':  #Percent of target's bonus health
                        eff = eff + float(l.values[lvl])*(champ2.stats.health 
                            - champ2.stats_base.health)/100
                    elif l.units[lvl] == '% of missing health':  #Percent of own missing health
                        eff = eff + float(l.values[lvl])*(champ1.stats.health 
                            - champ1.healthCurrent)
                    elif l.units[lvl] == '% of target''s missing health':  #Percent of target's missing health
                        eff = eff + float(l.values[lvl])*(champ2.stats.health 
                            - champ2.healthCurrent)/100
                    elif l.units[lvl] == '[ 1% per 35 ][ 2.86% per 100 ]bonus AD':  #Vi W scaling with target max health and bonus AD
                        eff = eff + 2.86/100*(champ1.stats.attackDamage - 
                            champ1.stats_base.attackDamage)*champ2.stats.health/100
                    elif l.units[lvl] == '% max health per 100 AP':  #Varus W/Trundle R/Nasus R/Malz R/KogMaw W scaling with AP and target max health
                        eff = eff + float(l.values[lvl])/100*champ1.stats.abilityPower*champ2.stats.health/100
                    elif l.units[lvl] == '% current health per 100 AP':  #Fiddlesticks scaling with AP and target current health
                        eff = eff + float(l.values[lvl])/100*champ1.stats.abilityPower*champ2.healthCurrent/100
                    elif l.units[lvl] == '% missing health per 100 AP':  #Kayle E scaling with AP and target missing health
                        eff = eff + float(l.values[lvl])/100*champ1.stats.abilityPower*(champ2.stats.health - champ2.healthCurrent)/100
                    elif l.units[lvl] == '% max health per 100 bonus AD':  #Kled R scaling
                        eff = eff + float(l.values[lvl])/100*(champ1.stats.attackDamage
                            - champ1.stats_base.attackDamage)*champ2.stats.health/100
                    elif l.units[lvl] == ' per Soul collected':  #Thresh soul scaling on W and E
                        eff = eff + float(l.values[lvl])*champ1.Stack.val
                    elif l.units[lvl] == ' per Mist collected':  #Senna scaling
                        eff = eff + float(l.values[lvl])*champ1.Stack.val
                    elif l.units[lvl] == '% (+ 0.25% per 100 AP) of target''s maximum health':  #Amumu W scaling
                        eff = eff + (float(l.values[lvl])+0.25*champ1.stats.abilityPower/100)*champ2.stats.health/100
                    elif l.units[lvl] == '% (+ 1% per 100 AP) of target''s maximum health':  #Maokai E scaling
                        eff = eff + (float(l.values[lvl])+1*champ1.stats.abilityPower/100)*champ2.stats.health/100
                    elif l.units[lvl] == '% (+ 1.5% per 100 AP) of target''s maximum health':  #Shen Q/Evelynn E1 scaling
                        eff = eff + (float(l.values[lvl])+1.5*champ1.stats.abilityPower/100)*champ2.stats.health/100
                    elif l.units[lvl] == '% (+ 2.5% per 100 AP) of target''s maximum health':  #Evelynn E2 scaling
                        eff = eff + (float(l.values[lvl])+2.5*champ1.stats.abilityPower/100)*champ2.stats.health/100
                    elif l.units[lvl] == '% (+ 4.5% per 100 AP) of target''s maximum health':  #Shen Q scaling
                        eff = eff + (float(l.values[lvl])+4.5*champ1.stats.abilityPower/100)*champ2.stats.health/100
                    elif l.units[lvl] == '% (+ 6% per 100 AP) of target''s maximum health':  #Shen Q scaling
                        eff = eff + (float(l.values[lvl])+4.5*champ1.stats.abilityPower/100)*champ2.stats.health/100
                    elif l.units[lvl] == '% (+ 3% per 100 AP) of target''s missing health':  #Elise Q2 scaling
                        eff = eff + (float(l.values[lvl])+3*champ1.stats.abilityPower/100)*(champ2.stats.health - champ2.healthCurrent)/100
                    elif l.units[lvl] == '% (+ 3% per 100 AP) of target''s current health':  #Elise Q1 scaling
                        eff = eff + (float(l.values[lvl])+3*champ1.stats.abilityPower/100)*champ2.healthCurrent/100
                    elif l.units[lvl] == '% (+ 10% per 100 bonus AD) of expended Grit':  #Sett W Shield scaling
                        eff = eff + (float(l.values[lvl]) + 10*(champ1.stats.attackDamage - 
                            champ1.stats_base.attackDamage)/100)*0.5*champ1.stats.health/100
                    elif l.units[lvl] == '% per 1% of health lost in the past 4 seconds':  #Ekko R heal scaling
                        eff = eff + float(l.values[lvl])
                    elif l.units[lvl] == '2% (+ 2 / 3 / 4 / 5 / 6% per 100 AD) of target''s maximum health':  #Sett Q scaling
                        eff = eff + (2 + (l+1)*champ1.stats.attackDamage/100)*champ2.stats.health
                    elif l.units[lvl] == '1% (+ 1 / 1.5 / 2 / 2.5 / 3% per 100 AD) of target''s maximum health':  #Sett Q scaling
                        eff = eff + (1 + (l+1)/2*champ1.stats.attackDamage/100)* champ2.stats.health
                    elif l.units[lvl] == '% bonus mana':  #Ryze mana scaling
                        eff = eff + float(l.values[lvl])*(champ1.stats.mana - 
                            champ1.stats_base.mana)/100
                    elif l.units[lvl] == '% maximum mana':  #Kassadin mana scaling
                        eff = eff + float(l.values[lvl])*champ1.stats.mana/100
                    elif l.units[lvl] == '% of missing mana':  #Kassadin mana restoration
                        eff = eff + float(l.values[lvl])*(champ1.stats.mana - 
                            champ1.manaCurrent)/100*champ1.stats.mana
                    elif l.units[lvl] == 'Siphoning Strike stacks':  #Nasus Q scaling
                        eff = eff + float(l.values[lvl])*champ1.Stack.val
                    elif l.units[lvl] == '% (+ 5% per 100 bonus AD) of target''s maximum health':  #Kled W scaling
                        eff = eff + (float(l.values[lvl])+5*(champ1.stats.attackDamage - 
                            champ1.stats_base.attackDamage)/100)*champ2.stats.health/100
                    elif l.units[lvl] == '% (+ 0.5% per Mark) of target''s missing health':  #Kindred E mark scaling
                        eff = eff + (float(l.values[lvl])+0.5*champ1.Stack.val)*(champ2.stats.health-champ2.healthCurrent)/100
                    elif l.units[lvl] == '% (+ 1% per Mark) of target''s current health':  #Kindred W mark scaling
                        eff = eff + (float(l.values[lvl])+1*champ1.Stack.val)*champ2.healthCurrent/100
                    elif l.units[lvl] == '% (+ 1.5% per Mark) of target''s current health':  #Kindred W mark scaling
                        eff = eff + (float(l.values[lvl])+1.5*champ1.Stack.val)* champ2.healthCurrent/100
                    elif l.units[lvl] == '% (+ 1.5% per Feast stack) of target''s maximum health':  #Chogath feast scaling
                        eff = eff + (float(l.values[lvl]) + 1.5*champ1.Stack.val)/100*champ2.stats.health
                    elif l.units[lvl] == '% (+ 0.5% per Feast stack) of target''s maximum health':  #Chogath feast scaling
                        eff = eff + (float(l.values[lvl]) + 0.5*champ1.Stack.val)/100*champ2.stats.health
                    elif l.units[lvl] == '% per 100 bonus magic resistance':  #Galio magic damage reduction scaling W
                        eff = eff + float(l.values[lvl])/100*(champ1.stats.magicResistance
                            - champ1.stats_base.magicResistance)
                    else:
                       print("Missing modifier!")
                       pass
                effect[idx].value[(jdx+1)*(kdx+1)-1] = eff
                effect[idx].type = i.damageType
            
    #Removing extraneous elements of effect structure
    for idx, i in enumerate(effect):
            for jdx in range(len(i.att)):
                if not effect[idx].att[jdx]:
                    effect[idx].value[jdx] = 'None'         
    for idx,i in enumerate(effect):
        while 'None' in effect[idx].value:
            effect[idx].att.remove('')
            effect[idx].value.remove('None')
        effect[idx].dealt = ['']*len(effect[idx].value)
            
    #Calculating damage dealt post mitigation
    mix = 0
    for idx,i in enumerate(effect):
        if not i.type:
            effect[idx].dealt = ''
            break
        for jdx,j in enumerate(i.dealt):
            effect[idx].dealt[jdx] = 0
            if i.type == 'MAGIC_DAMAGE':
               effect[idx].dealt[jdx] = magi(effect[idx].value[jdx],champ1,champ2)
            elif i.type == 'PHYSICAL_DAMAGE':
                effect[idx].dealt[jdx] = phys(effect[idx].value[jdx],champ1,champ2)
            elif i.type == 'MIXED_DAMAGE':
                mix = 1
            elif i.type == 'TRUE_DAMAGE':
                effect[idx].dealt[jdx] = effect[idx].value[jdx]
            if mix == 1:
                effect[idx] = valMix(effect[idx],champ1,champ2,abi)
    return effect
    