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
        K_SPACE,
        QUIT,
        K_r,
        K_p,
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
        LIFE_POS,
        DIV_POS,
        DIV_COLOR,
        DIV_WIDTH,
        NAME_COLOR,
        NAME_POS
    )
        
    from text import Score, Life, Name
    from paddle import Paddle
    from ball import Ball
    from brick import Brick
    from stage import Stage
    
    # setup FPS governor
    clock = pygame.time.Clock()

    # set the window size
    divTop = int(DIV_POS*SIZE[1]) # top of divider. Affects bounds for ball
    divBot = divTop + DIV_WIDTH
    screen = pygame.display.set_mode(SIZE)
    area = pygame.Rect(0, divBot, SIZE[0], SIZE[1]-divBot)
    
    # create game screen objects/sprites
    score = Score(SCORE_POS, screen, SCORE_START, SCORE_COLOR)
    life = Life(LIFE_POS, screen, LIFE_START, LIFE_COLOR)
    name = Name(NAME_POS, screen, '', NAME_COLOR)
    paddle = Paddle(area)
    ball = Ball(area)
    stages = load_stages(screen)
    divider = (screen, DIV_COLOR, [0, divTop], [SIZE[0], divTop], DIV_WIDTH)
    sprites = pygame.sprite.RenderPlain((paddle, ball))
    
    for stage in stages:
    
        # update the ball's check surfaces
        ball.surfaces = set()
        ball.surfaces.add(paddle)
        ball.surfaces.update(stage.bricks)
        
        # update the stage name
        name.value = '%i: %s' % (stage.number, stage.name)
        
        # draw the stage to prepare the round
        life.change_by(stage.lives)
        stage.draw()
        pygame.draw.line(*divider)
        ball.reset()
        paddle.reset()
        sprites.draw(screen)
        pygame.display.flip()
        paused = True # flag to indicate if the stage is paused or moving 
        
        # play the round
        while True:
        
            # Handle Input Events
            for event in pygame.event.get():
            
                # quit the game
                if event.type == QUIT: return
                elif event.type == KEYDOWN:
                
                    # quit the game
                    if event.key == K_ESCAPE: return
                    
                    # move the paddle
                    else: paddle.move(event.key)
                    
                elif event.type == KEYUP:
                
                    # reset the ball and paddle (dont reset stage)
                    if event.key == K_r:
                        ball.reset()
                        paddle.reset()
                        life.change_by(-1)
                        if life.value < 0: return
                        paused = True
                        
                    # pause the game
                    elif event.key == K_p:
                        ball.pause()
                        paddle.pause()
                        if paused: paused = False
                        else: paused = True
                        
                    elif event.key == K_SPACE:
                    
                        # start the stage
                        if paused:
                            ball.pause()
                            if paddle.paused: paddle.pause()
                            paused = False
                            
                    # move the paddle
                    paddle.move(None)
                    
                    
            # update the ball and see what action to take (restarting, scoring, etc)
            if ball.inbounds:
                if (
                    isinstance(ball.bouncedOff, Brick) and
                    ball.bouncedOff.destroyed
                ): 
                    score.change_by(ball.bouncedOff.points)
                    
            else: # ball went out of bounds
                life.change_by(LIFE_INCREMENT)
                ball.reset()
                paused = True
                if life.value < 0: return
                
            # check if the stage is complete and go to the next stage if so
            if stage.completed:
                ball.bouncedOff = None
                break
             
            # Draw Everything             
            sprites.update()
            stage.update()
            stage.draw()
            pygame.draw.line(*divider)
            name.render()
            life.render()
            score.render()
            sprites.draw(screen)
            pygame.display.flip()
            clock.tick(FRAMES_PER_SECOND)

    
if __name__ == '__main__': main()