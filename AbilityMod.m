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
ignore = [51,81,113]; %Exlcuding Karma, Nidalee, Sona (Review these champions)
for i = setdiff(range,ignore)
    champ = ChampGen(itemdat,champdat,cha{i});
    champ = QuickLevel(champdat,champ);
    for j = 1:length(abi)
        [~,m] = AbilityVal(champdat,champ,abi(j));
        if m == 1
            disp("Missing modifier for "+champ.ch+"'s "+abi(j)+".")
            if ~any(strcmp(unfin,champ.ch))
                unfin{unfinN+1} = champ.ch;
                unfinN = unfinN + 1;
            end
        end
    end
end
