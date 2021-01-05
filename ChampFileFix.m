%This function is a means to investigate the champdat structure and to fix
%any discovered errors.
%% Initialization
load champ_original.mat champdat
cha = fieldnames(champdat);
abi = {'Q','W','E','R'};
%% Investigating modifier types and attributes
% att = {''};
% mod = {''};
% relCha = {''};
% a = 0;
% m = 0;
% for i = 1:length(cha)
%     for j = 1:length(abi)
%         for p = 1:length(champdat.(cha{i}).abilities.(abi{j}))
%             for l = 1:length(champdat.(cha{i}).abilities.(abi{j})(p).effects)
%                 ability = champdat.(cha{i}).abilities.(abi{j})(p).effects(l).leveling;
%                 if ~isempty(ability)
%                     for n = 1:length(ability)
%                         if ~any(strcmp(att,ability(n).attribute))
%                             a = a + 1;
%                             att{a} = ability(n).attribute;
%                             disp(ability(n).attribute+" appears first in one of "+champdat...
%                                 .(cha{i}).name+"'s abilities.")
%                         end
%                         for k =1:length(ability(n).modifiers)
%                             if ~any(strcmp(mod,ability(n).modifiers(k).units{1}))
%                                 m = m + 1;
%                                 mod{m} = ability(n).modifiers(k).units{1};
%                                 disp("The modifier: "+mod{m}+" first appears in one of "+...
%                                     champdat.(cha{i}).name+"'s abilities.")
%                                 relCha{m} = champdat.(cha{i}).name;
%                             end
%                         end
%                     end
%                 end
%             end
%         end
%     end
% end
%% Fixing missing damageType field
% for i = 1:length(cha)
%     for j = 1:length(abi)
%         if ~isfield(champdat.(cha{i}).abilities.(abi{j}),'damageType')
%             champdat.(cha{i}).abilities.(abi{j}).damageType = [];
%             disp("Fixed missing damageType field on "+champdat.(cha{i}).name+...
%                 "'s "+abi{j}+".")
%         end
%     end
% end
            
%% Manually fixing unit issues
%Katarina modifier ambiguity and damageType
for i = 1:5
    champdat.Katarina.abilities.W.effects.leveling.modifiers.units{i} = '% MS';
end
champdat.Katarina.abilities.R.damageType = 'MIXED_DAMAGE';
%Updating Aatrox units
champdat.Aatrox.abilities.E.effects(1).leveling.modifiers.units = ...
    {'% PMD';'% PMD';'% PMD';'% PMD';'% PMD'};
champdat.Aatrox.abilities.R.effects(1).leveling.modifiers.units = ...
    {'% MS';'% MS';'% MS'};
champdat.Aatrox.abilities.R.effects(2).leveling(2).modifiers.units = ...
    {'% healing';'% healing';'% healing'};
%Updating Akali units
champdat.Akali.abilities.W.effects(1).leveling(1).modifiers.units = ...
    {'% MS';'% MS';'% MS';'% MS';'% MS'};
%Updating Zoe units
champdat.Zoe.abilities.E.effects(2).leveling(1).modifiers.units = ...
    {'% slow';'% slow';'% slow';'% slow';'% slow'};
champdat.Zoe.abilities.W.effects(4).leveling(2).modifiers.units = ...
    {'s';'s';'s';'s';'s'};
champdat.Zoe.abilities.W.effects(4).leveling(1).modifiers.units = ...
    {'% MS';'% MS';'% MS';'% MS';'% MS'};
%Updating Lux units
champdat.Lux.abilities.E.effects(1).leveling.modifiers.units = ...
    {'% slow';'% slow';'% slow';'% slow';'% slow'};
%% Saving changes to champdat
save champdat.mat champdat
        
    