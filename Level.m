function sta = Level(champdat,ch,l)
%The level function takes input champion (ch, a string) and level (l, a
%double) and parses through data to return the stats of the given champ at
%level l. Also requires input of the parsed JSON data file champ
str = fieldnames(champdat.(ch).stats);
for i = 1:length(str)
    sta.(str{i}) = getStat(champdat,str{i},ch,l);
end
sta.attackSpeed = champdat.(ch).stats.attackSpeed.flat; %Attack speed is handled in LevelUp.m
function staInd = getStat(champ,stat,ch,l)
    staInd = champ.(ch).stats.(stat).flat + champ.(ch).stats.(stat).perLevel...
        *(l-1);
end
end