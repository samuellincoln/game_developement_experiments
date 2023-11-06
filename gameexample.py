import pygame
import keyboard

BLUE = lambda : (0, 0, 255)
RED = lambda : (255, 0, 0)
GREEN = lambda : (0, 255, 0)
WHITE = lambda : (255, 255, 255)
BLACK = lambda : (0, 0, 0)

KEYUP = lambda : "w"
KEYDOWN = lambda : "x"
KEYLEFT = lambda : "a"
KEYRIGHT = lambda : "d"

levelcounter = 0

KEYS = lambda : [KEYUP (), KEYDOWN (), KEYLEFT (), KEYRIGHT ()]
AMOUNT = lambda : 10
DIMENSIONS = lambda maplist : [len (maplist) * AMOUNT (), len (maplist) * AMOUNT ()]
RADIUS = lambda : AMOUNT () // 2

PATHFOLDER = lambda : "C:\\Users\\samue\\Software\\eclipse-workspace\\PythonParaPF\\games\\"
PF = PATHFOLDER
LEVELS = lambda : [PATHFOLDER () + "map1.txt", PATHFOLDER () + "map2.txt"]
MAPLIST = lambda file : [[c for c in str (l)] for l in file]

MAP = lambda levelcounter : MAPLIST (open (LEVELS () [levelcounter], "r"))

INITIALPOSITION = lambda : [RADIUS (), len (MAPLIST (open (LEVELS () [levelcounter], "r"))) * AMOUNT () - RADIUS ()]

allowed = lambda position, amount, maplist : maplist [position [1] // amount][position [0] // amount] in ["P", "F"]
completed_level = lambda position, amount, maplist : maplist [position [1] // amount][position [0] // amount] == "F"

inrangesub = lambda op1, op2 : op1 - op2 if op1 >= op2 else op1
inrangesum = lambda op1, op2, interval : op1 + op2 if op1 + op2 <= interval else op1

class Character :
    def __init__ (self, position, keys, keyboard, amount, maplist):
        self.__position, self.__keys = position, keys
        self.__keyboard, self.__pressed = keyboard, False
        self.__amount = amount
        self.__maplist = maplist
        self.__levelup = False
    def allowed (self, nextposition) :
        return allowed (nextposition, self.__amount, self.__maplist)
    def completed_level (self) :
        am = self.__amount
        b = self.__position [0] // am < 0 or self.__position [1] // am < 0
        b2 = self.__position [0] // am >= len (self.__maplist) or self.__position [1] // am >= len (self.__maplist)
        return False if b or b2 else completed_level (self.__position, self.__amount, self.__maplist)
    def update (self, key):
        self.__keypressed = key
        keyup, keydown = self.__keys [0], self.__keys [1]
        keyleft, keyright = self.__keys [2], self.__keys [3]
        b, self.__pressed = not self.__pressed, True
        if (self.__keypressed == keyup and b) :
            next_position = [self.__position [0], inrangesub (self.__position [1] , self.__amount)]
            self.__position = next_position if self.allowed (next_position) else self.__position
        elif (self.__keypressed == keydown and b) :
            next_position = [self.__position [0], inrangesum (self.__position [1] , self.__amount, DIMENSIONS (self.__maplist) [0])]
            self.__position = next_position if self.allowed (next_position) else self.__position
        elif (self.__keypressed == keyleft and b) :
            next_position = [inrangesub (self.__position [0] , self.__amount), self.__position [1]]
            self.__position = next_position if self.allowed (next_position) else self.__position
        elif (self.__keypressed == keyright and b) :
            next_position = [inrangesum (self.__position [0] , self.__amount, DIMENSIONS (self.__maplist) [0]), self.__position [1]]
            self.__position = next_position if self.allowed (next_position) else self.__position
        else :
            self.__pressed = True
    def __onpresskey (self, k):
        keyboard.on_press_key (k, lambda _: self.update (k))
    def onpress (self) :
        self.__pressed = False
        self.__onpresskey (self.__keys [0])
        self.__onpresskey (self.__keys [1])
        self.__onpresskey (self.__keys [2])
        self.__onpresskey (self.__keys [3])
    def getPosition (self) :
        return self.__position

def draw_map (lstmap, amount, screen, pygame) :
    x, y = 0, 0
    for i in range (len (lstmap)) :
        for j in range (len (lstmap [i])) :
            if lstmap [i][j] == "O" :
                pygame.draw.rect (screen, BLACK (), pygame.Rect (j * amount, i * amount, amount, amount))
            elif lstmap [i][j] == "P" :
                pygame.draw.rect (screen, WHITE (), pygame.Rect (j * amount, i * amount, amount, amount))
            elif lstmap [i][j] == "F" :
                pygame.draw.rect (screen, RED (), pygame.Rect (j * amount, i * amount, amount, amount))
            x += 1
        y += 1

pygame.init()
running = True
mode_set = False

character = Character (INITIALPOSITION (), KEYS (), keyboard, AMOUNT (), MAP (levelcounter))
while running:
    if character.completed_level() :
        levelcounter = levelcounter + 1
        character = Character (INITIALPOSITION (), KEYS (), keyboard, AMOUNT (), MAP (levelcounter))
        mode_set = False
    if not mode_set :
        screen = pygame.display.set_mode(DIMENSIONS (MAP (levelcounter)))
        mode_set = True
    colour = BLUE ()
    radius = RADIUS ()
    for event in pygame.event.get ():
        character.onpress ()
        if event.type == pygame.QUIT:
            running = False
    screen.fill(WHITE ())
    draw_map (MAP (levelcounter), AMOUNT (), screen, pygame)
    pygame.draw.circle (screen, colour, character.getPosition(), radius)
    pygame.display.flip ()
pygame.quit ()
