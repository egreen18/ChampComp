function champ_out = ItemAdd(itemdat,champ,item,slot)
%This function adds an item to the inventory of a champion and updates its
%stats accordingly.
%
%    champ_out = ItemAdd(itemdat,champ,item)
%
%The output, champ_out, is the resulting champion structure. itemdat is the
%item data structure. champ is the input champion structure. item is the 
%item ID, a 4 digit scalar.
champ_out = champ;
item = ['x',num2str(item)];
champ_out.inv{slot} = itemdat.(item).name;
champ_out.inv_id{slot} = item;
str = fieldnames(itemdat.(item).stats);
for i = 1:length(str)
    champ_out.stats.(str{i}) = champ_out.stats.(str{i}) ...
        + itemdat.(item).stats.(str{i}).flat + itemdat.(item).stats...
        .(str{i}).percent*champ_out.stats.(str{i})/100 + itemdat...
        .(item).stats.(str{i}).percentBase*champ.sta_base.(str{i})/100;
end
end