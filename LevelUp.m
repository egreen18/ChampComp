function champ_out = LevelUp(champdat,champ,l)
%This function levels up a champion structure
%
%    champ_out = LevelUp(champdat,champ,l)
%
%The output, champ_out, is the newly levelled champion structure. Champdat
%is the champion data file, champ is the champion structure to be levelled,
%and l is a scalar value between 1 and 18 indicating the new champion level

champ_out = champ;
if l < 1
    disp("Champion level indicated is too low. Choose a level between one and 18.")
elseif l > 18
    disp("Champion level indicated is too high. Choose a level between one and 18.")
else
    champ_out.l = l; %setting the new level                        
    sta = Level(champdat,champ.ch,champ.l); %pulling the stats from the current level
    sta_new = Level(champdat,champ.ch,l); %pulling the stats for the new level
    str = fieldnames(sta); %acquiring field names of all stats in structure
    for i = 1:length(str)
        %subtracting stats of the old level
        champ_out.stats.(str{i}) = champ_out.stats.(str{i}) - sta.(str{i}); 
        %adding stats of the new level
        champ_out.stats.(str{i}) = champ_out.stats.(str{i}) + sta_new.(str{i});
        %this method is done instead of just setting the stats equal to the
        %new level in order to preserve any potential stats from items.
        %the same treatment isnt necessary for the base stat tracking
        champ_out.sta_base.(str{i}) = sta_new.(str{i});
    end
    %Attack speed base is handled differently, remaining constant
    champ_out.sta_base.attackSpeed = Level(champdat,champ.ch,1).attackSpeed;
end
end