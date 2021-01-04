function champ_out = QuickLevel(champdat,champ)
%This function quickly sets a champ level to 6 and levels Q,W,E, and R.
%(3,1,1,1)
%
%   champ_out = QuickLevel(champ)
%
%champ_out is the output champion structure. champ is the champion input
%structure.
champ_out = champ;
champ_out = LevelUp(champdat,champ_out,6);
champ_out.abi.Q = 3;
champ_out.abi.W = 1;
champ_out.abi.E = 1;
champ_out.abi.R = 1;
end