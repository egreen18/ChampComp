function champ_out = PassiveUp(itemdat,champ)
%This function updates the passives and their interactions on a champion.
%Primarily it calculates mythic passive bonuses and examines on hit.
%
%    champ_out = PassiveUp(itemdat,champ)
%
%The resulting structure, champ_out, is the modified and up to date
%champion structure. itemdat is the item data structure.champ is the input 
%champion structure.
%% Initialization
champ_out = champ;
%% Mythic passives
nLeg = 0; %Counting the number of legendary items in the inventory
mID = 0;
for i = 1:6
    if ~isempty(champ.inv{i})
        if strcmp(itemdat.(champ.inv_id{i}).rank,'LEGENDARY')
            nLeg = nLeg+1;
        elseif strcmp(itemdat.(champ.inv_id{i}).rank,'MYTHIC')
            mID = champ.inv_id{i};
            for j = 1:length(itemdat.(mID).passives)
                if itemdat.(mID).passives(j).mythic == 1
                    mIN = j;
                end
            end
        end
    end
end
if mID > 0
    statin = itemdat.(mID).passives(mIN).stats;
    sta = fieldnames(statin);
    fie = fieldnames(statin.(sta{1}));
    for i = 1:length(sta)
        for j = 1:length(fie)
        statin.(sta{i}).(fie{j}) = statin.(sta{i}).(fie{j})*nLeg;
        end
    end
    champ_out = StatChange(champ_out,champ_out.passive.statsMythic,'remove');
    champ_out.passive.statsMythic = statin;
    champ_out = StatChange(champ_out,statin,'add');
end
%% Current health and mana
champ_out.stats.healthCurrent = champ_out.stats.health;
champ_out.stats.manaCurrent = champ_out.stats.mana;
%% Item Passives
for i = 1:6
    switch champ.inv_id{i}
        case 'x3041' %Mejai's
            champ_out.pass.mod = 5;
        case 'x1082' %Dark Seal
            champ_out.pass.mod = 5;
    end
end
end
