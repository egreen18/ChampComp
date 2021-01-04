function [effect,m] = AbilityVal(champdat,champ,key)
%This function calculates the effects of an ability
%
%   effect = AbilityVal(champdat,champ,key)
%
%effect is a structure output containing the values and attributes.
%champdat is the champion data structure. champ is the input champion
%structure. key is a string ('P','Q','W',E','R') representing which ability 
%is used.
%% Switch Case Test
m = 0;
l = champ.abi.(key);
effect.value = []; %Predefinition of output structure
for p = 1:length(champdat.(champ.ch).abilities.(key))
    for k = 1:length(champdat.(champ.ch).abilities.(key)(p).effects)
        if ~isempty(champdat.(champ.ch).abilities.(key)(p).effects(k).leveling)
            for j = 1:length(champdat.(champ.ch).abilities.(key)(p).effects(k).leveling)
                effect(j,k,p).value = 0;
                effect(j,k,p).att = champdat.(champ.ch).abilities.(key)(p).effects(k).leveling(j).attribute;
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
                        otherwise
                            %disp("Missing modifier!")
                            m = 1;
                    end
                    effect(j,k,p) = eff;
                end
            end
        end
    end
end
end