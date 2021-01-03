function champ_out = ItemRemove(itemdat,champ,slot)
%This function removes a specified item from a champion's inventory
%
%   champ_out = ItemRemove(itemdat,champ,slot)
%
%The output, champ_out, is the resulting champion structure. itemdat is the
%item data structure.champ is thechampion structure. slot is a scalar 
%between 1 and 6 indicating the the slot number from which the item should 
%be removed
champ_out = champ;
if slot < 1
    disp("The slot number chosen is too small. Choose a slot number between 1 and 6.")
elseif slot > 6
    disp("The slot number chosen is too large. Choose a slot number between 1 and 6.")
else
    champ_out.inv{slot} = ''; %Clearing slots and pulling IDs
    item = champ_out.inv_id{slot}; champ_out.inv_id{slot} = '';
    statin = itemdat.(item).stats;
    champ_out = StatChange(champ_out,statin,'remove');
    champ_out.pass.(['slot',num2str(slot)]) = struct;
end
end
