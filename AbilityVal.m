function [effect,m] = AbilityVal(champdat,champ,key,champ2)
%This function calculates the effects of an ability
%
%   [effect,m,champ,champ2] = AbilityVal(champdat,champ,key,champ2)
%
%effect is a structure output containing the values and attributes.
%champdat is the champion data structure. champ is the input champion
%structure. key is a string ('P','Q','W',E','R') representing which ability 
%is used. m is a logical value (1 or 0) indicating if a modifier is missing
%for the given ability. true if missing. champ2 is a follow through output
%of the input champ2, the subject champion. This is done so that champions
%whose abilities modify the stats of their oponents can have impact. champ
%similarly follows through so that self-buffing abilities can have impact.
%% Switch Case Test
if strcmp(champ.ch,'Sylas') && strcmp(key,'R')
    Champ = champ;
    champ = champ2;
    champ.stats = Champ.stats;
    champ.stats.attackDamage = 0.6*Champ.stats.abilityPower;
    champ.sta_base.attackDamage = 0.2*Champ.stats.abilityPower;
    champ.abi.R = Champ.abi.R;
end
m = 0;
l = champ.abi.(key);
if l <= 0
    disp("Make sure to level your abilities before using this function!")
    effect = {''};
    return
end
effect.value = []; %Predefinition of output structure
for p = 1:length(champdat.(champ.ch).abilities.(key))
    for k = 1:length(champdat.(champ.ch).abilities.(key)(p).effects)
        if ~isempty(champdat.(champ.ch).abilities.(key)(p).effects(k).leveling)
            for j = 1:length(champdat.(champ.ch).abilities.(key)(p).effects(k).leveling)
                effect(j,k,p).value = 0;
                effect(j,k,p).att = champdat.(champ.ch).abilities.(key)(p).effects(k).leveling(j).attribute;
                effect(j,k,p).type = '';
                eff = effect(j,k,p);
                abi = champdat.(champ.ch).abilities.(key)(p).effects(k).leveling(j).modifiers;
                for i = 1:length(abi)
                    unit = abi(i).units{l};
                    switch unit
                        case '' %Base damage
                            eff.value = eff.value + abi(i).values(l);
                        case '%' %Unique champion stat or effect modifier
                            eff.value = eff.value + abi(i).values(l);
                        case ' soldiers' %Azir R width
                            eff.value = eff.value + abi(i).values(l);
                        case ' AD' %Tryndamere flat damage reduction
                            eff.value = eff.value + abi(i).values(l);
                        case ' bonus health' %Chogath flat stats from R
                            eff.value = eff.value + abi(i).values(l);
                        case '% transmission per 100 AD' %Illaoi E soul transmission
                            eff.value = eff.value +abi(i).values(l)/100*champ.stats.attackDamage;
                        case '% (based on level) MS'
                            if champ.l < 10
                                eff.value = eff.value + abi(i).values(1);
                            elseif champ.l >= 10
                                eff.value = eff.value + abi(i).values(2);
                            end
                        case '% per 100 AP' %Unique champion stat or effect modifier scaling with AP
                            eff.value = eff.value + abi(i).values(l)*champ.stats.abilityPower/100;
                        case '% AD' %AD ratio
                            eff.value = eff.value + abi(i).values(l)*champ.stats.attackDamage/100;
                        case '% AP' %AP ratio
                            eff.value = eff.value + abi(i).values(l)*champ.stats.abilityPower/100;
                        case '% bonus AD' %Bonus AD ratio
                            eff.value = eff.value + abi(i).values(l)*(champ.stats.attackDamage...
                                - champ.sta_base.attackDamage)/100;
                        case '% attack speed' %Total AS ratio - modifier of AD ratio
                            eff.value = eff.value + abi(i).values(l)*champ.stats.attackSpeed*...
                                (champ.stats.attackDamage - champ.sta_base.attackDamage)/100;
                        case '% bonus armor' %Bonus Armor ratio
                            eff.value = eff.value + abi(i).values(l)*(champ.stats.armor...
                                - champ.sta_base.armor)/100;
                        case '% total armor' %Armor ratio
                            eff.value = eff.value + abi(i).values(l)*champ.stats.armor/100;
                        case '% total magic resistance'
                            eff.value = eff.value + abi(i).values(l)*champ.stats.magicResistance/100;
                        case '% bonus magic resistance' %Bonus MR ratio
                            eff.value = eff.value + abi(i).values(l)*(champ.stats.magicResistance...
                                - champ.sta_base.magicResistance)/100;
                        case '% of turret''s maximum health' %Ziggs demolition
                            eff.value = eff.value + abi(i).values(l);
                        case '% of damage dealt' %Zedd - Percent of damage dealt
                            eff.value = eff.value + abi(i).values(l);
                        case '% of maximum health' %Percent self max health
                            eff.value = eff.value + abi(i).values(l)*champ.stats.health/100;
                        case '% (+ 2% per 100 AP) of target''s maximum health' %Zac W/Shen Q scaling
                            eff.value = eff.value + (abi(i).values(l)+0.02*champ.stats.abilityPower)*...
                                champ2.stats.health/100;
                        case '% of target''s current health' %Percent target current HP
                            eff.value = eff.value + abi(i).values(l)*champ2.stats.healthCurrent/100;
                        case '% of target''s maximum health' %Percent target max HP
                            eff.value = eff.value + abi(i).values(l)*champ2.stats.health/100;
                        case '% of target''s armor' %Percent target armor
                            eff.value = eff.value + abi(i).values(l)*champ2.stats.armor/100;
                        case '% of bonus health' %Percent of self bonus health
                            eff.value = eff.value + abi(i).values(l)*(champ.stats.health ...
                                - champ.sta_base.health)/100;
                        case '% of target bonus health' %Percent of target's bonus health
                            eff.value = eff.value + abi(i).values(l)*(champ2.stats.health ...
                                - champ2.sta_base.health)/100;
                        case '% of missing health' %Percent of own missing health
                            eff.value = eff.value + abi(i).values(l)*(champ.stats.health ...
                                - champ.stats.healthCurrent);
                        case '% of target''s missing health' %Percent of target's missing health
                            eff.value = eff.value + abi(i).values(l)*(champ2.stats.health ...
                                - champ2.stats.healthCurrent)/100;
                        case '[ 1% per 35 ][ 2.86% per 100 ]bonus AD' %Vi W scaling with target max health and bonus AD
                            eff.value = eff.value + 2.86/100*(champ.stats.attackDamage - ...
                                champ.sta_base.attackDamage)*champ2.stats.health/100;
                        case '% max health per 100 AP' %Varus W/Trundle R/Nasus R/Malz R/KogMaw W scaling with AP and target max health
                            eff.value = eff.value + abi(i).values(l)/100*champ.stats.abilityPower*...
                                champ2.stats.health/100;
                        case '% current health per 100 AP' %Fiddlesticks scaling with AP and target current health
                            eff.value = eff.value + abi(i).values(l)/100*champ.stats.abilityPower*...
                                champ2.stats.healthCurrent/100;
                        case '% missing health per 100 AP' %Kayle E scaling with AP and target missing health
                            eff.value = eff.value + abi(i).values(l)/100*champ.stats.abilityPower*...
                                (champ2.stats.health - champ2.stats.healthCurrent)/100;
                        case '% max health per 100 bonus AD' %Kled R scaling
                            eff.value = eff.value + abi(i).values(l)/100*(champ.stats.attackDamage...
                                - champ.sta_base.attackDamage)*champ2.stats.health/100;
                        case ' per Soul collected' %Thresh soul scaling on W and E
                            eff.value = eff.value + abi(i).values(l)*champ.Stack.val;
                        case ' per Mist collected' %Senna scaling
                            eff.value = eff.value + abi(i).values(l)*champ.Stack.val;
                        case '% (+ 0.25% per 100 AP) of target''s maximum health' %Amumu W scaling
                            eff.value = eff.value + (abi(i).values(l)+0.25*champ.stats.abilityPower/100)*...
                                champ2.stats.health/100;
                        case '% (+ 1% per 100 AP) of target''s maximum health' %Maokai E scaling
                            eff.value = eff.value + (abi(i).values(l)+1*champ.stats.abilityPower/100)*...
                                champ2.stats.health/100;
                        case '% (+ 1.5% per 100 AP) of target''s maximum health' %Shen Q/Evelynn E1 scaling
                            eff.value = eff.value + (abi(i).values(l)+1.5*champ.stats.abilityPower/100)*...
                                champ2.stats.health/100;
                        case '% (+ 2.5% per 100 AP) of target''s maximum health' %Evelynn E2 scaling
                            eff.value = eff.value + (abi(i).values(l)+2.5*champ.stats.abilityPower/100)*...
                                champ2.stats.health/100;
                        case '% (+ 4.5% per 100 AP) of target''s maximum health' %Shen Q scaling
                            eff.value = eff.value + (abi(i).values(l)+4.5*champ.stats.abilityPower/100)*...
                                champ2.stats.health/100;
                        case '% (+ 6% per 100 AP) of target''s maximum health' %Shen Q scaling
                            eff.value = eff.value + (abi(i).values(l)+4.5*champ.stats.abilityPower/100)*...
                                champ2.stats.health/100;
                        case '% (+ 3% per 100 AP) of target''s missing health' %Elise Q2 scaling
                            eff.value = eff.value + (abi(i).values(l)+3*champ.stats.abilityPower/100)*...
                                (champ2.stats.health - champ2.stats.healthCurrent)/100;
                        case '% (+ 3% per 100 AP) of target''s current health' %Elise Q1 scaling
                            eff.value = eff.value + (abi(i).values(l)+3*champ.stats.abilityPower/100)*...
                                champ2.stats.healthCurrent/100;
                        case '% (+ 10% per 100 bonus AD) of expended Grit' %Sett W Shield scaling
                            eff.value = eff.value + (abi(i).values(l) + 10*(champ.stats.attackDamage - ...
                                champ.sta_base.attackDamage)/100)*0.5*champ.stats.health/100;
                        case '% per 1% of health lost in the past 4 seconds' %Ekko R heal scaling
                            eff.value = eff.value + abi(i).values(l);
                        case '2% (+ 2 / 3 / 4 / 5 / 6% per 100 AD) of target''s maximum health' %Sett Q scaling
                            eff.value = eff.value + (2 + (l+1)*champ.stats.attackDamage/100)*...
                                champ2.stats.health;
                        case '1% (+ 1 / 1.5 / 2 / 2.5 / 3% per 100 AD) of target''s maximum health' %Sett Q scaling
                            eff.value = eff.value + (1 + (l+1)/2*champ.stats.attackDamage/100)*...
                                champ2.stats.health;
                        case '% bonus mana' %Ryze mana scaling
                            eff.value = eff.value + abi(i).values(l)*(champ.stats.mana - ...
                                champ.sta_base.mana)/100;
                        case '% maximum mana' %Kassadin mana scaling
                            eff.value = eff.value + abi(i).values(l)*champ.stats.mana/100;
                        case '% of missing mana' %Kassadin mana restoration
                            eff.value = eff.value + abi(i).values(l)*(champ.stats.mana - ...
                                champ.stats.manaCurrent)/100*champ.stats.mana;
                        case 'Siphoning Strike stacks' %Nasus Q scaling
                            eff.value = eff.value + abi(i).values(l)*champ.Stack.val;
                        case '% (+ 5% per 100 bonus AD) of target''s maximum health' %Kled W scaling
                            eff.value = eff.value + (abi(i).values(l)+5*(champ.stats.attackDamage - ...
                                champ.sta_base.attackDamage)/100)*champ2.stats.health/100;
                        case '% (+ 0.5% per Mark) of target''s missing health' %Kindred E mark scaling
                            eff.value = eff.value + (abi(i).values(l)+0.5*champ.Stack.val)*...
                                (champ2.stats.health-champ2.stats.healthCurrent)/100;
                        case '% (+ 1% per Mark) of target''s current health' %Kindred W mark scaling
                            eff.value = eff.value + (abi(i).values(l)+1*champ.Stack.val)*...
                                champ2.stats.healthCurrent/100;
                        case '% (+ 1.5% per Mark) of target''s current health' %Kindred W mark scaling
                            eff.value = eff.value + (abi(i).values(l)+1.5*champ.Stack.val)*...
                                champ2.stats.healthCurrent/100;
                        case '% (+ 1.5% per Feast stack) of target''s maximum health' %Chogath feast scaling
                            eff.value = eff.value + (abi(i).values(l) + 1.5*champ.Stack.val)/100*champ2.stats.health;
                        case '% (+ 0.5% per Feast stack) of target''s maximum health' %Chogath feast scaling
                            eff.value = eff.value + (abi(i).values(l) + 0.5*champ.Stack.val)/100*champ2.stats.health;
                        case '% per 100 bonus magic resistance' %Galio magic damage reduction scaling W
                            eff.value = eff.value + abi(i).values(l)/100*(champ.stats.magicResistance...
                                - champ.sta_base.magicResistance);
                        otherwise
                            %disp("Missing modifier!")
                            m = 1;
                    end
                    effect(j,k,p) = eff;
                    effect(j,k,p).type = champdat.(champ.ch).abilities.(key)(p).damageType;
                end
            end
        end
    end
end
if ~isfield(effect,'type')
    %disp(champ.ch+"'s "+key+" is a utility ability.")
    return
end
mix = 0;
for j = 1:size(effect,1)
    for k = 1:size(effect,2)
        for p = 1:size(effect,3)
            effect(j,k,p).dealt = 0;
            eff = effect(j,k,p);
            if isempty(eff.type)
                eff.dealt = [];
            else
                switch eff.type
                    case 'MAGIC_DAMAGE'
                        MR = champ2.stats.magicResistance;
                        MR = MR*(100-champ.stats.magicPenPer)/100;
                        MR = MR - champ.stats.magicPenetration;
                        if MR < 0
                            MR = 0;
                        end
                        if MR >= 0
                            dm = 100/(100+MR);
                            eff.dealt = eff.value*dm;
                        else
                            dm = 2-100/(100-MR);
                            eff.dealt = eff.value*dm;
                        end
                    case 'PHYSICAL_DAMAGE'
                        AR = champ2.stats.armor;
                        AR = AR*(100-champ.stats.armorPenetration)/100;
                        AR = AR - champ.stats.lethality*(0.6+0.4*champ.l/18);
                        if AR >= 0
                            dm = 100/(100+AR);
                            eff.dealt = eff.value*dm;
                        else
                            dm = 2-100/(100-AR);
                            eff.dealt = eff.value*dm;
                        end
                    case 'MIXED_DAMAGE'
                        mix = 1;
                    case 'TRUE_DAMAGE'
                        eff.dealt = eff.value;
                end
            end
            effect(j,k,p) = eff;
        end
    end
end
if mix == 1
    [effect,mix] = ValMix(effect,champ,key,champ2);
end
if mix == 1
    disp(champ.ch+"'s "+key+" has mixed damage and needs to be reviewed!")
end
end