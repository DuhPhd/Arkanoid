from utilities import load_image, pygame, os
from config import (
    STAGE_BG, 
    STAGE_NAME,
    STAGE_NUM,
    STAGE_CONFIG_DELIM,
    STAGE_CONFIG_COMMENT,
    STAGE_CONFIG_NAME,
    STAGE_CONFIG_NUM,
    STAGE_CONFIG_BG,
    STAGE_CONFIG_BRICK,
    STAGE_CONFIG_TIME,
    STAGE_TIME,
    STAGE_CONFIG_POWER,
    STAGE_CONFIG_PWBSP,
    SIZE
)
from brick import Brick
from powerup import BallSpeedup

class Stage:
    """
    Stage for the game, including the background and brick locations and types.
    
    INPUTS:
        
        screen      = screen/frame on which the stage will appear
        
        configFile  = (optional) input configuration file. See load_config() for 
            more details
        
    OUTPUTS: Stage object. See methods for more details.
    """
    
    
    
    # ~~~~ __init__() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def __init__(self, screen, configFile=None):
        
        self.screen = screen
        self.cfg = configFile
        self.name = STAGE_NAME
        self.number = STAGE_NUM
        self.image = pygame.Surface(SIZE).convert()
        self.image.fill(STAGE_BG)
        self.rect = self.screen.get_rect()
        self.bricks = pygame.sprite.RenderPlain()
        self.powerups = pygame.sprite.RenderPlain()
        self.time = STAGE_TIME
        self.completed = False # has stage completed?
        self.nObstacles = 0 # keeps track of number of obstacles for faster completion check
        
        # update defaults in case the configFile was already supplied
        if configFile is not None: self.load_config(configFile)

            
    # ~~~~ load_config() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def load_config(self, configFile):
        """
        Loads the stage configuration file from the specified path and updates
        stage attributes in place.
        
        INPUTS:
            configFile  = path to the config file. The configuration file is
                space delimited and each line represents a single feature of
                the stage. Blank lines are allowed. Specify features in the
                first with the feature type and then its details, with each
                detail separated by a space. The following features can be
                specified, and some are required (denoted):
                
                name: (string) name of the stage. Not currently used; required
                number: (int) order of the stage, with lower numbers first; required
                time: (int) amount of time expected to complete the stage; optional
                background: (str) path to the background image; optional
                brick: (at least one required)
                    [1] (int, int) (row, col) top-left brick centroid position in frame; required
                    [2] (int) brick life; optional
                    [3] (int) damage done to brick by ball; make 0 for obstacles; optional
                    [4] (int) number of points awarded when brick is destroyed; optional
                    [5] (str) path to the brick sprite file; optional
                power: (optional)
                    [1] (int, int) (row, col) top-left powerup centroid position in frame; required
                    [2] (str) powerup type; required; options are: {ball_speed, }
                
                An example:
                    
                    name death lazer
                    number 1
                    time 120
                    background bg.png # inside the stage folder
                    brick 100 100 3 2 1 3brick.png
                    brick 200 100 1 1
                    brick 300 200 1 0 1 obstacle.png
                    power 400 400 ball_speed
                    
        OUTPUTS: Updates the Stage object with the objects needed for the stage.
        """
        configdir = os.path.split(os.path.abspath(configFile))[0]
        cnt = 0 # line count
        with open(configFile, 'r') as fh:
            for line in fh:
                cnt += 1
                line = line.strip()
                lowered = line.lower()
                
                # skip empty lines
                if line == '': continue
                
                # skip commented lines
                if lowered.startswith(STAGE_CONFIG_COMMENT): continue
                
                # raise an error for lines with no useful information
                sLine = line.split(STAGE_CONFIG_DELIM, 1)
                if len(sLine) < 1:
                    raise ValueError('Invalid line in configuration file. Line %i' % cnt)
                    
                # parse out other valid stage configuration information
                key, line = sLine
                key = key.lower()
                
                try:
                    if key == STAGE_CONFIG_NAME: self.name = line
                    elif key == STAGE_CONFIG_NUM: self.number = int(line)
                    elif key == STAGE_CONFIG_TIME: self.time = int(line)
                    elif key == STAGE_CONFIG_BG: 
                        imagePath = os.path.join(configdir, line)
                        self.image, self.rect = load_image(imagePath)
                        
                    # load bricks
                    elif key == STAGE_CONFIG_BRICK:
                        sLine = line.split(STAGE_CONFIG_DELIM, 5)
                        optArgs = {}
                        if len(sLine) > 2: optArgs['life'] = int(sLine[2])
                        if len(sLine) > 3: optArgs['damage'] = int(sLine[3])
                        if len(sLine) > 4: optArgs['points'] = int(sLine[4])
                        if len(sLine) > 5:
                            imagePath = os.path.join(configdir, sLine[5])
                            optArgs['image'] = imagePath
                        brick = Brick(
                            (int(sLine[0]), int(sLine[1])),
                            **optArgs
                        )
                        self.bricks.add(brick)
                        if brick.damage == 0: self.nObstacles += 1
                        
                    # load powerups
                    elif key == STAGE_CONFIG_POWER:
                        sLine = line.split(STAGE_CONFIG_DELIM)
                        powerType = sLine[2]
                        if powerType == STAGE_CONFIG_PWBSP:
                            powerup = BallSpeedup((int(sLine[0]), int(sLine[1])))
                        else:
                            raise ValueError('Invalid powerup type %s' % powerType)
                        self.powerups.add(powerup)
                    
                    
                except ValueError as e:
                    print e.message
                    raise ValueError('Invalid line in configuration file. Line %i' % cnt)
                    
        # check that bricks dont overlap
        for brick1 in self.bricks:
            for brick2 in self.bricks:
                if brick1 is not brick2:
                    offsetX = brick2.rect.left - brick1.rect.left
                    offsetY = brick2.rect.top - brick1.rect.top
                    overlap = brick1.mask.overlap_area(brick2.mask, (offsetX, offsetY))
                    if overlap:
                        errMsg = ' '.join([
                            'Bricks may not overlap. Bricks at',
                            '(%i, %i)' % (brick1.rect.centerx, brick1.rect.centery),
                            'and (%i, %i).' % (brick2.rect.centerx, brick2.rect.centery)
                        ])
                        raise ValueError(errMsg)
                    
        
        
    # ~~~~ update() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def update(self):
        """
        Updates stage attributes including redrawing images and checking
        to see if the stage is finished.
        """
        self.powerups.update()
        self.draw()
        self.check_completion()
        

    # ~~~~ draw() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def draw(self):
        """
        Draws the background of the stage and any remaining bricks and powerups.
        """
        self.screen.blit(self.image, (0, 0))
        [powerup.draw(self.screen) for powerup in self.powerups]
        self.bricks.draw(self.screen)
        
        
    # ~~~~ check_completion() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def check_completion(self):
        """Checks if the user has completed the stage"""
        if len(self.bricks) == self.nObstacles: self.completed = True
        
        
    # ~~~~ reset() ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    def reset(self):
        """Resets the stage, reloading all bricks and the background."""
        self.load_config(self.cfg)