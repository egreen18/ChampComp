function [champ_out,m,b,g] = ItemAdd(itemdat,champ,item,slot)
%This function adds an item to the inventory of a champion and updates its
%stats accordingly.
%
%    [champ_out,m,b,g] = ItemAdd(itemdat,champ,item)
%
%The output, champ_out, is the resulting champion structure. itemdat is the
%item data structure. champ is the input champion structure. item is the 
%item ID, a 4 digit scalar. m tracks mythics, b tracks boots, and g tracks
%glory items.
champ_out = champ;
if slot < 1
    disp("The slot number chosen is too small. Choose a slot number between 1 and 6.")
    return
elseif slot > 6
    disp("The slot number chosen is too large. Choose a slot number between 1 and 6.")
    return
end
m = 0;
b = 0;
g = 0;
item = ['x',num2str(item)];
%Checking that the item is valid
if ~isfield(itemdat,item)
    disp("Please enter a valid item ID.")
    return
end
%Checking if item to be added is mythic
if strcmp(itemdat.(item).rank,'MYTHIC')
    %Checking for mythic already in inventory
    if champ.unique.m == 1
        m = 1;
    else
        champ_out.unique.m = 1;
    end
end
%Checking if item to be added is a boot
bootID = [3111;3006;3009;3020;3047;3117;3158;1001];
if any(bootID == itemdat.(item).id)
    %Checking for boot already in inventory
    if champ.unique.b == 1
        b = 1;
    else
        champ_out.unique.b = 1;
    end
end
%Checking if item to be added is a glory item
gloryID = [3041,1082];
if any(gloryID == itemdat.(item).id)
    %Checking for glory item already in inventory
    if champ.unique.g == 1
        g = 1;
    else
        champ_out.unique.g = 1;
    end
end
%Updating m,b,g upon removal of unique item
if m == 0 && b == 0 && g == 0
    if ~isempty(champ.inv{slot})
        if strcmp(itemdat.(champ.inv_id{slot}).rank,'MYTHIC')
            champ_out.unique.m = 0;
        elseif any(bootID == itemdat.(champ.inv_id{slot}).id)
            champ_out.unique.b = 0;
        elseif any(gloryID == itemdat.(champ.inv_id{slot}).id)
            champ_out.unique.g = 0;
        end
        champ_out = ItemRemove(itemdat,champ_out,slot);
    end
    champ_out.inv{slot} = itemdat.(item).name;
    champ_out.inv_id{slot} = item;
    statin = itemdat.(item).stats;
    champ_out = StatChange(champ_out,statin,'add');
    champ_out.pass.(['slot',num2str(slot)]) = itemdat.(item).passives;
elseif m == 1
    disp("A champion can only have one mythic item.")
elseif b == 1
    disp("A champion can only have one pair of boots.")
elseif g == 1
    disp("A champion can only have one glory item.")
end
end