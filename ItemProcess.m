%This function seeks to process the item data and create a cell array 
%% Initializing
clear
load item_original.mat itemdat
%% Getting keys
itemkeyS = fieldnames(itemdat); 
itemkeyS = split(itemkeyS,'x'); itemkeyS = itemkeyS(:,2);
itemkey = zeros(1,length(itemkeyS));
for i = 1:length(itemkeyS)
    itemkey(i) = str2double(itemkeyS{i});
end
%% Removing irrelevant items from key and referencing names
listing = dir('item');
itemRelS(2,length(listing)-2) = {''};
itemRel = zeros(1,length(listing)-2);
for i = 3:length(listing)
    itemRelS(:,i) = split(listing(i).name,'.png');
    itemRel(i) = str2double(itemRelS(1,i));
end
itemkey = intersect(itemkey,itemRel);
itemname = {''};
for i = 1:length(itemkey)
    itemname{i} = itemdat.(['x',num2str(itemkey(i))]).name;
end
%% Display Item Names
for i = 1:length(itemname)
    disp(itemname{i})
end
%% Display Item Keys
for i = 1:length(itemkey)
    disp(itemkey(i))
end
%% Saving
save('itemdat.mat','itemkey','itemname','-append')