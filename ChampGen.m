function champ = ChampGen(itemdat,champdat,ch)
%This function generates a new champion structure given champion name ch
%
%   champ = ChampGen(itemdat,champdat,ch)
%
%The output champ is a structure containing fields l, ch, inv, and stats. 
%itemdat is the item data structure, champdat is the champion data
%structure, and ch is the name of the desired champion as a string.
%sta_base are the base stas of the champion at their level before items.
%inv_id mirrors the inv character array but contains the corresponding item ids

champ.l = 1;
champ.ch = ch;
champ.inv = {'';'';'';'';'';''};
champ.inv_id = {'';'';'';'';'';''};
champ.stats = itemdat.x3363.stats;
str = fieldnames(champ.stats);
for i = 1:length(str)
    champ.stats.(str{i}) = 0;
end
sta = Level(champdat,ch,champ.l);
str = fieldnames(sta);
for i = 1:length(str)
    champ.stats.(str{i}) = sta.(str{i});
end
champ.sta_base = champ.stats;
end
