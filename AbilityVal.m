function [effect,m,champ,champ2] = AbilityVal(champdat,champ,key,champ2)
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
                        case '% AD' %AD ratio
                            eff.value = eff.value + abi(i).values(l)*champ.stats.attackDamage/100;
                        case '% AP' %AP ratio
                            eff.value = eff.value + abi(i).values(l)*champ.stats.abilityPower/100;
                        case '% MS'  %Percent movespeed
                            eff.value = abi(i).values(l)*champ.stats.movespeed/100;
                        case '% bonus AD' %Bonus AD ratio
                            eff.value = eff.value + abi(i).values(l)*(champ.stats.attackDamage...
                                - champ.sta_base.attackDamage)/100;
                        case '% attack speed' %Total AS ratio - modifier of AD ratio
                            eff.value = eff.value + abi(i).values(l)*champ.stats.attackSpeed*...
                                (champ.stats.attackDamage - champ.sta_base.attackDamage)/100;
                        case '% bonus armor' %Bonus Armor ratio
                            eff.value = eff.value + abi(i).values(l)*(champ.stats.armor...
                                - champ.sta_base.armor)/100;
                        case '% bonus magic resistance' %Bonus MR ratio
                            eff.value = eff.value + abi(i).values(l)*(champ.stats.magicResistance...
                                - champ.sta_base.magicResistance)/100;
                        case '% PMD' %Aatrox's percent post mitigation damage
                            disp("This app does not play well with the Passive on Aatrox's E!")
                        case '% healing' %Percent bonus incoming healing
                            eff.value = eff.value + abi(i).values(l);
                            eff.value = [num2str(eff.value),' %'];
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
    disp("This is a utility ability.")
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
    disp(champ.ch+"'s "+key+" has mixed damage and needs to be reviewed!")
end
end