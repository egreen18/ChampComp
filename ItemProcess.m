%This function seeks to process the item data and create a cell array 
clear
load itemdat.mat itemdat
itemkeyS = fieldnames(itemdat); 
itemkeyS = split(itemkeyS,'x'); itemkeyS = itemkeyS(:,2);
itemkey = zeros(1,length(itemkeyS));
for i = 1:length(itemkeyS)
    itemkey(i) = str2double(itemkeyS{i});
end
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
clear i
save itemdat.mat