%This function fills the spells file with appropriately named png's of
%league champion spells downloaded from CDrag
cha = fieldnames(champdat);
abi = 'QWER';
for i = 1:length(cha)
    for j = 1:length(abi)
        for k = 1:length(champdat.(cha{i}).abilities.(abi(j)))
            if length(champdat.(cha{i}).abilities.(abi(j))) > 1
                name = [cha{i},abi(j),num2str(k)];
                I = imread(champdat.(cha{i}).abilities.(abi(j))(k).icon);
                if ~isfile(name)
                imwrite(I,[name,'.png']);
                end
            else
                name = [cha{i},abi(j)];
                I = imread(champdat.(cha{i}).abilities.(abi(j))(k).icon);
                if ~isfile(name)
                imwrite(I,[name,'.png']);
                end
            end
        end
    end
end