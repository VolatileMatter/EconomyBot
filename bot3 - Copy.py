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

#this is the matrix used while the program is running to store information.
#Matrix[x][0] = Username
#Matrix[x][1] = Money they have
#Matrix[x][2] = How much they cost to buy; their "worth"
w, h = 3, 9
Matrix = [[0 for x in range(w)] for y in range(h)]
last = 0

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
            file.write(str(Matrix[x][2])+"$\n")
        await bot.say("Saved the file.")

@bot.command(name='start')
async def _start():
    """Used to read the text file into the matrix."""
    started = False
    xi = 0
    with open('testfile.txt') as fp:
        for line in fp:
            if(started and xi < h):
                print(line)
                Matrix[xi][0] = line.split("$")[0]
                Matrix[xi][1] = line.split("$")[1]
                Matrix[xi][2] = line.split("$")[2]
                xi+=1
            if (str(line) == "$$DATA_STARTS$$\n"):
                print("Found the start!")
                await bot.say("Found the start!")
                started = True
            
    
#Money Commands
@bot.command()
async def lb():
    """Leaderboard command, showing all of the people in the economy and their money."""
    ans = ""
    for x in range(0,h):
         ans += "**"+str(Matrix[x][0])+"** has $"+str(Matrix[x][1])+" and is worth $"+str(Matrix[x][2])+".\n"
         #await bot.say(Matrix[x][0])
    await bot.say(ans)
        
@bot.command(pass_context=True)
async def m(ctxt):
    """Tells you how much money the author has."""
    for x in range(0,h):
        if Matrix[x][0] == ('{0.message.author}'.format(ctxt)):
            await bot.say(Matrix[x][1])
            
@bot.command(pass_context=True)
async def give(ctxt, amt, user:discord.Member):
    """Used to trade money between players. Usage is =give AMOUNT @USERTORECEIVE"""
    for x in range(0,h):
        if Matrix[x][0] == ('{0.message.author}'.format(ctxt)):
            Matrix[x][1] -= int(amt)
    for x in range(0,h):
        if Matrix[x][0] == ('{}'.format(user)):
            Matrix[x][1] += int(amt)
    await bot.say("Moved "+str(amt)+" from "+('{0.message.author}'.format(ctxt))+" to "+('{}'.format(user)))

@bot.command(pass_context=True)
async def join(ctxt):
    """Adds the author to the economy. Everyone starts with $1000 and a value of $1."""
    exists = True
    global last
    for x in range(0,9):
        if Matrix[x][0] == ('{0.message.author}'.format(ctxt)):
            exists = False 
        if Matrix[x][0] == 0:
            last = x
            break
    if(exists):
        Matrix[last][0] = ('{0.message.author}'.format(ctxt))
        Matrix[last][1] = 1000
        Matrix[last][2] = 1
        last += 1
    await bot.say("Welcome to the economy, {0.message.author}!".format(ctxt))
    #file.write("\n{0.message.author} has joined the economy.".format(ctxt))
    #await bot.say("{0.message.author} has joined the economy.".format(ctxt))

@bot.command(pass_context=True)
async def award(ctxt, amt, user:discord.Member):
    """Used to award free money to players. Usage is =give AMOUNT @USERTORECEIVE"""
    for x in range(0,h):
        if Matrix[x][0] == ('{}'.format(user)):
            Matrix[x][1] += int(amt)
    await bot.say("Gave "+str(amt)+" to "+('{}'.format(user)))
    
bot.run('MzM0MTMyMjI0NDQ4Mzk3MzEy.DEWxDw.wYXjtzelFKzaWImBJN6pN1L-3U4')