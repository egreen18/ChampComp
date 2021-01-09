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
ignore = [8,51,81]; %Excluding Aphelios, Karma, Nidalee(Review these champions)
n = 0;
var = {''};
si = 0;
for i = setdiff(range,ignore)
    champ = ChampGen(itemdat,champdat,cha{i});
    champ = QuickLevel(champdat,champ);
    for j = 1:length(abi)
        [effect,m] = AbilityVal(champdat,champ,abi(j),champ);
        num = numel(effect);
        siTemp = 0;
        for z = 1:num
            if ~isempty(effect(z).value)
                siTemp = siTemp + 1;
            end
        end
        if siTemp > si
            si = siTemp;
        end
        if m == 1
            n = n+1;
            var{n} = ['champdat.',champ.ch,'.abilities.',abi(j),'.effects'];
            disp(['Missing modifier for ',champ.ch,'''s ',abi(j),'.'])
            if ~any(strcmp(unfin,champ.ch))
                unfin{unfinN+1} = champ.ch;
                unfinN = unfinN + 1;
            end
        end
    end
end
if unfinN > 0
    disp('<a href="matlab:openvar(var{n})">Link to last issue</a>')
end
