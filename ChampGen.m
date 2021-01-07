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
%pass is a field with 6 elements containing the item passives corresponding
%to each inventory slot

champ.l = 1;
champ.ch = ch;
champ.inv = {'';'';'';'';'';''};
champ.inv_id = {'';'';'';'';'';''};
champ.stats = itemdat.x3363.stats;
str = fieldnames(champ.stats);
for i = 1:length(str)
    champ.stats.(str{i}) = 0;
end
champ.stats.magicPenPer = 0;
sta = Level(champdat,ch,champ.l);
str = fieldnames(sta);
for i = 1:length(str)
    champ.stats.(str{i}) = sta.(str{i});
end
champ.sta_base = champ.stats;
for i = 1:6
    champ.pass.(['slot',num2str(i)]) = struct;
end
abi = ['Q','W','E','R'];
for i = 1:length(abi)
    champ.abi.(abi(i)) = 0;
end
champ.stats.healthCurrent = champ.stats.health;
champ.stats.manaCurrent = champ.stats.mana;
if strcmp(champ.ch,'Thresh')
    champ.Souls = 0;
elseif strcmp(champ.ch,'Senna')
    champ.Mist = 0;
elseif strcmp(champ.ch,'Nasus')
    champ.Siphon = 0;
elseif strcmp(champ.ch,'Kindred')
    champ.Mark = 0;
elseif strcmp(champ.ch,'Chogath')
    champ.Feast = 0;
end

