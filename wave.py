"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in
the Alien Invaders game.  Instances of Wave represent a single wave. Whenever
you move to a new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on
screen. These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or
models.py. Whether a helper method belongs in this module or models.py is
often a complicated issue.  If you do not know, ask on Piazza and we will
answer.

# Nathnael Tesfaw (nbt26) & Akmal Rupasingha (ar2346)
# December 11th, 2023
"""
from game2d import *
from consts import *
from models import *
from Images import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts
    on screen. It animates the laser bolts, removing any aliens as necessary.
    It also marches the aliens back and forth across the screen until they are
    all destroyed or they reach the defense line (at which point the player
    loses). When the wave is complete, you  should create a NEW instance of
    Wave (in Invaders) if you want to make a new wave of aliens.

    If you want to pause the game, tell this controller to draw, but do not
    update.  See subcontrollers.py from Lecture 24 for an example.  This
    class will be similar to than one in how it interacts with the main class
    Invaders.

    All of the attributes of this class ar to be hidden. You may find that
    you want to access an attribute in class Invaders. It is okay if you do,
    but you MAY NOT ACCESS THE ATTRIBUTES DIRECTLY. You must use a getter
    and/or setter for any attribute that you need to access in Invaders.
    Only add the getters and setters that you need for Invaders. You can keep
    everything else hidden.

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _ship: the player ship to control
    # Invariant: _ship is a Ship object or None
    #
    # Attribute _aliens: the 2d list of aliens in the wave
    # Invariant: _aliens is a rectangular 2d list containing Alien objects or None
    #
    # Attribute _bolts: the laser bolts currently on screen
    # Invariant: _bolts is a list of Bolt objects, possibly empty
    #
    # Attribute _dline: the defensive line being protected
    # Invariant : _dline is a GPath object
    #
    # Attribute _lives: the number of lives left
    # Invariant: _lives is an int >= 0
    #
    # Attribute _time: the amount of time since the last Alien "step"
    # Invariant: _time is a float >= 0s
    #
    # Attribute _direction: the direction of alien SHIP_MOVEMENT
    # Invarient: _direction is an int = 1 or -1
    #
    #  Attribute _stepFire : the number of steps until the aliens fire
    # Invarient: _stepFire is an int > = 1 and <= BOLT_RATE
    #
    # Attribute _steps : the number of steps the aliens have took
    # Invariant: _steps is an int >= 0
    #
    # Attribute _isGameOver: shows if the Game is over or not
    # Invariant: _isGameOver is a boolean
    #
    # Attribute _waveSpeed: the speed at which Alien waves move
    # Invariant: _waveSpeed is an float
    #
    # Attribute _aliensShot: the number of Aliens shoot by the ship
    # Invariant: _aliensShot is an int
    #
    # Attribute _scoreUsed: the amount of Scores used on powerups
    # Invariant: _scoreUsed is an int
    #
    # Attribute _shipSpeed: the amount of frames the ship moves each seconds
    # Invariant: _shipSpeed is an int
    #
    # Attribute _boltVelocity: the speed of the bolt from the ships
    # Invariant: _boltVelocity is a float
    #
    #Attribute _bossWave: whether the  wave is a boss wave or # NOTE:
    # Invariant: _bossWave is a boolean
    #
    # You may change any attribute above, as long as you update the invariant
    # You may also add any new attributes as long as you document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setAliens(self):
        """ Sets a list of alien objects to aliens list"""
        if(self._bossWave == False):

            twod= []
            x = ALIEN_H_SEP + (ALIEN_WIDTH/2)
            y = GAME_HEIGHT - (ALIEN_CEILING + (ALIEN_HEIGHT/2))
            imagenum = 1

            for row in range(ALIEN_ROWS):
                alienrow = []
                if(row > 5):
                    imagenum = ((row%6) //2) +1
                else:
                    imagenum = (row //2) + 1

                for col in range(ALIENS_IN_ROW):
                    src = 'alien-strip'+str(imagenum) +'.png'
                    image = Alien(source=src,format = (4,2))
                    image.x=x
                    image.y=y
                    alienrow.append(image)
                    x = x + ALIEN_WIDTH + ALIEN_H_SEP

                twod.append(alienrow)
                y = y - (ALIEN_HEIGHT + ALIEN_V_SEP)
                x = ALIEN_H_SEP + (ALIEN_WIDTH/2)
            self._aliens = twod

        if(self._bossWave == True):
            boss = BossAlien(source='boss-strip.png', format = (4,2))
            boss.x= GAME_WIDTH /2
            boss.y= GAME_HEIGHT - ((ALIEN_H_SEP * 5) + ((ALIEN_WIDTH/2) * 5))
            self._aliens = boss


    def setShip(self):
        """ Sets a ship of ship object """
        ship = Ship(source = 'ship.png')
        ship.x = GAME_WIDTH/2
        ship.y = SHIP_BOTTOM
        self._ship = ship

    def setdLine(self):
        """ Sets a defense line of GPath object"""
        line = GPath(points= [0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE])
        line.linewidth = 1.1
        line.linecolor = [0.1,0.1,0.1,1]
        self._dline = line

    def setBolt(self,isPlayer,xpos,ypos):
        """ Sets a bolt object to bolts list

        Parameter isPlayer: Indicates whether a player or an alien making a bolt
        Precondition: isPlayer is a boolean

        Parameter xpos: the x position of the bolt/ship making a bolt
        Precondition: xpos is an float >= 0

        Parameter ypos: the y position of the bolt/ship making a bolt
        Precondition: ypos is an float >= 0
        """
        assert isinstance(isPlayer,bool) and isinstance(xpos, float)
        assert isinstance(ypos,float) and xpos >= 0 and ypos >= 0

        bolt = Bolt(fillcolor = [1,0,0,1], linecolor = [0.1,0.1,0.1,1])
        if isPlayer == False:
            bolt.changeVelocity()
        bolt.x = xpos
        bolt.y = ypos
        bolt.width = BOLT_WIDTH
        bolt.height = BOLT_HEIGHT
        self._bolts.append(bolt)

    def setStepFire(self):
        """ Sets a random number of steps between 1 and BOLT_RATE"""
        x = random.randint(1,BOLT_RATE)
        self._stepFire = x

    def setWaveSpeed(self,speed):
        """Sets Wave speed """
        assert isinstance(speed,float)
        self._waveSpeed = speed

    def setAliensShot(self, waveNum):
        """Accumlates number of aliens shot accros
        Parameter waveNum: Number of Waves that have passed
        Precondition: waveNum is an integer"""
        assert isinstance(waveNum, int)
        aliensCount = ALIENS_IN_ROW * ALIEN_ROWS

        self._aliensShot = (waveNum * aliensCount) - self._scoreUsed

    def setScoreUsed(self,used):
        """Sets the Score amount that has been used on powerups so far
        Parameter used: The score amount used so far
        Precondition: used is an int"""
        assert isinstance(used, int)
        self._scoreUsed = used

    def setShipSpeed(self,speed):
        """Sets the amount of frames the ship moves each second
        Parameter: speed is the amount of frames the ship moves a second
        Precondition: speed is an int """
        assert isinstance(speed,int) or isinstance(speed,float)
        self._shipSpeed = speed

    def setLives(self,lives):
        """Sets the number of lives the ship has
        Parameter: lives is the amount of lives the ship happens
        Precondition: lives is an int"""
        assert isinstance(lives,int)
        self._lives = lives

    def setBossWave(self,waveNum):
        """Determines if the wave is a boss wave or not
        Parameter waveNum: Number of Waves that have passed
        Precondition: waveNum is an integer"""
        assert isinstance(waveNum,int)
        if((waveNum +1) % 3 == 0 ):
            self._bossWave = True
        else:
            self._bossWave = False

    def getAliens(self):
        """Gets the Alien list"""
        return self._aliens

    def getShip(self):
        """Gets the Ship object"""
        return self._ship

    def getdLine(self):
        """Gets the defense line object"""
        return self._dline

    def getDirection(self):
        """Gets the direction of Alien steps"""
        return self._direction

    def getBolt(self):
        """Gets the list of bolts"""
        return self._bolts

    def getStepFire(self):
        """Gets the number of steps until an alien fires"""
        return self._stepFire

    def getSteps(self):
        """Gets the number of steps an alien since shooting a bolt"""
        return self._stepFire

    def getLives(self):
        """Gets the number of lives the player has"""
        return self._lives

    def getIsGameOver(self):
        """Gets whether the game is over or not"""
        return self._isGameOver

    def getWaveSpeed(self):
        """Gets the wave Aliens speed value"""
        return self._waveSpeed

    def getAliensShot(self):
        """Gets the the number of Aliens Shot"""
        return self._aliensShot

    def getScoreUsed(self):
        """Gets the score used up so far"""
        return self._scoreUsed
    def getShipSpeed(self):
        """Gets the ship speed at the current moment """
        return self._shipSpeed

    def getBoltVelocity(self):
        """Gets the velocity of the bolt from the ship"""
        return self._boltVelocity

    def getBossWave(self):
        """ Gets whether the wave is a boss wave"""
        return self._bossWave


    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self,wavespeed = ALIEN_SPEED,wavenum = 0,
     lives = int((ALIENS_IN_ROW * ALIEN_ROWS) /2) ,used = 0, shipspeed = 2):
        """
        Initializes all attribites
        """
        self.setScoreUsed(used)
        self.setAliensShot(wavenum)
        self.setLives(lives)
        self.setWaveSpeed(wavespeed)
        self.setShipSpeed(shipspeed)
        self.setBossWave(wavenum)
        self.setAliens()
        self.setShip()
        self.setdLine()
        self.setStepFire()
        self._bolts = []
        self._time = 0
        self._steps = 0
        self._direction = 1
        self._isGameOver = False
        self._boltVelocity = 1
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS

    def update(self,input,dt,shipboltsound,alienboltsound,alienShotSound,
     shipShotSound):
        """ Animates a single frame in the game.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: user input, used to control the ship or resume the game
        Precondition: input is an instance of GInput (inherited from GameApp)

        Parameter alienboltsound: the sound of a bolt firing from Alien
        Precondition: alienboltsound is an instance of Sound Class

        Parameter shipboltsound: the sound of a bolt firing from Ship
        Precondition: shipboltsound is an instance of Sound Class

        Parameter alienShotsound: the sound of an Alien being Shot
        Precondition: alienboltsound is an instance of Sound Class

        Parameter shipShotsound: the sound of an Ship being Shot
        Precondition: shipboltsound is an instance of Sound Class`"""

        assert isinstance(dt,int) or isinstance(dt,float)
        assert isinstance(input,GInput)
        assert isinstance(alienboltsound,Sound)
        assert isinstance(shipboltsound,Sound)
        assert isinstance(alienShotSound,Sound)
        #moving ship left and right
        self.shipInputs(input,shipboltsound)
        #rightmost alien and leftmost aliens
        if(self._bossWave == False):
            ralien = self.rightmostAlien()
            lalien = self.leftmostAlien()
        #time acculumator
        self._time += dt
        #vertical increments
        if(self._time > self._waveSpeed):
            #vertical increment
            if(self._bossWave == False):
                if(ralien.x>= GAME_WIDTH - ALIEN_H_SEP):
                    self.vIncrement()
                if(self._direction == -1 and lalien.x <= 0 + ALIEN_H_SEP):
                    self.vIncrement()
            if(self._bossWave == True):
                if(self._aliens.x >= GAME_WIDTH - (self._aliens.width /2)):
                    self.vIncrement()
                if(self._direction == -1 and self._aliens.x <= 0 + (self._aliens.width /2) ):
                    self.vIncrement()

            self.moveAliens()
            self._steps += 1
            self._time = 0


        #removing bolts from screen
        self.removeBolts()
        #random column
        self.whenAlienFire(alienboltsound)
        #bolt collides with aliens and ships
        self.removeAliens(alienShotSound)
        self.removeShip(shipShotSound)
        #checking if Game is Over
        self.checkGameOver()

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self,view):
        """
        Draws the game objects to the view.

        Parameter view: the game view, used in drawing
        Precondition: view is an instance of GView (inherited from GameApp)"""
        assert isinstance(view,GView)
        if(self._bossWave == False):
            for row in self._aliens:
                for alien in row:
                    if(alien != None):
                        alien.draw(view)
        if(self._bossWave == True):
            self._aliens.draw(view)

        for i in self._bolts:
            i.draw(view)
        #draw the ship
        if(self._ship != None):
            self._ship.draw(view)
        #draw the defense line
        self._dline.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def changeDirection(self):
        """
        Changes the direction of alien movement when called
        """
        if(self._direction == 1 ):
            self._direction = -1
        else:
            self._direction = 1

    def vIncrement(self):
        """ Decrements the Alien list and changes direction at window edge """
        if(self._bossWave == False):
            for row in self._aliens:
                for alien in row:
                    if(alien != None):
                        alien.y -= ALIEN_V_WALK
        if(self._bossWave == True):
            self._aliens.y -= ALIEN_V_WALK * 3
        self.changeDirection()

    def isPlayerThere(self):
        """ Determines if there is a player bolt in bolt list"""
        x = False
        for i in self._bolts:
            if i.isPlayerBolt() and i != None:
                x = True
        return x

    def isAlienThere(self):
        """Determines if there is an alien bolt in bolt list"""
        x = False
        for i in self._bolts:
            if i.isPlayerBolt()== False and i != None:
                x = True
        return x

    def shipInputs(self,input,boltsound):
        """
        Moves the ship object to the right when 'd' or 'right arrow' are pressed
        Moves the ship object to the left when 'a' or 'left arrow' are pressed

        Fires a player bolt when 'up arrow' or 'w' are pressed

        Parameter input: user input, used to control the ship or resume the game
        Precondition: input is an instance of GInput (inherited from GameApp)

        Parameter boltsound: the sound of a bolt firing
        Precondition: boltsound is an instance of Sound Class"""
        assert isinstance(input,GInput)

        if input.is_key_down('a') or input.is_key_down('left'):
            if(self._ship.x == 0):
                self._ship.x = 0 + (SHIP_WIDTH/2)
            else:
                self._ship.x -= self._shipSpeed
        if input.is_key_down('d') or input.is_key_down('right'):
            if(self._ship.x == GAME_WIDTH):
                self._ship.x = GAME_WIDTH - (SHIP_WIDTH/2)
            else:
                self._ship.x += self._shipSpeed
        #shooting bolts from ship
        if input.is_key_pressed('w') or input.is_key_pressed('up'):
            if self.isPlayerThere() == False:
                self.setBolt(True,self._ship.x, SHIP_BOTTOM * 1.8)
                boltsound.play()




    def rightmostAlien(self):
        """
        Determines the rightmost Alien object in the Alien list
        """
        rightcol = len(self._aliens[0]) -1
        uprow= len(self._aliens) -1
        ralien = self._aliens[uprow][rightcol]
        while self._aliens[uprow][rightcol] == None and rightcol != -1:
            uprow -= 1
            ralien = self._aliens[uprow][rightcol]
            if(uprow == -1):
                rightcol -= 1
                uprow = len(self._aliens) -1
                ralien = self._aliens[uprow][rightcol]
        return ralien

    def leftmostAlien(self):
        """
        Determines the leftmost Alien object in the Alien list
        """
        lcol = 0
        uprow2= len(self._aliens) -1
        lalien = self._aliens[uprow2][lcol]
        while self._aliens[uprow2][lcol] == None:
            uprow2 -= 1
            lalien = self._aliens[uprow2][lcol]
            if(uprow2 == -1):
                lcol += 1
                uprow2 = len(self._aliens) -1
                lalien = self._aliens[uprow2][lcol]
        return lalien

    def whenAlienFire(self, boltsound):
        """
        Finds a random column and its lowest valid row to fire bolts from
        Bolts are fired when the number of alien steps is above steps until Fire

        Parameter boltsound: the sound of a bolt firing
        Precondition: boltsound is an instance of Sound Class
        """
        if(self._bossWave == False):
            randCol = random.randint(0,len(self._aliens[0]) -1)
            while(self._aliens[0][randCol] == None):
                randCol = random.randint(0,len(self._aliens[0]) -1)

            #bottom row
            brow = len(self._aliens) -1
            while(self._aliens[brow][randCol] == None):
                brow = brow -1

            #when alien to fire
            if self._steps >= self._stepFire and self.isAlienThere() == False:
                xp = self._aliens[brow][randCol].x
                yp =self._aliens[brow][randCol].y
                self.setBolt(False,xp,yp)
                boltsound.play()
                self.setStepFire()

        if(self._bossWave == True):
            if self._steps >= self._stepFire and  self.isAlienThere() == False:
                xp = self._aliens.x
                yp =self._aliens.y
                self.setBolt(False,xp,yp)
                boltsound.play()
                #change if possible
                self.setStepFire()

    def removeShip(self, shipShotSound):
        """Sets ship to None if it collides with a bolt
            Additionally, decrements number of player lives
        Parameter shipShotSound: the sound of an alien being shot
        Precondition:shipShotSound is an instance of Sound Class     """
        for bolt in self._bolts:
            if self._ship== None :
                pass
            else:
                if self._ship.collides(bolt):
                    self._bolts.remove(bolt)
                    self._ship = None
                    self._lives -= 1
                    shipShotSound.play()

    def removeAliens(self,alienShotSound):
        """Sets alien object to None if it collides with a bolt
        Parameter alienShotSound: the sound of an alien being shot
        Precondition: alienShotSound is an instance of Sound Class"""

        if(self._bossWave == False):
            numrow = range(len(self._aliens))
            numcol = range(len(self._aliens[0]))
            for row in numrow:
                for col in numcol:
                    for bolt in self._bolts:
                        if self._aliens[row][col]== None :
                            pass
                        else:
                            if self._aliens[row][col].collides(bolt):
                                self._bolts.remove(bolt)
                                self._aliens[row][col] = None
                                self._aliensShot += 1
                                alienShotSound.play()

        if(self._bossWave == True):
            for bolt in self._bolts:
                if self._aliens.collides(bolt):
                    self._bolts.remove(bolt)
                    if(self._aliens.getHitPoints()   > 0):
                        self._aliens.takeDamage()
                        alienShotSound.play()
                    if(self._aliens.getHitPoints() == 0):
                        self._aliens == None
                        alienShotSound.play()

                        self._aliensShot = self._aliensShot + 30
                        self._isGameOver = True#change later


    def checkGameOver(self):
        """Checks if the Game is Over
            The Game is over when either:
            1) Player lives is zero
            2) There alien objects are None
            3) Any alien object passes the defense line object """

        if(self._lives == 0):
            self._isGameOver = True

        alienAlive = False
        #if all aliens are None
        if(self._bossWave == False):
            for row in self._aliens:
                for alien in row:
                    if(alien != None):
                        alienAlive = True


        if(self._bossWave == True):
            if(self._aliens != None):
                alienAlive = True

        if(alienAlive == False):
            self._isGameOver = True

        if(self._bossWave == False):
            for row in self._aliens:
                for alien in row:
                    if(alien != None):
                        if(alien.y <= DEFENSE_LINE):
                            self._isGameOver = True
                            self._lives = 0

        if(self._bossWave == True):
            if(self._aliens.y <= DEFENSE_LINE):
                self._isGameOver = True
                self._lives = 0
        #if any alien is below dline


    def removeBolts(self):
        """Removes a bolt object from bolts list"""
        for i in self._bolts:
            if i.y -(i.height /2) > GAME_HEIGHT:
                self._bolts.remove(i)
            if i.y + (i.height /2) < 0:
                self._bolts.remove(i)
            else:
                i.y += i.getVelocity()

    def moveAliens(self):
        """Moves aliens list when called"""
        if(self._bossWave == False):
            for row in self._aliens:
                for alien in row:
                    if(alien != None):
                        alien.x += (self._direction * ALIEN_H_WALK)
                        alien.frame = (alien.frame+1) % 2

        if(self._bossWave == True):
            self._aliens.x += (self._direction * ALIEN_H_WALK * 2)
            self._aliens.frame = (self._aliens.frame +1) % 2

    def increasePlayerBoltVel(self):
        """Increases the Velocity of a player's bolt each time called"""
        self._boltVelocity = self._boltVelocity  +1

    def increasePlayerSpeed(self):
        """Increases the Speed of the the Ship each time called"""
        self._shipSpeed = self._shipSpeed * 1.5
