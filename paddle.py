from utilities import load_image, pygame, K_LEFT, K_RIGHT
from config import (
    USER_SPEED, 
    USER_SPRITE, 
    FRAMES_PER_SECOND, 
    USER_BALL_MINANGLE,
    USER_BALL_MAXANGLE
)
from math import pi, sin, cos

# ~~ Paddle () ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
class Paddle(pygame.sprite.Sprite):
    """User's paddle/ship"""

    # ~~~~ __init__() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def __init__(self, area):
    
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(USER_SPRITE)
        self.area = area
        self.speedLeft = (int(-USER_SPEED / float(FRAMES_PER_SECOND)), 0)
        self.speedRight = (int(USER_SPEED / float(FRAMES_PER_SECOND)), 0)
        self.rect.midbottom = (self.area.centerx, self.area.bottom)
        self.moving = False # flag to indicate if user is currently moving paddle
        self.paused = False # flag to indicate the paddle is paused
        self.direction = None # direction user is moving paddle\
        self.sin = sin
        self.cos = cos
        
        # calculate the minimum angle (in radians) of the ball when bouncing 
        # off the paddle
        self.ballAngleMin = USER_BALL_MINANGLE * pi / 180.
        self.ballAngleMax = USER_BALL_MAXANGLE * pi / 180.
        self.ballAngleRange = self.ballAngleMax - self.ballAngleMin
        
    
    # ~~~~ update() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def update(self):
        """Move the user's paddle if key is being pressed"""
        
        if self.paused: return
        if self.moving:
            newpos = self.rect
            
            # attempt to move left
            if self.direction == K_LEFT:
                newpos = self.rect.move(self.speedLeft)
                if newpos.left < 0: newpos = self.rect
            
            # attempt to move right
            elif self.direction == K_RIGHT:
                newpos = self.rect.move(self.speedRight)
                if newpos.right > self.area.right: newpos = self.rect
                
            self.rect = newpos
    
    
    # ~~~~ move() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def move(self, direction):
        """Update the moving attribute to indicate we should move or stop."""
        
        if direction is None: self.moving = False
        else:
            self.moving = True
            self.direction = direction
            
            
    # ~~~~ reset() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def reset(self):
        """Resets the paddle to the initial position."""
        self.rect.midbottom = (self.area.centerx, self.area.bottom)
        
    
    # ~~~~ pause() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def pause(self):
        """Pauses the paddle to prevent moving or unpauses to allow it."""
        if self.paused: self.paused = False
        else: self.paused = True
        
        
    # ~~~~ ball_effect() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def ball_effect(self, ball):
        """
        Effect of paddle on the ball when they collide. The ball bounces off
        the paddle, but the direction of the bounce depends on the position
        on the paddle that the ball hits. Hits further towards the edge 
        bounce the ball off in a more obtuse angle.
        """
        
        if not self.rect.colliderect(ball.rect): return False
        else:
            
            # get the x-position on the paddle where the ball collides to
            # determine the angle of bouncing
            ballPosition = ball.rect.centerx - self.rect.centerx
            ballPosition /= float(self.rect.right - self.rect.centerx)
            
            # determine the ball bounce angle based on its position on the paddle
            ballAngle = self.ballAngleRange*abs(1-ballPosition) + self.ballAngleMin
            
            # get the new x- and y- components of the ball's speed
            ball.speed[0] = self.cos(ballAngle) * ball.speedExact
            ball.speed[1] = self.sin(ballAngle) * ball.speedExact
            ball.speed[1] *= -1
            
            return True