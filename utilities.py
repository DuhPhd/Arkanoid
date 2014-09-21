# import and initialize
import sys, pygame, os
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.init()

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'


# ~~ load_image() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def load_image(filepath):
    """
    Loads an image from the given file path. This code was borrowed from the
    Pygame documentation: http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
    """
    image = pygame.image.load(filepath)
    image = image.convert_alpha()
    return image, image.get_rect()

    
    
# ~~ load_sound() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def load_sound(filepath):
    """
    Loads a sound from the given file path. This code was borrowed from the
    Pygame documentation: http://www.pygame.org/docs/tut/chimp/ChimpLineByLine.html
    """
    class NoneSound:
        def play(self): pass
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()
    try:
        sound = pygame.mixer.Sound(filepath)
    except pygame.error, message:
        print 'Cannot load sound:', filepath
        raise SystemExit, message
    return sound
    
    
# ~~ load_stages() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
def load_stages(screen):
    """
    Loads stages into Stage objects from the stage folder and returns a list
    of Stages ordered by their stage number.
    
    INPUTS: screen  = the pygame screen on which Stages are drawn
    OUTPUTS: list of ordered Stages
    """
    from config import STAGE_FILE, SOURCE_DIR, STAGE_DIR
    from glob import glob
    from stage import Stage
    
    searchStr = os.path.join(SOURCE_DIR, STAGE_DIR, '*', STAGE_FILE)
    stageFiles = glob(searchStr)
    stageDict = {}
    for f in stageFiles:
        stage = Stage(screen, f)
        if stage.number in stageDict: stageDict[stage.number].append(stage)
        else: stageDict[stage.number] = [stage]
        
    stageOrder = sorted(stageDict.keys())
    stages = []
    for i in stageOrder: stages.extend(stageDict[i])
    return stages