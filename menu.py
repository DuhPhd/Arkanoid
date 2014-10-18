from utilities import load_image, pygame, os
from config import (
    SIZE,
    START_BG,
    START_START_TEXT,
    START_QUIT_TEXT,
    START_TITLE,
    DIE_BG,
    DIE_RESTART_TEXT,
    DIE_QUIT_TEXT,
    DIE_TITLE,
    WIN_BG,
    WIN_TITLE
)
from button import StartButton, QuitButton
from text import Text

class StartMenu:
    """
    Start menu
    
    INPUTS:
        screen = screen being drawn to
    OUTPUTS: Start menu object. See methods for more details.
    """
    
    # ~~~~ __init__() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def __init__(self, screen):
        
        self.screen = screen
        self.image = pygame.Surface(SIZE).convert()
        self.image.fill(START_BG)
        self.rect = self.screen.get_rect()
        self.make_buttons()
        self.highlighted = 0 # index of the highlighted menu item
        self.title = Text((0.5, 0.1), self.screen, START_TITLE)

            
        
    # ~~~~ update() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def update(self):
        """
        Updates menu attributes including redrawing images and checking
        to see if the stage is finished.
        """
        [button.update() for button in self.buttons]
        

    # ~~~~ draw() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def draw(self):
        """Draws the background of the menu and buttons."""
        self.screen.blit(self.image, (0, 0))
        self.title.render()
        [button.render() for button in self.buttons]
        
        
    # ~~~~ make_buttons() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def make_buttons(self):
        """Makes the start menu buttons."""
        self.buttons = []
        self.buttons.append(StartButton((0.5, 0.5), self.screen, START_START_TEXT))
        self.buttons.append(QuitButton((0.5, 0.8), self.screen, START_QUIT_TEXT))
        
        
    # ~~~~ play() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def play(self, game):
        
        C = game.C
        self.buttons[self.highlighted].highlighted = True

        # play the round
        while True:
        
            # Handle Input Events
            for event in game.pygame.event.get():
            
                # quit the game
                if event.type == C.QUIT: return 2
                
                # take another action
                elif event.type == C.KEYDOWN:
                
                    # quit the game
                    if event.key == C.K_ESCAPE: return 2
                    
                    # move the highlighting
                    elif event.key in (C.K_UP, C.K_DOWN):
                        self.buttons[self.highlighted].highlighted = False
                        if event.key == C.K_UP: self.highlighted -= 1
                        else: self.highlighted += 1
                        if self.highlighted == -1: self.highlighted = len(self.buttons) - 1
                        elif self.highlighted == len(self.buttons): self.highlighted = 0
                        try: self.buttons[self.highlighted].highlighted = True
                        except IndexError:
                            print self.highlighted
                            raise

                # key has been un-pressed
                elif event.type == C.KEYUP:
                    
                    # take a menu choice action
                    if event.key == C.K_RETURN:
                        actionCode = self.buttons[self.highlighted].action(game)
                        
                        # run the game
                        if actionCode == 0: return 0
                        
                        # quit the game
                        elif actionCode == 2: return 2
            
            # Draw Everything
            self.update()
            self.draw()
            game.pygame.display.flip()
            game.clock.tick(C.FRAMES_PER_SECOND)
            
            
            
class DieMenu(StartMenu):
    
    def __init__(self, *args, **kwargs):
        StartMenu.__init__(self, *args, **kwargs)
        self.image.fill(DIE_BG)
        self.title.value = DIE_TITLE
        self.buttons[0].value = DIE_RESTART_TEXT
        self.buttons[1].value = DIE_QUIT_TEXT
        
        
class WinMenu(DieMenu):
    def __init__(self, *args, **kwargs):
        DieMenu.__init__(self, *args, **kwargs)
        self.image.fill(WIN_BG)
        self.title.value = WIN_TITLE
        