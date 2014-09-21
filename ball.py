from config import (
    BALL_SPEED, 
    BALL_SPRITE,
    BALL_SOUND, 
    FRAMES_PER_SECOND, 
    BALL_POS
)
from utilities import pygame, load_sound, load_image


# ~~ BALL() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
class Ball(pygame.sprite.Sprite):
    """Bouncing ball sprite."""

    # ~~~~ __init__() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def __init__(self, area, surfaces=set()):
        
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(BALL_SPRITE)
        self.area = area
        self.speedFactor = 1. / FRAMES_PER_SECOND
        self.speed = [0, 0]
        self.speedExact = 0 # speed the ball should be going in pixels/frame
        self.reset()
        self.ballHitSound = load_sound(BALL_SOUND)
        self.surfaces = surfaces
        self.bouncedOff = None # object that the ball last bounced off
        self.inbounds = True # flag to indicate if the ball is out-of-bounds
        self.mask = pygame.mask.from_surface(self.image)
    
    
    # ~~~~ update() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def update(self):
        """Moves the ball, including bouncing."""
        
        self.rect = self.rect.move(self.speed)
        return self.bounce()
        
        
    # ~~~~ bounce() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def bounce(self):
        """Bounces the ball off surfaces."""
        
        self.bouncedOff = None
        
        # first check if the ball out of bounds
        bounced = False
        if self.rect.bottom > self.area.bottom: 
            self.inbounds = False
            return
            
        # check for bounces off the screen sides
        elif self.rect.top < self.area.top:
            self.speed[1] *= -1
            bounced = True
        
        if self.rect.left < self.area.left:
            self.speed[0] *= -1
            bounced = True
            
        elif self.rect.right > self.area.right:
            self.speed[0] *= -1
            bounced = True
            
        if bounced:
            self.bouncedOff = self.area
            return
            
            
        # check for bounces off all other objects included in surfaces[] until
        # one surface is bounced off of
        for surface in self.surfaces:
            if surface.ball_effect(self):
                self.bouncedOff = surface
            
        
        
    # ~~~~ reset() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #    
    def reset(self):
        """
        Resets the ball's position and speed.
        """
        # set the initial direction and speed
        self.speed = [0, -BALL_SPEED*self.speedFactor]
        self.speedExact = BALL_SPEED*self.speedFactor
        
        # set the position back to the center
        self.rect.center = [
            int(self.area.width*BALL_POS[0]), 
            int(self.area.height*BALL_POS[1])
        ]
        self.inbounds = True