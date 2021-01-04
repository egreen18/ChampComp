function champ_out = StatChange(champ,statin,mod)
%This function updates the stats of a champion given the input stats
%
%    champ_out = StatChange(champ,statin,mod)
%
%champ_out is the resulting output champion structure. champ is the input
%champion structure. statin is a structure of stats to update the champ
%with. statin must be a structure of the base league stats with 6 fields
%per stat. mod is the modifier, 'add' or 'remove'
champ_out = champ;
str = fieldnames(statin);
if strcmp(mod,'add')
    for i = 1:length(str)
        champ_out.stats.(str{i}) = champ_out.stats.(str{i}) ...
                + statin.(str{i}).flat + statin.(str{i}).percent*...
                champ_out.stats.(str{i})/100 + statin.(str{i})...
                .percentBase*champ.sta_base.(str{i})/100;
    end
elseif strcmp(mod,'remove')
    for i = 1:length(str)
        champ_out.stats.(str{i}) = champ_out.stats.(str{i}) ...
                - itemdat.(item).stats.(str{i}).flat - statin.(str{i})...
                .percent*champ_out.stats.(str{i})/100 - statin.(str{i})...
                .percentBase*champ.sta_base.(str{i})/100;
    end
else
    disp("Please enter a valid modifier, 'add' or 'remove'.")
end
end