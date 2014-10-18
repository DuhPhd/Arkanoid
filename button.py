from config import (
    WHITE, 
    BUTTON_FONTCOLOR, 
    BUTTON_FONTSIZE, 
    BUTTON_FONTNAME,
    BUTTON_HIGHLIGHTED_FONTCOLOR,
    BUTTON_ANGLE_MAX,
    BUTTON_SCALE,
    BUTTON_SPEED,
    SIZE
)
from utilities import pygame
from text import Text

class Button(Text):
    def __init__(self, *args, **kwargs):
        kwargs['color'] = BUTTON_FONTCOLOR
        kwargs['fontsize'] = BUTTON_FONTSIZE
        kwargs['fontname'] = BUTTON_FONTNAME
        Text.__init__(self, *args, **kwargs)
        self.highlighted = False
        self.angle = 0
        self.scale = 1
        self.rotdir = BUTTON_SPEED # speed and direction of rotation
    
    # ~~~~ update() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #    
    def update(self):
        if self.highlighted:
            self.color = BUTTON_HIGHLIGHTED_FONTCOLOR
            self.angle += self.rotdir
            if (self.angle > BUTTON_ANGLE_MAX) or (self.angle < -BUTTON_ANGLE_MAX):
                self.rotdir *= -1
                self.angle += self.rotdir
            self.scale = BUTTON_SCALE
        else:
            self.color = BUTTON_FONTCOLOR
            self.angle = 0
            self.scale = 1
            self.rotdir = BUTTON_SPEED
            
    # ~~~~ render() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def render(self):
        """Renders the text of the counter on its screen."""
        text = self.font.render(str(self.value), 1, self.color)
        text = pygame.transform.rotozoom(text, self.angle, self.scale)
        width, height = text.get_size()
        pos = [int(self.pos[0]-width/2.), int(self.pos[1]-height/2.)]
        self.screen.blit(text, pos)
            
    def action(self, game):
        """Action to take when the user has selected the button."""
        return 0 
        
class StartButton(Button):
    def action(self, game): return 0
    
class QuitButton(Button):
    def action(self, game): return 2