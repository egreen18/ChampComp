function sta = Level(champdat,ch,l)
%The level function takes input champion (ch, a string) and level (l, a
%double) and parses through data to return the stats of the given champ at
%level l. Also requires input of the parsed JSON data file champ
str = fieldnames(champdat.(ch).stats);
for i = 1:length(str)
    sta.(str{i}) = getStat(champdat,str{i},ch,l);
end
sta.healthCurrent = sta.health;
function staInd = getStat(champ,stat,ch,l)
    b = champ.(ch).stats.(stat).flat;
    g = champ.(ch).stats.(stat).perLevel;
    if strcmp(stat,'attackSpeed')
        staInd = b*(100+g*(l-1)*(0.7025+0.0175*(l-1)))/100;
    else
        staInd = b + g*(l-1)*(0.7025+0.0175*(l-1));
    end
end
end