"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders app.
There is no need for any additional classes in this module.  If you need
more classes, 99% of the time they belong in either the wave module or the
models module. If you are unsure about where a new class should go, post a
question on Piazza.

# Nathnael Tesfaw (nbt26) & Akmal Rupasingha (ar2346)
# December 11th, 2023
"""
from consts import *
from game2d import *
from wave import *
from Fonts import *
from Sounds import *
import random


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary
    for processing the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create
    an initializer __init__ for this class.  Any initialization should be done
    in the start method instead.  This is only for this class.  All other
    classes behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will
    have its own update and draw method.

    The primary purpose of this class is to manage the game state: which is
    when the game started, paused, now, etc. It keeps track of that in
    an internal (hidden) attribute.

    For a complete description of how the states work, see the specification
    for the method update.

    Attribute view: the game view, used in drawing
    Invariant: view is an instance of GView (inherited from GameApp)

    Attribute input: user input, used to control the ship or resume the game
    Invariant: input is an instance of GInput (inherited from GameApp)

    """
    # HIDDEN ATTRIBUTES:
    # Attribute _state: the current state of the game represented as an int
    # Invariant: _state is one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE,
    # STATE_PAUSED, STATE_CONTINUE, or STATE_COMPLETE
    #
    # Attribute _wave: the subcontroller for a single wave, managing aliens
    # Invariant: _wave is a Wave object, or None if there is no wave currently
    # active. It is only None if _state is STATE_INACTIVE.
    #
    # Attribute _text: the currently active message
    # Invariant: _text is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is STATE_ACTIVE.
    #
    # Attribute _waveNum: a label of the number of waves have been cleared
    # Invarient: _waveNum is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is not STATE_ACTIVE.
    #
    # Attribute _wavesnow: the number of waves cleared so far
    # Invariant: _wavesnow is a float or int
    #
    # Attribute _livesNum: a label of the number of lives left
    # Invarient: _livesNum is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is not STATE_ACTIVE.
    #
    # Attribute _score: a label of the number aliens shot
    # Invarient: _score is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is not STATE_ACTIVE.
    #
    # Attribute _powerupson: whether or not powerups are on
    # Invarient: _powerupson is a boolean
    #
    # Attribute _usedScore: the total Amount of points used on powerups so features
    # Invarient: _usedScore is an int
    #
    # Attribute _wavespeed: the speed of the waves of ALiens
    # Invarient: _wavespeed is a float
    #
    # Attribute _endWaveLives: the amount of lives at the end of a wave
    # Invarient: _endWaveLives is an int
    #
    # Attribute _shipSpeed: the speed of the ship
    # Invarient: _shipSpeed is an int ot float

    # Attribute _powerupLabel: a label of weather powerups and/or Sound is on
    # Invarient:  _powerupLabel is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is not STATE_ACTIVE.
    #
    # Attribute _ost: the background music
    # Invarient: _ost is a Sound object
    #
    # Attribute _ost2: the background music in wave 2
    # Invarient: _ost2 is a Sound object

    # Attribute _ost3: the background music in wave 3
    # Invarient: _ost3 is a Sound object
    #
    # Attribute _alienBoltfireSound: Alien sound effect of firing a bolts
    # Invariant: _alienBoltfireSound is a Sound object
    #
    # Attribute _shipBoltfireSound: Ship sound effect of firing a bolts
    # Invariant: _shipBoltfireSound is a Sound object
    #
    # Attribute _powerUpScreenSound: whether the powerup screen ost is on
    # Invarient: _powerUpScreenSound is a boolean
    #
    #Attribute _backgroundImage: the background of the whole game
    # Invariant: _backgroundImage is a GImage class and is None when state is
    # not STATE_ACTIVE
    #
    # Attribute _alienShotSound: the sound that plays when an alien is Shot
    # Invariant: _alienShotSound is a Sound object
    #
    # Attribute _shipShotSound: the sound that plays when an ship is Shot
    # Invariant: _shipShotSound is a Sound object
    #
    # Attribute _soundOn: whether the sound is on
    # Invariant:_soundOn is a boolaen
    #
    # Attribute _source: the source for the background imagenum
    # Invariant: _source is a string
    #
    # Attribute _scoreAfter: the score after a wave is completed
    # Invariant: _scoreAfter is an integer
    #
    #Attribute _livesAfter: the number of lives after a wave is completed
    # Invariant: _livesAfter is an integer
    #
    # Attribute _seeCreditsLabel: a label to show how to get to Credits
    # Invarient:  _seeCreditsLabel is a GLabel object, or None if there is no message to
    # display. It is only None if _state is  STATE_ACTIVE.
    #
    # Attribute _bottomImage: Image at bottom of screen
    # Invarient: _bottomImage is a GImage if the state is STATE_WIN or GSprite
    # the state is STATE_WIN
    #
    # Attribute _creditsLabel: the Title of the Credits screen
    # Invariant: _ is a GLabel object, or None if there is no message to
    # display. It is onl None if _state is not STATE_ACTIVE.
    # You may have new attributes if you wish (you might want an attribute to
    # store any score across multiple waves). But you must document them.
    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which
        you should not override or change). This method is called once the
        game is running. You should use it to initialize any game specific
        attributes.

        This method should make sure that all of the attributes satisfy the
        given invariants. When done, it sets the _state to STATE_INACTIVE and
        create a message (in attribute _text) saying that the user should press
        to play a game.
        """
        self._state = STATE_INACTIVE
        self.setText("SHIP GAME! \n Press 'Space' to play", 40)
        self._wave = None
        self._wavesnow = 1
        self._waveNum = None
        self._score = None
        self._powerupson = True
        self._usedScore = 0
        self._wavespeed = ALIEN_SPEED
        self._endWaveLives = 0
        self._shipSpeed = 2
        self._powerupLabel = None
        self._ost = Sound('Title.mp3')
        self._ost.play(True)
        self._alienBoltfireSound = Sound('pew2.wav')
        self._shipBoltfireSound = Sound('betterpew.wav')
        self._shipBoltfireSound.volume = 0.2
        self._powerUpScreenSound = False
        self._backgroundImage = None
        self._alienShotSound = Sound('blast1.wav')
        self._shipShotSound = Sound('blast2.wav')
        self._shipShotSound.volume = 0.5
        self._alienShotSound.volume = 0.3
        self._source = 'background.jpg'
        self._soundOn = True
        self._livesAfter = 0
        self._scoreAfter = 0
        self._creditsLabel = None
        self._seeCreditsLabel = None
        # IMPLEMENT ME
        pass

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of
        playing the game.  That is the purpose of the class Wave. The primary
        purpose of this game is to determine the current state, and -- if the
        game is active -- pass the input to the Wave object _wave to play the
        game.

        As part of the assignment, you are allowed to add your own states.
        However, at a minimum you must support the following states:
        STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED,
        STATE_CONTINUE, and STATE_COMPLETE.  Each one of these does its own
        thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.
        It is a paused state, waiting for the player to start the game.  It
        displays a simple message on the screen. The application remains in
        this state so long as the player never presses a key.  In addition,
        this is the state the application returns to when the game is over
        (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on
        the screen. The application switches to this state if the state was
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        This state only lasts one animation frame before switching to
        STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can
        move the ship and fire laser bolts.  All of this should be handled
        inside of class Wave (NOT in this class).  Hence the Wave class
        should have an update() method, just like the subcontroller example
        in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However,
        the game is still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed.
        The application switches to this state if the state was STATE_PAUSED
        in the previous frame, and the player pressed a key. This state only
        lasts one animation frame before switching to STATE_ACTIVE.

        STATE_LOSE: The game is lost

        STATE_WIN: When the game is WON

        STATE_CREDITS: State to show Credits

        STATE_POWERUP: State to buy powerups

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        assert isinstance(dt,int) or isinstance(dt,float)

        if(self.input.is_key_pressed('spacebar')):
            if(self._state == STATE_INACTIVE or self._state == STATE_LOSE):
                self._state = STATE_NEWWAVE

            if(self._state == STATE_PAUSED):
                self._state = STATE_ACTIVE
                self._wave.setShip()

            if(self._state == STATE_WIN):
                self._wavespeed = self._wavespeed * 0.5
                self.waveStart()

        if(self.input.is_key_pressed('enter')):
            if(self._state == STATE_ACTIVE):
                self._state = STATE_PAUSED


        if(self._state == STATE_INACTIVE):
            self.setText("SHIP GAME! \n Press 'Space' to play", 40)

        if(self._state == STATE_NEWWAVE ):
            self._wavespeed = ALIEN_SPEED
            self._scoreUsed =0
            self._score = 0
            self._wave = Wave()
            self._state = STATE_ACTIVE

            self._source = 'background.jpg'
            self._ost = Sound('wil.wav')
            self._ost.play(True)

        if(self._state == STATE_ACTIVE):

            self._wave.update(self.input,dt,
             self._shipBoltfireSound, self._alienBoltfireSound,
             self._alienShotSound, self._shipShotSound)


        if(self._soundOn == False):
            self._shipBoltfireSound.volume = 0
            self._ost.volume = 0
            self._alienShotSound.volume = 0
            self._shipShotSound.volume = 0
            self._alienBoltfireSound.volume = 0

        if(self._soundOn):
            self._shipBoltfireSound.volume = 0.2
            self._ost.volume = 1
            self._alienShotSound.volume = 0.3
            self._shipShotSound.volume = 0.5
            self._alienBoltfireSound.volume = 1

        if(self._wave != None and self._state == STATE_ACTIVE):
            if(self._wave.getShip() == None and self._wave.getLives() > 0):
                self._state = STATE_PAUSED
            if(self._wave.getIsGameOver() and self._wave.getLives() == 0):
                self._state = STATE_LOSE
                self._wavesnow = 1

            if(self._wave.getIsGameOver() and self._wave.getLives() > 0):
                self._endWaveLives = self._wave.getLives()
                self._wavesnow = self._wavesnow + 1
                if(self._wavesnow == 4):
                    self._state = STATE_WIN
                    self._ost = Sound('Victory.mp3')
                    self._ost.play()

                if(self._state != STATE_WIN):
                    if(self._powerupson == True and self._wave.getAliensShot() >= 10):
                        self._state = STATE_POWERUP
                        self._livesAfter = self._wave.getLives()
                        self._scoreAfter = self._wave.getAliensShot()

                    if(self._state != STATE_POWERUP or self._wave.getAliensShot() < 10):
                        self._wavespeed = self._wavespeed * 0.4
                        self.waveStart()

        if(self._state == STATE_POWERUP):
            self._source = 'powerups.jpg'
            if(self._powerUpScreenSound == False):
                self._ost = Sound('powerups.mp3')
                self._ost.play(True)
                self._powerUpScreenSound = True

            if(self.input.is_key_pressed('1') and
             self._scoreAfter >= 10):
                self._usedScore = self._usedScore + 10
                self._endWaveLives = self._endWaveLives + 2
                self._livesAfter = self._livesAfter + 2
                self._scoreAfter = self._scoreAfter - 10
            if (self.input.is_key_pressed('2') and
              self._scoreAfter>= 20):
                self._usedScore = self._usedScore + 20
                self._endWaveLives = self._endWaveLives + 5
                self._livesAfter = self._livesAfter + 5
                self._scoreAfter = self._scoreAfter - 20


            if (self.input.is_key_pressed('3')  and
             self._scoreAfter >= 25):
                self._usedScore = self._usedScore + 25
                self._shipSpeed = self._shipSpeed * 1.5
                self._scoreAfter = self._scoreAfter - 25



            if( self.input.is_key_pressed('4')):
                self._wavespeed = self._wavespeed * 0.4
                self.waveStart()


        if(self.input.is_key_pressed('k')):
            if(self._state == STATE_INACTIVE or self._state == STATE_WIN):
                self._state = STATE_CREDITS
                self._ost = Sound('credits.mp3')
                self._ost.play(True)
        if(self.input.is_key_pressed('l')):
            if(self._state == STATE_CREDITS):
                self._ost = Sound('Title.mp3')
                self._ost.play()
                self._state = STATE_INACTIVE

        if(self.input.is_key_pressed('r')):
            self._powerupson = not self._powerupson

        if(self.input.is_key_pressed('j')):
            self._soundOn = not self._soundOn


#IMPLEMENT THE OTHER INIT STATS

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To
        draw a GObject g, simply use the method g.draw(self.view).  It is
        that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are
        attributes in Wave. In order to draw them, you either need to add
        getters for these attributes or you need to add a draw method to
        class Wave.  We suggest the latter.  See the example subcontroller.py
        from class.
        """
        if self._state == STATE_INACTIVE:
            self._text.draw(self.view)

            self.setOptionsLabel()
            self._powerupLabel.draw(self.view)

            self.setSeeCreditsLabel()
            self._seeCreditsLabel.draw(self.view)

            self.setBottomImage()
            self._bottomImage.draw(self.view)

        if self._state == STATE_ACTIVE:
            self.setBackground(self._source)
            self._backgroundImage.draw(self.view)

            self._wave.draw(self.view)

            self.setWaveNum(self._wavesnow)
            self._waveNum.draw(self.view)

            self.setLivesNum()
            self._livesNum.draw(self.view)

            self.setScore()
            self._score.draw(self.view)

            self.setOptionsLabel()
            self._powerupLabel.draw(self.view)

        if self._state == STATE_POWERUP:
            self.setBackground(self._source)
            self._backgroundImage.draw(self.view)
            self.setText(("Choose Your Powerup by Presssing the "
             + " Number \n \n '1' for 2 Extra Lives for 10 Points \n \n  '2' "+
              "for 5 Extra Lives for " +
              "20 points \n \n  '3' for Speed Upgrade for 25 Points " +
              "\n \n '4' Exit"),20)
            self._text.draw(self.view)

            self.setLivesNum()
            self._livesNum.draw(self.view)

            self.setScore()
            self._score.draw(self.view)

        if self._state == STATE_PAUSED:
            self.setText("Press 'Space' to Continue", 40)
            self._text.draw(self.view)

        if self._state == STATE_LOSE:
            if self._wave.getLives() > 0 and self._wavesnow == 4 :
                self.setText("Congrats You Won ! \n Press  'Space' to" +
                 ' restart', 35)
                self._text.draw(self.view)
            else:
                self.setText("You LOSE! \n Wave Number: "+
                str(self._wavesnow) + '\n Score Number: ' +
                str(self._wave.getAliensShot()) + "\n \n Press  'Space' to" +
                 ' restart', 30)
                self._text.draw(self.view)

        if self._state == STATE_CREDITS:
            self.setSeeCreditsLabel()
            self._seeCreditsLabel.draw(self.view)
            self.setcreditsLabel()
            self._creditsLabel.draw(self.view)

            text = ( 'Lead Developer of Project: Nathnael Tesfaw' +
             '\n \n Co-creator of base Game: Akmal Rupasingha' +
              '\n \n Kivy Engine from: Walter White, Cornell University ' +
             '\n \n Wave 1 Music: Willy Fortress 1 from Mega Man 2 by Capcom' +
             '\n \n Wave 2 Music: Bubble Man Stage from Mega Man 2 by Capcom' +
             '\n \n Boss Wave Music: Big Arms & Final Boss from Sonic 3 by Sega' +
             '\n \n Powerups Screen Music: Super Smash Bros Melee - ' +
             '\n All-Star Rest Area (8-Bit version) by Hat-Loving Gamer' +
             '\n \n Wave 1 Background: Pixel City With Fire And Lights by ' +
             ' \n tt.thanh.tran from WallPaper.com'+
             '\n \n Wave 2 Background:Pixel Sunset by JoshuaAkins1 from ' +
             '\n imgur.com' +
             '\n \n Wave 3 Background: kosmos-art-pikseli-8bit'+
             '\n -planeta-zvezdy-retro-grafika'+
             '\n by Kipish_fön on GoodFon.com' +
             '\n \n Trophy Photo: From Pixabay' +
             '\n \n PowerUp Screen Background: pikisuperstar from .freepik.com' +
              '\n \n Credits Music: Credits from Super Mario World by Nintendo' +
              '\n \n Victory Music: All Stage Clear from Mega Man 3 by Capcom' +
              '\n \n Title Music: Title from Mega Man 3 by Capcom')
            self.setText(text,12)
            self._text.draw(self.view)

        if(self._state == STATE_WIN):
            self.setText('YOU HAVE WON !'
             + '\n Score :' + str(self._scoreAfter) + '\n Lives :' +
            str(self._livesAfter) + '\n Press Space if You Dare Continue!', 30)
            self._text.draw(self.view)
            self.setSeeCreditsLabel()
            self._seeCreditsLabel.draw(self.view)

            self.setBottomImage()
            self._bottomImage.draw(self.view)

        # IMPLEMENT ME
        pass


    # HELPER METHODS FOR THE STATES GO HERE
    def setText(self,text,fontsize):
        """
        Sets the the Welcome Message

        Parameter text: the currently active message
        Precondition: text is a string

        Parameter fontsize: how big of a font to used
        Precondition: fontsize is an integer
        """
        assert isinstance(text,str)
        assert isinstance(fontsize,int)

        self._text = GLabel(text=text,font_size=fontsize)
        self._text.font_name = 'RetroGame.ttf'
        self._text.fillcolor = [1,1,1,0.5]
        self._text.x = GAME_WIDTH/2
        y = GAME_HEIGHT /2
        if(self._state == STATE_CREDITS):
            y = y - 50
        self._text.y = y
        self._text.halign = 'center'
        self._text.valign = 'bottom'

    def setWaveNum(self,num):
        """Sets the the Waves Number Label
        Parameter num: number of waves that have been cleared
        Precondition: num is a int or float"""

        assert isinstance(num,int) or isinstance(num,float)

        self._waveNum = GLabel(text="Wave: " + str(num),font_size=20)
        self._waveNum.font_name = 'RetroGame.ttf'
        self._waveNum.fillcolor = [0.3,0.3,0.3,0.5]
        self._waveNum.x = 0 + 100
        self._waveNum.y = GAME_HEIGHT - (ALIEN_CEILING) + 20
        self._waveNum.halign = 'center'
        self._waveNum.valign = 'middle'

    def setScore(self):
        """Sets the Score, the number of Aliens Shot"""
        if(self._state == STATE_ACTIVE):
            score = str(self._wave.getAliensShot())
        if(self._state == STATE_POWERUP):
            score = str(self._scoreAfter)

        self._score = GLabel(text="Score: " + score,font_size=20)
        self._score.font_name = 'RetroGame.ttf'
        self._score.fillcolor = [0.3,0.3,0.3,0.5]
        self._score.x = GAME_WIDTH /2
        self._score.y = GAME_HEIGHT - (ALIEN_CEILING) + 20
        self._score.halign = 'center'
        self._score.valign = 'middle'

    def setLivesNum(self):
        """Sets the the Lives Number Left"""
        if(self._state == STATE_ACTIVE):
            lives = str(self._wave.getLives())
        if(self._state == STATE_POWERUP):
            lives = str(self._livesAfter)

        self._livesNum = GLabel(text="Lives: " + lives,font_size=20)
        self._livesNum.font_name = 'RetroGame.ttf'
        self._livesNum.fillcolor = [0.3,0.3,0.3,0.5]
        self._livesNum.x = GAME_WIDTH - 100
        self._livesNum.y = GAME_HEIGHT - (ALIEN_CEILING) + 20
        self._livesNum.halign = 'center'
        self._livesNum.valign = 'middle'

    def setOptionsLabel(self):
        """Shows if Power Ups and Sound are on"""
        textp = "Press 'r' to turn off Powerups"
        if(self._powerupson == False):
            textp = "Press 'r' to turn on Powerups"
        texts = "Press 'j' to turn off Sound"
        if(self._soundOn == False):
            texts = "Press 'j' to turn on Sound"

        self._powerupLabel = GLabel(text= texts
         + '\n'+ textp,font_size=10)
        self._powerupLabel.font_name = 'RetroGame.ttf'
        fill = [0.3,0.3,0.3,0.5]
        if(self._state == STATE_INACTIVE):
            fill = [1,1,1,0.5]
        self._powerupLabel.fillcolor = fill
        self._powerupLabel.x = GAME_WIDTH - 100
        self._powerupLabel.y = DEFENSE_LINE + 40
        self._powerupLabel.halign = 'center'
        self._powerupLabel.valign = 'middle'

    def waveStart(self):
        """Starts a new modified wave"""
        self._wave = Wave(self._wavespeed, self._wavesnow -1,
         self._endWaveLives,self._usedScore,self._shipSpeed)
        self._state = STATE_ACTIVE

        if(self._wavesnow == 2 or (self._wavesnow % 2) == 0 ):
            self._ost = Sound('wave22.mp3')
            self._source = 'wave2back2.jpeg'
        if(self._wavesnow == 3 or (self._wavesnow % 3) == 0):
            self._ost = Sound('boss.mp3')
            self._source = 'background2.jpg'

        if(self._wavesnow % 3 != 0 and self._wavesnow % 2 != 0 ):
            self._ost = Sound('wil.wav')
            self._source = 'background.jpg'
        #add  others and make random?
        self._ost.play(True)
        self._powerUpScreenSound = False

    def setBackground(self,source):
        """Sets up the Background image
        Parameter source: the source for Background photo
        Precondition: source is a string"""
        assert isinstance(source,str)
        self._backgroundImage = GImage(source = source)
        self._backgroundImage.x = GAME_WIDTH /2
        self._backgroundImage.y = GAME_HEIGHT /2
        self._backgroundImage.height = GAME_HEIGHT
        self._backgroundImage.width = GAME_WIDTH
        self._backgroundImage.halign = 'center'
        self._backgroundImage.valign = 'middle'


    def setcreditsLabel(self):
        """Sets the Credits Title Label"""
        self._creditsLabel = GLabel(text= ("Credits:") ,font_size= 35)
        self._creditsLabel.font_name = 'RetroGame.ttf'
        self._creditsLabel.fillcolor = [1,1,1,0.5]
        self._creditsLabel.x = GAME_WIDTH /2
        self._creditsLabel.y = GAME_HEIGHT - ((ALIEN_CEILING) + 20)
        self._creditsLabel.halign = 'center'
        self._creditsLabel.valign = 'middle'

    def setSeeCreditsLabel(self):
        """Sets Label at the Bottom to view credits"""
        text = "Press 'k' to see Credits"
        if(self._state == STATE_CREDITS):
            text = "Press 'l' to go Back to Home Screen"

        self._seeCreditsLabel = GLabel(text= text,
            font_size=10)
        self._seeCreditsLabel.font_name = 'RetroGame.ttf'
        self._seeCreditsLabel.fillcolor = [1,1,1,0.5]
        self._seeCreditsLabel.x = GAME_WIDTH - 100
        self._seeCreditsLabel.y = DEFENSE_LINE - 75
        self._seeCreditsLabel.halign = 'center'
        self._seeCreditsLabel.valign = 'middle'
    def setBottomImage(self):
        """Sets the Bottom Image"""
        im = GImage(source = 'trophy.png')
        im.height = 110
        im.width = 60
        if(self._state == STATE_INACTIVE):
            im = GSprite(source = 'alien-strip1.png', format = (4,2))
            im.height = ALIEN_HEIGHT * 5
            im.width = ALIEN_WIDTH * 6
        im.x = GAME_WIDTH /2
        im.y = GAME_HEIGHT /4
        im.halign = 'center'
        im.valign = 'middle'
        self._bottomImage = im
