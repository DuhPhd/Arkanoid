# PLAY_STAGE() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def play_stage(stage):
    """ main"""


# MAIN() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def main():
    """Creates and executes Arkanoid."""
    
    from utilities import (
        pygame, 
        KEYDOWN, 
        KEYUP, 
        K_ESCAPE, 
        QUIT,
        load_stages
    )
    from config import (
        SIZE,
        FRAMES_PER_SECOND,
        SCORE_START,
        SCORE_COLOR,
        SCORE_INCREMENT,
        SCORE_POS,
        LIFE_START,
        LIFE_COLOR,
        LIFE_INCREMENT,
        LIFE_POS
    )
        
    from counter import Score, Life
    from paddle import Paddle
    from ball import Ball
    from brick import Brick
    from stage import Stage
    
    # setup FPS governor
    clock = pygame.time.Clock()

    # set the window size
    screen = pygame.display.set_mode(SIZE)
    area = pygame.display.get_surface().get_rect()
    
    # create game screen objects/sprites
    score = Score(SCORE_POS, screen, SCORE_START, SCORE_COLOR)
    life = Life(LIFE_POS, screen, LIFE_START, LIFE_COLOR)
    paddle = Paddle(area)
    ball = Ball(area)
    stages = load_stages(screen)
    sprites = pygame.sprite.RenderPlain((paddle, ball))
    
    for stage in stages:
    
        # update the ball's check surfaces
        ball.surfaces = set()
        ball.surfaces.add(paddle)
        ball.surfaces.update(stage.bricks)
        
        # draw the stage to prepare the round
        stage.draw()
        ball.reset()
        paddle.reset()
        sprites.draw(screen)
        pygame.display.flip()
        
        # play the round
        while True:
        
            # Handle Input Events
            for event in pygame.event.get():
                if event.type == QUIT: return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE: return
                    paddle.move(event.key)
                elif event.type == KEYUP:
                    paddle.move(None)
                    
            # update the ball and see what action to take (restarting, scoring, etc)
            if ball.inbounds:
                if (
                    isinstance(ball.bouncedOff, Brick) and \
                    ball.bouncedOff.destroyed
                ): 
                    score.change_by(ball.bouncedOff.points)
            else: # ball went out of bounds
                life.change_by(LIFE_INCREMENT)
                ball.reset()
                if life.count < 0: return
                
            # check if the stage is complete and go to the next stage if so
            if stage.completed: break
             
            # Draw Everything             
            sprites.update()
            stage.update()
            stage.draw()
            life.render()
            score.render()
            sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FRAMES_PER_SECOND)

    
if __name__ == '__main__': main()