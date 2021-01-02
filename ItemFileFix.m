%This function fixes naming anomalies in the item JSON file. It also proves
%that no items are utilizing a change in stats provided per level, so this
%value can be constant for each item.
load item_original.mat itemdat
items = fieldnames(itemdat);
str = fieldnames(itemdat.(items{1}).stats);
fie = fieldnames(itemdat.(items{1}).stats.(str{1}));
for i = 1:length(items)
    for j = 1:length(str)
        fie_temp = fieldnames(itemdat.(items{i}).stats.(str{j}));
        for k = 3:length(fie)
            if ~strcmp(fie_temp{k},fie{k})
                disp("Nomenclature anomaly encountered with item "+items{i}...
                    +", stat "+str{j}+", field "+fie{k})
                disp(fie_temp{k}+" changed to "+fie{k})
                itemdat.(items{i}).stats.(str{j}).(fie{k}) = ... %Correcting name
                    itemdat.(items{i}).stats.(str{j}).(fie_temp{k});
                itemdat.(items{i}).stats.(str{j}) = rmfield(... %Removing anomaly
                    itemdat.(items{i}).stats.(str{j}),fie_temp{k});
            end
            if itemdat.(items{i}).stats.(str{j}).(fie{k}) ~=0
                disp("Identified nonzero.")
                disp(items{i}+" has a nonzero element in the stat "+str{j}+...
                    " and the field "+fie{k})
            end
        end
    end
end
%manually fixing an issue with rejuvination bead
itemdat.x1006.stats.healthRegen.percentBase = itemdat.x1006.stats.healthRegen.percent;
itemdat.x1006.stats.healthRegen.percent = 0;
%manually fixing an issue with dagger
itemdat.x1042.stats.attackSpeed.percentBase = itemdat.x1042.stats.attackSpeed.flat;
itemdat.x1042.stats.attackSpeed.flat = 0;
ite = fieldnames(itemdat);
for i = 1:length(ite)
    if itemdat.(ite{i}).stats.attackSpeed.flat ~= 0
        itemdat.(ite{i}).stats.attackSpeed.percentBase = itemdat.(ite{i}).stats.attackSpeed.flat;
        itemdat.(ite{i}).stats.attackSpeed.flat = 0;
    end
end
save itemdat.mat itemdat