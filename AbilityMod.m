%This function investigates which modifiers are still missing from the
%AbilityVal.m function. This currently is not investigating champion
%passives.
load itemdat.mat itemdat
load champdat.mat champdat
cha = fieldnames(champdat);
abi = 'QWER';
unfin = {''};
unfinN = 0;
range = 1:length(cha); 
ignore = [8,51,81,113]; %Exlcuding Aphelios, Karma, Nidalee, Sona (Review these champions)
n = 0;
var = {''};
for i = setdiff(range,ignore)
    champ = ChampGen(itemdat,champdat,cha{i});
    champ = QuickLevel(champdat,champ);
    for j = 1:length(abi)
        [~,m] = AbilityVal(champdat,champ,abi(j),champ);
        if m == 1
            n = n+1;
            var{n} = ['champdat.',champ.ch,'.abilities.',abi(j),'.effects'];
            disp(['Missing modifier for ',champ.ch,'''s ',abi(j),'. '])
            if ~any(strcmp(unfin,champ.ch))
                unfin{unfinN+1} = champ.ch;
                unfinN = unfinN + 1;
            end
        end
    end
end
disp('<a href="matlab:openvar(var{n})">Link to last issue</a>')
