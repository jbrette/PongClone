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


#Determines Paddle Movements Inside Window
def paddleMovement(tappedKey):
    global pause
    global gameMode
    
    #Paddle A Movements
    if (pause == False): #Prevents paddle movement when the game is paused
        if (tappedKey == 'w' or tappedKey == 's' or tappedKey == 'a' or tappedKey == 'd'):
            global paddleA
            
            if (tappedKey == 'w' or tappedKey == 's'): #Up & Down
                yCorPA = paddleA.ycor()

                if (tappedKey == 'w' and yCorPA < 250):
                    yCorPA += 50
                if (tappedKey == 's' and yCorPA > -250):
                    yCorPA -= 50

                paddleA.sety(yCorPA)
            
            if (gameMode == 1):
                if (tappedKey == 'a' or tappedKey == 'd'): #Left & Right
                    xCorPA = paddleA.xcor()

                    if (tappedKey == 'a' and xCorPA > -350):
                        xCorPA -= 50
                    if (tappedKey == 'd' and xCorPA < -50):
                        xCorPA += 50

                    paddleA.setx(xCorPA)
            
        #Paddle B Movements    
        if (tappedKey == 'Up' or tappedKey == 'Down' or tappedKey == 'Left' or tappedKey == 'Right'):
            global paddleB
            
            if (tappedKey == 'Up' or tappedKey == 'Down'): #Up & Down
                yCorPB = paddleB.ycor()

                if (tappedKey == 'Up' and yCorPB < 250):
                    yCorPB += 50
                if (tappedKey == 'Down' and yCorPB > -250):
                    yCorPB -= 50

                paddleB.sety(yCorPB)
                
            if (gameMode == 1):
                if (tappedKey == 'Left' or tappedKey == 'Right'): #Left & Right
                    xCorPB = paddleB.xcor()

                    if (tappedKey == 'Left' and xCorPB > 50):
                        xCorPB -= 50
                    if (tappedKey == 'Right' and xCorPB < 350):
                        xCorPB += 50

                    paddleB.setx(xCorPB)


# In[8]:


#Called Movements by 'onkeypress'
#Paddle A
def paddleAUp():
    paddleMovement('w')
    
def paddleADown():
    paddleMovement('s')
    
def paddleALeft():
    paddleMovement('a')
    
def paddleARight():
    paddleMovement('d')

#Paddle B
def paddleBUp():
    paddleMovement('Up')
    
def paddleBDown():
    paddleMovement('Down')
    
def paddleBLeft():
    paddleMovement('Left')
    
def paddleBRight():
    paddleMovement('Right')


# In[9]:


#Determines Ball Movement Speed
def setBallSpeed(speed):
    ball.dx = speed #Movement on x-axis
    ball.dy = speed #Movement on y-axis


# In[10]:


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
    


# In[11]:


#Makes the ball move
def moveBall(bl):
    bl.setx(bl.xcor() + bl.dx)
    bl.sety(bl.ycor() + bl.dy)


# In[12]:


def randomizeBallServe():
    global ball
    ball.dy *= random.uniform(-1, 1)


# In[13]:


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


# In[14]:


#Determines Paddle & Ball Collisions
def paddleBallCollision():
    global ball
    yCorBall = ball.ycor()
    xCorBall = ball.xcor()
    
    global paddleA
    yCorPA = paddleA.ycor()
    xCorPA = paddleA.xcor()
    
    global PaddleB
    yCorPB = paddleB.ycor()
    xCorPB = paddleB.xcor()
    
    #Right Paddle
    if ((yCorBall >= yCorPB - 50 and yCorBall <= yCorPB + 50) and 
        (xCorBall >= xCorPB - 10 and xCorBall <= xCorPB + 10)):

        ball.setx(xCorPB - 10)
        ball.dx *= -1
        randomizeBallServe()
        
        os.system('afplay ButtonClickOff.mp3&')
        
    #Left Paddle
    if ((yCorBall >= yCorPA - 50 and yCorBall <= yCorPA + 50) and 
        (xCorBall <= xCorPA + 10 and xCorBall >= xCorPA - 10)):
        
        ball.setx(xCorPA + 10)
        ball.dx *= -1
        randomizeBallServe()
        
        os.system('afplay ButtonClickOn.mp3&')
        
    limitBallSpeed()


# In[15]:


def pauseGame():
    global pause
    global pauseMessage
    
    if (pause == True):
        pause = False
        pauseMessage.clear()
    else:
        pause = True
        pauseMessage = genText(0, 'white', 0, 0, '  Game  Paused', 'center', ('Courier', 24, 'normal'))


# In[16]:


#Allows players to end and quit the game without errors
def exitGame():
    global running 
    running = False


# In[17]:


#Creates a Very Simple Player 0 AI
def opponentAI(bl, pB, pA, nP, gM):

    yCorBall = bl.ycor()
    xCorBall = bl.xcor()
    
    yCorPB = pB.ycor()
    xCorPB = pB.xcor()
    
    yCorPA = pA.ycor()
    xCorPA = pA.xcor()
    
    if (yCorBall > (yCorPB + 50)):
        paddleBUp()
    
    elif (yCorBall < (yCorPB - 50)):
        paddleBDown()
    
    if (gM == 1):
        if (xCorBall > 0 and xCorBall < xCorPB - 10 and xCorBall - xCorPB < 75):
            paddleBLeft()

        elif (xCorBall > xCorPB - 10):
            paddleBRight()
        
        else:
            paddleBRight()

    if (nP == 0):
        if (yCorBall > (yCorPA + 50)):
            paddleAUp()

        elif (yCorBall < (yCorPA - 50)):
            paddleADown()
        
        if (gM == 1):
            if (xCorBall < 0 and xCorBall < xCorPA + 10 and xCorBall - xCorPA < 75):
                paddleALeft()

            elif (xCorBall > xCorPA + 10):
                paddleARight()
                
            else:
                paddleALeft()


# In[18]:


#Initiates the game environment
gameWindow = genGameWindow()
running = True
pause = False
pauseMessage = genText(0, 'white', 0, 0, '', 'center', ('Courier', 24, 'normal'))


# In[19]:


#Main Menu
#Number of Players
playerCount = genText(0, 'white', 0, 0, 'How many players?\nPress: "0", "1" or "2"', 
                      'center', ('Courier', 24, 'normal'))

numPlayers = gameWindow.numinput('PlayerCountSelection', 'How many players? ', 1, minval = 0, maxval = 2)
playerCount.clear()

#Game Type
gameType = genText(0, 'white', 0, 0, 'Which Game Mode: Classic or Advanced\nPress: "0" or "1"', 
                   'center', ('Courier', 24, 'normal'))

gameMode = gameWindow.numinput('GameModeSelection', 'Which Game Mode: Classic or Advanced?', 
                               0, minval = 0, maxval = 1)
gameType.clear()


# In[20]:


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

if (gameMode == 1):
    controls = genText(0, 'white', 0, 230, 'Left: "a" Right: "d"    Left: "\u2190" Right: "\u2192"', 
                       'center', ('Courier', 10, 'normal'))

#Exiting the Game Instructions
exitInstructions = genText(0, 'white', 0, -280, '  To exit the game press: "q"', 
                           'left', ('Courier', 10, 'normal'))

#Pausing the Game Instructions
exitInstructions = genText(0, 'white', 0, -280, 'To pause the game press: "p"  ', 
                           'right', ('Courier', 10, 'normal'))


# In[21]:


def playerControlsSwitch(nP, gM):
    
    #Player 1
    if (nP >= 1):
        gameWindow.onkeypress(paddleAUp, 'w')
        gameWindow.onkeypress(paddleADown, 's')
        
        if (gM == 1):
            gameWindow.onkeypress(paddleALeft, 'a')
            gameWindow.onkeypress(paddleARight, 'd')

    #Player 2
    if (nP == 2):
        gameWindow.onkeypress(paddleBUp, 'Up')
        gameWindow.onkeypress(paddleBDown, 'Down')
        
        if (gM == 1):
            gameWindow.onkeypress(paddleBLeft, 'Left')
            gameWindow.onkeypress(paddleBRight, 'Right')


# In[22]:


#Keyboard Binding
gameWindow.listen()

#Pauses the Game
gameWindow.onkeypress(pauseGame, 'p')

#Stop the Game Executing and Exit
gameWindow.onkeypress(exitGame, 'q')


# In[23]:


#Main Game Loop
while (running):
    
    if (pause == False):
        playerControlsSwitch(numPlayers, gameMode)
        moveBall(ball)
        borderChecking()
        paddleBallCollision()

        if (numPlayers < 2):
            opponentAI(ball, paddleB, paddleA, numPlayers, gameMode)

    gameWindow.update()


# In[24]:


turtle.done()

