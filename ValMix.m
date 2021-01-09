function [eff,mix] = ValMix(eff,champ,key,champ2)
%This function works within AbilityVal to evaluate mixed damage on a case
%by case basis
%
%   [eff,mix] = ValMix(eff,champ,key,champ2)
%
%eff is the input and output effect structure to be returned to AbilityVal
%after processing of the effect.dealt field. mix is a logical variable to
%indicate if a champion is not yet included in this function (1 if
%missing). champ and champ2 are the passed through champion structures, and
%key is thepassed through string indicating the current ability.
%structure
mix = 0;
chkey = [champ.ch,key];
switch chkey
    case 'AhriQ'
        eff(1).dealt = magi(eff(1).value,champ,champ2);
        eff(2).dealt = eff(1).dealt + eff(1).value;
    case 'AkaliR'
        eff(2,3).dealt = magi(eff(2,3).value,champ,champ2);
        eff(1,3).dealt = magi(eff(1,3).value,champ,champ2);
        eff(1,1).dealt = phys(eff(1,1).value,champ,champ2);
    case 'CamilleQ'
        eff(1,1).dealt = phys(eff(1,1).value,champ,champ2);
        if champ.l <= 16
            mod = 0.36 + 0.04*champ.l;
        elseif champ.l > 16
            mod = 1;
        end
        eff(1,3).dealt = phys((1-mod)*eff(1,3).value,champ,champ2);
            eff(1,3).dealt = eff(1,3).dealt + mod*eff(1,3).value;
    case 'CorkiE'
        eff(1).dealt = phys(0.5*eff(1).value,champ,champ2);
            eff(1).dealt = eff(1).dealt + magi(0.5*eff(1).value,champ,champ2);
        eff(2).dealt = phys(0.5*eff(2).value,champ,champ2);
            eff(2).dealt = eff(2).dealt + magi(0.5*eff(2).value,champ,champ2);
    case 'FizzQ'
        eff.dealt = magi(eff.value,champ,champ2);
            eff.dealt = eff.dealt + phys(champ.stats.attackDamage,champ,champ2);
    case 'IllaoiE'
    case 'KatarinaR'
        eff(1).dealt = phys(eff(1).value,champ,champ2);
        eff(2).dealt = phys(eff(2).value,champ,champ2);
        eff(3).dealt = magi(eff(3).value,champ,champ2);
        eff(4).dealt = magi(eff(4).value,champ,champ2);
    case 'LilliaQ'
        eff(1,2).dealt = magi(eff(1,2).value,champ,champ2);
        eff(2,2).dealt = eff(1,2).dealt + eff(1,2).value;
    case 'NunuQ'
        eff(1,1).dealt = magi(eff(1,1).value,champ,champ2);
        eff(1,2).dealt = eff(1,2).value;
    case 'RekSaiE'
        eff(1).dealt = phys(eff(1).value,champ,champ2);
        eff(2).dealt = eff(2).value;
    case 'SettW'
        eff(2).dealt = eff(2).value;
        eff(3).dealt = phys(eff(3).value,champ,champ2);
    case 'SkarnerQ'
        eff(1,1).dealt = phys(eff(1,1).value,champ,champ2);
        eff(1,2).dealt = magi(eff(1,2).value,champ,champ2);
        eff(2,2).dealt = eff(1,2).dealt + eff(1,1).dealt;
    case 'SkarnerE'
        eff(1,2).dealt = magi(eff(1,2).value,champ,champ2);
        eff(1,3).dealt = phys(eff(1,3).value,champ,champ2);
    case 'SkarnerR'
        eff(1).dealt = magi(eff(1).value,champ,champ2);
        eff(2).dealt = 2*eff(1).dealt + phys(1.2*champ.stats.attackDamage,champ,champ2);
    case 'UrgotR'
        eff.dealt = phys(eff.value,champ,champ2);
    case 'VelkozR'
        eff(1,3).dealt = magi(eff(1,3).value,champ,champ2);
        eff(2,3).dealt = magi(eff(2,3).value,champ,champ2);
    case 'YoneW'
        eff(2).dealt = phys(eff(2).value,champ,champ2);
        eff(3).dealt = magi(eff(3).value,champ,champ2);
        eff(1).dealt = eff(2).dealt + eff(3).dealt;
    case 'YoneR'
        eff(3,2).dealt = magi(eff(3,2).value,champ,champ2);
        eff(2,2).dealt = phys(eff(2,2).value,champ,champ2);
        eff(1,2).dealt = eff(3,2).dealt + eff(2,2).dealt;
    otherwise
        mix = 1;
end
    function dealt = magi(value,champ,champ2)
        MR = champ2.stats.magicResistance;
        MR = MR*(100-champ.stats.magicPenPer)/100;
        MR = MR - champ.stats.magicPenetration;
        if MR < 0
            MR = 0;
        end
        if MR >= 0
            dm = 100/(100+MR);
            dealt = value*dm;
        else
            dm = 2-100/(100-MR);
            dealt = value*dm;
        end
    end
    function dealt = phys(value,champ,champ2)
        AR = champ2.stats.armor;
        AR = AR*(100-champ.stats.armorPenetration)/100;
        AR = AR - champ.stats.lethality*(0.6+0.4*champ.l/18);
        if AR >= 0
            dm = 100/(100+AR);
            dealt = value*dm;
        else
            dm = 2-100/(100-AR);
            dealt = value*dm;
        end
    end
end