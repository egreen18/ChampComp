%This function is a means to investigate the champdat structure and to fix
%any discovered errors.
%% Initialization
load champ_original.mat champdat
cha = fieldnames(champdat);
abi = {'Q','W','E','R'};
%% Investigating modifier types and attributes
att = {''};
mod = {''};
relCha = {''};
a = 0;
m = 0;
for i = 1:length(cha)
    for j = 1:length(abi)
        for p = 1:length(champdat.(cha{i}).abilities.(abi{j}))
            for l = 1:length(champdat.(cha{i}).abilities.(abi{j})(p).effects)
                ability = champdat.(cha{i}).abilities.(abi{j})(p).effects(l).leveling;
                if ~isempty(ability)
                    for n = 1:length(ability)
                        if ~any(strcmp(att,ability(n).attribute))
                            a = a + 1;
                            att{a} = ability(n).attribute;
                            disp(ability(n).attribute+" appears first in one of "+champdat...
                                .(cha{i}).name+"'s abilities.")
                        end
                        for k =1:length(ability(n).modifiers)
                            if ~any(strcmp(mod,ability(n).modifiers(k).units{1}))
                                m = m + 1;
                                mod{m} = ability(n).modifiers(k).units{1};
                                disp("The modifier: "+mod{m}+" first appears in one of "+...
                                    champdat.(cha{i}).name+"'s abilities.")
                                relCha{m} = champdat.(cha{i}).name;
                            end
                        end
                    end
                end
            end
        end
    end
end
%% Manually fixing unit issues
%Katarina modifier ambiguity
for i = 1:5
    champdat.Katarina.abilities.W.effects.leveling.modifiers.units{i} = '% MS';
end
%Updating aatrox units
champdat.Aatrox.abilities.E.effects(1).leveling.modifiers.units = ...
    {'% PMD';'% PMD';'% PMD';'% PMD';'% PMD'};
%% Saving changes to champdat
save champdat.mat champdat
        
    