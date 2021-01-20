def fix():
    #This function fixes naming anomalies in the item JSON file. It also proves
    #that no items are utilizing a change in stats provided per level, so this
    #value can be constant for each item.
    import json
    with open(r"../itemOriginal.json") as f:
        itemdat = json.load(f)
    ## Fixing a nomenclature issue
    items = list(itemdat.keys())
    ## Fixing stat placement issues
    #manually fixing an issue with rejuvination bead
    itemdat['1006']['stats']['healthRegen']['percentBase'] = itemdat['1006']['stats']['healthRegen']['percent']
    itemdat['1006']['stats']['healthRegen']['percent'] = 0;
    #manually fixing an issue with dagger
    itemdat['1042']['stats']['attackSpeed']['percentBase'] = itemdat['1042']['stats']['attackSpeed']['flat']
    itemdat['1042']['stats']['attackSpeed']['flat'] = 0;
    for i in items:
        if itemdat[i]['stats']['attackSpeed']['flat'] != 0:
            itemdat[i]['stats']['attackSpeed']['percentBase'] = itemdat[i]['stats']['attackSpeed']['flat']
            itemdat[i]['stats']['attackSpeed']['flat'] = 0;
    print("Manually fixed stat placement issues.")
    ## Fixing an issue with movespeed being treated as a scalar instead of a structure
    #First checking stats on all items, then checking stats on item passives
    for i in items:
        if not type(itemdat[i]['stats']['movespeed']) is dict:
            ms = itemdat[i]['stats']['movespeed']
            itemdat[i]['stats']['movespeed'] = itemdat['1001']['stats']['abilityPower']
            itemdat[i]['stats']['movespeed']['flat'] = ms;
            for jdx in range(itemdat[i]['passives']):
                if not type(itemdat[i]['passives'][jdx]['stats']['movespeed']) is dict:
                    ms = itemdat[i]['passives'][jdx]['stats']['movespeed']
                    itemdat[i]['passives'][jdx]['stats']['movespeed'] = itemdat['1001']['stats']['abilityPower']
                    itemdat[i]['passives'][jdx]['stats']['movespeed']['flat'] = ms;
    print("Movespeed stat structures were updated across items and their passives.")
    with open(r"../Items.json","w") as outfile:
        json.dump(itemdat,outfile)