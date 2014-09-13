from utilities import load_image, pygame
from config import BRICK_SPRITE

# ~~ Brick () ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
class Brick(pygame.sprite.Sprite):
    """
    Bricks that are destroyed by the ball. Bricks can also become obstacles
    by having infinite life and you can supply a custom image for different
    bricks.
    
    INPUTS:
        screen  = screen on which the brick is rendered
        
        pos     = position of the center of the Brick. Note it shouldnt touch
            other bricks
        
        life    = (optional) amount of life the brick has. Default is 1 hit.
        
        image   = (optional) image to use for the brick sprite
        
        damage  = (optional) amount of life taken off by a collision with the 
            ball
            
        points  = (optional) number of points given when the brick is destroyed
    
    OUTPUTS: A Brick object
    """

    # ~~~~ __init__() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def __init__(self, pos, life=1, image=BRICK_SPRITE, damage=1, points=1):
    
        assert life % 1 == 0, 'Brick life must be an integer.'
        
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = load_image(image)
        self.life = life
        self.rect.center = pos
        self.damage = damage
        self.destroyed = False
        self.points = points
        
    
    # ~~~~ update() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def update(self):
        """Bricks are destroyed when they run out of life"""
        if (not self.destroyed) and (self.life <= 0): self.destroy()
        
    
    # ~~~~ destroy() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def destroy(self):
       """"Destroys" a brick by removing it from the Stage.bricks group."""
       self.destroyed = True
       self.kill()
        
            
    # ~~~~ reset() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def reset(self, direction): pass
        
        
    # ~~~~ ball_effect() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def ball_effect(self, ball):
        """
        Effect of brick on the ball and vice versa when they collide. The ball
        bounces off the brick in a normal way as in a vacuum with perfect
        bouncing. Being hit by the ball reduces the brick's life.
        """
        
        if self.destroyed: return False
        elif not self.rect.colliderect(ball.rect): return False
        else:
        
            self.life -= self.damage
            self.update()
        
            # figure out which side of the brick the ball is bouncing off of
            # to determine the bouncing effect on the ball
            if ball.rect.centerx > self.rect.right: ball.speed[0] *= -1 # right side
            elif ball.rect.centerx < self.rect.left: ball.speed[0] *= -1 # left side
            if ball.rect.centery > self.rect.bottom: ball.speed[1] *= -1 # bottom
            elif ball.rect.centery < self.rect.top: ball.speed[1] *= -1 # top

            return True