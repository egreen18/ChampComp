function [sta, name, tier, mythPas, price] = Item(item,xid)
%This function returns the stats, name, and on-hit effects of an item given
%the item.mat JSON data file and the item ID lead by x as a string

%%% DEFUNCT %%%

%Remained intact for reference

str = fieldnames(item.(xid).stats);
for i = 1:length(str)
    sta.(str{i}) = item.(xid).stats.(str{i}).flat;
end
tier = item.(xid).tier;
price = item.(xid).shop.prices.total;
end
