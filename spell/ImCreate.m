%This function fills the spells file with appropriately named png's of
%league champion spells downloaded from CDrag
cha = fieldnames(champdat);
abi = 'QWER';
for i = 1:length(cha)
    for j = 1:length(abi)
        I = imread(champdat.(cha{i}).abilities.(abi(j))(1).icon);
        name = [cha{i},abi(j)];
        imwrite(I,[name,'.png']);
    end
end