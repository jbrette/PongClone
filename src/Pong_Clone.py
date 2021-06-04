#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Orginally based upon the 'Python Game Tutorial: Pong' video tutorial by freeCodeCamp.org


# In[2]:


import turtle #Used for simple games in python
import random
import os
import platform
#import winsound


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
def paddleMovement(tappedKey, pa, gM):   
    #Paddle A Movements
    if (pa == False): #Prevents paddle movement when the game is paused
        if (tappedKey == 'w' or tappedKey == 's' or tappedKey == 'a' or tappedKey == 'd'):
            global paddleA
            
            if (tappedKey == 'w' or tappedKey == 's'): #Up & Down
                yCorPA = paddleA.ycor()

                if (tappedKey == 'w' and yCorPA < 250):
                    yCorPA += 50
                if (tappedKey == 's' and yCorPA > -250):
                    yCorPA -= 50

                paddleA.sety(yCorPA)
            
            if (gM == 1):
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
                
            if (gM == 1):
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
    paddleMovement('w', pause, gameMode)
    
def paddleADown():
    paddleMovement('s', pause, gameMode)
    
def paddleALeft():
    paddleMovement('a', pause, gameMode)
    
def paddleARight():
    paddleBallMoveCollision(ball, paddleA, paddleB)
    paddleMovement('d', pause, gameMode)

#Paddle B
def paddleBUp():
    paddleMovement('Up', pause, gameMode)
    
def paddleBDown():
    paddleMovement('Down', pause, gameMode)
    
def paddleBLeft():
    paddleBallMoveCollision(ball, paddleA, paddleB)
    paddleMovement('Left', pause, gameMode)
    
def paddleBRight():
    paddleMovement('Right', pause, gameMode)


# In[9]:


#Allows players to hit the ball harder or softer
def paddleSwingPower(swingStrength):
    global paddleAStrength
    global paddleBStrength
    
    if (swingStrength == 'r'):
        paddleAStrength = 2
    if (swingStrength == 'f'):
        paddleAStrength = 0.5
        
    if (swingStrength == 'o'):
        paddleBStrength = 2
    if (swingStrength == 'l'):
        paddleBStrength = 0.5


# In[10]:


#Call strength by 'onkeypress'
#Paddle A
def strongerPaddleASwing():
    paddleSwingPower('r')
    
def weakerPaddleASwing():
    paddleSwingPower('f')

#Paddle B
def strongerPaddleBSwing():
    paddleSwingPower('o')
    
def weakerPaddleBSwing():
    paddleSwingPower('l')


# In[11]:


#Determines Ball Movement Speed
def setBallSpeed(speed):
    ball.dx = speed #Movement on x-axis
    ball.dy = speed #Movement on y-axis


# In[12]:


#Limits the Ball Movement Speed to Resonable Levels
def limitBallSpeed(bl):
    dxBall = bl.dx
    dyBall = bl.dy
    
    if (dxBall < -3):
        bl.dx = -3
    
    if (dxBall > 3):
        bl.dx = 3

    if (dyBall < -3):
        bl.dy = -3
    
    if (dyBall > 3):
        bl.dy = 3
    
    if (dxBall > -0.75 and dxBall < 0):
        bl.dx = -0.75
    
    if (dxBall < 0.75 and dxBall > 0):
        bl.dx = 0.75
    
    if (dyBall > -0.5 and dyBall < 0):
        bl.dy = -0.5
        
    if (dyBall > 0 and dyBall < 0.5):
        bl.dy = 0.5


# In[13]:


#Makes the ball move
def moveBall(bl):
    bl.setx(bl.xcor() + bl.dx)
    bl.sety(bl.ycor() + bl.dy)


# In[14]:


def randomizeBallServe(bl):
    bl.dy *= random.uniform(-1, 1)


# In[15]:


def playSound(soundFile):
    sound = str(soundFile + '&')
    systemType = platform.system()
    print(sound)
    print(systemType)
    
    if (systemType == 'Linux' or systemType == 'Linux2'): # Linux
        os.system('aplay ' + soundFile)
        
    elif (systemType == 'Darwin'): # Mac OS X
        os.system('afplay ' + soundFile)
        
    elif (systemType == 'Windows'): # Windows
        #winsound.PlaySound(soundFile, winsound.SND_ASYNC)
        print('Currently non functional.')


# In[16]:


#Screen Border Checking
def borderChecking(bl):
    global score1
    global score2 
    
    yCorBall = bl.ycor()
    xCorBall = bl.xcor()
    
    if (yCorBall > 290 or yCorBall < -290):
        if (yCorBall > 290): #Top Screen Border
            bl.sety(290)

        if (yCorBall < -290): #Bottom Screen Border
            bl.sety(-290)
        
        bl.dy *= -1
    
    if (xCorBall > 390 or xCorBall < -390):
        if (xCorBall > 390): #Right Screen Border
            bl.setx(390)
            score1 += 1
            setBallSpeed(-1 * defaultBallSpeed)

        if (xCorBall < -390): #Left Screen Border
            bl.setx(-390)
            score2 += 1
            setBallSpeed(defaultBallSpeed)
        
        playSound('AirPlaneDing.mp3')
        
        bl.goto(0, 0)
        #randomizeBallServe(bl)
        
        sb.clear()
        sb.write('Player {}: {}  Player {}: {}'.format(setScoreNames()[0], score1, setScoreNames()[1], score2), 
                 align = 'center', font = ('Courier', 24, 'normal'))

    limitBallSpeed(bl)


# In[17]:


#Determines Paddle & Ball Collisions
def paddleBallCollision(bl, bH, pA, pAS, pB, pBS):
    global ballHit
    
    yCorBall = bl.ycor()
    xCorBall = bl.xcor()
    
    yCorPA = pA.ycor()
    xCorPA = pA.xcor()
    
    yCorPB = pB.ycor()
    xCorPB = pB.xcor()
    
    #Right Paddle
    if ((yCorBall >= yCorPB - 50 and yCorBall <= yCorPB + 50) and 
        (xCorBall >= xCorPB - 10 and xCorBall <= xCorPB + 10)):

        bl.setx(xCorPB - 10)
        bl.dx *= -1 * pBS
        #bH = 1
        ballHit = 1
        resultingCollisionAngle(bl, yCorBall, yCorPB)
        playSound('ButtonClickOff.mp3')
        
    #Left Paddle
    if ((yCorBall >= yCorPA - 50 and yCorBall <= yCorPA + 50) and 
        (xCorBall <= xCorPA + 10 and xCorBall >= xCorPA - 10)):
        
        bl.setx(xCorPA + 10)
        bl.dx *= -1 * pAS
        #bH = 0
        ballHit = 0
        resultingCollisionAngle(bl, yCorBall, yCorPA)
        playSound('ButtonClickOn.mp3')
        
    limitBallSpeed(bl)


# In[18]:


#Prevents the Ball from glitching through a paddle moving towards it
def paddleBallMoveCollision(bl, pA, pB):
    yCorBall = bl.ycor()
    xCorBall = bl.xcor()
    
    yCorPA = pA.ycor()
    xCorPA = pA.xcor()
    
    yCorPB = pB.ycor()
    xCorPB = pB.xcor()
    
    if (xCorBall > 0 and xCorPB - 10 - 50 < xCorBall):
        bl.setx(xCorPB - 60)
        
    if (xCorBall < 0 and xCorPA + 10 + 50 > xCorBall):
        bl.setx(xCorPA + 60)


# In[19]:


#Adjust the angle of the ball's trajectory depending on where it struck along the paddle's length
def resultingCollisionAngle(bl, bYCor, pYCor):
    bl.dy *= (abs(pYCor - bYCor) / 16.66)
    
    if (bYCor >= pYCor - 50 and bYCor < pYCor and bl.dy > 0):
        bl.dy *= -1
  
    elif (bYCor <= pYCor + 50 and bYCor > pYCor and bl.dy < 0):
        bl.dy *= -1
            
    #else:
    #    bl.dy *= 0 


# In[20]:


def pauseGame():
    global pause
    global pauseMessage
    
    if (pause == True):
        pause = False
        pauseMessage.clear()
    else:
        pause = True
        pauseMessage = genText(0, 'white', 0, 0, '  Game  Paused', 'center', ('Courier', 24, 'normal'))


# In[21]:


#Allows players to end and quit the game without errors
def exitGame():
    global running 
    running = False


# In[22]:


#Creates a Very Simple Player 0 AI
def simpleOpponentAI(bl, bH, pB, pA, nP, gM):
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
        strength = random.randint(0, 1)
        if (strength == 1):
            strongerPaddleBSwing()
        else:
            weakerPaddleBSwing()
    
        if (xCorBall > 0 and xCorBall < xCorPB - 10 and xCorPB - xCorBall <= 75 and bH == 0):
            pass
        
        elif (xCorBall > 0 and xCorBall < xCorPB - 10 and bH == 0):
            paddleBLeft()
        
        else:
            paddleBRight()

    if (nP == 0):
        if (yCorBall > (yCorPA + 50)):
            paddleAUp()

        elif (yCorBall < (yCorPA - 50)):
            paddleADown()
        
        if (gM == 1):
            strength = random.randint(0, 1)
            if (strength == 1):
                strongerPaddleASwing()
            else:
                weakerPaddleASwing()
            
            if (xCorBall < 0 and xCorBall > xCorPA + 10 and abs(xCorPA - xCorBall) <= 75 and bH == 1):
                pass
            
            elif (xCorBall < 0 and xCorBall > xCorPA + 10 and bH == 1):
                paddleARight()
            
            else:
                paddleALeft()


# In[23]:


#Accurately predict's the ball's path; currently only functions for classic mode
def predictBallMovement(bl):
    global ballScoreXCor
    global ballScoreYCor
    
    xCorBall = bl.xcor()
    yCorBall = bl.ycor()
    
    dxBall = bl.dx
    dyBall = bl.dy
    
    xCorBaseline = 350
    yCorSideline = 290
    
    if (abs(xCorBall) < 5):
        if (dxBall > 0):
            xCorBasline = 350
        elif (dxBall < 0):
            xCorBasline = -350
         
        xDistToBaseline = xCorBaseline - xCorBall
        xTimeToBaseline = abs(xDistToBaseline / dxBall)
            
        if (dyBall > 0):
            yCorSideline = 290
        
        elif (dyBall < 0):
            yCorSideline = -290
        
        yDistToSideline = yCorSideline - yCorBall
        yTimeToSideline = abs(yDistToSideline / dyBall)
    
        if (xTimeToBaseline < yTimeToSideline): 
            ballScoreYCor = yCorBall + (xTimeToBaseline * dyBall)
    
        elif (xTimeToBaseline > yTimeToSideline):
            xTimeToBaseline -= yTimeToSideline
                
            yTimeToCrossHalfOfField = abs(290 / dyBall)
            ratio = xTimeToBaseline / yTimeToCrossHalfOfField
            wholeRatio = int(ratio)
                
            timeLeft = xTimeToBaseline - (yTimeToCrossHalfOfField * wholeRatio)
                
            numBounces = int(wholeRatio / 2) + 1
                
            wholeRatiosAfterLastBounce = wholeRatio - (2 * (numBounces - 1))
                
            if ((numBounces % 2 > 0 and dyBall > 0) or (numBounces % 2 == 0 and dyBall < 0)):
                ballScoreYCor = 290 - (wholeRatiosAfterLastBounce * 290) - abs(timeLeft * dyBall)
                    
            elif ((numBounces % 2 > 0 and dyBall < 0) or (numBounces % 2 == 0 and dyBall > 0)):
                ballScoreYCor = -290 + (wholeRatiosAfterLastBounce * 290) + abs(timeLeft * dyBall)


# In[24]:


#Control's the AI Paddles
#As the AI always correctly predict's the ball's path, with 0 players the same ball movement repeats infinitely
def predictiveOpponentAI(bl, bH, pA, pB, nP):    
    xCorBall = bl.xcor()
    yCorBall = bl.ycor()
    
    xCorPB = pB.xcor()
    yCorPB = pB.ycor()
    
    if (xCorBall > 0 and bH == 0):
        
        if (ballScoreYCor > (yCorPB + 50)):
            paddleBUp()

        elif (ballScoreYCor < (yCorPB - 50)):
            paddleBDown()
               
    if (bH == 1):
        
        if (yCorPB < 0):
            paddleBUp()
            
        elif (yCorPB > 0):
            paddleBDown()
        
    if (nP == 0):
        
        xCorPA = pA.xcor()
        yCorPA = pA.ycor()
            
        if (xCorBall < 0 and bH == 1):
        
            if (ballScoreYCor > (yCorPA + 50)):
                paddleAUp()
    
            elif (ballScoreYCor < (yCorPA - 50)):
                paddleADown()  
                
        if (bH == 0):
            
            if (yCorPA < 0):
                paddleAUp()
            
            elif (yCorPA > 0):
                paddleADown()


# In[25]:


#Initiates the game environment
gameWindow = genGameWindow()
running = True

pause = False
pauseMessage = genText(0, 'white', 0, 0, '', 'center', ('Courier', 24, 'normal'))

speedSAI = 26
speedPAI = 26

ballScoreXCor = 0
ballScoreYCor = 0


# In[26]:


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

#AI Mode
typeAI = genText(0, 'white', 0, 0, 'Which AI Mode: Simple or Predictive\nPress: "0" or "1"', 
                 'center', ('Courier', 24, 'normal'))

modeAI = gameWindow.numinput('AIModeSelection', 'Which AI Mode: Simple or Predictive?', 
                             0, minval = 0, maxval = 1)

typeAI.clear()


# In[27]:


#Sets up the game environment    
#Generates the Playing Field Divider
playingFieldDivider = genObject(0, 'square', 30, 0.1, 'white', 0, 0)


#Generates the Paddles
#Left Paddle A
paddleA = genObject(0, 'square', 5, 1, 'white', -350, 0)
paddleAStrength = 1

#Right Paddle B
paddleB = genObject(0, 'square', 5, 1, 'white', 350, 0)
paddleBStrength = 1


#Generates the Ball
#Ball
ball = genObject(0, 'square', 1, 1, 'white', 0, 0)
ballHit = 0
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
controls = genText(0, 'white', 0, 250, 'Up: "w" Down: "s"    Up: "\u2191" Down: "\u2193"', 
                   'center', ('Courier', 10, 'normal'))

if (gameMode == 1):
    controls = genText(0, 'white', 0, 230, 'Left: "a" Right: "d"    Left: "\u2190" Right: "\u2192"', 
                       'center', ('Courier', 10, 'normal'))
    controls = genText(0, 'white', 0, 210, 
                       'Stronger Swing: "r" Weaker Swing: "f"    Stronger Swing: "o" Weaker Swing: "l"', 
                       'center', ('Courier', 10, 'normal'))

#Exiting the Game Instructions
exitInstructions = genText(0, 'white', 0, -280, '  To exit the game press: "q"', 
                           'left', ('Courier', 10, 'normal'))

#Pausing the Game Instructions
exitInstructions = genText(0, 'white', 0, -280, 'To pause the game press: "p"  ', 
                           'right', ('Courier', 10, 'normal'))


# In[28]:


def playerControlsSwitch(nP, gM):
    #Player 1
    if (nP >= 1):
        gameWindow.onkeypress(paddleAUp, 'w')
        gameWindow.onkeypress(paddleADown, 's')
        
        if (gM == 1):
            gameWindow.onkeypress(paddleALeft, 'a')
            gameWindow.onkeypress(paddleARight, 'd')
            
            gameWindow.onkeypress(strongerPaddleASwing, 'r')
            gameWindow.onkeypress(weakerPaddleASwing, 'f')

    #Player 2
    if (nP == 2):
        gameWindow.onkeypress(paddleBUp, 'Up')
        gameWindow.onkeypress(paddleBDown, 'Down')
        
        if (gM == 1):
            gameWindow.onkeypress(paddleBLeft, 'Left')
            gameWindow.onkeypress(paddleBRight, 'Right')
                    
            gameWindow.onkeypress(strongerPaddleASwing, 'o')
            gameWindow.onkeypress(weakerPaddleASwing, 'l')


# In[29]:


#Keyboard Binding
gameWindow.listen()

#Pauses the Game
gameWindow.onkeypress(pauseGame, 'p')

#Stop the Game Executing and Exit
gameWindow.onkeypress(exitGame, 'q')


# In[ ]:


#Main Game Loop
while (running):
    
    if (pause == False):
        playerControlsSwitch(numPlayers, gameMode)
        moveBall(ball)
        borderChecking(ball)
        paddleBallCollision(ball, ballHit, paddleA, paddleAStrength, paddleB, paddleBStrength)

        if (numPlayers < 2):
            if (modeAI == 0):
                speedSAI -= 1
                if (speedSAI == 0):
                    simpleOpponentAI(ball, ballHit, paddleB, paddleA, numPlayers, gameMode)
                    speedSAI = 26
            else:
                predictBallMovement(ball)
                speedPAI -= 1
                if (speedPAI == 0):
                    predictiveOpponentAI(ball, ballHit, paddleA, paddleB, numPlayers)
                    speedPAI = 26
                    
    gameWindow.update()


# In[ ]:


turtle.done()


# In[ ]:





# In[ ]:




