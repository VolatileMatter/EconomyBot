import discord
import random
import operator
from discord.ext import commands

client = discord.Client()
bot = commands.Bot(command_prefix='=', description='A real, sustainable economy for your server')
isbet = False

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
#h is the number of people in the economy. 
w, h = 4, 14
Matrix = [[0 for x in range(w)] for y in range(h)]

#Basic Commands
@bot.command()
async def hello():
    """Basic command to check that the bot is on and responding."""
    await bot.say("Hello, World!")
        
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
    
@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

#personal methods
def getStarted():
    started = False
    xi = 0
    with open('testfile.txt') as fp:
        for line in fp:
            if(started and xi < h):
                #print(line)
                for a in range(0,w):
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

def setValue(whose, amt):
    Matrix[getIndex(whose)][2] = amt

def last():
    ansa = 0
    for x in range(0,9):
        if str(Matrix[x][0]) == str(0):
            ansa = x
            break
    return ansa

def getIndex(un):
    return find(un, Matrix)
        
def find(who, what,col=0):
    for x in range(0,h):
        if str(what[x][col]) == str(who):
            return x
def isfind(who, what,col=0):
    for x in range(0,h):
        if str(what[x][col]) == str(who):
            return True

def saveBot():
    global Matrix
    with open("testfile.txt","w") as file:
    #file = open("testfile.txt","a")  
        file.write("$$DATA_STARTS$$\n")
        for x in range(0,h):
            file.write(str(Matrix[x][0])+"$")
            file.write(str(Matrix[x][1])+"$")
            file.write(str(Matrix[x][2])+"$")
            file.write(str(Matrix[x][3])+"$\n")

def checkOwner(who):
    #if manage_server(who) == True:
        #return True
    if str(who) == "VolatileMatter#5451":
        return True
    else:
        return False
    
def existsIn(thing, what):
    for x in range(0,len(what)):
        if what[x] == thing:
            print("x: "+str(x)+", "+what[x])
            return True
    

#File Commands
@bot.command()
async def close():
    """Closes the file. This should only be used if the file is giving you issues."""
    file.close()
    await bot.say("Closed the file.")
    
@bot.command(name='save')
async def _save():
    """Used to save the current matrix to the .txt file."""
    saveBot()
    await bot.say("Saved the file.")

@bot.command(pass_context=True, name='start')
async def _start(ctxt):
    """Used to read the text file into the matrix."""
    if checkOwner('{0.message.author}'.format(ctxt)):
        getStarted()
            
    
#Money Commands
@bot.command(pass_context=True)
async def buy(ctxt, user:discord.Member, amt):
    """Used to buy someone."""
    buyer = ('{0.message.author}'.format(ctxt))
    waifu = ('{}'.format(user))
    if int(amt) >= int(getValue(waifu)) and int(amt) <= int(getMoney(buyer)):
        if buyer != waifu:
            setOwner(buyer, waifu)
            changeMoney(buyer, 0-int(amt))
            changeMoney(waifu, amt)
            setValue(waifu, int(getValue(waifu))+int(amt))
            await bot.say("Congrats, you've bought "+waifu+" for "+str(amt))
    else:
        await bot.say("You either don't have enough money, or the waifu is worth more than that.")
    saveBot()
    
@bot.command()
async def all():
    """Shows info about all users."""
    ans = ""
    for x in range(0,h):
         ans += "**"+str(Matrix[x][0])+"** has $"+str(Matrix[x][1])+", is worth $"+str(Matrix[x][2])+", and is owned by "+str(Matrix[x][3])+"\n"
         #await bot.say(Matrix[x][0])
    await bot.say(ans)
    
@bot.command()
async def lb():
    """Actual leaderboard, ranking people by worth."""
    ans = "__**Worth:**__\n"
    global Matrix
    tempmat = Matrix
    temp = [0 for x in range(h)]
    for x in range(h):
        temp[x] = int(tempmat[x][2])
    for x in range(h):
        tempmat[x][2] = int(temp[x])
    tempmat = sorted(tempmat, key=operator.itemgetter(2), reverse=True)
    for n in range(h):
        if(tempmat[n][0] != str(0)):
            ans += "**"+tempmat[n][0]+"** is worth $"+str(tempmat[n][2])+".\n"
    await bot.say(ans)
    await bot.say("\n\n __**Number of Waifus Owned:**__\n")
    temp = [[0 for x in range(2)] for y in range(h)]
    for n in range(h):
        temp[n][0] = Matrix[n][0]
    for x in range(0,h):
        for n in range(0,h):
            if Matrix[x][3] == str(temp[n][0]):
                temp[n][1] += 1
    #await bot.say(temp)
    temp = sorted(temp, key=operator.itemgetter(1), reverse=True)
    ans = ""
    for n in range(h):
        if(temp[n][0] != str(0)):
            ans += "**"+temp[n][0]+"** owns "+str(temp[n][1])+" waifus.\n"
    await bot.say(ans)
    
        
@bot.command(pass_context=True)
async def me(ctxt):
    """Tells you about the author in the economy"""
    global Matrix
    who = ('{0.message.author}'.format(ctxt))
    await bot.say("You have $"+str(getMoney(who))+" and are worth $"+str(getValue(who)))
    ans = "__**Waifus:**__\n"
    for n in range(0,h):
        if Matrix[n][3] == who:
            ans += Matrix[n][0]+"\n"
    await bot.say(ans)

@bot.command(pass_context=True)
async def info(ctxt, user:discord.Member):
    """Tells you about the pinged player in the economy"""
    who = ('{}'.format(user))
    await bot.say(who+" has $"+str(getMoney(who))+" and is worth $"+str(getValue(who)))
    ans = "__**Waifus:**__\n"
    for n in range(0,h):
        if Matrix[n][3] == who:
            ans += Matrix[n][0]+"\n"
            
@bot.command(pass_context=True)
async def give(ctxt, amt, user:discord.Member):
    """Used to trade money between players."""
    if(amt > 0):
        changeMoney(('{}'.format(user)), amt)
        changeMoney(('{0.message.author}'.format(ctxt)), 0 - int(amt))
        await bot.say("Moved "+str(amt)+" from "+('{0.message.author}'.format(ctxt))+" to "+('{}'.format(user)))
    else:
        await bot.say("Lol you can't give negative money.")
    saveBot()

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
    saveBot()

@bot.command(pass_context=True)
async def award(ctxt, amt, user:discord.Member):
    """Used to award free money to players. Entering a negative amount will take money."""
    if checkOwner('{0.message.author}'.format(ctxt)):
        changeMoney(('{}'.format(user)), amt)
        await bot.say("Gave "+str(amt)+" to "+('{}'.format(user)))
        saveBot()
    
    
#betting commands
class bet(object):
    """Used to start up a bet. Winnings will be evenly divided amongst the winners."""
    bets =  [[0 for x in range(3)] for y in range(h)]
    options = [0 for x in range(1)]
    pot = 0
    lasta = 0
    owner = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, owner, opt):
        self.owner = owner
        self.options = [0 for x in range(len(opt))]
        for x in range(0,len(opt)):
            self.options[x] = opt[x]
    
    def addBet(self, who, amt, opt):
        self.bets[self.lasta][0] = who
        self.bets[self.lasta][1] = amt
        self.bets[self.lasta][2] = opt
        self.lasta += 1
        print("added bet: "+who+", "+str(amt)+", "+str(opt))
        
    def getNumOpt(self):
        return len(self.options)
    
    def getBet(self, who):
        print (self.bets)
        return self.bets[find(who, self.bets)][1]
    def getOptions(self):
        return self.options
    
    def getChoices(self):
        ans = ""
        for x in range(0,len(self.options)):
            ans = str(ans) + str(self.options[x])+", "
        return ans
    def getOwner(self):
        return self.owner
    def getPot(self):
        ans = 0
        for x in range(len(self.bets)):
            ans += int(self.bets[x][1])
        return ans
    def getBets(self):
        return self.bets
    
current = bet("test", [0 for x in range(w)])

@bot.command(pass_context=True)
async def startbet(ctxt, *choices : str):
    """Launches a bet. Can only be ended by the person who started it. Betting options are seperated by spaces"""
    global isbet
    global current
    if len(choices) > 1:
        if not isbet:
            current = bet('{0.message.author}'.format(ctxt), choices)
            await bot.say("A bet has been started by "+current.getOwner()+". The current options are: "+current.getChoices())
            isbet = True
        else:
            await bot.say("There's already a bet going! End that one first!")
    else:
        await bot.say("You must have at least two options in your bet.")

@bot.command(pass_context=True, name='bet')
async def _bet(ctxt, opt, amt):
    """Contribute your bet to the currently running bet."""
    global current
    who = ('{0.message.author}'.format(ctxt))
    print("Option: "+str(opt))
    print("Amt: "+str(amt))
    print (current.getOptions())
    found = True
    if(existsIn(opt, current.getOptions())):
        if not amt.isdigit():
            await bot.say("Your bet must be in digit form, without a $")
            found = False
        if not int(amt) <= int(getMoney(who)):
            await bot.say("You don't have enough money! Your bet of "+str(amt)+" is larger than your wallet of "+str(getMoney(who))+"!")
            found = False
        if found:
             current.addBet(who, amt, opt)
             await bot.say(who+" has added their bet of **$"+str(current.getBet(who))+"** on **"+str(opt)+"** to the pot!")
             changeMoney(who, int(0 - int(amt)))
    else:
        await bot.say("Your bet must be on one of the options.")

@bot.command()
async def pot():
    """The current amount of money in the pot."""
    await bot.say(current.getPot())
    
@bot.command()
async def getChoices():
    """gets all of the options current available to bet on"""
    global current
    await bot.say(current.getChoices())

@bot.command()
async def getbets():
    """gets all of the bets currently placed."""
    global current
    await bot.say(current.getBets())
    
@bot.command(pass_context=True)
async def endbet(ctxt, win=""):
    """Ends the bet and distributes the winnings equally to the winners."""
    global current
    go = True
    who = ('{0.message.author}'.format(ctxt))
    global Matrix
    global isbet
    winners = [0 for x in range(h)]
    numwin = 0
    any = False
    
    if not isbet:
        await bot.say("There's no bet going right now. Start a bet before you end one.")
        go = False
    if win == "" and go:
        await bot.say("You must put in a winning option.")
        go = False
    if not existsIn(win, current.getOptions()) and go:
        await bot.say("Your winning option must be a given option.")
        go = False 
    if who != current.getOwner() and go:
        await bot.say("Only "+current.getOwner()+" can end the bet.")
        go = False
    for x in range(current.getNumOpt()):
        if (current.getBets())[x][2] == win:
            numwin += 1
            winners[x] = (current.getBets())[x][0]
            any = True
    if not any and go:
        await bot.say("Nobody bet anything on that option. Ending the bet and releasing the money to the void.")
        isbet = False
        go = False
    if go:
        toeach = current.getPot()/numwin
        for n in range(0,len(winners)):
            for r in range(0,h):
                if Matrix[r][0] == winners[n]:
                    changeMoney(winners[n], toeach)
                    await bot.say("Gave $"+str(toeach)+" to "+winners[n])
        isbet = False
        await bot.say("Success! Awarded the money to the winners.")
    
    
bot.run('MzM0MTMyMjI0NDQ4Mzk3MzEy.DEWxDw.wYXjtzelFKzaWImBJN6pN1L-3U4')