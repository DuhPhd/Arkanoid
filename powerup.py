from utilities import load_image, pygame, os
from config import (
    SIZE,FRAMES_PER_SECOND, PU_BALL_SP_IMAGE, PU_BALL_SP_SPEED, 
    PU_BALL_SP_TIME, SOURCE_DIR, IMAGE_DIR, BALL_SPEED, PU_TIME,
    PU_IMAGE
)

class Powerup(pygame.sprite.Sprite):
    """
    Generic Powerup
    
    INPUTS:
        pos     = position of the center of the Powerup on the screen
        
        image   = (optional) image to use for the powerup sprite
        
        time    = (optional) length of time the powerup lasts
    
    OUTPUTS: A Powerup
    """
    
    # ~~~~ __init__() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def __init__(self, pos, image=PU_IMAGE, time=PU_TIME):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        imagePath = os.path.join(SOURCE_DIR, IMAGE_DIR, image)
        self.image, self.rect = load_image(imagePath)
        self.time = time*FRAMES_PER_SECOND
        self.rect.center = pos
        self.mask = pygame.mask.from_surface(self.image)
        self.activated = False
        self.ball = None
        
        
    # ~~~~ update() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #    
    def update(self):
        
        # decrement timer life until the timer runs out
        if self.activated: self.time -= 1
        if self.time < 0: self.destroy(False)

        
        
    # ~~~~ destroy() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def destroy(self, reset):
        """
        Destroys" a powerup by removing it from the Stage.powerups group.
        Also restores ball's properties.
        """
        self.ball.surfaces.remove(self)
        self.kill()
        
    
    # ~~~~ draw() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #    
    def draw(self, screen):
        if not self.activated: screen.blit(self.image, self.rect)
        
        
    # ~~~~ activate() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def activate(self, ball):
        """
        Tests for collision between the powerup and ball. Activates upon
        collision.
        """
        if self.activated: return False
        offsetX = ball.rect.left - self.rect.left
        offsetY = ball.rect.top - self.rect.top
        if self.mask.overlap(ball.mask, (offsetX, offsetY)) is None: return False
        else:
            self.activated = True
            return True
            
            
    # ~~~~ ball_effect() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def ball_effect(self, ball):
        """
        Effect of powerup on the ball and vice versa when they collide. The 
        ball passes through powerups, but activates them when it does so.
        Activation makes a powerup invisible until it is destroyed.
        """
        if self.activate(ball): pass
        return False
        
        
class BallPowerup(Powerup):
    """
    Ball Powerups. Adds some ball-specific actions to the Powerup object.
    
    INPUTS:
        pos     = position of the center of the Powerup on the screen
        
        image   = (optional) image to use for the powerup sprite
        
        time    = (optional) length of time the powerup lasts
        
        speed   = (optional) speedfactor increase for the ball
    
    OUTPUTS: A BallPowerup object
    """

    # ~~~~ restore_ball() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def restore_ball(self, reset):
        """
        Restores a ball's properties when the powerup ends. Does nothing if
        the ball reset itself. In the generic BallPowerup class, does nothing.
        """
        
        if not reset: pass
        
        
    # ~~~~ destroy() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def destroy(self, reset):
        """
        Destroys" a powerup by removing it from the Stage.powerups group.
        Also restores ball's properties.
        """
        self.restore_ball(reset)
        self.ball.surfaces.remove(self)
        self.kill()
    
    
    

        
class BallSpeedup(BallPowerup):
    """
    Speeds up the ball
    
    INPUTS:
        pos     = position of the center of the Powerup on the screen
        
        image   = (optional) image to use for the powerup sprite
        
        time    = (optional) length of time the powerup lasts
        
        speed   = (optional) speedfactor increase for the ball
    
    OUTPUTS: A BallSpeedup object
    """
    
    # ~~~~ __init__() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def __init__(
        self, pos, image=PU_BALL_SP_IMAGE, time=PU_BALL_SP_TIME, 
        speed=PU_BALL_SP_SPEED
    ):
        BallPowerup.__init__(self, pos, image, time)
        self.speed = PU_BALL_SP_SPEED
        
        
    # ~~~~ restore_ball() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def restore_ball(self, reset):
        """
        Restores a ball's properties when the powerup ends. Does nothing if
        the ball reset itself.
        """
        if not reset:
           self.ball.speed[0] /= self.speed
           self.ball.speed[1] /= self.speed
           self.ball.speedExact /= self.speed
            
        
    # ~~~~ ball_effect() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def ball_effect(self, ball):
        """
        Effect of powerup on the ball and vice versa when they collide. The 
        ball passes through powerups, but activates them when it does so.
        Activation makes a powerup invisible until it is destroyed.
        """
        
        if self.activated: return False
        
        # see if the ball hit the powerup, in which case we activate it
        offsetX = ball.rect.left - self.rect.left
        offsetY = ball.rect.top - self.rect.top
        if self.mask.overlap(ball.mask, (offsetX, offsetY)) is None: return False
        
        self.activated = True
        self.ball = ball
        
        # change ball properties
        self.ball.speed[0] *= self.speed
        self.ball.speed[1] *= self.speed
        self.ball.speedExact *= self.speed
        
        return False