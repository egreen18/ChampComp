from items import itemfix
from champions import champfix
import json
import os
import requests
import re

def patch():
    urlChamp = 'http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/champions.json'
    urlItem = 'http://cdn.merakianalytics.com/riot/lol/resources/latest/en-US/items.json'
    champdatNew = json.loads(requests.get(urlChamp).text)
    itemdatNew = json.loads(requests.get(urlItem).text)
    
    os.chdir(os.path.join('version','latest'))
    from patch import key
    with open(r"champions.json",encoding="utf8") as f:
        champdat = json.load(f)
    with open(r"Items.json",encoding="utf8") as f:
        itemdat = json.load(f)
        
    keyFind = re.compile(r'.*cdn/([\d\.]*)/.*')    
    keyNew = keyFind.split(champdatNew['Aatrox']['icon'])[1]
    
    if key == keyNew:
        print('Up to date, no patch required')
    else:
        print('Updating to patch '+keyNew)
        with open(r"patch.py","w") as outfile:
            outfile.write("key = '"+keyNew+"'")
        with open(r"champOriginal.json","w") as outfile:
            json.dump(champdatNew,outfile)
        with open(r"itemOriginal.json","w") as outfile:
            json.dump(itemdatNew,outfile)
        os.chdir('..')
        os.makedirs('patch'+key)
        os.chdir('patch'+key)
        with open(r"champions.json","w") as outfile:
            json.dump(champdat,outfile)
        with open(r"Items.json","w") as outfile:
            json.dump(itemdat,outfile)
        with open(r"patch.py","w") as outfile:
            outfile.write("key = '"+key+"'")
            
    os.chdir('..')
    os.chdir('..')
    
    print('\n')
    itemfix.fix_items()
    champfix.fix_champs()