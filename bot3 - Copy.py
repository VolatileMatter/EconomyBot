import discord
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix='=', description='A real, sustainable economy for your server')

file = open("testfile.txt","a")  
print("Opened File")

#show when it connects to discord
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    getStarted()

#this is the matrix used while the program is running to store information.
#Matrix[x][0] = Username
#Matrix[x][1] = Money they have
#Matrix[x][2] = How much they cost to buy; their "worth"
#Matrix[x][3] = Who owns them
w, h = 4, 9
Matrix = [[0 for x in range(w)] for y in range(h)]

#Basic Commands
@bot.command()
async def hello():
    """Basic command to check that the bot is on and responding."""
    await bot.say("Hello World!")
        
@bot.command(pass_context=True)
async def whoami(ctxt):
    """Tells you what your username is; this is how you are saved in the file."""
    await bot.say('You are {0.message.author}'.format(ctxt))
    
@bot.command()
async def joined(member : discord.Member):
    """Tells you when a mentioned member joined"""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))
    
@bot.command()
async def real(user:discord.Member):
    """Tells you what the real username of a mentioned user is. This is how they are saved in the file"""
    await bot.say("Their real name is {}.".format(user))

#personal methods
def getStarted():
    started = False
    xi = 0
    with open('testfile.txt') as fp:
        for line in fp:
            if(started and xi < h):
                #print(line)
                for a in range(0,w-1):
                    Matrix[xi][a] = line.split("$")[a]
                xi+=1
            if (str(line) == "$$DATA_STARTS$$\n"):
                print("Found the start!")
                #await bot.say("Found the start!")
                started = True
                
def changeMoney(whose, amt):
    Matrix[getIndex(whose)][1] = int(Matrix[getIndex(whose)][1]) + int(amt)
    
def getMoney(whose):
    return Matrix[getIndex(whose)][1]

def getValue(whose):
    return Matrix[getIndex(whose)][2]

def changeValue(whose, amt):
    Matrix[getindex(whose)][2] = int(Matrix[getindex(whose)][2]) + int(amt)
    
def getOwner(whose):
    return Matrix[getIndex(whose)][3]

def setOwner(owner, pet):
    Matrix[getIndex(pet)][3] = owner

def last():
    ansa = 0
    for x in range(0,9):
        if str(Matrix[x][0]) == str(0):
            ansa = x
            break
    return ansa

def getIndex(un):
    #used to get the x-coord of a certain username
    x = 0
    for x in range(0,h):
        if Matrix[x][0] == str(un):
            return x
    
    

#File Commands
@bot.command()
async def close():
    """Closes the file. This should only be used if the file is giving you issues."""
    file.close()
    await bot.say("Closed the file.")
    
@bot.command(name='save')
async def _save():
    """Used to save the current matrix to the .txt file."""
    with open("testfile.txt","w") as file:
    #file = open("testfile.txt","a")  
        file.write("$$DATA_STARTS$$\n")
        for x in range(0,h):
            file.write(str(Matrix[x][0])+"$")
            file.write(str(Matrix[x][1])+"$")
            file.write(str(Matrix[x][2])+"$")
            file.write(str(Matrix[x][3])+"$\n")
        await bot.say("Saved the file.")

@bot.command(name='start')
async def _start():
    """Used to read the text file into the matrix."""
    getStarted()
            
    
#Money Commands
@bot.command(pass_context=True)
async def buy(ctxt, amt, user:discord.Member):
    """Used to buy someone. Use is =buy AMOUNT @UserToBuy"""
    buyer = ('{0.message.author}'.format(ctxt))
    waifu = ('{}'.format(user))
    if int(amt) >= int(getValue(waifu)) and int(amt) <= int(getMoney(buyer)):
        if buyer != waifu:
            setOwner(buyer, waifu)
            changeMoney(buyer, 0-int(amt))
            changeMoney(waifu, amt)
            setValue(waifu, amt)
    await bot.say("Congrats, you've bought "+waifu+" for "+str(amt))
    
@bot.command()
async def lb():
    """Leaderboard command, showing all of the people in the economy and their money."""
    ans = ""
    for x in range(0,h):
         ans += "**"+str(Matrix[x][0])+"** has $"+str(Matrix[x][1])+", is worth $"+str(Matrix[x][2])+", and is owned by "+str(Matrix[x][3])+"\n"
         #await bot.say(Matrix[x][0])
    await bot.say(ans)
        
@bot.command(pass_context=True)
async def me(ctxt):
    """Tells you about the author in the economy"""
    ans = ('{0.message.author}'.format(ctxt))
    await bot.say("You have $"+str(getMoney(ans))+" and are worth $"+str(getValue(ans)))
    #await bot.say(Matrix[getIndex(('{0.message.author}'.format(ctxt)))][1])

@bot.command(pass_context=True)
async def info(ctxt, user:discord.Member):
    """Tells you about the pinged player in the economy"""
    ans = ('{}'.format(user))
    await bot.say(ans+" has $"+str(getMoney(ans))+" and is worth $"+str(getValue(ans)))
    #await bot.say(Matrix[getIndex(('{0.message.author}'.format(ctxt)))][1])
            
@bot.command(pass_context=True)
async def give(ctxt, amt, user:discord.Member):
    """Used to trade money between players. Usage is =give AMOUNT @USERTORECEIVE"""
    if(amt > 0):
        changeMoney(('{}'.format(user)), amt)
        changeMoney(('{0.message.author}'.format(ctxt)), 0 - int(amt))
        await bot.say("Moved "+str(amt)+" from "+('{0.message.author}'.format(ctxt))+" to "+('{}'.format(user)))
    else:
        await bot.say("Lol you can't give negative money.")

@bot.command(pass_context=True)
async def join(ctxt):
    """Adds the author to the economy. Everyone starts with $1000 and a value of $1."""
    notExist = True
    for x in range(0,9):
        if Matrix[x][0] == ('{0.message.author}'.format(ctxt)):
            notExist = False 
    if(notExist):
        Matrix[last()][1] = 1000
        Matrix[last()][2] = 1
        Matrix[last()][0] = ('{0.message.author}'.format(ctxt))
    await bot.say("Welcome to the economy, {0.message.author}!".format(ctxt))

@bot.command(pass_context=True)
async def award(ctxt, amt, user:discord.Member):
    """Used to award free money to players. Usage is =give AMOUNT @USERTORECEIVE. Entering a negative amount will take money."""
    changeMoney(('{}'.format(user)), amt)
    await bot.say("Gave "+str(amt)+" to "+('{}'.format(user)))
    
bot.run('token_here')