# breakout.py
# Allie Shuldman (as2594) Margaret Seeman (mes424)
# 12/4/16
"""Primary module for Breakout application

This module contains the main controller class for the Breakout application. There is no
need for any any need for additional classes in this module.  If you need more classes, 
99% of the time they belong in either the play module or the models module. If you 
are ensure about where a new class should go, 
post a question on Piazza."""
from constants import *
from game2d import *
from play import *


# PRIMARY RULE: Breakout can only access attributes in play.py via getters/setters
# Breakout is NOT allowed to access anything in models.py

class Breakout(GameApp):
    """Instance is the primary controller for the Breakout App
    
    This class extends GameApp and implements the various methods necessary for processing 
    the player inputs and starting/running a game.
    
        Method start begins the application.
        
        Method update either changes the state or updates the Play object
        
        Method draw displays the Play object and any other elements on screen
    
    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.
    
    Most of the work handling the game is actually provided in the class Play.
    Play should have a minimum of two methods: updatePaddle(input) which moves
    the paddle, and updateBall() which moves the ball and processes all of the
    game physics. This class should simply call that method in update().
    
    The primary purpose of this class is managing the game state: when is the 
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.
    
    INSTANCE ATTRIBUTES:
        view    [Immutable instance of GView; it is inherited from GameApp]:
                the game view, used in drawing (see examples from class)
        input   [Immutable instance of GInput; it is inherited from GameApp]:
                the user input, used to control the paddle and change state
        _state  [one of STATE_INACTIVE, STATE_COUNTDOWN, STATE_PAUSED, STATE_ACTIVE]:
                the current state of the game represented a value from constants.py
        _game   [Play, or None if there is no game currently active]: 
                the controller for a single game, which manages the paddle, ball, and bricks
        _mssg   [GLabel, or None if there is no message to display]
                the currently active message
    
    STATE SPECIFIC INVARIANTS: 
        Attribute _game is only None if _state is STATE_INACTIVE.
        Attribute _mssg is only None if  _state is STATE_ACTIVE or STATE_COUNTDOWN.
    
    For a complete description of how the states work, see the specification for the
    method update().
    
    You may have more attributes if you wish (you might need an attribute to store
    any text messages you display on the screen). If you add new attributes, they
    need to be documented here.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
        last_keys   [Int]: The last key that was pressed
        timer       [Int]: Keeps track of the amount of time that passes
        _score      [Label]
        _scoremssg  [GLabel]: Display's the player's current score
        _nowplaying [GLabel]: Display's the song that's currently playing
        _title      [GLabel]: Display's the title
        
    """
    
    
    # DO NOT MAKE A NEW INITIALIZER!
    
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """Initializes the application.
        
        This method is distinct from the built-in initializer __init__ (which you 
        should not override or change). This method is called once the game is running. 
        You should use it to initialize any game specific attributes.
        
        This method should make sure that all of the attributes satisfy the given 
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message 
        (in attribute _mssg) saying that the user should press to play a game."""
        
        self._state = STATE_INACTIVE
        self._game = None
        self._title = GLabel(text = 'BRICKBREAKER', font_size = 44, font_name = 'pez.ttf')
        self._title.x = GAME_WIDTH / 2.0
        self._title.y = GAME_HEIGHT * (2.0 / 3.0)
        self._mssg = GLabel(text = 'Press a key \n to start the game!',
                            halign = 'center', valign = 'middle',
                            font_size = 32, font_name = 'ArialBold.ttf')
        self._mssg.x = GAME_WIDTH / 2.0
        self._mssg.y = GAME_HEIGHT * (1.0 / 3.0)
        self.timer = 0
        self._scoremssg = None
        
        
    
    def update(self,dt):
        """Animates a single frame in the game.
        
        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Play.  The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Play object _game to play the game.
        
        As part of the assignment, you are allowed to add your own states.  However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWGAME,
        STATE_COUNTDOWN, STATE_PAUSED, and STATE_ACTIVE.  Each one of these does its own
        thing, and so should have its own helper.  We describe these below.
        
        STATE_INACTIVE: This is the state when the application first opens.  It is a 
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen.
        
        STATE_NEWGAME: This is the state creates a new game and shows it on the screen.  
        This state only lasts one animation frame before switching to STATE_COUNTDOWN.
        
        STATE_COUNTDOWN: This is a 3 second countdown that lasts until the ball is 
        served.  The player can move the paddle during the countdown, but there is no
        ball on the screen.  Paddle movement is handled by the Play object.  Hence the
        Play class should have a method called updatePaddle()
        
        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        paddle and the ball moves on its own about the board.  Both of these
        should be handled by methods inside of class Play (NOT in this class).  Hence
        the Play class should have methods named updatePaddle() and updateBall().
        
        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.
        
        The rules for determining the current state are as follows.
        
        STATE_INACTIVE: This is the state at the beginning, and is the state so long
        as the player never presses a key.  In addition, the application switches to 
        this state if the previous state was STATE_ACTIVE and the game is over 
        (e.g. all balls are lost or no more bricks are on the screen).
        
        STATE_NEWGAME: The application switches to this state if the state was 
        STATE_INACTIVE in the previous frame, and the player pressed a key.
        
        STATE_COUNTDOWN: The application switches to this state if the state was
        STATE_NEWGAME in the previous frame (so that state only lasts one frame).
        
        STATE_ACTIVE: The application switches to this state after it has spent 3
        seconds in the state STATE_COUNTDOWN.
        
        STATE_PAUSED: The application switches to this state if the state was 
        STATE_ACTIVE in the previous frame, the ball was lost, and there are still
        some tries remaining.
        
        You are allowed to add more states if you wish. Should you do so, you should 
        describe them here.
        
        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            self._checkKeyPressed(STATE_NEWGAME)
            
        if self._state == STATE_COUNTDOWN:
            self.countdown()
            
        if self._state == STATE_NEWGAME:
            self.newgame()
        
        if self._game is not None:
            self.currentgame()
            
        if self._state == STATE_ACTIVE:
            self.active()
                
        if self._state == STATE_PAUSED:
            self._checkKeyPressed(STATE_COUNTDOWN)
        
    
    def draw(self):
        """Draws the game objects to the view.
        
        Every single thing you want to draw in this game is a GObject.  To draw a GObject 
        g, simply use the method g.draw(self.view).  It is that easy!
        
        Many of the GObjects (such as the paddle, ball, and bricks) are attributes in Play. 
        In order to draw them, you either need to add getters for these attributes or you 
        need to add a draw method to class Play.  We suggest the latter.  See the example 
        subcontroller.py from class."""
        if self._state == STATE_INACTIVE:
            self._mssg.draw(self.view)
            self._title.draw(self.view)
        else:
            self._mssg = None
            self._title = None
            
        if self._state == STATE_PAUSED:
            if self._game.getTries() == 1:
                mssg = 'You now have 1 try.\n Press a key to get a new ball.'
            else:
                mssg = 'You now have ' + str(self._game.getTries()) + ' tries.\n Press a key to get a new ball.'
            pausedmssg = GLabel(text = mssg, haligh = 'center', valign = 'middle',
                                font_name = 'ArialBold.ttf')
            pausedmssg.x = GAME_WIDTH / 2.0
            pausedmssg.y = GAME_HEIGHT / 2.0
            
            pausedmssg.draw(self.view)
            
        
    
    
    # HELPER METHODS FOR THE STATES GO HERE
    def _checkKeyPressed(self, state):
        """Checks to see if a key was pressed after the welcome message was
        shown.  This determines whether or not a new game should start.
        
        Parameter state: The state the game should be changed to if a key
        was pressed.
        Precondition: state is one of the states listed in constants.py (int)
        """
        
        current_number_of_keys = self.input.key_count
        should_change = current_number_of_keys > 0 and self.last_keys == 0
        
        if should_change:
            self._state = state
        self.last_keys= current_number_of_keys
        
    def countdown(self):
        """ Helper function for update.  Resets the paddle and ball positions
        and counts down 3 seconds before changing the state to STATE_ACTIVE."""
        
        self._game.resetBall()
        self._game.resetPaddle()
        self.timer = 0
        while self.timer < 1800000:
            self.timer += 1
        self._state = STATE_ACTIVE
        
    def newgame(self):
        """ Helper function for update.  Makes a new game, creates the message
        that displays the score and the message that displays the current song
        playing.  Sets the state to STATE_COUNTDOWN when done.  """
        
        self._game = Play()
        
        self._scoremssg = GLabel(text = 'Score: ', font_size = 20, font_name = 'ArialBold.ttf')
        self._scoremssg.left = BRICK_SEP_H
        self._scoremssg.y = 10
        self._scoremssg.draw(self.view)
        
        self._nowplaying = GLabel(text = '', font_size = 15, font_name = 'ArialBold.ttf')
        self._nowplaying.y = 10
        self._nowplaying.left = GAME_WIDTH / 4.0
        self._nowplaying.draw(self.view)
        
        self._state = STATE_COUNTDOWN
        
    def active(self):
        """ Helper function for update.  While the game is occurring, the ball
        is updated.  If there is a powerup it draws the powerup to the view.  If
        the ball hits the bottom, the tries is decremented and the the state
        becomes STATE_PAUSED.  """
        
        self._game.updateBall()
        self._game.detectPowerup(self.view)
        if self._game.ballHitsBottom():
            self._game.decrementTries()
            self._state = STATE_PAUSED
            
    def currentgame(self):
        """ Helper function for update.  The paddle is updated and the game is
        drawn the view.  The score and now playing message are updated."""
        
        self._game.updatePaddle(self.input)
        self._game.draw(self.view)
        self._scoremssg.text = 'Score: ' + str(self._game.getScore())
        self._scoremssg.draw(self.view)
        
        if self._game.getSong() is not None:
            songtitle = self._game.getSong().source[:-4]
            self._nowplaying.text = 'Now playing : ' + songtitle.replace('_', ' ')
            self._nowplaying.draw(self.view)
        
        if self._game.getTries() == 0 or len(self._game.getBricks()) == 0:             
            self._state = STATE_COMPLETE
            if self._game.getTries() == 0:
                finaltext = 'GAME\nOVER'
            else:
                finaltext = 'WINNER\nWINNER\nCHICKEN\nDINNER'
            finalmssg = GLabel(text = finaltext, haligh = 'center', valign = 'middle',
                            font_size = 75, font_name = 'pez.ttf')
            finalmssg.x = GAME_WIDTH / 2.0
            finalmssg.y = GAME_HEIGHT / 2.0
            finalmssg.draw(self.view)
        
    
        
        
    
    
    
    
    
    