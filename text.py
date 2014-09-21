from config import (
    WHITE, 
    TEXT_FONTCOLOR, 
    TEXT_FONTSIZE, 
    TEXT_FONTNAME,
    SIZE
)
from utilities import pygame

class Text:
    """Generic text to display on screen.
    
    INPUTS:
        
        position    = (top, left) position of center of text on game frame in
            proportion of the frame size, e.g. (0.1, 0.1)
            
        background  = background object on which the counter is being rendered
        
        color       = (optional) (r, g, b) color of font. Default is white.
        
        fontsize    = (optional) size of counter font. Default is 72 pixels
        
        fontname    = (optional) font name to use for text. Default is Arial
        
    OUTPUTS: Text object. See methods for more details.
    """
    
    
    
    # ~~~~ __init__() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def __init__(
        self, 
        position,
        screen,
        value='',
        color=TEXT_FONTCOLOR, 
        fontsize=TEXT_FONTSIZE, 
        fontname=TEXT_FONTNAME
    ):
        
        self.value = value
        self.screen = screen
        self.color = color
        
        # define the font, using the pygame default if the requested one is not
        # available
        fontfile = pygame.font.match_font(fontname.lower())
        self.font = pygame.font.Font(fontfile, fontsize)
        
        # define the position of the counter
        self.pos = [int(SIZE[0]*position[0]), int(SIZE[1]*position[1])]
        
        
    # ~~~~ render() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def render(self):
        """Renders the text of the counter on its screen."""
        text = self.font.render(str(self.value), 1, self.color)
        width, height = text.get_size()
        pos = [int(self.pos[0]-width/2.), int(self.pos[1]-height/2.)]
        self.screen.blit(text, pos)


class Counter(Text):
    """Generic counter to display on screen.
    
    INPUTS:
        
        position    = (top, left) position of center of text on game frame in
            proportion of the frame size, e.g. (0.1, 0.1)
            
        background  = background object on which the counter is being rendered
        
        color       = (optional) (r, g, b) color of font. Default is white.
        
        fontsize    = (optional) size of counter font. Default is 72 pixels
        
        fontname    = (optional) font name to use for text. Default is Arial
        
    OUTPUTS: Counter object. See methods for more details.
    """

    # ~~~~ change_by ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def change_by(self, amount=1):
        """Change the counter by the specified value (or default of 1)."""
        assert amount % 1 == 0, 'Change amount must be an integer.'
        self.value += amount
        
class Score(Counter): pass
class Life(Counter): pass
class Name(Text): pass