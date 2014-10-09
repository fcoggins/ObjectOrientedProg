import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8

#### Put class definitions here ####
class Rock(GameElement):
    IMAGE = "Rock"
    SOLID = True

class Key(GameElement):
    IMAGE = "Key"
    SOLID = False

    def interact(self, player):
        player.key_list.append(self)
        GAME_BOARD.draw_msg("You just acquired a key! You have %d keys!"%(len(player.key_list)))


class Chest(GameElement):
    IMAGE = "Chest"
    SOLID = True

    def interact(self, player):

            if len(player.key_list) >= 1 and self.IMAGE == "Chest":
                self.change_image("Open_chest")
                player.key_list.pop()
                player.inventory.append(Gem)
                #print player.inventory
                #message is being overwritten by SOLID error message, need to give this message priority
                #GAME_BOARD.draw_msg("You opened the chest and got a gem!")


class Door(GameElement):
    IMAGE = "DoorClosed"
    SOLID = True

    def interact(self, player):
        #if OrangeGem.DOOR_OPEN == True:
        if "orange" in player.inventory:
            self.change_image("DoorOpen")
            player.inventory.remove("orange")
            SOLID = False


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

                if existing_el and existing_el.SOLID:
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

class Gem(GameElement):
    #IMAGE = "BlueGem"
    SOLID = False

    def interact(self, player):
        #player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!"%(len(player.inventory)))
        print player.inventory
        for i in player.inventory:
            print type(i)

class BlueGem(Gem):
    IMAGE = "BlueGem"
    def interact(self, player):
        player.inventory.append("blue")
        return super(BlueGem, self).interact(player)

class OrangeGem(Gem):
    IMAGE = "OrangeGem"
    DOOR_OPEN = False
    def interact(self, player):
        player.inventory.append("orange")
        #DOOR_OPEN = True
        #print DOOR_OPEN
        
        return super(OrangeGem, self).interact(player)

class GreenGem(Gem):
    IMAGE = "GreenGem"

    def interact(self, player):
        player.inventory.append("green")
        return super(GreenGem, self).interact(player)

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

    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(2, 2, player)

    GAME_BOARD.draw_msg("This game is wicked awesome.")

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

