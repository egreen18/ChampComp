function ChampFileFix
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
%% Fixing general unit issues
max100AP = {'Varus' 'Trundle' 'Nasus' 'Malzahar' 'Kog''Maw' 'Gragas'};
for v = 1:length(cha)
    for x = 1:length(abi)
        for p = 1:length(champdat.(cha{v}).abilities.(abi{x}))
        for k = 1:length(champdat.(cha{v}).abilities.(abi{x})(p).effects)
        if ~isempty(champdat.(cha{v}).abilities.(abi{x})(p).effects(k).leveling)
            for j = 1:length(champdat.(cha{v}).abilities.(abi{x})(p).effects(k).leveling)
                abil = champdat.(cha{v}).abilities.(abi{x})(p).effects(k).leveling(j).modifiers;
                for i = 1:length(abil)
                    for l = 1:length(abil(i).units)
                        switch abil(i).units{l}
                            case '%  of target''s maximum health'
                                abil(i).units{l} = '% of target''s maximum health';
                            case '% of Zac''s maximum health'
                                abil(i).units{l} = '% of maximum health';
                            case {'% of his maximum health','% of Braum''s maximum health'}
                                abil(i).units{l} = '% of maximum health';
                            case {'% of the target''s current health','%  of target''s current health'}
                                abil(i).units{l} = '% of target''s current health';
                            case '% of his bonus health'
                                abil(i).units{l} = '% of bonus health';
                            case {'% of his missing health','% missing health'}
                                abil(i).units{l} = '% of missing health';
                            case '% maximum health'
                                abil(i).units{l} = '% of maximum health';
                            case '% bonus health'
                                abil(i).units{l} = '% of bonus health';
                            case '% per 100 AP'
                                if any(strcmp(max100AP,champdat.(cha{v}).name))
                                    abil(i).units{l} = '% max health per 100 AP';
                                elseif strcmp(champdat.(cha{v}).name,'Galio') && strcmp(abi{x},'Q')
                                    abil(i).units{l} = '% max health per 100 AP';
                                elseif strcmp(champdat.(cha{v}).name,'Fiddlesticks')
                                    abil(i).units{l} = '% current health per 100 AP';
                                elseif strcmp(champdat.(cha{v}).name,'Kayle') && strcmp(abi{x},'E')
                                    abil(i).units{l} = '% missing health per 100 AP';
                                end
                            case '% per 100 bonus AD'
                                if any(strcmp(champdat.(cha{v}).name,{'Camille','Kled'}))
                                    abil(i).units{l} = '% max health per 100 bonus AD';
                                end
                            case '% per 100 AD'
                                if strcmp(champdat.(cha{v}).name,'Illaoi')
                                    abil(i).units{l} = '% transmission per 100 AD';
                                end
                            case '%  of the target''s maximum health'
                                abil(i).units{l} = '% of target''s maximum health';
                            case {'% of primary target''s bonus health','% of kicked target''s bonus health'}
                                abil(i).units{l} = '% of target bonus health';
                            case '% of her maximum health'
                                abil(i).units{l} = '% of maximum health';
                            case {'% of armor','% armor','% of Taric''s armor'}
                                abil(i).units{l} = '% total armor';
                            case '%  of target''s missing health'
                                abil(i).units{l} = '% of target''s missing health';
                        end
                        champdat.(cha{v}).abilities.(abi{x})(p).effects(k).leveling(j).modifiers = abil;
                    end
                end
            end
        end
        end
        end
    end
end    
disp("Modifer units were updated across champion abilities")
%% Manually fixing issues that can't be fixed iteratively
%Katarina damageType
champdat.Katarina.abilities.R.damageType = 'MIXED_DAMAGE';
%Sett W splitting damage types
champdat.Sett.abilities.W.effects(2).leveling = champdat.Sett.abilities.W.effects(3).leveling;
champdat.Sett.abilities.W.effects(2).leveling.attribute = 'True Damage';
champdat.Sett.abilities.W.effects(3).leveling.attribute = 'Physical Damage';
%Fixing Karma non-repeating modifiers and adding R scale indicator (Sona
%and Nidalee also had non repeating modifiers
modBrok = {'Karma','Sona','Nidalee'};
for p = 1:length(modBrok)
for i = 1:3
    for j = 1:length(champdat.(modBrok{p}).abilities.(abi{i}))
        for k = 1:length(champdat.(modBrok{p}).abilities.(abi{i})(j).effects)
            if ~isempty(champdat.(modBrok{p}).abilities.(abi{i})(j).effects(k).leveling)
            for l = 1:length(champdat.(modBrok{p}).abilities.(abi{i})(j).effects(k).leveling)
                for m = 1:length(champdat.(modBrok{p}).abilities.(abi{i})(j).effects(k).leveling(l).modifiers)
                    chTemp = champdat.(modBrok{p}).abilities.(abi{i})(j).effects(k).leveling(l).modifiers(m);
                    if length(chTemp.units) == 4
                        for n = 1:4
                            chTemp.units{n,1} = [chTemp.units{n,1},':Rscale'];
                        end
                    elseif strcmp(champdat.(modBrok{p}).name,'Nidalee') && j == 2
                        uni = chTemp.units{1,1};
                        chTemp.units{''};
                        for n = 1:4
                            chTemp.units{n,1} = uni;
                            chTemp.units{n,1} = [chTemp.units{n,1},':Rscale'];
                        end
                    end
                    if length(chTemp.values) == 1
                        val = chTemp.values;
                        for n = 1:5
                            chTemp.values(n,1) = val;
                        end
                    end
                    if length(chTemp.units) == 1
                        uni = chTemp.units;
                        for n = 1:5
                            chTemp.units(n,1) = uni;
                        end
                    end
                    champdat.(modBrok{p}).abilities.(abi{i})(j).effects(k).leveling(l).modifiers(m) = chTemp;
                end
            end
            end
        end
    end
end
end                    
        
disp("Sett and Katarina were updated for mixed damage clarity")
disp("Sona, Karma and Nidalee had their non-repeating modifiers updated")
disp("Karma and Nidalee had the 'Rlevel' modifer added to some of their scalings.")
%% Investigating resource cost field
% for i = 1:length(cha)
%     for j = 1:length(abi)
%         if isempty(champdat.(cha{i}).abilities.(abi{j}).cost)
%             disp([cha{i},' is missing a cost structure on their ',abi{j}])
%         end
%     end
% end
%% Saving changes to champdat
save champdat.mat champdat
end
    