# play.py
# Allie Shuldman (as2594) Margaret Seeman (mes424)
# 12/4/16
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
        lives           [int >= 0]: The amount of tries the user has.
        score           [int >= 0]: The score.
        currentpalette  [int]: The current color scheme implemented by the bricks.
    """
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getTries(self):
        """ Returns the number of tries. """
        return self._tries
        
    def decrementTries(self):
        """ Subtracts one from the number of tries left """
        self._tries -= 1
        
    def getBricks(self):
        """ Returns the list of bricks """
        return self._bricks
        
    def getScore(self):
        """ """
        return self._score
    
    def getSong(self):
        return self._currentsong
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """ Initializer: Creates a game to play which is a subcontroller for Breakout.
        
        The number of tries is set to NUMBER_TURNS which is defined in constants.py.
        The array of bricks is initialized so that every two rows the color changes.
        The brick attributes are defined in constants.py such as the height,
        width and separation.  The paddle is made and is set up in the center.
        A new ball is also made.
        """
        self._tries = NUMBER_TURNS
        self.setupBricks()
        self.setupPowerups()
             
        #paddle
        self._paddle = Paddle((GAME_WIDTH / 2.0) - (PADDLE_WIDTH / 2.0))
        
        #ball
        self._ball = Ball()
        
        #score
        self._score = 0
        
    def setupBricks(self):
        """ Helper function for init.  Creates the array of bricks. """
        
        self._bricks = []
        self.currentpalette = BRICK_COLORS
        y = GAME_HEIGHT - BRICK_Y_OFFSET
        for a in range(BRICK_ROWS):
            x = BRICK_SEP_H / 2.0
            color = BRICK_COLORS[(a / 2) % 5]
            points = BRICK_POINTS[(a / 2) % 5]
            for b in range(BRICKS_IN_ROW):
                newbrick = Brick(x, y, color, points)
                newbrick._colorIndex = (a / 2) % 5
                self._bricks.append(newbrick)
                x = x + BRICK_WIDTH + BRICK_SEP_H
            y = y - BRICK_HEIGHT - BRICK_SEP_V
            
    def setupPowerups(self):
        """ Helper function for init.  Sets up the powerups by randomly selecting
        bricks and adding a release powerup functionality to them.  Randomly selects
        the amount of powerups to incorporate bounded between the number of rows and
        the total number of bricks.  This ensures that there are ample power ups. """
        
        self._currentsong = None    
        numberOfPowerups = random.randint(BRICK_ROWS, (BRICK_ROWS * BRICKS_IN_ROW))
        powerupbricks = []
        k = 0
        while k < numberOfPowerups:
            randbrick = random.choice(self._bricks)
            if not randbrick in powerupbricks:
                powerupbricks.append(randbrick)
                randbrick.setShouldReleasePowerup(True)
            k = k + 1
            
        self._currentpowerups = [] 
        
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    def updatePaddle(self, theinput):
        """ The paddle moves based on which arrow key.  This method also insures
        that the paddle doesn't go off the screen.
        
        Parameter theinput: User input passed by Breakout.
        Precondition: theinput is computer input."""
        
        leftpos = self._paddle.getLeft()
        if theinput.is_key_down('left'):
            leftpos -= ANIMATION_STEP
        if theinput.is_key_down('right'):
            leftpos += ANIMATION_STEP
        
        if leftpos > GAME_WIDTH - self._paddle.width:
            leftpos = min(GAME_WIDTH - self._paddle.width, leftpos)
        if leftpos < 0:
            leftpos = max(0, leftpos)
        self._paddle.setLeft(leftpos)
        
    def serveBall(self):
        """ Releases the ball from its spot in the center of the screen before
        the game starts.  This activates the game."""
        self.updateBall()
        
    def updateBall(self):
        """ Updates the ball's position.  It moves the ball and bounces
        it if needed."""
        self._ball.moveBall()
        self._ball.bounceBall()
        self.detectCollision()
        
    def updatePowerup(self, powerup):
        """ Lowers the powerup down the screen.
        
        Parameter powerup: the powerup that is moving
        Precondition: powerup is of type Powerup"""
        
        assert isinstance(powerup, Powerup)
        powerup.movePowerup()
    
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def draw(self, view):
        """Draws the paddles, ball, and bricks
        
        Paramaeter view: The current view to draw to
        Precondition: view is a GView """
        
        for brick in self._bricks:
            brick.draw(view)
        self._paddle.draw(view)
        self._ball.draw(view)
        if len(self._currentpowerups) != 0:
            for p in self._currentpowerups:
                self.updatePowerup(p)
                p.draw(view)
                if p.hitsBottom():
                    self._currentpowerups.remove(p)

    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def detectCollision(self):
        """ Detects a collision between the ball and the paddle or the ball
        and a brick.  If the ball collides with a brick, the brick is removed."""
        
        if self._paddle.collides(self._ball):
            self._ball.negateVVelocity()
            if self._paddle.collidesfourth(self._ball):
                self._ball.negateHVelocity()
        for brick in self._bricks:
            if brick.collides(self._ball):
                self.releasePowerup(brick)
                self._ball.negateVVelocity()
                self._score += brick.getWorth()
                self._bricks.remove(brick)
            
                
    def detectPowerup(self, view):
        """ Helper method for update in Breakout.  Determines if there are any
        powerups in play and delegates catching and activating the powerup. Removes
        the powerup from the list of powerups once it has been caught by the
        paddle.
        
        Parameter view: the view the game is on
        Precondition: view is of type GView"""
        
        if len(self._currentpowerups) != 0:
            for p in self._currentpowerups:
                if self._paddle.catchesPowerup(p):
                    self.activatePowerup(p, view)
                    self._currentpowerups.remove(p)
                       
     
    def ballHitsBottom(self):
        """ Determines whether or not the ball hit the bottom of the screen. """
        return self._ball.hitsBottom()
    
    
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def resetBall(self):
        """ Resets the ball to its position in the middle of the screen. """
        self._ball.x = GAME_WIDTH / 2.0
        self._ball.y = GAME_HEIGHT / 2.0
       
        
    def resetPaddle(self):
        """ Resets the paddle to its position in the middle of the screen. """
        self._paddle.x = GAME_WIDTH / 2.0
        
        
    def releasePowerup(self, brick):
        """ Releases the powerup stored in the brick if the brick's _shouldReleasePowerup
        attribute is True.  The powerup is chosen at random from the list of powerups.
        
        Parameter brick: the brick that got destroyed
        Precondition: brick is of type brick"""
        
        isinstance(brick, Brick)
        
        if brick.getShouldReleasePowerup():
            power = random.choice(POWERUPS)
            if power == POWERUP_MUSIC:
                image = random.choice(ALBUM_ART) + '.png'
            else:
                image = IMAGES[power]
            newpowerup = Powerup(brick.x, brick.y, image, power)
            self._currentpowerups.append(newpowerup)
        
        
    def activatePowerup(self, p, view):
        """ Determines the type of powerup the powerup is and calls the powerup's
        helper method.
        
        Parameter p: the powerup
        Precondition: p is of type Powerup
        
        Parameter view: the view the game is on
        Precondition: view is of type GView """
        
        assert isinstance(p, Powerup)
        
        if p.getPower() == POWERUP_COLOR:
            self.activateColorChange(view)
        elif p.getPower() == POWERUP_GROW:
            self.activateGrowPaddle()
        elif p.getPower() == POWERUP_SHRINK:
            self.activateShrinkPaddle()
        elif p.getPower() == POWERUP_SPEEDUP:
            self.activateSpeedupBall()
        elif p.getPower() == POWERUP_SLOWDOWN:
            self.activateSlowdownBall()
        elif p.getPower() == POWERUP_BOMB:
           self.activateBombBricks()
        elif p.getPower() == POWERUP_GOLD:
            self.activateGoldCoins()
        elif p.getPower() == POWERUP_MUSIC:
            self.activatePlayMusic(p)
    
    
    def activateColorChange(self, view):
        """ Activates the color change alteration.  This powerup changes the color
        scheme of the bricks randomly.  The various color schemes are listed in
        constants.py
        
        Parameter view: the view the game is on
        Precondition: view is of type GView """
        
        palette = random.choice(PALETTES)
        while self.currentpalette is palette:
            palette = random.choice(PALETTES)
        self.currentpalette = palette
        for brick in self._bricks:
            brick.fillcolor = palette[brick._colorIndex % len(palette)]
            brick.draw(view)
           
            
    def activateGrowPaddle(self):
        """ Activates the powerup that doubles the paddle width.  The paddle
        width is constricted so that even if the user has multiple grow paddle
        powerups, the paddle will not exceed PADDLE_WIDTH * 4. """
        
        if self._paddle.width < PADDLE_WIDTH * 4:
            self._paddle.width *= 2
            
            
    def activateShrinkPaddle(self):
        """ Activates the powerup the shrinks the paddle width.  The paddle width
        is constricted so that even if the user has multiple shrink paddle
        powerups, the paddle will not be smaller than PADDLE_WIDTH / 2. """
        
        if self._paddle.width >= PADDLE_WIDTH / 2:
            self._paddle.width /= 2
          
                
    def activateSpeedupBall(self):
        """ Activates the powerup that increases the ball's y velocity.  The ball's
        y velocity is incrememented by 1 in the direction it is currently traveling."""
        
        if self._ball.getVY() < 0:
            self._ball.setVY(self._ball.getVY() - 1)
        else:
            self._ball.setVY(self._ball.getVY() + 1)
          
            
    def activateSlowdownBall(self):
        """ Activates the powerup that decreases the ball's y velocty.  The ball's
        y velocity is decremented by 1 in the direction it is currently traveling.
        If the ball's y velocity is 1 or -1, the velocity does not change."""
        
        if self._ball.getVY != 1 or self.ball.getVY != -1:
            if self._ball.getVY() < 0:
                self._ball.setVY(self._ball.getVY() + 1)
            else:
                self._ball.setVY(self._ball.getVY() - 1)
               
                
    def activateBombBricks(self):
        """ Activates the powerup that randomly removes bricks.  Both the number
        of bricks and the bricks themselves are chosen at random.  The number of
        bricks is constricted to be between 1 and a fourth of the number of bricks
        currently in use. If a brick that is being removed had a powerup, it still
        releases it."""
        
        if len(self._bricks) / 4 <= 1:
            numbricks = 1
        else:
            numbricks = random.choice(range(1, len(self._bricks) / 4))
        brickstobomb = []
        for x in range(numbricks):
            randbrick = random.choice(self._bricks)
            self._bricks.remove(randbrick)
            self.releasePowerup(randbrick)
           
            
    def activateGoldCoins(self):
        """ Drops a gold coin worth 100 points.  If the user catches it, the score
        increases by 100. """
        
        self._score += 100
      
            
    def activatePlayMusic(self, p):
        """ Activate the powerup that plays music.  The song is determined by the
        powerup's icon which was determined in detectCollision in Play.
        
        Parameter p: the powerup
        Precondition: p is of type Powerup """
        
        filename = p.source[:-3] + 'wav'
        if self._currentsong is not None:
            self._currentsong.stop()
        self._currentsong = Sound(source = filename)
        self._currentsong.play()
    