# models.py
# Allie Shuldman (as2594) Margaret Seeman (mes424)
# 12/4/16
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setLeft(self, x):
        """ Setter that sets the left attribute of the paddle to x.
        
        Parameter x: the x coordinate for the left edge of the paddle.
        Precondition: x is an int """
        
        assert type(x) == int or type(x) == float
        self.left = x
    
    def getLeft(self):
        """ Getter that returns the left attribute of the paddle. """
        
        return self.left
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self, x):
        """
        Initializer:  Creates a paddle.  The y coordinate is automatically set
        as the PADDLE_OFFSET value specified in constants.py.  The width and height
        are also automatically set by PADDLE_WIDTH and PADDLE_HEIGHT respectively
        which are defined in constants.py.  The fill color is set to black.  The
        only variable that changes is the x coordinate which is specified by
        the paramter.
        
        Parameter x: The x coordinate of the paddle
        Precondition: x is a number (int or float)
        """
        
        assert type(x) == int or type(x) == float
        GRectangle.__init__(self, left = x, y = PADDLE_OFFSET, width = PADDLE_WIDTH,
                            height = PADDLE_HEIGHT, fillcolor = colormodel.BLACK)
    
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def collides(self, ball):
        """ Checks to see if the ball collides with the paddle by checking
        the bottom corners of the rectangle defined by the radius and current
        coordinates of the ball.
        
        Parameter ball: The ball used in the current game
        Precondition: ball is of type Ball
        """
        
        assert isinstance(ball, Ball)
        #checks bottom left corner
        if self.contains(ball.x - BALL_RADIUS, ball.y - BALL_RADIUS):
            return True
        
        #checks bottom right corner
        if self.contains(ball.x + BALL_RADIUS, ball.y - BALL_RADIUS):
            return True
        
        #checks center
        if self.contains(ball.x, ball.y - BALL_RADIUS):
            return True
        
        return False
    
    def collidesfourth(self, ball):
        """
        Returns True if the ball collides with either the left fourth or
        the right fourth of the paddle approaching from the left side or right
        side respectively.
        
        Parameter ball: The ball used in the current game
        Precondition: ball is of type Ball
        """
        
        assert isinstance(ball, Ball)
        #check left fourth
        leftcoord = self.left
        rightcoord = self.left + (self.width / 4.0)
        if ((leftcoord <= (ball.x - BALL_RADIUS) <= rightcoord
            or leftcoord <= (ball.x + BALL_RADIUS) <= rightcoord)
            and ball.getVX() > 0):
            return True
        
        #check right fourth
        leftcoord = (self.left + self.width) - (self.width / 4.0)
        rightcoord = self.left + self.width
        if ((leftcoord <= ball.x - BALL_RADIUS <= rightcoord
            or leftcoord <= ball.x + BALL_RADIUS <= rightcoord)
            and ball.getVX() < 0):
            return True
        
        return False
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def catchesPowerup(self, powerup):
        """ Returns true of the paddle 'catches' the powerup.  The paddle can
        catch the powerup by touching either the bottom, left, or right side.
        Each side has three points that are checked: the ends and the midpoint.
        
        Parameter powerup: the powerup that is falling
        Precondition: powerup is of type Powerup """
        
        assert isinstance(powerup, Powerup)
        #bottom left corner
        if self.contains(powerup.x - (POWERUP_WIDTH / 2.0), powerup.y - (POWERUP_WIDTH / 2.0)):
            return True
        
        #bottom right corner
        if self.contains(powerup.x + (POWERUP_WIDTH / 2.0), powerup.y - (POWERUP_WIDTH / 2.0)):
            return True
        
        #bottom center
        if self.contains(powerup.x, powerup.y - (POWERUP_WIDTH / 2.0)):
            return True
        
        #top left corner
        if self.contains(powerup.x - (POWERUP_WIDTH / 2.0), powerup.y + (POWERUP_WIDTH / 2.0)):
            return True
        
        #left center
        if self.contains(powerup.x - (POWERUP_WIDTH / 2.0), powerup.y):
            return True
        
        #top right corner
        if self.contains(powerup.x + (POWERUP_WIDTH / 2.0), powerup.y  + (POWERUP_WIDTH / 2.0)):
            return True
        
        #right center
        if self.contains(powerup.x + (POWERUP_WIDTH / 2.0), powerup.y):
            return True
        
        return False

class Brick(GRectangle):
    """An instance is the a brick.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _points                 [int]:  the number of points the brick is worth
        _shoudldReleasePowerup  [Boolean]: True if the brick should release
                                a powerup, False if it shouldn't.
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getWorth(self):
        """ Getter that returns the points the brick is worth if it is hit by
        the ball. """
        
        return self._points
    
    def getShouldReleasePowerup(self):
        """ Getter that returns the _shouldReleasePowerup attribute """
        
        return self._shouldReleasePowerup
    
    def setShouldReleasePowerup(self, boolean):
        """ Setter that sets the _shouldReleasePowerup attribute.
        
        Parameter boolean: True if the attribute should be true, false otherwise
        Precondition: boolean is of type bool"""
        
        assert type(boolean) == bool
        self._shouldReleasePowerup = boolean
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self, xcoord, ycoord, color, worth):
        """
        Initializer: Creates a single brick as a GRectangle.  The width and height
        are specified by BRICK_WIDTH and BRICK_HEIGHT in constants.py.  The line
        width is automatically set to 0.
        
        Parameter xcoord: The left edge coordinate.
        Precondition: xcoord is a number (int or float)
        
        Parameter ycoord: The y coordinate of the center.
        Precondition: ycoord is a number (int or float)
        
        Parameter color: The color of the brick.
        Precondition: color is a colormodel object
        
        Parameter worth: the amount of points the brick is worth
        Precondition: worth is an int > 0
        """
        
        assert type(xcoord) == int or type(xcoord) == float
        assert type(ycoord) == int or type(ycoord) == float
        assert type(worth) == int
        assert worth > 0
        GRectangle.__init__(self, left = xcoord, y = ycoord, width = BRICK_WIDTH,
                          height = BRICK_HEIGHT, linewidth = 0, fillcolor = color)
        self._points = worth
        self._shouldReleasePowerup = False
        self._colorIndex = 0
    
    # METHOD TO CHECK FOR COLLISION
    def collides(self,ball):
        """Returns: True if the ball collides with this brick.
        
        Parameter ball: The ball to check
        Precondition: ball is of class Ball"""
        
        assert isinstance(ball, Ball)
        #checks top left corner
        if self.contains(ball.x - (BALL_RADIUS), ball.y + (BALL_RADIUS)):
            return True
        
        #checks top right corner
        if self.contains(ball.x + BALL_RADIUS, ball.y + BALL_RADIUS):
            return True
        
        #checks bottom left corner
        if self.contains(ball.x - BALL_RADIUS, ball.y - BALL_RADIUS):
            return True
        
        #checks bottom right corner
        if self.contains(ball.x + BALL_RADIUS, ball.y - BALL_RADIUS):
            return True
            
        return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    

class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getVX(self):
        """ Getter that returns the x direction velocity. """
        
        return self._vx
    
    def getVY(self):
        """ Getter that returns the y velocity of the ball. """
        
        return self._vy
    
    def setVY(self, val):
        """ Setter that sets the y velocity of the ball to val.
        
        Parameter val: the value to set the velocity to
        Precondition: val is an int or float. """
        
        assert type(val) == int or type(val) == float
        self._vy = val
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self):
        """
        Ininitializer: Creates a ball object.  The diameter of the ball is
        defined in constants.py.  The ball is automatically black and placed in
        the middle of the screen.  The ball has randomized x velocity between the
        values of either positive or negative 1.0 and 5.0 and y velocity as -5.0
        meaning it is going in the downward direction.
        """
        GEllipse.__init__(self, x = GAME_WIDTH /2.0, y = GAME_HEIGHT / 2.0,
                          fillcolor = colormodel.BLACK, width = BALL_DIAMETER,
                          height = BALL_DIAMETER)
        self._vx = random.uniform(1.0,3.0) 
        self._vx = self._vx * random.choice([-1, 1])
        self._vy = -5.0
    
    
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def moveBall(self):
        """ The ball is moved by one velocity value. """
        self.x = self.x + self._vx
        self.y = self.y + self._vy
    
    
    def bounceBall(self):
        """ If the ball touches the top wall, its y velocity is flipped.  If
        the ball touches a side wall, its x velocity is flipped.  This creates
        the 'bouncing' illusion. """
        
        #top
        if self.top >= GAME_HEIGHT:
            self._vy = -self._vy
            
        #right
        if self.right >= GAME_WIDTH:
            self._vx = -self._vx
            
        #left
        if self.left <= 0:
            self._vx = -self._vx
            
    def hitsBottom(self):
        """ Returns true if the ball hits the bottom. False otherwise. """
        if self.bottom <= 0:
            return True
        return False
        
        
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def negateVVelocity(self):
        """ Helper function to negate the vertical velocity of the ball.  """
        self._vy = -self._vy
        
    def negateHVelocity(self):
        """ Helper function to negate the horizontal velocity of the ball.  """
        self._vx = -self._vx


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
class Powerup(GImage):
    """ Instance is a powerup that alter for the game.
    
    INSTANCE ATTRIBUTES:
        _vy     [int or float]: Velocity in y direction 
        _power   [int]: An int (from constant.py) that specifies which powerup it is
    
    """
    
    def getPower(self):
        """ Getter that returns the power constant. """
        
        return self._power
    
    def __init__(self, xcoord, ycoord, image, power):
        """ Initializer: Creates a powerup object which is essencially an image
        but has two attributes, its y velocity and power.  The left and y attributes
        when initialized should be the same as the brick it comes from.  _vy is
        automatically set as 3.0 in the downward direction (so techincally -3.0).
        power is the integer constant that represents a certain alteration to
        the game.
        
        Parameter xcoord: the coordinate for the left edge of the powerup
        Precondition: xcoord is an int or a float.
        
        Parameter ycoord: the y coordinate for the center of the powerup
        Precondition: ycoord is an int or float.
        
        Parameter image: the image that is the icon for the powerup
        Precondition: image is a nonempty string with the suffix .png
        
        Parameter power: the alteration to the game
        Precondition: power is an int
        """
        
        assert type(xcoord) == int or type(xcoord) == float
        assert type(ycoord) == int or type(ycoord) == float
        assert type(image) == str
        assert type(power) == int
        GImage.__init__(self, left = xcoord, y = ycoord, width = POWERUP_WIDTH,
                        height = POWERUP_WIDTH, source = image)
        self._vy = -3.0
        self._power = power
    
    def movePowerup(self):
        """ The ball is moved by one velocity value. """
        self.y = self.y + self._vy
        
    def hitsBottom(self):
        """ Returns true if the powerup hits the bottom. False otherwise. """
        if self.bottom <= 0:
            return True
        return False
        





