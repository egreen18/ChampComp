def fix_champs():
    #This function is a means to investigate the champdat structure and to fix
    #any discovered errors.
    ## Initialization
    import json
    with open(r"version/latest/champOriginal.json") as f:
        champdat = json.load(f)
    cha = list(champdat.keys())
    abi = ('Q','W','E','R');
    ## Fixing general unit issues
    max100AP = ('Varus','Trundle','Nasus','Malzahar',"Kog'Maw",'Gragas');
    for v in cha:
        for x in abi:
            for idxp,p in enumerate(champdat[v]['abilities'][x]):
                for idxk,k in enumerate(p['effects']):
                    for idxj,j in enumerate(k['leveling']):
                        for idxi, i in enumerate(j['modifiers']):
                            for idxl,l in enumerate(i['units']):
                                if l == "%  of target's maximum health":
                                    l = "% of target's maximum health"
                                elif l == "% of Zac's maximum health":
                                    l = '% of maximum health'
                                elif l in ('% of his maximum health',"% of Braum's maximum health"):
                                    l = '% of maximum health'
                                elif l in ("% of the target's current health","%  of target's current health"):
                                    l = "% of target's current health"
                                elif l == '% of his bonus health':
                                    l = '% of bonus health'
                                elif l in ('% of his missing health','% missing health'):
                                    l = '% of missing health'
                                elif l == '% maximum health':
                                    l = '% of maximum health'
                                elif l == '% bonus health':
                                    l = '% of bonus health'
                                elif l == '% per 100 AP':
                                    if champdat[v]['name'] in max100AP:
                                        l = '% max health per 100 AP'
                                    elif champdat[v]['name'] == 'Galio' and x == 'Q':
                                        l = '% max health per 100 AP'
                                    elif champdat[v]['name'] == 'Fiddlesticks':
                                        l = '% current health per 100 AP'
                                    elif champdat[v]['name'] == 'Kayle' and x =='E':
                                        l = '% missing health per 100 AP'
                                elif l == '% per 100 bonus AD':
                                    if champdat[v]['name'] in ('Camille','Kled'):
                                        l = '% max health per 100 bonus AD'
                                elif l == '% per 100 AD':
                                    if champdat[v]['name'] == 'Illaoi':
                                        l = '% transmission per 100 AD'
                                elif l == "%  of the target's maximum health":
                                    l = "% of target's maximum health"
                                elif l == '%  bonus AD':
                                    l = '% bonus AD'
                                elif l in ("% of primary target's bonus health","% of kicked target's bonus health"):
                                    l = '% of target bonus health'
                                elif l == '% of her maximum health':
                                    l = '% of maximum health'
                                elif l in ('% of armor','% armor',"% of Taric's armor"):
                                    l = '% total armor'
                                elif l == "%  of target's missing health":
                                    l = "% of target's missing health"
                                elif l == '% total attack speed':
                                    l = '% attack speed'
                                elif l == '% (based on level) movement speed':
                                    l = '% (based on level) MS'
                                champdat[v]['abilities'][x][idxp]['effects']\
                                [idxk]['leveling'][idxj]['modifiers'][idxi]\
                                ['units'][idxl] = l
    print("Modifer units were updated across champion abilities")
    ## Manually fixing issues that can't be fixed iteratively
    #Katarina damageType
    champdat['Katarina']['abilities']['R'][0]['damageType'] = 'MIXED_DAMAGE';
    #Sett W splitting damage types
    champdat['Sett']['abilities']['W'][0]['effects'][1]['leveling'] = champdat['Sett']['abilities']['W'][0]['effects'][2]['leveling']
    champdat['Sett']['abilities']['W'][0]['effects'][1]['leveling'][0]['attribute'] = 'True Damage';
    champdat['Sett']['abilities']['W'][0]['effects'][2]['leveling'][0]['attribute'] = 'Physical Damage';
    #Fixing Karma non-repeating modifiers and adding R scale indicator (Sona
    #and Nidalee also had non repeating modifiers
    modBrok = {'Karma','Sona','Nidalee'}
    for p in modBrok:
        for i in range(3):
            for idxj,j in enumerate(champdat[p]['abilities'][abi[i]]):
                for idxk,k in enumerate(j['effects']):
                    for idxl,l in enumerate(k['leveling']):
                        for idxm,m in enumerate(l['modifiers']):
                            if len(m['units']) == 4:
                                for n in range(3):
                                    m['units'][n] = m['units'][n]+':Rscale'
                            elif p == 'Nidalee' and idxj == 2:
                                uni = m['units'][0]
                                for n in range(3):
                                    m['units'][n] = uni+':Rscale';
                            if len(m['values']) == 1:
                                val = m['values'][0]
                                m['values'] = [val]*5
                            if len(m['units']) == 1:
                                uni = m['units'][0]
                                m['units'] = [uni]*5
                            champdat[p]['abilities'][abi[i]][idxj]['effects'][idxk]['leveling'][idxl]['modifiers'][idxm] = m              
            
    print("Sett and Katarina were updated for mixed damage clarity")
    print("Sona, Karma and Nidalee had their non-repeating modifiers updated")
    print("Karma and Nidalee had the 'Rlevel' modifer added to some of their scalings.")  
    with open(r"version/latest/champions.json","w") as outfile:
        json.dump(champdat,outfile)