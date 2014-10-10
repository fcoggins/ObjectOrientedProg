import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 14
GAME_HEIGHT = 10

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True
    message = True
    #APPEAR = True

class Wall(GameElement):
    IMAGE = "Wall"
    SOLID = True
    message = True

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False
    #APPEAR = False

    def interact(self, player):
        player.key_list.append(self)
        GAME_BOARD.draw_msg("You just acquired a key! You have %d keys!"%(len(player.key_list)))
        self.message = False


class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True
    #APPEAR = True

    def interact(self, player):
            self.message = False
            if len(player.key_list) >= 1 and self.IMAGE == "Chest":
                self.change_image("Open_chest")
                player.key_list.pop()
                GAME_BOARD.draw_msg("You opened the chest! Now get the star.")
            elif self.IMAGE == "Open_chest":
                self.SOLID = False
                player.inventory.append("Star")
                #print player.inventory
                #message is being overwritten by SOLID error message, need to give this message priority
                GAME_BOARD.draw_msg("You got a star! You can now kill angry birds")
            else:
                GAME_BOARD.draw_msg("You need a key to open this chest.")


class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True
    #APPEAR = True

    def interact(self, player):
        self.message = False
        for item in player.inventory:
            if item.COLOR == "orange":
                self.change_image("DoorOpen")
                #player.inventory.remove(item)
                self.SOLID = False


class Character(GameElement):
    IMAGE = "Cat"

    def keyboard_handler(self, symbol, modifier):
        
        direction = None
        if symbol == key.UP:
            direction = "up"
        elif symbol == key.DOWN:
            direction = "down"
        elif symbol == key.LEFT:
            direction = "left"
        elif symbol == key.RIGHT:
            direction = "right"
        
        self.board.draw_msg("[%s] moves %s" % (self.IMAGE, direction))

        if direction:
            next_location = self.next_pos(direction)

            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]

                existing_el = self.board.get_el(next_x, next_y)

                if existing_el:
                    existing_el.interact(self)
                    hover_object = existing_el
                    # if existing_el.APPEAR:
                    #     self.temp_x = next_x
                    #     self.temp_y = next_y



                if existing_el and existing_el.SOLID and existing_el.message:
                    self.board.draw_msg("There's something in my way!")   
                elif existing_el is None or not existing_el.SOLID:
                    self.board.del_el(self.x, self.y)
                    self.board.set_el(next_x, next_y, self)
            elif next_location == False:
                self.board.draw_msg("You'll fall off the board!")


    def next_pos(self, direction):
        if direction == "up":
            if self.y-1 < 0:
                return False
            return (self.x, self.y-1)
        elif direction == "down":
            if self.y+1 >= GAME_HEIGHT:
                return False
            return (self.x, self.y+1)
        elif direction == "left":
            if self.x-1 < 0:
                return False
            return (self.x-1, self.y)
        elif direction == "right":
            if self.x+1 >= GAME_WIDTH:
                return False
            return (self.x+1, self.y)
        return None

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
        self.key_list = []

class BadGuy(GameElement):
        IMAGE = "Bug"
        direction = 1
        SOLID = True
        STATE = 0
        INPUT = False #delete later

        def update(self, dt):
            if self.STATE == 0:
                next_y = self.y + self.direction

                if next_y < 0 or next_y >= self.board.height:
                    self.direction *= -1
                    next_y = self.y

                self.board.del_el(self.x, self.y)
                self.board.set_el(self.x, next_y, self)
            else:
                pass

        def interact(self, player):
            self.message = False
            if self.STATE == 0:
                GAME_BOARD.draw_msg("Halt! You may not pass until you answer my riddle. (Press up to continue)")
                self.STATE = 1
            elif self.STATE == 1:
                GAME_BOARD.draw_msg("Question")
                if self.INPUT:
                    self.STATE = 2
                else:
                    GAME_BOARD.draw_msg("WRONG! Try again.")
                    self.INPUT = True
            else:
                GAME_BOARD.draw_msg("Congratulations! You may pass!")
                self.board.del_el(self.x, self.y)

class Gem(GameElement):
    SOLID = False
    APPEAR = False

    def interact(self, player):
        self.message = False
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d gems!"%(len(player.inventory)))
        #print player.inventory
        # for i in player.inventory:
        #     print type(i)

class BlueGem(Gem):
    IMAGE = "BlueGem"
    COLOR = "blue"
    
class OrangeGem(Gem):
    IMAGE = "OrangeGem"
    COLOR = "orange"
    
class GreenGem(Gem):
    IMAGE = "GreenGem"
    COLOR = "green"

class Princess(GameElement):
    SOLID = True
    IMAGE = "Princess" 

    def interact(self, player):
        self.message = False
        if len(player.inventory) == 3: 
            GAME_BOARD.draw_msg("Sparkly gems == true love.  Let's live happily ever after!")
            ###Make heart appear
        else:
            GAME_BOARD.draw_msg("No(t enough) gems, no love. Try again.")

class Tree(GameElement):
    SOLID = True
    IMAGE = "TallTree"  
    message = True

class Bug(GameElement):
    SOLID = True
    IMAGE = "Bug" 

    def interact(self, player):
        self.message = False
        if "Star" in player.inventory: 
            self.SOLID = False
            player.inventory.remove("Star")

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""
    rock_positions = [
            (2, 1),
            (1, 2),
            (3, 2),
            (2, 3)  
        ]

    rocks = []
    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    rocks[-1].SOLID = False

    wall_positions = [
            (1, 0),(1,1),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),
            (2, 0),(2,8),(4,8),(5,2), (5,3), (5,4), (5,5), (5,7), (5,8),
            (3, 0),
            (4, 0), (4,2) , (7, 3), (8, 3), (9, 3)
        ]

   # water = []
    for pos in wall_positions:
        wall = Wall()
        GAME_BOARD.register(wall)
        GAME_BOARD.set_el(pos[0], pos[1], wall)
        #water.append(water)

    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(2, 2, player)

    GAME_BOARD.draw_msg("Save the princess from the angry bird by getting all three gems!")

    bluegem = BlueGem()
    GAME_BOARD.register(bluegem)
    GAME_BOARD.set_el(3, 1, bluegem)

    key = Key()
    GAME_BOARD.register(key)
    GAME_BOARD.set_el(0, 0, key)

    chest = Chest()
    GAME_BOARD.register(chest)
    GAME_BOARD.set_el(7, 4, chest)

    door = Door()
    GAME_BOARD.register(door)
    GAME_BOARD.set_el(6, 2, door)

    orangegem = OrangeGem()
    GAME_BOARD.register(orangegem)
    GAME_BOARD.set_el(2, 6, orangegem)

    greengem = GreenGem()
    GAME_BOARD.register(greengem)
    GAME_BOARD.set_el(8, 8, greengem)

    princess = Princess()
    GAME_BOARD.register(princess)
    GAME_BOARD.set_el(13, 0, princess)

    tree_positions = [
            (6, 1),
            (12, 0),
            (12, 2),
            (13, 2),
  
        ]

    trees = []
    for pos in tree_positions:
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        trees.append(tree)

    bug = Bug()
    GAME_BOARD.register(bug)
    GAME_BOARD.set_el(12, 1, bug)

    moving_bug = BadGuy()
    GAME_BOARD.register(moving_bug)
    GAME_BOARD.set_el(10, 3, moving_bug)

