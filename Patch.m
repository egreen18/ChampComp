function Patch
%This function analyzes and processes data from a new patch. It looks for
%two JSON files: 'champion.json' and 'Items.json'. It converts them to
%structures itemdat and champdat and runs filefix functions among other
%modifiers to process all data.
%% Decoding JSON files
clear
champdat = jsondecode(fileread('champion.json'));
save champ_original.mat
clear

itemdat = jsondecode(fileread('Items.json'));
save item_original.mat
clear
%% Processing and saving data
ItemFileFix
ItemProcess(1)
ChampFileFix
AbilityMod
end