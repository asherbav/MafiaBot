import discord
import random
import asyncio

client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

i = 0
userNumDict = {}
namesDict = {}
aliveDict = {}

rolesDict = {}
mafiaDict = {}
gangDict = {}

pidList = []
rolesList = []
aliveList = []

killKey = -1
saveKey = -1
attackKey = -1

numMafia = 1
numNurse = 1
numDetect = 1
numVig = 0

vigKill = 0
numResponses = 0
numActiveRoles = 0


@client.event
async def on_message(message):
    global i
    global killKey
    global saveKey
    global attackKey
    
    global numMafia
    global numNurse
    global numDetect
    global numVig
    
    global vigKill
    global numResponses
    global numActiveRoles
    
    print(message.content)
    
    if message.author == client.user:
        return
    
            
    # List of commands
    if message.content.startswith('!help'):
        await message.channel.send("Pre-start: \n" + \
            "---------------------------------------------- \n" + \
            "'!join' to join the council \n" + \
            "'!assign' to assign roles \n" + \
            "'!setMaf #' to assign number of mafia \n" + \
            "'!setNur #' to assign number of nurses \n" + \
            "'!setDet #' to assign number of detectives \n" + \
            "'!setVig #' to assign number of vigilantes \n" + \
            "\n" + \
            "Council Actions: \n" + \
            "---------------------------------------------- \n" + \
            "'!start' to begin the first night \n " + \
            "'!day' to begin the council meeting \n " + \
            "'!night' to begin night activities \n " + \
            "'!list' to see list of those alive \n " + \
            "'!execute' to force an execution during a council meeting \n " + \
            "'!end' to reset game settings \n" + \
            "\n" + \
            "Role-specific Actions: \n" + \
            "---------------------------------------------- \n" + \
            "'!list' to see list of those alive \n " + \
            "'!kill #' to injure your target (Mafia ) \n " + \
            "'!attack #' to assault your target (Vigilante) \n " + \
            "'!save #' to protect your target (Nurse) \n " + \
            "'!inspect #' to check if your target is mafia (Detective) \n " + \
            "'!skip' to send a vote for no one ")
    
    # Adds council member
    if message.content.startswith('!join') and message.author.id not in userNumDict.values():
        await message.channel.send(f"{message.author} has joined the council")
        userNumDict[i]= message.author.id
        print(f"user dictionary is: {userNumDict}")
        namesDict[i] = message.author.name
        print(f"names dictionary is: {namesDict}")
        aliveDict[i] =True
        print(f"alive dictionary is: {aliveDict}")
        pidList.append(i)
        print(f"pid list is: {pidList}")
        i+=1
    
    # Set number of mafia members
    if message.content.startswith('!setMaf'):
        mafiaString = message.content
        numMafia = int(mafiaString[8:])
        await message.channel.send(f"number of mafia is: {numMafia}")
        
    # Set number of nurses
    if message.content.startswith('!setNur'):
        nurseString = message.content
        numNurse = int(nurseString[8:])
        await message.channel.send(f"number of nurses is: {numNurse}")
    
    # Set number of nurses
    if message.content.startswith('!setDet'):
        detectString = message.content
        numDetect = int(detectString[8:])
        await message.channel.send(f"number of detectives is: {numDetect}")
    
    # Set number of vigilante
    if message.content.startswith('!setVig'):
        vigString = message.content
        numVig = int(vigString[8:])
        await message.channel.send(f"number of vigilante is: {numVig}")
    
    # Assign roles to party members
    if message.content.startswith('!assign'):
        rolesDict.clear()
        mafiaDict.clear()
        gangDict.clear()
        
        rolesList.clear()
        
        #Adding mafia, vigilante(s), and citizens to roles list
        for n in range(numMafia):
            rolesList.append("mafia")
        for n in range(numNurse):
            rolesList.append("nurse")
        for n in range(numDetect):
            rolesList.append("detective")
        for n in range(numVig):
            rolesList.append("vigilante")
            
        while len(rolesList) < len(pidList):
            rolesList.append("citizen")    
            
        print(rolesList)

        #Creating randomized dictionary with pid,role and pid, mafia-status pairs
        for j in range(len(pidList)):
            rolesDict[j] = rolesList.pop(random.randint(0,len(rolesList)-1))
            
            if rolesDict[j] != 'citizen':
                numActiveRoles += 1
                
            if rolesDict[j] == 'mafia':
                mafiaDict[j] = 'mafia'
                gangDict[j] = namesDict[j]
            else:
                mafiaDict[j] = 'non-mafia'
                
            user = client.get_user(userNumDict[j])
            await user.send(f"{namesDict[j]} is playing the role of {rolesDict[j]}")
            
        for k in gangDict:
            user = client.get_user(userNumDict[k])
            await user.send(f"Awaken mafia! See la famiglia: {list(gangDict.values())}")
            
        print(f"Gang members: {list(gangDict.values())}")
        print(f"role is: {rolesDict}")
        print(f"mafia-status is: {mafiaDict}")
    
    # See first night
    if message.content.startswith('!start'):
        await message.channel.send("Night 1 has begun.\n"+ \
            "------------------------------------------------------------------ \n " + \
            "Allow mafia members to use this time to DM each other. \n" + \
            "You may wish to take this time to disable Message Sounds. \n" + \
            "\n" + \
            "'!day' to begin the first council meeting. \n" + \
            "'!end' to conclude game")
            
    # Begin day event
    if message.content.startswith('!day'):
        #Insert channel id below and delete '#'
        #channel = client.get_channel(insert channel here)
        await channel.send("Day has come.\n"+ \
            "------------------------------------------------------------------ \n " + \
            "'!list' to see a list of those alive. \n " + \
            "'!execute #' to execute party member. A majority vote is required.\n" + \
            "'!night' to begin night activities. \n" + \
            "'!end' to reset game settings")
    
    # Begin night event
    if message.content.startswith('!night'):
        #Insert channel id below and delete '#'
        #channel = client.get_channel(insert channel here)
        await channel.send(f"Night has come. Actions are pending... \n" +\
            "------------------------------------------------------------------")
        
        for j in range(len(pidList)):
            if rolesDict[j] == 'mafia' and aliveDict[j] == True:
                mafia = client.get_user(userNumDict[j])
                await mafia.send(f"Who will you attack? Discuss with your fellow mafia, if any.\n" + \
                "------------------------------------------------------------------ \n " + \
                "'!list' to see a list of those alive. \n " + \
                "'!skip' to send a vote for no one. \n " + \
                "'!kill #' once a decision has been made.")
                
            elif rolesDict[j] == 'nurse' and aliveDict[j] == True:
                nurse = client.get_user(userNumDict[j])
                await nurse.send(f"Who will you save? \n" + \
                "------------------------------------------------------------------ \n " + \
                "'!list' to see a list of those alive. \n " + \
                "'!skip' to send a vote for no one. \n " + \
                "'!save #' once a decision has been made.")
            elif rolesDict[j] == 'detective' and aliveDict[j] == True:
                detective = client.get_user(userNumDict[j])
                await detective.send(f"Who will you inspect? \n" + \
                "------------------------------------------------------------------ \n " + \
                "'!list' to see a list of those alive. \n " + \
                "'!skip' to send a vote for no one. \n " + \
                "'!inspect #' once a decision has been made.")   
            elif rolesDict[j] == 'vigilante' and aliveDict[j] == True and vigKill == 0:
                detective = client.get_user(userNumDict[j])
                await detective.send(f"Who will you attack? Only one assault can be made per game.\n" + \
                "------------------------------------------------------------------ \n " + \
                "'!list' to see a list of those alive. \n " + \
                "'!skip' to send a vote for no one. \n " + \
                "'!attack #' once a decision has been made.")  
                
        
    # Display unique ID's assigned to each user
    if message.content.startswith('!userNumDict'):
        print(userNumDict)
    
    # Display list of living players
    if message.content.startswith('!list'):
        await message.channel.send("Those alive:")
        for j in range(len(pidList)): 
            if aliveDict[j] == True:
                await message.channel.send(f"{j} - {namesDict[j]}")
                
    # Testing direct message functionality   
    if message.content == '!dm':
        user = client.get_user(message.author.id)
        await user.send('Test dm')
    
    # Kill off player without vote 
    if message.content.startswith('!execute'): 
        executeString = message.content
        executeKey = int(executeString[9:])
        if executeKey not in aliveDict.keys():
            await message.channel.send("Invalid target. ")
        else:
            aliveDict[executeKey] = False
            if rolesDict[executeKey] != 'citizen':
                numActiveRoles -= 1
            # Insert channel below and delete '#'    
            #channel = client.get_channel(insert channel here)
            await channel.send(f"{namesDict[executeKey]} has been executed.")
    
    # Mafia action: Attempt an attack on specified target
    if message.content.startswith('!kill'):
        killString = message.content
        killKey = int(killString[6:])
        if aliveDict[killKey] == False:
            await message.channel.send("Invalid target. ")
        else:
            numResponses +=1
            await message.channel.send(f"{namesDict[killKey]} has been injured")

    # Vigilante action: Attempt an attack on specified target
    if message.content.startswith('!attack'):
        attackString = message.content
        attackKey = int(attackString[8:])
        if aliveDict[attackKey] == False:
            await message.channel.send("Invalid target. ")
        elif vigKill == 0:
            numResponses +=1
            vigKill = 1
            await message.channel.send(f"{namesDict[attackKey]} has been injured")
            
        else:
            await message.channel.send(f"The vigilante can no longer act.")
    
    # Nurse action: Attempt to save specified target
    if message.content.startswith('!save'):
        saveString = message.content
        saveKey = int(saveString[6:])     
        if aliveDict[saveKey] == False:
            await message.channel.send("Invalid target. ")
        else:
            numResponses +=1
            await message.channel.send(f"{namesDict[saveKey]} is under your protection")
  
    # Detective action: Attempt to inspect specified target
    if message.content.startswith('!inspect'):
        inspectString = message.content
        inspectKey = int(inspectString[9:])    
        if aliveDict[inspectKey] == False:
            await message.channel.send("Invalid target. ")
        else:
            numResponses +=1
            await message.channel.send(f"{namesDict[inspectKey]} is {mafiaDict[inspectKey]}")
 
    # Night event action: Perform no action for the night
    if message.content.startswith('!skip'):
        numResponses += 1
        await message.channel.send(f"No action made for the night")
    
    # Display all roles, revealing mafia members 
    if message.content.startswith('!reveal'):
        await message.channel.send("# - Name: Role")
        for i in range(len(pidList)):
            await message.channel.send(str(pidList[i]) + " - " + str(namesDict[pidList[i]]) + ": " + str(rolesDict[pidList[i]]))

    # Verify whether somebody has been killed by comparing kill key and save key 
    if numResponses == numActiveRoles and numActiveRoles != 0: 
        print("killKey is: " + str(killKey))
        print(f"saveKey is {saveKey}")
        print(aliveDict.keys())
        
        # Insert channel below and delete '#'
        #channel = client.get_channel( insert channel here)
        
        #On Vigilante kill
        if attackKey != saveKey and attackKey in aliveDict.keys():
            aliveDict[attackKey] = False
            if rolesDict[attackKey] != 'citizen':
                numActiveRoles -= 1
            await channel.send(f"{namesDict[attackKey]} has been murdered. \n " + \
                "------------------------------------------------------------------ \n ")
            numActiveRoles -=1
        
        #On Mafia kill
        if killKey != saveKey and killKey != attackKey and killKey in aliveDict.keys():
            aliveDict[killKey] = False
            if rolesDict[killKey] != 'citizen':
                numActiveRoles -= 1
            await channel.send(f"{namesDict[killKey]} has been murdered. \n " + \
                "------------------------------------------------------------------ \n ")
        else:
            await channel.send("No one has died. \n" + \
                "------------------------------------------------------------------ \n ")
            
        await channel.send("Night has concluded. \n"+ \
            "------------------------------------------------------------------ \n " + \
            "'!day' to begin council meeting. \n"+ \
            "'!end' to conclude game")
                  
        attackKey = -1
        killKey = -1
        saveKey = -1
        numResponses = 0
    #Reset game state    
    if message.content.startswith('!end'):
        i = 0
        killKey = -1
        saveKey = -1
        attackKey = -1

        numMafia = 1
        numNurse = 1
        numDetect = 1
        numVig = 0

        vigKill = 0
        numResponses = 0
        numActiveRoles = 0
        
        userNumDict.clear()
        namesDict.clear()
        aliveDict.clear()

        rolesDict.clear()
        mafiaDict.clear()
        gangDict.clear()
        
        pidList.clear()
        rolesList.clear()
        aliveList.clear()
        
        # Insert channel below and delete '#'
        # channel = client.get_channel( insert channel here)
        await channel.send(f"The game has concluded. All settings have been reset.")
    
           
    #if message.content.startswith('!nurse'):
     #   await user.create_dm(user)
      #  await user.dm_channel.send('The spiciest role in the game: The Nurse')


#Insert token below and delete '#'
# client.run( insert token here)