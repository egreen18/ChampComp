function champ = StackUp(champ,stack)
%This function changes the number of stacks on a stacking champions passive
%
%   champ = StackUp(champ,stack)
%
%champ is the input champion structure. stack is the new number of stacks
switch champ.ch
    case 'Thresh'
        champ = StatChange(champ,champ.Stack.stats,'remove');
        champ.Stack.val = stack;
        champ.Stack.stats.abilityPower.flat = 0.75*champ.Stack.val;
        champ.Stack.stats.armor.flat = 0.75*champ.Stack.val;
        champ = StatChange(champ,champ.Stack.stats,'add');
    case 'Senna'
        champ = StatChange(champ,champ.Stack.stats,'remove');
        champ.Stack.val = stack;
        champ.Stack.stats.attackDamage.flat = 0.75*champ.Stack.val;
        champ.Stack.stats.criticalStrikeChance.percent = 10*floor(champ.Stack.val/20);
        champ.Stack.stats.lifesteal.percent = 0;
        champ = StatChange(champ,champ.Stack.stats,'add');
        if champ.stats.criticalStrikeChance > 100
            crit = champ.stats.criticalStrikeChance;
            champ = StatChange(champ,champ.Stack.stats,'remove');
            champ.Stack.stats.lifesteal.percent = 0.35*(crit - 100);
            champ.Stack.stats.criticalStrikeChance.percent = ...
                champ.Stack.stats.criticalStrikeChance.percent - (crit - 100);
            champ = StatChange(champ,champ.Stack.stats,'add');
        end
    case 'Chogath'
        champ = StatChange(champ,champ.Stack.stats,'remove');
        champ.Stack.val = stack;
        champ.Stack.stats.health.flat = (40+champ.abi.R*40)*champ.Stack.val;
        if champ.abi.R == 0 || isempty(champ.abi.R)
            champ.Stack.stats.health.flat = 0;
        end
        champ = StatChange(champ,champ.Stack.stats,'add');
    case 'Nasus'
        champ.Stack.val = stack;
    case 'Kindred'
        champ.Stack.val = stack;
end
        