from utilities import load_image, pygame
from config import BRICK_SPRITE
from math import atan2, sin, cos

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
        self.mask = pygame.mask.from_surface(self.image)
        
    
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
        else:
            
            # get the collision direction of the brick and ball
            offsetX = ball.rect.left - self.rect.left
            offsetY = ball.rect.top - self.rect.top
            leftOverlap = self.mask.overlap_area(ball.mask, (offsetX+1, offsetY))
            rightOverlap = self.mask.overlap_area(ball.mask, (offsetX-1, offsetY))
            bottomOverlap = self.mask.overlap_area(ball.mask, (offsetX, offsetY-1))
            topOverlap = self.mask.overlap_area(ball.mask, (offsetX, offsetY+1))
            dx = rightOverlap - leftOverlap
            dy = bottomOverlap - topOverlap
            
            # change ball trajectory based on collision direction
            if (dx <> 0) or (dy <> 0):
                self.life -= self.damage
                self.update()
                
                if dx == 0: ball.speed[1] = -ball.speed[1] 
                elif dy == 0: ball.speed[0] = -ball.speed[0]
                else:
                    angle = atan2(dy, dx)
                    ball.speed[0] = ball.speedExact * cos(angle)
                    ball.speed[1] = ball.speedExact * sin(angle)
                    
                return True
                
            else: return False