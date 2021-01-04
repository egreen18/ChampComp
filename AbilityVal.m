function effect = AbilityVal(champdat,champ,key)
%This function calculates the effects of an ability
%
%   effect = AbilityVal(champdat,champ,key)
%
%effect is a structure output containing the values and attributes.
%champdat is the champion data structure. champ is the input champion
%structure. key is a string ('P','Q','W',E','R') representing which ability 
%is used.
%% Katarina test
l = champ.abi.(key);
effect(length(champdat.(champ.ch).abilities.(key).effects(1).leveling))...
    .value = []; %Predefinition of output structure
if l < 1
    disp("This ability has not yet been learned.")
elseif l > 5
    disp("This ability has an invalid level.")
else
    for k = 1:length(champdat.(champ.ch).abilities.(key).effects)
        if ~isempty(champdat.(champ.ch).abilities.(key).effects(k).leveling)
            for j = 1:length(champdat.(champ.ch).abilities.(key).effects(k).leveling)
                effect(j,k).value = 0;
                effect(j,k).att = champdat.(champ.ch).abilities.(key).effects(k).leveling(j).attribute;
                abi = champdat.(champ.ch).abilities.(key).effects(k).leveling(j).modifiers;
                for i = 1:length(abi)
                    unit = abi(i).units{l};
                    switch unit
                        case '' %Base damage
                            effect(j,k).value = effect(j,k).value + abi(i).values(l);
                        case '% AD' %AD ratio
                            effect(j,k).value = effect(j,k).value + abi(i).values(l)*champ.stats.attackDamage/100;
                        case '% AP' %AP ratio
                            effect(j,k).value = effect(j,k).value + abi(i).values(l)*champ.stats.abilityPower/100;
                        case '% MS'  %Percent movespeed
                            effect(j,k).value = abi(i).values(l)*champ.stats.movespeed/100;
                        case '% bonus AD' %Bonus AD ratio
                            effect(j,k).value = effect(j,k).value + abi(i).values(l)*(champ.stats.attackDamage...
                                - champ.sta_base.attackDamage)/100;
                        case '% attack speed' %Total AS ratio - modifier of AD ratio
                            effect(j,k).value = effect(j,k).value + abi(i).values(l)*champ.stats.attackSpeed*...
                                (champ.stats.attackDamage - champ.sta_base.attackDamage)/100;
                    end
                end
            end
        end
    end
end