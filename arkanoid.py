class Constants:
    from utilities import (
        KEYDOWN, KEYUP, K_ESCAPE, K_SPACE, QUIT, K_r, K_p, K_RETURN, K_UP, K_DOWN
    )
    from config import (
        SIZE, FRAMES_PER_SECOND, SCORE_START, SCORE_COLOR, SCORE_INCREMENT,
        SCORE_POS, TIMER_START, TIMER_SPEED, TIMER_COLOR, TIMER_POS, DIV_POS,
        DIV_COLOR, DIV_WIDTH, NAME_COLOR, NAME_POS, SCORE_SIZE, TIMER_SIZE,
        S_LABEL_TEXT, S_LABEL_POS, S_LABEL_SIZE, S_LABEL_COLOR, 
        T_LABEL_TEXT, T_LABEL_POS, T_LABEL_SIZE, T_LABEL_COLOR 
    )
    TIMER_FRAME_SPEED = TIMER_SPEED / float(FRAMES_PER_SECOND)

class Arkanoid:

    def __init__(self):
    
        from utilities import pygame, load_stages
        from text import Score, Timer, Name, Text
        from paddle import Paddle
        from ball import Ball
        from brick import Brick
        from stage import Stage
        
        C = Constants()
        self.C = C
        self.pygame = pygame

        # setup FPS governor
        self.clock = pygame.time.Clock()

        # set the window size
        divTop = int(C.DIV_POS*C.SIZE[1]) # top of divider. Affects bounds for ball
        divBot = divTop + C.DIV_WIDTH
        self.screen = pygame.display.set_mode(C.SIZE)
        area = pygame.Rect(0, divBot, C.SIZE[0], C.SIZE[1]-divBot)

        # create game screen objects/sprites
        self.score = Score(C.SCORE_POS, self.screen, C.SCORE_START, C.SCORE_COLOR, C.SCORE_SIZE)
        self.scoreText = Text(C.S_LABEL_POS, self.screen, C.S_LABEL_TEXT, C.S_LABEL_COLOR, C.S_LABEL_SIZE)
        self.timer = Timer(C.TIMER_POS, self.screen, C.TIMER_START, C.TIMER_COLOR, C.TIMER_SIZE)
        self.timerText = Text(C.T_LABEL_POS, self.screen, C.T_LABEL_TEXT, C.T_LABEL_COLOR, C.T_LABEL_SIZE)
        self.name = Name(C.NAME_POS, self.screen, '', C.NAME_COLOR)
        self.paddle = Paddle(area)
        self.ball = Ball(area)
        self.stages = load_stages(self.screen)
        self.divider = (self.screen, C.DIV_COLOR, [0, divTop], [C.SIZE[0], divTop], C.DIV_WIDTH)
        self.sprites = pygame.sprite.RenderPlain((self.paddle, self.ball))

        self.paused = True # flag to indicate if the stage is paused or moving 
        self.pausedReset = False # flag to indicate pause was due to reset, in which case dont pause timer


    # stage_event() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def stage_event(self, event):
        """Handles stage events"""
        
        C = self.C
        
        # quit the game
        if event.type == C.QUIT: return 2
        elif event.type == C.KEYDOWN:
        
            # quit the game
            if event.key == C.K_ESCAPE: return 2
            
            # move the paddle
            else: self.paddle.move(event.key)
            
        # key has been un-pressed
        elif event.type == C.KEYUP:
            
            # stop moving the paddle
            self.paddle.move(None)
        
            # reset the ball and paddle (dont reset stage)
            if event.key == C.K_r:
                self.ball.reset()
                self.paddle.reset()
                self.paused = True
                self.pausedReset = True
                
            # pause the game
            elif event.key == C.K_p:
                self.ball.pause()
                self.paddle.pause()
                if self.paused: self.paused = False
                else: self.paused = True
                
            elif event.key == C.K_SPACE:
            
                # start the stage
                if self.paused:
                    self.ball.pause()
                    if self.paddle.paused: self.paddle.pause()
                    self.paused = False
                    self.pausedReset = False
                    
        return 0
        

    # update_ball() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def update_ball(self):
        """Updates the ball and does ball related actions"""

        from brick import Brick
        
        if self.ball.inbounds:
            if (
                isinstance(self.ball.bouncedOff, Brick) and
                self.ball.bouncedOff.destroyed
            ): 
                self.score.change_by(self.ball.bouncedOff.points * self.timer.value)
                
        else: # ball went out of bounds
            self.ball.reset()
            self.paused = True
            self.pausedReset = True
        
        
    # PLAY_STAGE() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def play_stage(self, stage):
        """Plays a single stage"""
        
        C = self.C
        
        # update the ball's check surfaces
        self.ball.surfaces = set()
        self.ball.surfaces.add(self.paddle)
        self.ball.surfaces.update(stage.bricks)
        
        # update the stage name
        self.name.value = '%i: %s' % (stage.number, stage.name)
        
        # draw the stage to prepare the round
        self.timer.change_by(stage.time)
        stage.draw()
        self.pygame.draw.line(*self.divider)
        self.ball.reset()
        self.paddle.reset()
        self.sprites.draw(self.screen)
        self.pygame.display.flip()
        
        self.paused = True
        self.pausedReset = False
        
        # play the round
        while True:
        
            # Handle Input Events
            for event in self.pygame.event.get():
                returnCode = self.stage_event(event)
                if returnCode == 2: return 2
                
            # update ball
            self.update_ball()
                
            # check if the stage is complete and go to the next stage if so
            if stage.completed:
                self.ball.bouncedOff = None
                stage.paused = False
                stage.pausedReset = False
                return 0
            
            # update timer. If time has run out, you lose
            if not self.paused or self.pausedReset:
                self.timer.change_by(C.TIMER_FRAME_SPEED)
            if self.timer.exact <= 0: return 1
            
            # Draw Everything
            self.sprites.update()
            stage.update()
            stage.draw()
            self.pygame.draw.line(*self.divider)
            self.name.render()
            self.timer.render()
            self.score.render()
            self.scoreText.render()
            self.timerText.render()
            self.sprites.draw(self.screen)
            self.pygame.display.flip()
            self.clock.tick(C.FRAMES_PER_SECOND)

        
# MAIN() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def main():
    """Creates and executes Arkanoid."""
    
    from menu import StartMenu, DieMenu, WinMenu
    
    arkanoid = Arkanoid()
    
    # play the start menu
    start = StartMenu(arkanoid.screen)
    menuResult = start.play(arkanoid)
    if menuResult == 0: pass # play
    elif menuResult == 2: return # quit
    
    # play through the stages
    stageNum = 0
    while True:
    
        # play the stage
        stage = arkanoid.stages[stageNum]
        stageResult = arkanoid.play_stage(stage)

        # stage was one, proceed to next
        if stageResult == 0:
            stageNum += 1
            
            # game has been won!
            if stageNum == len(arkanoid.stages):
                win = WinMenu(arkanoid.screen)
                menuResult = win.play(arkanoid)
                if menuResult == 0: 
                    stageNum = 0
                    arkanoid = Arkanoid()
                elif menuResult == 2: return
        
        # stage was lost, decide if restarting or quitting
        elif stageResult == 1: #lost
            dead = DieMenu(arkanoid.screen)
            menuResult = dead.play(arkanoid)
            if menuResult == 0: # restart
                stageNum = 0
                arkanoid = Arkanoid()
            elif menuResult == 2: return # quit
            
        # user quit game
        elif stageResult == 2: return # quit
        
        else: raise ValueError('Unrecognized stage return code.')
    
if __name__ == '__main__': main()