import pygame
import random
import math
import pickle
import time
from pygame.locals import *
limit = lambda maxval, minval, value: max(min(maxval, value), minval)
pack = "Assets/"

'''

This is a comment group.

(✿◠‿◠)

'''
random.seed(0)

BRUSH = 3

winsize = [500, 500]
pygame.init()
WIN = pygame.display.set_mode(winsize, RESIZABLE)

logo = pygame.image.load(pack + "GUIs/Logo.png")
otherlogo = pygame.image.load(pack + "GUIs/Other logo.png")

clock = pygame.time.Clock()

pygame.font.init()

FONT = pygame.font.Font(pack + "Font.ttf", 25)

def drawfont(text, pos):
    # Text is "FONT.render(f"And he said, \"Hi. (:\"", 1, (255, 255, 255))"
    WIN.blit(text, pos)

pygame.display.set_caption("SPRINGFEET")

def blit_alpha(target, source, location, opacity):
        x = location[0]
        y = location[1]
        temp = pygame.Surface((source.get_width(), source.get_height())).convert()
        temp.blit(target, (-x, -y))
        temp.blit(source, (0, 0))
        temp.set_alpha(limit(255, 0, opacity))
        
        target.blit(temp, location)
done = False
class Mouse():
    def __init__(self) -> None:
        self.leftMiddleRight = pygame.mouse.get_pressed()
        self.left = self.leftMiddleRight[0]
        self.right = self.leftMiddleRight[2]
        self.middle = self.leftMiddleRight[1]
        self.leftclick = False
        self.onetimeplaceholder = True

        self.pos = pygame.mouse.get_pos()
        self.x, self.y = self.pos
    
    def update(self):
        self.leftMiddleRight = pygame.mouse.get_pressed()
        self.left = self.leftMiddleRight[0]
        self.right = self.leftMiddleRight[2]
        self.middle = self.leftMiddleRight[1]
        self.down = self.left or self.middle or self.right

        if self.left and self.onetimeplaceholder:
            self.leftclick = True
            self.onetimeplaceholder = False
        else:
            self.leftclick = False
        if not self.left:
            self.onetimeplaceholder = True

        self.pos = pygame.mouse.get_pos()
        self.x, self.y = self.pos
MOUSE = Mouse()

class Button:
    def __init__(self) -> None:
        self.image = {
            "idle": pygame.image.load(pack + "GUIs/Buttons/idle.png"),
            "mousehover": pygame.image.load(pack + "GUIs/Buttons/hover.png"),
            "idlepushed": pygame.image.load(pack + "GUIs/Buttons/idlepushed.png"),
            "mousehoverpushed": pygame.image.load(pack + "GUIs/Buttons/hoverpushed.png"),
        }
        self.buttons = []
        self.menucurrent = 1
    
    def create(self, text, x, y, sizex, sizey, type, menu, action):
        
        self.buttons.append(
            {
             "pos": (x, y),
             "size": (sizex, sizey),
             "text": text,
             "rotationboost": 0,
             "viscoscity": 255,
             "style": type,
             "pushed": False,
             "menu": menu,
             "menuswitchaction": action,
            }
        )

    def removeAll(self):
        self.buttons = []
        
    def remove(self, ID):
        self.buttons.pop(ID)
        
    def draw(self):
        for button in self.buttons:
            if button["menu"] == self.menucurrent:
                bx, by = button["pos"]
                sx, sy = button["size"]
                
                bx, by = button["pos"]
                if bx == -1:
                    bx = pygame.transform.scale(self.image["idle"], (sx, sy)).get_rect(center = WIN.get_rect().center).x
                if by == -1:
                    by = pygame.transform.scale(self.image["idle"], (sx, sy)).get_rect(center = WIN.get_rect().center).y

                if MOUSE.x > bx and \
                MOUSE.x < bx + sx and \
                MOUSE.y > by and \
                MOUSE.y < by + sy:
                    if MOUSE.leftclick:
                        button["pushed"] = not button["pushed"]
                        if button["menuswitchaction"] > 0:
                            button["pushed"] = False
                            self.menucurrent = button["menuswitchaction"]
                            if button["menuswitchaction"] == 0: GAME.setup(); GAME.isPlaying = True
                    if button["pushed"]:
                        imageToBlit = self.image["mousehoverpushed"]
                    else:
                        imageToBlit = self.image["mousehover"]
                else:
                    if button["pushed"]:
                        imageToBlit = self.image["idlepushed"]
                    else:
                        imageToBlit = self.image["idle"]

                # Image to print
                printImg = pygame.transform.scale(
                    
                    # Image to resize
                    pygame.transform.rotate(
                        imageToBlit, # Image to rotate
                        
                        # Rotation
                        button["rotationboost"]
                    ),
                    
                    # Size × size booster
                    (sx, sy)
                )

                blit_alpha(WIN,
                    
                    # Image to print
                    
                    printImg,

                    # Location to print
                    (bx, by),

                    button["viscoscity"]
                )

                blit_alpha(WIN, 

                    # Image to print
                    pygame.transform.scale(
                        
                        # Image to resize
                        pygame.transform.rotate(
                            FONT.render(button["text"], 1, (255, 255, 255)), # Image to rotate
                            
                            # Rotation
                            button["rotationboost"]
                        ),
                        
                        # Size × size booster
                        ((sx) / 1.5, (sy) / 1.5)
                    ),

                    # Location to print
                    (bx + 2 * (sx / 40), by + 1 * (sy / 10)),

                    button["viscoscity"]
                )
BUTTON = Button()

displaywidth, displayheight = pygame.display.get_surface().get_size()

class Bossbars:
    def __init__(self):
        self.ID = [
            {"colour": "blue",
            "prog": pygame.image.load(pack + "GUIs/Bars/blue_progress.png"),
            "bg": pygame.image.load(pack + "GUIs/Bars/blue_background.png"),
            },
            {"colour": "green",
            "prog": pygame.image.load(pack + "GUIs/Bars/green_progress.png"),
            "bg": pygame.image.load(pack + "GUIs/Bars/green_background.png"),
            },
            {"colour": "pink",
            "prog": pygame.image.load(pack + "GUIs/Bars/pink_progress.png"),
            "bg": pygame.image.load(pack + "GUIs/Bars/pink_background.png"),
            },
            {"colour": "purple",
            "prog": pygame.image.load(pack + "GUIs/Bars/purple_progress.png"),
            "bg": pygame.image.load(pack + "GUIs/Bars/purple_background.png"),
            },
            {"colour": "red",
            "prog": pygame.image.load(pack + "GUIs/Bars/red_progress.png"),
            "bg": pygame.image.load(pack + "GUIs/Bars/red_background.png"),
            },
            {"colour": "white",
            "prog": pygame.image.load(pack + "GUIs/Bars/white_progress.png"),
            "bg": pygame.image.load(pack + "GUIs/Bars/white_background.png"),
            },
            {"colour": "yellow",
            "prog": pygame.image.load(pack + "GUIs/Bars/yellow_progress.png"),
            "bg": pygame.image.load(pack + "GUIs/Bars/yellow_background.png"),
            }
        ]

    def draw(self, y, valinp, maxinp, bb_colour):
        try:
            tempbg, tempprg = (
                pygame.transform.scale(self.ID[bb_colour]["bg"], (182 * 5, 5 * 5)),
                pygame.transform.scale(self.ID[bb_colour]["prog"], (182 * 5, 5 * 5))
                )
            
            # Printing the background
            WIN.blit(tempbg, (tempbg.get_rect(center = WIN.get_rect().center).x, y))

            # Printing the progress
            WIN.blit(
                tempprg,
                
                (
                    tempprg.get_rect(center = WIN.get_rect().center).x,
                    y
                ), 
                
                (   0, 0,
                    tempprg.get_rect(center = WIN.get_rect().center).x * (5 / (maxinp / valinp)),
                    5 * 5
                )
            )
        except: pass
bossbar = Bossbars()

BLOCKS = [
    {"img": pack + "Air.png",
     "name": "Air",
     "tags": ["NoRender"],
     "extratags": []
     }, # ID 0
    {"img": pack + "dirt_block.png",
     "name": "Dirt Block",
     "tags": ["Solid", "Non-transparent"],
     "extratags": ["DitchCorrodable"]
     }, # ID 1
    {"img": pack + "grass_block.png",
     "name": "Grass Block",
     "tags": ["Solid", "Non-transparent"],
     "extratags": ["DitchCorrodable"]
     }, # ID 2
    {"img": pack + "oak_log.png",
     "name": "Oak log",
     "tags": ["Solid"],
     "extratags": ["noOverhang"]
     }, # ID 3
    {"img": pack + "oak_leaves.png",
     "name": "Oak Leaves",
     "tags": ["Semisolid"],
     "extratags": []
     }, # ID 4
    {"img": pack + "lava.png",
     "name": "Lava",
     "tags": ["playerDmg"],
     "extratags": []
     }, # ID 5
    {"img": pack + "lava_top.png",
     "name": "Lava",
     "tags": ["playerDmg"],
     "extratags": []
     }, # ID 6
    {"img": pack + "bricks.png",
     "name": "Bricks",
     "tags": ["Solid"],
     "extratags": ["noOverhang"]
     }, # ID 7
]

def checkcollisions(pos1x, pos1y, pos2x, pos2y, pos1sze, pos2sze):

    if abs(pos1x - pos2x) < (pos1sze + pos2sze) / 2 and abs(pos1y - pos2y) < (pos1sze + pos2sze) / 2:
        return True
    else:
        return False
    
class Particles:
    def __init__(self):
        self.particlesOnScreen = []
        self.image = pygame.transform.scale(
            pygame.image.load(
            pack + "Particle.png"
              ),
              (4, 4))
        
    def draw(self):
        
        for particle in self.particlesOnScreen:
            print("We are drawing a particle at " + str(particle["pos"]))
            px, py = particle["pos"]
            WIN.blit(self.image,
                     
                     (px, py)

                    )
    def create(self, x, y, vx, vy, parttype, syncedwithtilemap):
        self.particlesOnScreen.append(
            {
                "pos": (x, y),
                "vel": (vx, vy),
                "type": parttype,
                "?BG": not syncedwithtilemap,
                "timer": 100,
            }
            )
        
    def createAll(self, amount):
        displaywidth, displayheight = pygame.display.get_surface().get_size()

        while len(self.particlesOnScreen) < amount:
            self.create( # Pos ↓
                        random.randint(1, displaywidth),
                        random.randint(1, displayheight),
                         # Vel ↓
                        0, 0,
                        0, # Particle type
                        False # Synced with tilemap
                       )
        
        while len(self.particlesOnScreen) > amount:
            self.particlesOnScreen.pop()

    def update(self, partID):
        
        displaywidth, displayheight = pygame.display.get_surface().get_size()

        currpart = self.particlesOnScreen[partID]
        pos = currpart["pos"]
        posx, posy = pos
        
        vel = currpart["vel"]
        velx, vely = vel

        parttype = currpart["type"]

        if parttype == 0:
            vely += (random.randint(1, 3) - 2)
            velx += (random.randint(1, 3) - 2)
        
        self.particlesOnScreen[partID]["timer"] -= 1
        posx += limit(1, -1, velx)
        posy += limit(1, -1, vely)
        pos = (limit(displaywidth, 0, posx), limit(displayheight, 0, posy))
        if parttype == 0: vel = (limit(1, -1, velx), limit(1, -1, vely))
        else: vel = (limit(1, -1, velx), limit(1, -1, vely))


        self.particlesOnScreen[partID]["pos"] = pos
        self.particlesOnScreen[partID]["vel"] = vel

    def updateAll(self):
        for particle in range(len(self.particlesOnScreen)):
            self.update(particle)
PARTICLE = Particles()

PARTICLE.createAll(amount = 0)
spaceDown = False
class Player:
    def __init__(self):
        self.x = 0
        self.y = 2
        self.vx = 10
        self.vy = 0
        self.spaceDown = False
        self.spaceDownTimer = True
        self.HP = 500
        self.MAX_HP = self.HP
        self.score = 0
        try:
        #if True:
            # Load the high score from the file
            with open('highscore.scores', 'rb') as f:
                self.highscore = pickle.load(f)
                #print(str(pickle.load(f)))
                print("Loading high scores as " + str(self.highscore))
                self.highscore = float(str(self.highscore))
        except:
        #else:
            # Save the dictionary to a file
            with open('highscore.scores', 'wb') as f:
                pickle.dump(20, f)
                self.highscore = 20
                print("Could not find high scores file, saving file named \"highscore.scores\" as \"" + str(self.highscore) + "\".")
                
        self.stamina = 10000
        self.maxscore = 0
        self.staminaMax = self.stamina
        self.saturation = self.score
        self.isRegeneratingStamina = False
        self.gravity = 0.01
        self.originalgravity = 0.01
        self.jumpHeight = -0.1
        self.jumpTime = 0
        self.twirlTime = 50
        self.jumped = False
        self.size = (64.1, 64.1)
        self.sizex, self.sizey = self.size
        self.image = pygame.transform.scale(
            pygame.image.load(
            pack + "Player/Playerframe1Run.png"
              ),
              self.size)
        
    def updateMovement(self):
        self.maxscore = max(self.score, self.maxscore)
        global keys, movex, movey
        
        if not self.spaceDownTimer:
            self.spaceDown = False
        if keys[pygame.K_SPACE] and self.spaceDownTimer:
            self.spaceDown = True
            self.spaceDownTimer = False
        if not keys[pygame.K_SPACE]:
            self.spaceDownTimer = True
            self.spaceDown = False

        self.vy = min(self.vy, 5)
        self.twirlTime -= 1
        #'''
        self.gravity = self.originalgravity
        
        if keys[pygame.K_s] and self.stamina > 0 and not self.isRegeneratingStamina: self.gravity += 0.03; self.stamina -= 2
        #'''
        
        collisions = TILEMAP.checkCollisions(self.x, self.y, self.sizex, self.sizey, "Solid")
        collisions2 = TILEMAP.checkCollisions(self.x, self.y, self.sizex, self.sizey, "Semisolid")

        if self.HP > self.MAX_HP: self.HP = self.MAX_HP
        if self.stamina > self.staminaMax: self.stamina = self.staminaMax; self.isRegeneratingStamina = False
        else:
            if self.isRegeneratingStamina: self.stamina += 4.5
            else: self.stamina += 1

        if self.vy > 0 and (True in collisions[2] or (True in collisions2[0] or True in collisions2[1] or True in collisions2[2])):
            while True in collisions[2] or (True in collisions2[0] or True in collisions2[1] or True in collisions2[2]):
                
                self.y -= 0.001
                collisions = TILEMAP.checkCollisions(self.x, self.y, self.sizex, self.sizey, "Solid")
                collisions2 = TILEMAP.checkCollisions(self.x, self.y, self.sizex, self.sizey, "Semisolid")
            if self.vy > 0: self.vy = 0
            self.jumpTime = 15
            self.twirlTime = 50
            self.jumped = True
            self.isSliding = False
        else:

            # Here is a note
            '''
            self.y += self.gravity
            collisions = TILEMAP.checkCollisions(self.x, self.y, self.sizex, self.sizey, "Solid")
            if collisions[0][2] or collisions[1][2] or collisions[2][2]: self.y -= self.gravity
            else: self.vy += self.gravity'''
            
            self.vy += self.gravity
            self.jumpTime -= 1
            if keys[pygame.K_SPACE] and self.jumpTime > 0 and self.jumped:
                if keys[pygame.K_s] and not self.isRegeneratingStamina: self.vy += self.jumpHeight * 5
                else: self.vy += self.jumpHeight
            if (self.jumped and not keys[pygame.K_SPACE]) or (keys[pygame.K_s] and not self.isRegeneratingStamina): self.jumped = False
            
            if keys[pygame.K_s] and not self.isRegeneratingStamina and self.stamina > 0: self.vy = limit(0.5, -0.7, self.vy); self.stamina -= 2; self.stamina -= 2
            else: self.vy = limit(0.4, -0.5, self.vy)
        if True in collisions[0]:
            while True in collisions[0]:
                self.HP += 0.001
                self.y += 0.001
                collisions = TILEMAP.checkCollisions(self.x, self.y, self.sizex, self.sizey, "Solid")
        


            #self.vy -= self.gravity
            self.vy *= -1
        


        if keys[pygame.K_a] and self.stamina > 0 and not self.isRegeneratingStamina: self.vx -= 0.05; self.stamina -= 2
        t = TILEMAP.checkCollisions(self.x, self.y, self.sizex, self.sizey, "playerDmg")
        if True in t[1]:
            self.HP -= 10
        
        if self.y > TILEMAP.height: self.HP -= self.y - TILEMAP.height

        if self.saturation < 0: self.HP += self.saturation / 8
        if not isNegative(self.vx - 0.001): self.saturation += 1
        if keys[pygame.K_RIGHT] and not self.isRegeneratingStamina: self.HP += 1; self.stamina -= 10
        if keys[pygame.K_LEFT]:
            self.HP -= 1; self.stamina += 10
        #'''
        if not (keys[pygame.K_LSHIFT] and self.stamina > 0 and not self.isRegeneratingStamina):
            if collisions[0][2] or collisions[1][2] or collisions[2][2]:
                self.score -= 1; self.saturation -= 1
                if (keys[pygame.K_s] and keys[pygame.K_SPACE] and not self.isRegeneratingStamina): prevpos = self.y
                while collisions[0][2] or collisions[1][2] or collisions[2][2]:
                    if not ((keys[pygame.K_s] and not self.isRegeneratingStamina) and keys[pygame.K_SPACE] and not collisions[0][2]): self.x -= 0.001
                    else: self.y -= 0.001; self.HP += 0.001
                    collisions = TILEMAP.checkCollisions(self.x, self.y, self.sizex, self.sizey, "Solid")
                
                if (keys[pygame.K_s] and not self.isRegeneratingStamina and keys[pygame.K_SPACE] and not collisions[0][2]):
                    if abs(prevpos - self.y) >= 1:
                        self.y = prevpos
                        while collisions[0][2] or collisions[1][2] or collisions[2][2]:
                            self.x -= 0.001
                            collisions = TILEMAP.checkCollisions(self.x, self.y, self.sizex, self.sizey, "Solid")
                if not ((keys[pygame.K_s] and not self.isRegeneratingStamina) or keys[pygame.K_SPACE]): self.vx = 0
                
            else:
                self.x += 0.001
                collisions = TILEMAP.checkCollisions(self.x, self.y, self.sizex, self.sizey, "Solid")
                if collisions[0][2] or collisions[1][2] or collisions[2][2]:
                    self.x -= 0.001
                else: 
                    self.vx += 0.001
                    if keys[pygame.K_d] and self.stamina > 0 and not self.isRegeneratingStamina and self.vx < 0.5: self.vx += 0.01; self.stamina -= 2
                
                while collisions[0][0] or collisions[1][0] or collisions[2][0]:
                    self.x += 0.001
                    self.vx = 0
                    collisions = TILEMAP.checkCollisions(self.x, self.y, self.sizex, self.sizey, "Solid")
                
        else: self.vx += 0.001; self.stamina -= 100
        if self.stamina <= 0:
            self.isRegeneratingStamina = True
        #'''
        self.vx = limit(0.3, -0.3, self.vx)
        self.saturation = limit(10, -10, self.saturation)

        if self.spaceDown and self.vy > 0 and isNegative(self.twirlTime):
            self.twirlTime = 50
            self.vy = 0.001

        self.x += (self.vx * 1) / 3
        self.score += self.vx - 0.2
        self.saturation += self.vx - 0.2
        self.y += self.vy / 4
        
    def scoreUpdate(self):
        if self.score > self.highscore:
            self.highscore = self.score

        print("Scores have been updated to " + str(self.highscore))

        # Save the dictionary to a file
        with open('highscore.scores', 'wb') as f:
            pickle.dump(self.highscore, f)
        
PLAYER = Player()

class Vibrate():
    def __init__(self):
        self.curAmount = 0
        self.curTime = 0
    
    def vibrate(self):
        pass
def stitch(list1, list2):
    tlist = list1
    for i in list2 :
        tlist.append(i)
    return tlist
    
class Tilemap:
    def __init__(self):
        self.width = 200
        self.height = 17
        self.camx = 20
        self.camy = 20
        self.selectedx = 0
        self.selectedy = 0
        self.size = 64
        self.name = ""
        self.tilemap = []
        self.tilemapaddon = []
        self.tilemapStart = []

    def checkCollisions(self, Player_X, Player_Y, Player_SizeX, Player_SizeY, Tag_To_Look_For):
        px, py, pszex, pszey, tsze, tm = (Player_X, Player_Y, Player_SizeX, Player_SizeY, self.size, self.tilemap)
        returnval = [
            [False, False, False],
            [False, False, False],
            [False, False, False]
        ]
        
        for x in range(3):
            for y in range(3):
                try:
                    if checkcollisions(px * pszex, py * pszey, round(px + (x - 1)) * pszex, round(py + y - 1) * pszey, pszex, tsze):
                        #pygame.sprite.spritecollideany()
                        #try:
                        if abs(round(py + (y - 1))) != round(py + (y - 1)):
                            pass
                        elif Tag_To_Look_For in BLOCKS[tm[round(py + (y - 1))][round(px + (x - 1))]]["tags"]:
                            if Tag_To_Look_For != "Semisolid": returnval[y][x] = True
                            else:
                                if (py * pszey < (round(py + y - 1) * pszey) - (tsze / 4)) and tm[round(py + (y - 1)) - 1][round(px + (x - 1))] == 0:
                                    returnval[y][x] = True
                                else:
                                    returnval[y][x] = False

                except: pass
        # if isRaise: raise Exception("Hi ~o( =∩ω∩= )m")
        return returnval
        
    def draw(self):
        displaywidth, displayheight = pygame.display.get_surface().get_size()
        for YI in range(self.height): 
            for XI in range(self.width):
                if not "NoRender" in BLOCKS[self.tilemap[YI][XI]]["tags"]:
                    WIN.blit(BLOCKS[self.tilemap[YI][XI]]["img"],
                        (
                        XI * self.size + self.camx, # X POS
                        YI * self.size + self.camy, # Y POS
                        ))
                    
    def generateName(self):
        nouns = ["Block", "Brick", "Ledge", "Path", "Blitz", "Journey", "Quest", "Chase"]
        
        for i in range(len(BLOCKS)):
            nouns.append(BLOCKS[i]["name"])

        verbs = ["Rush", "Hurdle", "Dash", "Race", "Sprint", "Leap", "Jump", "Run", "Charge"]
        adjectives = ["Swift", "Speedy", "Swift", "Quick", "Fast", "Rapid", "Fleet", "Zippy", "Nimble"]

        self.name = f"{random.choice(adjectives)} {random.choice(nouns)} {random.choice(verbs)}"
    def create(self, tw, th, tilemap):
        #tilemap = []
        for i in range(th): 
            tilemap.append([])
            for _ in range(tw):
                tilemap[i].append(0)
    
    def glue(self, tilemap1, tilemap2):
        tilemapoutput = tilemap1.copy()
        for y in range(len(tilemapoutput)):
            tilemapoutput[y] = stitch(tilemap1[y], tilemap2[y])
        return tilemapoutput
    
    def fix(self, Tilemap_to_fix):
        #raise Exception("We have reached the function")
        for x in range(len(Tilemap_to_fix[0])):
            for y in range(len(Tilemap_to_fix)):
                try:
                    if Tilemap_to_fix[y][x] == 2: # If the block is grass
                        if "Non-transparent" in BLOCKS[Tilemap_to_fix[y - 1][x]]["tags"]: # If the block above isn't transparent
                            Tilemap_to_fix[y][x] = 1 # Set the block to dirt

                    elif Tilemap_to_fix[y][x] == 1: # If the block is dirt
                        if not "Non-transparent" in BLOCKS[Tilemap_to_fix[y - 1][x]]["tags"]: # If the block above is transparent
                            Tilemap_to_fix[y][x] = 2 # Set the block to grass

                    elif Tilemap_to_fix[y][x] == 7: # If the block is bricks
                        #raise Exception("We have found di bricks!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        if not "Non-transparent" in BLOCKS[Tilemap_to_fix[y + 1][x]]["tags"]: # If the block below is transparent
                            Tilemap_to_fix[y + 1][x] == 7
                except: pass            
    
    def slice(self, Tilemap_to_slice, Column_to_slice):
        for i in range(len(Tilemap_to_slice)):
            Tilemap_to_slice[i].pop(Column_to_slice)
        
        TILEMAP.width -= 1
    def generateFlatArea(self, tilemap, groundHeight):
        print(len(tilemap[0]))
        
        print(len(tilemap))
        for X in range(len(tilemap[0])):
            
            for Y in range(len(tilemap)):
                if Y > groundHeight: tilemap[Y][X] = 1
                elif Y == groundHeight: tilemap[Y][X] = 2

    def generateTuotorial(self, tilemap):
        for x in range(len(tilemap[0])):
            tilemap[len(tilemap) - 1][x] = 1
            tilemap[len(tilemap) - 2][x] = 1
            tilemap[len(tilemap) - 3][x] = 2
        
        
        tilemap[len(tilemap) - 4][140] = 7
        tilemap[len(tilemap) - 4][141] = 7
        tilemap[len(tilemap) - 4][142] = 7
        tilemap[len(tilemap) - 4][143] = 7
        tilemap[len(tilemap) - 4][144] = 7
        tilemap[len(tilemap) - 5][141] = 7
        tilemap[len(tilemap) - 5][142] = 7
        tilemap[len(tilemap) - 5][143] = 7
        tilemap[len(tilemap) - 5][144] = 7
        tilemap[len(tilemap) - 6][142] = 7
        tilemap[len(tilemap) - 6][143] = 7
        tilemap[len(tilemap) - 6][144] = 7
        tilemap[len(tilemap) - 7][143] = 7
        tilemap[len(tilemap) - 7][144] = 7
        tilemap[len(tilemap) - 8][144] = 7

        
        def setblock(y, x, type, tilemap, allowErrors):
            if allowErrors:
                    tilemap[round(y)][round(x)] = type
                    if type >= len(BLOCKS):
                        raise Exception("UMMMM... The block you specified is out of range. (っ °Д °;)っ")
            else:
                try:
                    tilemap[round(y)][round(x)] = type
                except: pass
                if type >= len(BLOCKS):
                    raise Exception("UMMMM... The block you specified is out of range. (っ °Д °;)っ")
                

        targetpos = (len(tilemap) - 3, 170)
        targetposy, targetposx = targetpos

        height = 4

        # Floor
        setblock(targetposy, targetposx + 2, 7, tilemap, True)
        setblock(targetposy, targetposx + 1, 7, tilemap, True)
        setblock(targetposy, targetposx, 7, tilemap, True)
        setblock(targetposy, targetposx - 1, 7, tilemap, True)
        setblock(targetposy, targetposx - 2, 7, tilemap, True)

        # Walls
        for i in range(height):
            setblock(targetposy - (i + 1), targetposx + 2, 3, tilemap, True)
            setblock(targetposy - (i + 1), targetposx - 2, 3, tilemap, True)

        # Roof
        setblock(targetposy - (height + 1), targetposx + 2, 7, tilemap, True)
        setblock(targetposy - (height + 1), targetposx + 1, 7, tilemap, True)
        setblock(targetposy - (height + 1), targetposx, 7, tilemap, True)
        setblock(targetposy - (height + 1), targetposx - 1, 7, tilemap, True)
        setblock(targetposy - (height + 1), targetposx - 2, 7, tilemap, True)

        setblock(targetposy - (height + 2), targetposx + 1, 7, tilemap, True)
        setblock(targetposy - (height + 2), targetposx, 7, tilemap, True)
        setblock(targetposy - (height + 2), targetposx - 1, 7, tilemap, True)
        
        setblock(targetposy - (height + 3), targetposx, 7, tilemap, True)
        
    def generateTerrain(self, tilemap, segmentsGenerated, segmentStartX, segmentWidth, groundHeight):
        groundHeight = len(tilemap) - groundHeight
        def setblock(y, x, type, tilemap, allowErrors):
            if allowErrors:
                    tilemap[round(y)][round(x)] = type
                    if type >= len(BLOCKS):
                        raise Exception("UMMMM... The block you specified is out of range. (っ °Д °;)っ")
            else:
                try:
                    tilemap[round(y)][round(x)] = type
                except: pass
                if type >= len(BLOCKS):
                    raise Exception("UMMMM... The block you specified is out of range. (っ °Д °;)っ")
                

        for I in range(segmentsGenerated):
            # Generate the ground
            for Y in range(len(tilemap)):
                for X in range(min( len(tilemap[0]), segmentWidth )):
                    try:
                        if Y == groundHeight:
                            setblock(Y, X + segmentStartX, 2, tilemap, False)
                        if Y > groundHeight:
                            setblock(Y, X + segmentStartX, 1, tilemap, False)
                    except: pass

            # Generate obstacles
            rndvalue = random.randint(1, 5)
            #rndvalue2 = random.randint(1, 4)
            rndvalue2 = 1

            if rndvalue == 1:
                # Tree obstacle
                try:
                    for i in range(3):
                        targetpos = (groundHeight - i - 1, math.floor(segmentWidth / 2) + segmentStartX)
                        targetposy, targetposx = targetpos
                        setblock(targetposy, targetposx, 3, tilemap, True)
                        if i != 0:
                            setblock(targetposy, targetposx + 1, 4, tilemap, True)
                            setblock(targetposy, targetposx - 1, 4, tilemap, True)
                            setblock(targetposy, targetposx + 2, 4, tilemap, True)
                            setblock(targetposy, targetposx - 2, 4, tilemap, True)

                        if i == min(max(min(len(tilemap) - groundHeight - 1, 4), 3), len(tilemap)):
                            setblock(targetposy, targetposx - 2, 4, tilemap, True)
                    for i in range(2):
                        setblock(targetposy - i - 1, targetposx, 4, tilemap, True)
                        setblock(targetposy - i - 1, targetposx - 1, 4, tilemap, True)
                        setblock(targetposy - i - 1, targetposx + 1, 4, tilemap, True)
                except: pass

            elif rndvalue == 2:
                    # Ditch obstacle
                    for X in range(2):
                        for Y in range(groundHeight):
                            targetpos = (len(tilemap) - Y, X + round(segmentWidth / 2) - segmentStartX)
                            targetposy, targetposx = targetpos
                            try:
                                if "DitchCorrodable" in BLOCKS[tilemap[targetposy][targetposx]]["extratags"]:
                                    setblock(targetposy, targetposx, 0, tilemap, False)
                            except: pass
            
            elif rndvalue == 3:
                    # Lava pool obstacle
                    for X in range(2):
                        setblock(groundHeight, X + round(segmentWidth / 2) - segmentStartX, 6, tilemap, False)
                        setblock(groundHeight + 1, X + round(segmentWidth / 2) - segmentStartX, 2, tilemap, False)

            elif rndvalue == 4:
                # Bricks obstacle
                dir = random.randint(1, 3) - 2
                dir = -1
                height = random.randint(2, 5)
                for Y in range(height):
                    setblock((groundHeight - height) + Y, round(segmentWidth / 2) - segmentStartX, 7, tilemap, False)
                    for X in range(Y):
                        setblock((groundHeight - height) + Y, (round(segmentWidth / 2) - segmentStartX) + (X + 1) * dir, 7, tilemap, False)

            elif rndvalue == 5:
                # House obstacle
                try:
                    targetpos = (groundHeight, math.floor(segmentWidth / 2) + segmentStartX)
                    targetposy, targetposx = targetpos

                    height = 3

                    # Floor
                    setblock(targetposy, targetposx + 2, 7, tilemap, True)
                    setblock(targetposy, targetposx + 1, 7, tilemap, True)
                    setblock(targetposy, targetposx, 7, tilemap, True)
                    setblock(targetposy, targetposx - 1, 7, tilemap, True)
                    setblock(targetposy, targetposx - 2, 7, tilemap, True)

                    # Walls
                    for i in range(height):
                        setblock(targetposy - (i + 1), targetposx + 2, 3, tilemap, True)
                        setblock(targetposy - (i + 1), targetposx - 2, 3, tilemap, True)

                    # Roof
                    setblock(targetposy - (height + 1), targetposx + 2, 7, tilemap, True)
                    setblock(targetposy - (height + 1), targetposx + 1, 7, tilemap, True)
                    setblock(targetposy - (height + 1), targetposx, 7, tilemap, True)
                    setblock(targetposy - (height + 1), targetposx - 1, 7, tilemap, True)
                    setblock(targetposy - (height + 1), targetposx - 2, 7, tilemap, True)

                    setblock(targetposy - (height + 2), targetposx + 1, 7, tilemap, True)
                    setblock(targetposy - (height + 2), targetposx, 7, tilemap, True)
                    setblock(targetposy - (height + 2), targetposx - 1, 7, tilemap, True)
                    
                    setblock(targetposy - (height + 3), targetposx, 7, tilemap, True)

                except: pass


            segmentStartX += segmentWidth

        self.fix(tilemap)
TILEMAP = Tilemap()

for i in range(len(BLOCKS)):
    BLOCKS[i]["img"] = pygame.transform.scale(
            pygame.image.load(
            BLOCKS[i]["img"]
              ),
              (TILEMAP.size, TILEMAP.size))
movex, movey = (0, 0)
movex2, movey2 = (0, 0)
keys = pygame.key.get_pressed()

class Game:
    def __init__(self):
        self.isPlaying = False
        self.timeSinceStartPlaying = 0
        self.paused = False
        self.pausedForAReason = False
        
    
    def setup(self):
        random.seed = 18756189465832765
        print(f"Name: {TILEMAP.name}")
        TILEMAP.generateName()
        TILEMAP.tilemap = []; TILEMAP.tilemapaddon = []; TILEMAP.tilemapStart = []
        TILEMAP.create(TILEMAP.width, TILEMAP.height, TILEMAP.tilemap)
        TILEMAP.create(30, TILEMAP.height, TILEMAP.tilemapStart)
        TILEMAP.generateName()
        tgroundHeight = random.randint(1, 5)
        if BUTTON.buttons[4]["pushed"]:
            TILEMAP.generateTuotorial(TILEMAP.tilemap)
        else:
            TILEMAP.generateTerrain(TILEMAP.tilemap, 99, 0, 6, 3 + tgroundHeight)
            TILEMAP.generateFlatArea(TILEMAP.tilemapStart, tgroundHeight)
            TILEMAP.tilemap = TILEMAP.glue(TILEMAP.tilemapStart, TILEMAP.tilemap)

        PLAYER.x = 0
        PLAYER.y = 2
        PLAYER.vx = 10
        PLAYER.vy = 0
        PLAYER.HP = 500
        PLAYER.MAX_HP = PLAYER.HP
        PLAYER.score = 0
        PLAYER.stamina = 10000
        PLAYER.staminaMax = PLAYER.stamina
        PLAYER.isRegeneratingStamina = False
        PLAYER.gravity = 0.01
        PLAYER.originalgravity = 0.01
        PLAYER.jumpHeight = -0.1
        PLAYER.jumpTime = 0
        PLAYER.jumped = False
    
GAME = Game()

def controlsupdate():
    global keys, movex, movey, movex2, movey2, timer
    MOUSE.update()
    movex, movey = (0, 0)
    movex2, movey2 = (0, 0)
    spaceDown = True
    spaceDownTimer = True
    if keys[pygame.K_w]: movey += 1
    if keys[pygame.K_s]: movey -= 1
    if keys[pygame.K_a]: movex += 1
    if keys[pygame.K_d]: movex -= 1

    if keys[pygame.K_UP]: movey2 += 1
    if keys[pygame.K_DOWN]: movey2 -= 1
    if keys[pygame.K_LEFT]: movex2 += 1
    if keys[pygame.K_RIGHT]: movex2 -= 1
    keys = pygame.key.get_pressed()

    if keys[pygame.K_p] or GAME.pausedForAReason: GAME.paused = True; timer += 1
    else:
        if keys[pygame.K_f]:
            GAME.paused = not GAME.paused
        else:
            GAME.paused = False

    if (not GAME.paused) and GAME.isPlaying:
        GAME.timeSinceStartPlaying += 1

tothenearest = lambda val, inp : round(val / inp) * inp

pause = pygame.transform.scale(
        pygame.image.load(
            pack + "GUIs/Pause.png"
              ),
              (TILEMAP.size, TILEMAP.size))
ANYKEYS = False
GAME.paused = False
animState = 0
animStateVel = 0

isNegative = lambda x: abs(x) != x
isDecimal = lambda x: round(x) != x
def percentage(percent, whole):
    return (percent * whole) / 100.0
timer = 0

animState = logo.get_rect(center = WIN.get_rect().center).y
timeSinceStart = 0
gradient = 0
gradientToggle = False

def drawCentredText(text, posy):
    drawfont(
        text, (text.get_rect(center = WIN.get_rect().center).x, posy))
    
def pausewhen(time, valToMeasure, key, textToDraw):
    if BUTTON.buttons[4]["pushed"]:
        if round(valToMeasure) == time and not key:
            GAME.pausedForAReason = True
            for i in textToDraw:
                drawCentredText(i["text"], i["ypos"])
        else: 
            
            # If I just set it to false, then only one of them
            # will work. So, I have to make it so that it only
            # sets this variable to false if there is a small
            # enough distance between each of the tuotorial popups.

            if abs(valToMeasure - time) < 10:
                GAME.pausedForAReason = False

timesStripped = 0

while not done:

    displaywidth, displayheight = pygame.display.get_surface().get_size()
    WIN.fill((0, 100, 255))

    controlsupdate()

    if GAME.isPlaying:
        WIN.blit(

            PLAYER.image,
            (PLAYER.x * TILEMAP.size + TILEMAP.camx, PLAYER.y * TILEMAP.size + TILEMAP.camy)

        )
        TILEMAP.draw()

    if GAME.isPlaying:
        if PLAYER.x > 25:
            TILEMAP.slice(TILEMAP.tilemap, 0)
            PLAYER.x -= 1
            TILEMAP.camx += TILEMAP.size
            timesStripped += 1

        if PLAYER.x >= TILEMAP.width / 4 * 3:
            print("Generating new chunks...  ")
            TILEMAP.create(TILEMAP.width, TILEMAP.height, TILEMAP.tilemapaddon)
            TILEMAP.generateTerrain(TILEMAP.tilemapaddon, 32, 0, 6, 2)
            TILEMAP.tilemap = TILEMAP.glue(TILEMAP.tilemap, TILEMAP.tilemapaddon)
            TILEMAP.width = len(TILEMAP.tilemap[0])
            TILEMAP.height = len(TILEMAP.tilemap)
            TILEMAP.fix(TILEMAP.tilemap)
            TILEMAP.tilemapaddon = []

        if PLAYER.HP > 0 and not GAME.paused:
            PLAYER.updateMovement()
            
            hi = displaywidth / 2 - PLAYER.x * TILEMAP.size - TILEMAP.size / 2
            TILEMAP.camx += (hi - TILEMAP.camx) / 8
            hi = displayheight / 2 - PLAYER.y * TILEMAP.size - TILEMAP.size / 2 
            TILEMAP.camy += (hi - TILEMAP.camy) / 8

        bossbar.draw(10, PLAYER.HP, PLAYER.MAX_HP, 4)
        if PLAYER.isRegeneratingStamina:
            if isDecimal(PLAYER.stamina % 2):
                bossbar.draw(50, PLAYER.stamina, PLAYER.staminaMax, 1)
            else: bossbar.draw(50, PLAYER.stamina, PLAYER.staminaMax, 4)
        else: bossbar.draw(50, PLAYER.stamina, PLAYER.staminaMax, 1)
        

        val = 1
        tempscore = PLAYER.maxscore
        while tempscore > PLAYER.highscore:
            tempscore -= PLAYER.highscore
            val += 1
            if val > 100: break
        
        dt = FONT.render(f"Aim: {val * 100}%, Score: {round(PLAYER.maxscore)}, High score: {round(PLAYER.highscore)}", 1, (255, 255, 255))
        drawfont(
            dt, (dt.get_rect(center = WIN.get_rect().center).x, displayheight - 60))
        bossbar.draw(displayheight - 100, tempscore, PLAYER.highscore, 6)
        #bossbar.draw(90, PLAYER.score - math.floor(PLAYER.highscore / 100) * 100, math.ceil(PLAYER.highscore / 100) * 100, 6)
        bossbar.draw(90, PLAYER.saturation, 10, 5)

        '''
        try:
            if BUTTON.buttons[4]["pushed"]:
                if GAME.timeSinceStartPlaying == 200 and not MOUSE.onetimeleft:
                    GAME.pausedForAReason = True
                    dt = 
                    drawfont(
                        dt, (dt.get_rect(center = WIN.get_rect().center).x + 10, 120))
                    dt = FONT.render(f"Click to continue.", 1, (255, 255, 255))
                    drawfont(
                        dt, (dt.get_rect(center = WIN.get_rect().center).x + 10, 180))
                else: GAME.pausedForAReason = False
        except: pass
        '''
        
        pausewhen(200, GAME.timeSinceStartPlaying, MOUSE.leftclick, [
                {"text": FONT.render(f"Welcome to springfeet!", 1, (255, 255, 255)), "ypos": 120},
                {"text": FONT.render(f"In this game, you automatically run forward.", 1, (255, 255, 255)), "ypos": 160},
                {"text": FONT.render(f"Click to continue.", 1, (255, 255, 255)), "ypos": 200},
        ])

        pausewhen(400, GAME.timeSinceStartPlaying, keys[pygame.K_SPACE], [
                {"text": FONT.render(f"Press the spacebar to jump! (:", 1, (255, 255, 255)), "ypos": 180},
        ])

        pausewhen(450, GAME.timeSinceStartPlaying, not keys[pygame.K_SPACE], [
                {"text": FONT.render(f"", 1, (255, 255, 255)), "ypos": 180},
        ])

        pausewhen(500, GAME.timeSinceStartPlaying, keys[pygame.K_SPACE], [
                {"text": FONT.render(f"Press it in midair to do a", 1, (255, 255, 255)), "ypos": 180},
                {"text": FONT.render(f"booster jump!", 1, (255, 255, 255)), "ypos": 220},
        ])

        pausewhen(600, GAME.timeSinceStartPlaying, keys[pygame.K_a], [
                {"text": FONT.render(f"Press the A key to", 1, (255, 255, 255)), "ypos": 120},
                {"text": FONT.render(f"go in the left direction.", 1, (255, 255, 255)), "ypos": 180},
        ])

        pausewhen(700, GAME.timeSinceStartPlaying, keys[pygame.K_d], [
                {"text": FONT.render(f"Notice how your health bar has gone down!", 1, (255, 255, 255)), "ypos": 120},
                {"text": FONT.render(f"In this game, if you go back or slow down", 1, (255, 255, 255)), "ypos": 160},
                {"text": FONT.render(f"you lose health. If you do, you quickly", 1, (255, 255, 255)), "ypos": 200},
                {"text": FONT.render(f"hold the D key to accelerate back again.", 1, (255, 255, 255)), "ypos": 240},
        ])
        pausewhen(943, GAME.timeSinceStartPlaying, MOUSE.leftclick, [
                {"text": FONT.render(f"Did you see the white bar go back up again?", 1, (255, 255, 255)), "ypos": 120},
                {"text": FONT.render(f"That is the saturation bar. If you slow", 1, (255, 255, 255)), "ypos": 160},
                {"text": FONT.render(f"down, it goes down. If you speed up, it", 1, (255, 255, 255)), "ypos": 200},
                {"text": FONT.render(f"goes back up again. If it goes so far down", 1, (255, 255, 255)), "ypos": 240},
                {"text": FONT.render(f"that you can't see it, then you lose health.", 1, (255, 255, 255)), "ypos": 280},
                {"text": FONT.render(f"Click to continue.", 1, (255, 255, 255)), "ypos": 320},
        ])
        pausewhen(1100, GAME.timeSinceStartPlaying, keys[pygame.K_RIGHT], [
                {"text": FONT.render(f"You seem to be down on health,", 1, (255, 255, 255)), "ypos": 120},
                {"text": FONT.render(f"I would reccomend regenerating", 1, (255, 255, 255)), "ypos": 160},
                {"text": FONT.render(f"health. Press the right arrow", 1, (255, 255, 255)), "ypos": 200},
                {"text": FONT.render(f"to spend stamina to regain some", 1, (255, 255, 255)), "ypos": 240},
                {"text": FONT.render(f"health.", 1, (255, 255, 255)), "ypos": 280},
        ])
        pausewhen(1300, GAME.timeSinceStartPlaying, keys[pygame.K_LEFT], [
                {"text": FONT.render(f"If you wanted to (which might be often),", 1, (255, 255, 255)), "ypos": 120},
                {"text": FONT.render(f"then you can also press the left arrow", 1, (255, 255, 255)), "ypos": 160},
                {"text": FONT.render(f"to spend health to regenerate stamina!", 1, (255, 255, 255)), "ypos": 200},
                {"text": FONT.render(f"(Stamina bar = green)", 1, (255, 255, 255)), "ypos": 240},
                {"text": FONT.render(f"Please note that you get back stamina over time.", 1, (255, 255, 255)), "ypos": 280},
        ])
        
        pausewhen(136, PLAYER.x + timesStripped, keys[pygame.K_SPACE] and keys[pygame.K_s], [
                {"text": FONT.render(f"Here's a useful trick to know:", 1, (255, 255, 255)), "ypos": 120},
                {"text": FONT.render(f"If you hold space and S at the", 1, (255, 255, 255)), "ypos": 160},
                {"text": FONT.render(f"same time, then you can stairhop!", 1, (255, 255, 255)), "ypos": 200},
                {"text": FONT.render(f"You are going to whizz up stairs as", 1, (255, 255, 255)), "ypos": 240},
                {"text": FONT.render(f"if you're a pro at this game.", 1, (255, 255, 255)), "ypos": 280},
        ])

        pausewhen(156, PLAYER.x + timesStripped, MOUSE.left, [
                {"text": FONT.render(f"Please note that stairhopping", 1, (255, 255, 255)), "ypos": 120},
                {"text": FONT.render(f"takes up stamina. Be careful!", 1, (255, 255, 255)), "ypos": 160},
                {"text": FONT.render(f"Click to continue.", 1, (255, 255, 255)), "ypos": 200},
        ])

        pausewhen(166, PLAYER.x + timesStripped, keys[pygame.K_LSHIFT], [
                {"text": FONT.render(f"If you ever encounter something like", 1, (255, 255, 255)), "ypos": 120},
                {"text": FONT.render(f"a huge wall that you can't get past,", 1, (255, 255, 255)), "ypos": 160},
                {"text": FONT.render(f"then you can always just hold left", 1, (255, 255, 255)), "ypos": 200},
                {"text": FONT.render(f"shift to phase through the walls!", 1, (255, 255, 255)), "ypos": 240},
                {"text": FONT.render(f"However, it takes up a LOT of stamina.", 1, (255, 255, 255)), "ypos": 280},
        ])

        pausewhen(188, PLAYER.x + timesStripped, keys[pygame.K_LSHIFT], [
                {"text": FONT.render(f"Oh, and don't forget that the S key", 1, (255, 255, 255)), "ypos": 120},
                {"text": FONT.render(f"can also be used to fall faster, useful", 1, (255, 255, 255)), "ypos": 160},
                {"text": FONT.render(f"for some very fast maneuvering!", 1, (255, 255, 255)), "ypos": 200},
                {"text": FONT.render(f"Click to end the tuotorial. Good luck!", 1, (255, 255, 255)), "ypos": 240},
        ])


    if GAME.paused and GAME.isPlaying and not GAME.pausedForAReason:
        WIN.blit(
            pause,
            (displaywidth / 2 - TILEMAP.size / 2, displayheight / 2 - TILEMAP.size / 2)
        )
    if GAME.isPlaying:
        if PLAYER.HP <= 0:
            animState += animStateVel
            animTar = displayheight / 2 - 140
            #animTar = MOUSE.y
            animStateVel -= (animState - animTar) / 1000

            if isNegative(animStateVel): animStateVel += 0.1
            else: animStateVel -= 0.1

            dt = FONT.render(f"You died.", 1, (0, 0, 0))
            drawfont(
                dt, (dt.get_rect(center = WIN.get_rect().center).x + 10, animState + 1))
                
            dt = FONT.render(f"Score: {round(PLAYER.maxscore)}", 1, (0, 0, 0))
            drawfont(
                dt, (dt.get_rect(center = WIN.get_rect().center).x + 10, animState + 30 + 1))
            dt = FONT.render(f"Press the home button to exit.", 1, (0, 0, 0))
            drawfont(
                dt, (dt.get_rect(center = WIN.get_rect().center).x + 10, animState + 60 + 1))
            dt = FONT.render(f"You died.", 1, (255, 255, 255))
            drawfont(
                dt, (dt.get_rect(center = WIN.get_rect().center).x, animState))
                
            dt = FONT.render(f"Score: {round(PLAYER.maxscore)}", 1, (255, 255, 255))
            drawfont(
                dt, (dt.get_rect(center = WIN.get_rect().center).x, animState + 30))
            dt = FONT.render(f"Press the home button to exit.", 1, (255, 255, 255))
            drawfont(
                dt, (dt.get_rect(center = WIN.get_rect().center).x, animState + 60))
            
            hi = displaywidth / 2 - PLAYER.x * TILEMAP.size - TILEMAP.size / 2
            TILEMAP.camx += (hi - TILEMAP.camx) / 32
            hi = displayheight / 2 - PLAYER.y * TILEMAP.size - TILEMAP.size / 2
            TILEMAP.camy += (hi - TILEMAP.camy) / 32

            if keys[pygame.K_HOME]:
                done = True
                print("Awww. Too bad for you. u(ﾟДﾟ)u")
                break
        
        if keys[pygame.K_u]:
            PLAYER.scoreUpdate()
    

    if not GAME.isPlaying:
        # If you replace the screen.blit(happy, (100, 100))
        # with a call to blit_alpha(screen, happy, (100, 100), 128), you get the following:
        if keys[pygame.K_p]: spd = 8
        else: spd = 1
        if gradientToggle:
            gradient += 1 * spd
            if gradient > 400: gradientToggle = not gradientToggle
        else:
            gradient -= 1 * spd
            if gradient < 0: gradientToggle = not gradientToggle

        if timeSinceStart > 1302: animState = animState / 1.016
        if timeSinceStart > 1352: BUTTON.draw()
        #if BUTTON.menucurrent == 

        if timeSinceStart > 1608:
        
            try:
                if len(BUTTON.buttons) == 0:
                    raise Exception("WAAA! im compwaining cuz theres no buttunsss")
                for i in range(len(BUTTON.buttons)):
                    BUTTON.buttons[i]["viscoscity"] += 1
                    #if i in [5, 6, 7, 8, 9]:
            except:
                BUTTON.menucurrent = 1
                '''
                (method) def create(
                    text: Any,
                    x: Any,
                    y: Any,
                    sizex: Any,
                    sizey: Any,
                    type: Any,
                    menu: Any,
                    action: Any
                ) -> None
                '''
                #             text               x  y,   szx  szy t  m  action
                BUTTON.create("Start",          -1, 200, 200, 50, 0, 1, 0)  # ID 0
                BUTTON.create("Back",           -1, 200, 200, 50, 0, 2, 1)  # ID 1
                BUTTON.create("Back",           -1, 200, 200, 50, 0, 2, -1) # ID 2
                BUTTON.create("Options",        -1, 300, 300, 50, 0, 1, 2)  # ID 3
                BUTTON.create("Play tuotorial", -1, 400, 300, 50, 0, 1, 0)  # ID 4
                for i in BUTTON.buttons: i["viscoscity"] = 0
                
        if timeSinceStart > 802:
            blit_alpha(WIN, logo, (
                            logo.get_rect(center = WIN.get_rect().center).x, animState + 50
                           ), gradient
            )
        else:
            blit_alpha(WIN, otherlogo, (
                                        otherlogo.get_rect(center = WIN.get_rect().center).x, animState + 50
                                       ), gradient
            )
                
        
        try:
            if BUTTON.buttons[0]["pushed"]: GAME.isPlaying = True; animState = 0; animStateVel = 0; GAME.setup()
            if BUTTON.buttons[4]["pushed"]: BUTTON.buttons[0]["pushed"] = True
        except: pass
        
    clock.tick(100)
    PARTICLE.updateAll()
    PARTICLE.draw()


    pygame.display.update()
    
    timeSinceStart += 1 * spd
    if keys[pygame.K_END]:
        pass
    print(PLAYER.x + timesStripped)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break

PLAYER.scoreUpdate()