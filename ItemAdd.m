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
if slot < 1
    disp("The slot number chosen is too small. Choose a slot number between 1 and 6.")
elseif slot > 6
    disp("The slot number chosen is too large. Choose a slot number between 1 and 6.")
else
    m = 0;
    item = ['x',num2str(item)];
    %Checking that the item is valid
    if isfield(itemdat,item)
    %Checking if item to be added is mythic
        if strcmp(itemdat.(item).rank,'MYTHIC')
            %Checking for mythic already in inventory
            range = 1:6;
            for i = range(range~=slot) %Skipping the slot being replaced
                %Exlcusion of slot from range is to allow for the user to
                %easily replace a mythic item with another
                if ~isempty(champ.inv_id{i})
                    it = champ.inv_id{i};
                    if strcmp(itemdat.(it).rank,'MYTHIC')
                        m = 1;
                    end
                end
            end
        end
        if m == 0
            if ~isempty(champ.inv{slot})
                champ_out = ItemRemove(itemdat,champ_out,slot);
            end
            champ_out.inv{slot} = itemdat.(item).name;
            champ_out.inv_id{slot} = item;
            statin = itemdat.(item).stats;
            champ_out = StatChange(champ_out,statin,'add');
            champ_out.pass.(['slot',num2str(slot)]) = itemdat.(item).passives;
        elseif m == 1
            disp("A champion can only have one mythic item.")
        end
    else
        disp("Please enter a valid item ID.")
    end
end
end