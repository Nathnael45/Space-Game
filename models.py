"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Nathnael Tesfaw (nbt26) & Akmal Rupasingha (ar2346)
# December 11th, 2023
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    #  IF YOU ADD ATTRIBUTES, LIST THEM BELOW
    pass

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self,**keywords):
        """Initializes a Ship object """
        GImage.__init__(self,**keywords)
        self._width = SHIP_HEIGHT
        self._height = SHIP_WIDTH
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS

    def collides(self,bolt):
        """
        Returns True if the alien bolt collides with the ship

        This method returns False if bolt was fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt,Bolt)
        if(bolt.isPlayerBolt() == True):
            return False
        if self.contains([bolt.x + (bolt.width /2), bolt.y + (bolt.height /2)]):
            return True
        if self.contains([bolt.x - (bolt.width /2), bolt.y + (bolt.height /2)]):
            return True
        if self.contains([bolt.x - (bolt.width /2), bolt.y - (bolt.height /2)]):
            return True
        if self.contains([bolt.x + (bolt.width /2), bolt.y - (bolt.height /2)]):
            return True
        else:
            return False


    # COROUTINE METHOD TO ANIMATE THE SHIP

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GSprite):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    # HIDDEN ATTRIBUTES:


    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self,**keywords):
        """Initializes an Alien object """
        GSprite.__init__(self,**keywords)
        self._width = ALIEN_WIDTH
        self._height = ALIEN_HEIGHT

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt,Bolt)
        if(bolt.isPlayerBolt() == False):
            return False
        if self.contains([bolt.x + (bolt.width /2), bolt.y + (bolt.height /2)]):
            return True
        if self.contains([bolt.x - (bolt.width /2), bolt.y + (bolt.height /2)]):
            return True
        if self.contains([bolt.x - (bolt.width /2), bolt.y - (bolt.height /2)]):
            return True
        if self.contains([bolt.x + (bolt.width /2), bolt.y - (bolt.height /2)]):
            return True
        else:
            return False

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant: _velocity is an int or float

    # LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    pass

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVelocity(self):
        """Gets velocity attribute"""
        return self._velocity

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self,**keywords):
        """Initializes a Bolt object """
        GRectangle.__init__(self,**keywords)
        self._velocity = BOLT_SPEED
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

    def isPlayerBolt(self):
        """Determines if the bolt object is from a player or not

           Returns True if it is from player, False if not"""

        if self._velocity > 0:
            return True
        else:
            return False

    def changeVelocity(self):
        """Changes the velocity of the bolt object

           Each time it is called, the velocity is velocity * -1"""

        self._velocity = -1 * BOLT_SPEED

    def increaseVelocity(self):
        """Increases the velocity of bolts by multiplying by 1.25
        for the number of calls
        """
        self._velocity = self._velocity * 1.2

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
class BossAlien(Alien):
    """Subclass of the Alien class since it is the Boss Alien"""

    def __init__(self,**keywords):
        """Initializes an Alien object """
        Alien.__init__(self,**keywords)
        self.height = (ALIEN_WIDTH * 5)
        self.width  = (ALIEN_HEIGHT * 6)
        self.setHitPoints(30)


    def setHitPoints(self,hits):
        """Sets the Amount of shoots required until the Boss Alien dies
        Parameter: hits is the number of shoots required to beat a Boss Alien
        Precondition: hits is an integer"""
        assert isinstance(hits,int)
        self._hitpoints = hits

    def getHitPoints(self):
        """Returns the number of hitpoints"""
        return self._hitpoints

    def takeDamage(self):
        """Reduces hitpoints by each time called"""
        self._hitpoints = self._hitpoints -1
