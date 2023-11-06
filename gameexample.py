import pygame
import keyboard

#Acima, vemos as bibliotecas que precisamos importar para que o nosso joguinho fosse implementado...
#Cabe salientar que, caso estes modulos nao estejam instalados ainda, voce precisara instala-los...

#Abaixo vemos funcoes lambda que retornam as coordenadas R, G e B correspondentes a algumas cores
#Utilizamos o estilo de funcoes lambda sem parametros para simularmos o efeito de variaveis finais (final)

BLUE = lambda : (0, 0, 255)
RED = lambda : (255, 0, 0)
GREEN = lambda : (0, 255, 0)
WHITE = lambda : (255, 255, 255)
BLACK = lambda : (0, 0, 0)

#Abaixo vemos as funcoes que representam as constantes com os simbolos das teclas que devem ser digitadas
#pelo usuario...

KEYUP = lambda : "w"
KEYDOWN = lambda : "x"
KEYLEFT = lambda : "a"
KEYRIGHT = lambda : "d"

#Aqui abaixo vemos as constantes que representam o estado do local ("P" se for um local livre para
#o personagem, "O" se for uma parede, ou "F" se for o local em que o personagem passara de fase)

FREEPATH = lambda : "P"
WALL = lambda : "O"
TARGET = lambda : "F"

#Abaixo, o contador de niveis do jogo, que sera incrementado cada vez que o usuario passar de fase

levelcounter = 0

#Abaixo, constantes de conveniencia.
#    KEYS retorna todas as teclas direcionais
#    AMOUNT eh a quantidade de pixels a que corresponde um lado de local "P"
#    DIMENSIONS eh o tamanho total do mapa da fase do jogo
#    RADIUS eh o raio do circulo correspondente ao nosso personagem (sempre serah o lado do local dividido
#        por dois)...

KEYS = lambda : [KEYUP (), KEYDOWN (), KEYLEFT (), KEYRIGHT ()]
AMOUNT = lambda : 10
DIMENSIONS = lambda maplist : [len (maplist) * AMOUNT (), len (maplist) * AMOUNT ()]
RADIUS = lambda : AMOUNT () // 2

#Aqui nos vemos uma funcao que retorna uma constante com o caminho dos mapas (fases) do jogo
#, e tambem a lista de listas (MAPLIST ()) que corresponde ao mapa armazenado pelo programa...

PATHFOLDER = lambda : "C:\\Users\\samue\\Software\\eclipse-workspace\\PythonParaPF\\games\\"
PF = PATHFOLDER
LEVELS = lambda : [PATHFOLDER () + "map1.txt", PATHFOLDER () + "map2.txt"]
MAPLIST = lambda file : [[c for c in str (l) if c != "\n"] for l in file if l != "\n"]

MAP = lambda levelcounter : MAPLIST (open (LEVELS () [levelcounter], "r"))

INITIALPOSITION = lambda : [RADIUS (), len (MAP (levelcounter)) * AMOUNT () - RADIUS ()]

#allowed e completed_level sao funcoes que checam respectivamente se o local eh alcancavel
#pelo personagem, e se o personagem alcancou o local que lhe permite passar de fase

allowed = lambda position, amount, maplist : maplist [position [1] // amount][position [0] // amount] in [FREEPATH (), TARGET ()]
completed_level = lambda position, amount, maplist : maplist [position [1] // amount][position [0] // amount] == TARGET ()

#Algumas funcoes de conveniencia abaixo...

inrangesub = lambda op1, op2 : op1 - op2 if op1 >= op2 else op1
inrangesum = lambda op1, op2, interval : op1 + op2 if op1 + op2 <= interval else op1

#No nosso jogo, o mapa soh serah valido se ele tiver quantidades de linhas e colunas iguais

def valid_map (maplist) :
        b = len (maplist) > 0
        if (b) :
            return len (maplist) == len (maplist [0])
        else :
            #print ("INVALID MAP! Rows and Columns have different sizes!!")
            return False;

#A classe que guarda as informacoes do nosso personagem, e implementa a logica de resposta
#do personagem ao clique nas teclas

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
        if (self.__keypressed == keyup and b) : #Aqui, por exemplo, checa se o usuario clicou no direcional para cima e se ja nao estava pressionado (caso em que o pressionar eh ignorado)
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
    def onpress (self) : #Aqui eh uma especie de "escuta" de pressionar de teclas...
        self.__pressed = False
        self.__onpresskey (self.__keys [0])
        self.__onpresskey (self.__keys [1])
        self.__onpresskey (self.__keys [2])
        self.__onpresskey (self.__keys [3])
    def getPosition (self) :
        return self.__position

def draw_map (lstmap, amount, game_surface, pygame) : #Aqui a gente desenha o mapa para o usuario (jogador)
    x, y = 0, 0
    for i in range (len (lstmap)) :
        for j in range (len (lstmap [i])) :
            if lstmap [i][j] == "O" :
                pygame.draw.rect (game_surface, BLACK (), pygame.Rect (j * amount, i * amount, amount, amount))
            elif lstmap [i][j] == "P" :
                pygame.draw.rect (game_surface, WHITE (), pygame.Rect (j * amount, i * amount, amount, amount))
            elif lstmap [i][j] == "F" :
                pygame.draw.rect (game_surface, RED (), pygame.Rect (j * amount, i * amount, amount, amount))
            x += 1
        y += 1

pygame.init()
game_on = True
mode_set = False

character = Character (INITIALPOSITION (), KEYS (), keyboard, AMOUNT (), MAP (levelcounter))
while game_on: #Aqui eh a logica de colocar o jogo para rodar... Vamos entao rodar o nosso jogo agora?!
    if character.completed_level() :
        levelcounter = levelcounter + 1
        currentmap = MAP (levelcounter)
        character = Character (INITIALPOSITION (), KEYS (), keyboard, AMOUNT (), currentmap)
        if (not valid_map (currentmap)) :
            print ("INVALID MAP!!")
        mode_set = False
    if not mode_set :
        game_surface = pygame.display.set_mode(DIMENSIONS (MAP (levelcounter)))
        mode_set = True
    colour = BLUE ()
    radius = RADIUS ()
    for e in pygame.event.get ():
        character.onpress ()
        if e.type == pygame.QUIT:
            game_on = False
    game_surface.fill(WHITE ())
    draw_map (MAP (levelcounter), AMOUNT (), game_surface, pygame)
    pygame.draw.circle (game_surface, colour, character.getPosition(), radius)
    pygame.display.flip ()
pygame.quit ()

#Na execucao, tivemos um pequeno problema de list out of range... Facilmente solucionavel... Vamos ver!