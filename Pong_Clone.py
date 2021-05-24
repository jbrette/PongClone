#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Orginally based upon the 'Python Game Tutorial: Pong' video tutorial by freeCodeCamp.org


# In[2]:


import turtle #Used for simple games in python
import random
import os


# In[3]:


#Generates the game window
def genGameWindow():
    gameWindow = turtle.Screen()
    gameWindow.title('Pong Clone by Maxence Brette') #Title
    gameWindow.bgcolor('black') #Background color
    gameWindow.setup(width = 800, height = 600) #Screen size
    gameWindow.tracer(0) #Prevents automatic updates
    
    return gameWindow


# In[4]:


#Generates interactive game objects
def genObject(speed, shape, stretchW, stretchL, color, startX, startY):
    gameObject = turtle.Turtle()
    gameObject.speed(speed) #Animation Speed
    gameObject.shape(shape)
    gameObject.shapesize(stretch_wid = stretchW, stretch_len = stretchL)
    gameObject.color(color)
    gameObject.penup()
    gameObject.goto(startX, startY) #Starting Position
    
    return gameObject


# In[5]:


#Generates in game text
def genText(speed, color, xCor, yCor, text, alignment, textFont):
    gameText = turtle.Turtle()
    gameText.speed(speed)
    gameText.color(color)
    gameText.penup()
    gameText.hideturtle()
    gameText.goto(xCor, yCor)
    gameText.write(text, align = alignment, font = textFont)
    
    return gameText


# In[6]:


#Changes the scoreboard player names according to whether or not it is PVP or PVE
def setScoreNames():
    player1 = 1
    player2 = 2
    if (numPlayers < 2):
        player2 = 0
    if (numPlayers == 0):
        player1 = 0
    playerNames = [player1, player2]    
    return(playerNames)


# In[7]:


#Determines Paddle Movements
#Currently not working due to some strage interaction with onkeypress method
def paddleMovement(tappedKey):
    if (tappedKey == 'w' or tappedKey == 's'):
        global paddleA
        y = paddleA.ycor()
        
        if (tappedKey == 'w'):
            y += 50
        else:
            y -= 50
        
        paddleA.sety(y)
    
    if (tappedKey == 'Up' or tappedKey == 'Down'):
        global paddleB
        y = paddleB.ycor()
        
        if (tappedKey == 'Up'):
            y += 50
        else:
            y -= 50
        
        paddleB.sety(y)
        
def paddleAUp():
    paddleMovement('w')
    
def paddleADown():
    paddleMovement('s')
    
def paddleBUp():
    paddleMovement('Up')
    
def paddleBDown():
    paddleMovement('Down')


# In[8]:


#Determines Ball Movement Speed
def setBallSpeed(speed):
    ball.dx = speed #Movement on x-axis
    ball.dy = speed #Movement on y-axis


# In[9]:


#Limits the Ball Movement Speed to Resonable Levels
def limitBallSpeed():
    global ball
    if (abs(ball.dx) > 3):
        ball.dx = 3
        if (ball.dx > 0):
            ball.dx *= random.uniform(0.25, 1)
        if (ball.dx < 0):
            ball.dx *= (-1 * random.uniform(0.25, 1))
    
    if (abs(ball.dy) > 3):
        ball.dy = 3
        if (ball.dy > 0):
            ball.dy *= random.uniform(0.25, 1)
        if (ball.dy < 0):
            ball.dy *= (-1 * random.uniform(0.25, 1))
    
    if (abs(ball.dx) < 0.75):
        ball.dx = 0.75
        if (ball.dx > 0):
            ball.dx *= random.uniform(1, 4)
        if (ball.dx < 0):
            ball.dx *= (-1 * random.uniform(1, 4))
    
    if (abs(ball.dy) < 0.75):
        ball.dy = 0.75
        if (ball.dy > 0):
            ball.dy *= random.uniform(1, 4)
        if (ball.dy < 0):
            ball.dy *= (-1 * random.uniform(1, 4))
    


# In[10]:


#Makes the ball move
def moveBall():
    global ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)


# In[11]:


def randomizeBallServe():
    global ball
    ball.dy *= random.uniform(-1, 1)


# In[12]:


#Screen Border Checking
def borderChecking():
    global ball
    global score1
    global score2
    
    yCorBall = ball.ycor()
    xCorBall = ball.xcor()
    
    if (yCorBall > 290 or yCorBall < -290):
        if (yCorBall > 290): #Top Screen Border
            ball.sety(290)

        if (yCorBall < -290): #Bottom Screen Border
            ball.sety(-290)
        
        ball.dy *= -1
    
    if (xCorBall > 390 or xCorBall < -390):
        if (xCorBall > 390): #Right Screen Border
            ball.setx(390)
            score1 += 1
            setBallSpeed(-1 * defaultBallSpeed)

        if (xCorBall < -390): #Left Screen Border
            ball.setx(-390)
            score2 += 1
            setBallSpeed(defaultBallSpeed)
        
        os.system('afplay AirPlaneDing.mp3&')
        
        ball.goto(0, 0)
        randomizeBallServe()
        
        sb.clear()
        sb.write('Player {}: {}  Player {}: {}'.format(setScoreNames()[0], score1, setScoreNames()[1], score2), 
                 align = 'center', font = ('Courier', 24, 'normal'))
        
    limitBallSpeed()


# In[13]:


#Determines Paddle & Ball Collisions
def paddleBallCollision():
    global ball
    yCorBall = ball.ycor()
    xCorBall = ball.xcor()
    
    #Right Paddle
    if ((xCorBall > 340) and (xCorBall < 350) and
        ((yCorBall < paddleB.ycor() + 50) and (yCorBall > paddleB.ycor() - 50))):
        ball.setx(340)
        ball.dx *= -1
        randomizeBallServe()
        
        os.system('afplay ButtonClickOff.mp3&')
        
    #Left Paddle
    if ((xCorBall < -340) and (xCorBall > -350) and
        
        ((yCorBall < paddleA.ycor() + 50) and (yCorBall > paddleA.ycor() - 50))):
        ball.setx(-340)
        ball.dx *= -1
        randomizeBallServe()
        
        os.system('afplay ButtonClickOn.mp3&')
        
    limitBallSpeed()


# In[14]:


def pauseGame():
    global pause
    if (pause == True):
        pause = False
    else:
        pause = True


# In[15]:


#Allows players to end and quit the game without errors
def exitGame():
    global running 
    running = False


# In[16]:


#Creates a Very Simple Player 0 AI
def opponentAI():
    global numPlayers
    
    global ball
    yCorBall = ball.ycor()
    
    global paddleB
    yCorPB = paddleB.ycor()
    
    global paddleA
    yCorPA = paddleA.ycor()
    
    if (yCorBall > (yCorPB + 50)):
        paddleBUp()
    
    if (yCorBall < (yCorPB - 50)):
        paddleBDown()
        
    if (numPlayers == 0):
        if (yCorBall > (yCorPA + 50)):
            paddleAUp()
    
        if (yCorBall < (yCorPA - 50)):
            paddleADown()


# In[17]:


#Initiates the game environment
gameWindow = genGameWindow()
running = True
pause = False


# In[18]:


#Main Menu
playerCount = genText(0, 'white', 0, 0, 'How many players?\nPress: "0", "1" or "2"', 
                      'center', ('Courier', 24, 'normal'))

numPlayers = gameWindow.numinput('PlayerCountSelection', 'How many players? ', 1, minval = 0, maxval = 2)
playerCount.clear()


# In[19]:


#Sets up the game environment    
#Generates the Playing Field Divider
playingFieldDivider = genObject(0, 'square', 30, 0.1, 'white', 0, 0)


#Generates the Paddles
#Left Paddle A
paddleA = genObject(0, 'square', 5, 1, 'white', -350, 0)

#Right Paddle B
paddleB = genObject(0, 'square', 5, 1, 'white', 350, 0)


#Generates the Ball
#Ball
ball = genObject(0, 'square', 1, 1, 'white', 0, 0)
defaultBallSpeed = 1.5
setBallSpeed(defaultBallSpeed)


#Scoreboard & Scoring
#Starting Players & Scores
score1 = 0
score2 = 0

#Scoreboard
sb = genText(0, 'white', 0, 260, 
             'Player {}: {}  Player {}: {}'.format(setScoreNames()[0], score1, setScoreNames()[1], score2), 
             'center', ('Courier', 24, 'normal'))

#Player Controls Instructions
controls = genText(0, 'white', 0, 250, 'Up: "w" Down: "q"    Up: "\u2191" Down: "\u2193"', 
                   'center', ('Courier', 10, 'normal'))

#Exiting the Game Instructions
exitInstructions = genText(0, 'white', 0, -280, '  To exit the game press: "q"', 
                           'left', ('Courier', 10, 'normal'))

#Pausing the Game Instructions
exitInstructions = genText(0, 'white', 0, -280, 'To pause the game press: "p"  ', 
                           'right', ('Courier', 10, 'normal'))


# In[20]:


#Keyboard Binding
gameWindow.listen()


#Player 1
if (numPlayers == 1 or numPlayers == 2):
    gameWindow.onkeypress(paddleAUp, 'w')
    gameWindow.onkeypress(paddleADown, 's')

#Player 2
if (numPlayers == 2):
    gameWindow.onkeypress(paddleBUp, 'Up')
    gameWindow.onkeypress(paddleBDown, 'Down')

#Pauses the Game
gameWindow.onkeypress(pauseGame, 'p')

#Stop the Game Executing and Exit
gameWindow.onkeypress(exitGame, 'q')


# In[21]:


#Main Game Loop
while (running):
    
    if (pause == False):
        moveBall()
        borderChecking()
        paddleBallCollision()

        if (numPlayers < 2):
            opponentAI()

    gameWindow.update()


# In[22]:


turtle.done()

