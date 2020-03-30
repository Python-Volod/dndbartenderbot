#MMMMSSSSSSSSSSSSSSSSSMSS;.     .dMMMMSSSSSSMMSSSSSSSSS
#MMSSSSSSSMSSSSSMSSSSMMMSS."-.-":MMMMMSSSSMMMMSSMSSSMMS
#MSSSSSSSMSSSSMMMSSMMMPTMM;"-/\":MMM^"     MMMSSMMMSSMM
#SSSSSSSMMSSMMMMMMMMMP-.MMM :  ;.;P       dMMMMMMMMMP' 
#SSMSSSMMMSMMMMMMMMMP   :M;`:  ;.'+"""t+dMMMMMMMMMMP   
#MMMSSMMMMMMMMPTMMMM"""":P `.\// '    ""^^MMMMMMMP'    
#MMMMMMPTMMMMP="TMMMsg,      \/   db`c"  dMMMMMP"      
#MMMMMM  TMMM   d$$$b ^          /T$; ;-/TMMMP         
#MMMMM; .^`M; d$P^T$$b          :  $$ ::  "T(          
#MMMMMM   .-+d$$   $$$;         ; d$$ ;;  __           
#MMMMMMb   _d$$$   $$$$         :$$$; :MmMMMMp.        
#MMMMMM"  " T$$$._.$$$;          T$P.'MMMSSSSSSb.      
#MMM`TMb   -")T$$$$$$P'       `._ ""  :MMSSSMMP'       
#MMM / \    '  "T$$P"           /     :MMMMMMM         
#MMSb`. ;                      "      :MMMMMMM         
#MMSSb_lSSSb.      \ `.   .___.       MMMMMMMM         
#MMMMSSSSSSSSb.                     .MMMMMMMMM         
#MMMMMMMMMMMSSSb                  .dMMMMMMMMM'         
#MMMMMMMMMMMMMSS;               .dMMMMMMMMMMP          
#MMMMMMMMMMMMMb`;"-.          .dMMMMMMMMMMP'           
#MMMMMMMMMMMMMMb    ""--.___.dMMMMMMMMMP^"
# Art by "bug" from http://www.ascii-art.de/ascii/ab/anime.txt

import discord
from random import randint
from math import floor
import time

import weapons_data
import monsters_data
import spells_data

def checkDice(dice):
    if dice == "4" or dice == "6" or dice == "8" or dice == "10" or dice == "12" or dice == "20" or dice == "100":
        return 0
    else:
        return 1


class MyClient(discord.Client):
    async def on_ready(self):
        current_time =  str(time.ctime(time.time())).split()
        time_hhmmss = current_time[3]
        print('[' + time_hhmmss + '] Logged on as "{0}"!'.format(self.user))

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content.startswith('$help'):
            await message.channel.send('Greetings adventurer !\n I\'m bartender bot. Here\'s feature list\n@ Dice rolling - $roll [d20] or $roll [2d20] \n@ Getting info about monsters/spells/items - $info [spell/weapon/monster] [Fireball/Greatsword/Beholder] (soon)\n @ Calculate currency exchange - $exchange [amount] [type]')
        if message.content.startswith('$roll'):
            text = message.content
            textsplit = text.split()
            try:
                raw = textsplit[1]
            except IndexError:
                message.channel.send("So... What should I roll ?")
            diceinfo = raw.split('d')
            if(diceinfo[0] == ""):
                diceinfo[0] = "1"
            if(checkDice(diceinfo[1]) == 1):
                await message.channel.send('oh no...\nThere\'s no such dice !\nHere\'s list of all dices I can roll\nd4, d6, d8, d10, d20, d100')
                return 1
            dicesum = 0
            await message.channel.send('🎲 Rolling ' + raw)
            for i in range(0, int(diceinfo[0])):
                diceval = randint(1, int(diceinfo[1]))
                dicesum = dicesum + diceval
                await message.channel.send('Dice #' + str(i+1) + ": " + str(diceval))
            await message.channel.send("--------------------------\nTotal: " + str(dicesum))
        if message.content.startswith('$exchange'):
            args = message.content.split()
            try:
                amount = int(args[1])
            except IndexError:
                await message.channel.send("You should tell me how much and in which curency you want to exchange")
                return 1
            try:
                currency = args[2]
            except IndexError:
                await message.channel.send("You should tell me what curency you want to exchange")
                return 1
            answer = "💰 Exchange calculator: \n"
            if(currency == "cp" or currency == "copper"):
                answer += "Copper coin: " + str(amount) + "\n" + "Silver coin: " + str(floor(amount/10)) + "\n" + "Electrum coin: " + str(floor(amount/50)) + "\n" + "Gold coin: " + str(floor(amount/100)) + "\n" + "Platinum coin: " + str(floor(amount/1000))
            elif(currency == "sp" or currency == "silver"):
                answer += "Copper coin: " + str(floor(amount/0.1)) + "\n" + "Silver coin: " + str(amount) + "\n" + "Electrum coin: " + str(floor(amount/5)) + "\n" + "Gold coin: " + str(floor(amount/10)) + "\n" + "Platinum coin: " + str(floor(amount/100))
            elif(currency == "ep" or currency == "electrum"):
                answer += "Copper coin: " + str(floor(amount/0.02)) + "\n" + "Silver coin: " + str(floor(amount/0.5)) + "\n" + "Electrum coin: " + str(amount) + "\n" + "Gold coin: " + str(floor(amount/2)) + "\n" + "Platinum coin: " + str(floor(amount/20))
            elif(currency == "gp" or currency == "gold"):
                answer += "Copper coin: " + str(floor(amount/0.01)) + "\n" + "Silver coin: " + str(floor(amount/0.10)) + "\n" + "Electrum coin: " + str(floor(amount/0.5)) + "\n" + "Gold coin: " + str(amount) + "\n" + "Platinum coin: " + str(floor(amount/10))
            elif(currency == "pp" or currency == "platinum"):
                answer += "Copper coin: " + str(floor(amount/0.001)) + "\n" + "Silver coin: " + str(floor(amount/0.01)) + "\n" + "Electrum coin: " + str(floor(amount/0.05)) + "\n" + "Gold coin: " + str(floor(amount/0.1)) + "\n" + "Platinum coin: " + str(amount)
            await message.channel.send(answer)
        if message.content.startswith('$info'):
            text = message.content
            text = text.split()
            if text[1] == "weapon":
                weap = weapons_data.oneDictToRuleThemAll[text[2].lower().replace(' ', '').replace(',', '')]
                await message.channel.send("⚔️    " + weap["name"] + "    🏹\nDamage: " + weap["damagetype"] + "\nPrice: " + weap["price"] + "\nWeight: " + weap["weight"])
            elif text[1] == "monster":
                if len(text) > 2:
                    text[2] += text[3]
                monstername = text[2].lower().replace(' ', '').replace(',', '').replace('/', '').replace('-', '').replace('\'', '')
                try:
                    monst = monsters_data.MonstersFirstHalf[monstername]
                    await message.channel.send("🧟‍♂️    " + monst["name"] + "    🐉" + "\nType: " + monst["type"] + "\nAlignment: " + monst["alignment"] + "\nSize: " + monst["size"] + "\nChallange Rating: " + monst["cr"] + "\nArmor Class: " + monst["ac"] + "\nHit Points: " + monst["hp"] + "\nSpellcaster: " + monst["spellcaster"] + "\nEnvironment: " + monst["environment"] + "\nBook: " + monst["book"] + "\nPage: " + monst["page"])
                except KeyError:
                    try:
                        monst = monsters_data.MonstersSecondHalf[monstername]
                        await message.channel.send("Found")
                    except KeyError:
                        await message.channel.send("Seems like I can't find it in my archive")
            elif text[1] == "spell":
                spellname = text[2].lower().replace(' ', '').replace('\'', '').replace('/', '').replace('-', '')
                spl = spells_data.oneDictToRuleThemAll[spellname]
                await message.channel.send("🔮    " + spl["name"] + "    🪔" + "\nLevel:" + spl["level"] + "\nSchool: " + spl["school"] + "\nCasting time: " + spl["castingtime"] + "\nComponents: " + spl["components"] + "\nSource: " + spl["source"])
            else:
                await message.channel.send("Sorry. This feature will be available later !")
                 
client = MyClient()

client.run('TOKEN')
