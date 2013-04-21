import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys
import random

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
KEYBOARD = None
PLAYER = None
######################

GAME_WIDTH = 8
GAME_HEIGHT = 8
#item_x = 0
#item_y = 0

#### Put class definitions here ####
class Rock(GameElement):
	IMAGE = "Rock"
	SOLID = True

# class Gem(GameElement):
# 	IMAGE = "BlueGem"
# 	SOLID = False

class WinningStar(GameElement):
	IMAGE = "Star"


class Player(GameElement):
	IMAGE = "Beard0"


	def __init__(self): #each time an object of class Character is made...
		GameElement.__init__(self) #from Game Element class, run the game element
		#init method on the new Character object we're making
		self.inventory = [] #each Character object starts with an empty inventory
		self.timer = 0

	def next_pos(self, direction): #instance method
		if direction == "up": #looks to the direction variable from keyboard handler
			return (self.x, self.y-1) #on the instantiated object (SELF), 
		elif direction == "down":
			return (self.x, self.y+1)
		elif direction == "left":
			return (self.x-1, self.y)
		elif direction == "right":
			return (self.x+1, self.y)
		return None
		
class AwesomePython(Player):
	IMAGE = "Horns"

	def update(self, dt):
		pass
		# print "Updating inside Player:", dt
		# self.timer += dt
		# if self.timer >= 1:
		# 	print "1 second has passed"
		# 	self.timer = 0

class AwesomePython(GameElement):
	IMAGE = "Python"
	SOLID = True
	

class Items(GameElement):
    IMAGE = "Cheetos"
    SOLID = False
    
    def interact(self, player):
		if len(player.inventory) >= 9:
			GAME_BOARD.draw_msg("YOU WINNN !!!!  Maximum neckbeard achieved!")

			for i in range(0,8):
				for j in range(0,8):
					star = WinningStar()
					GAME_BOARD.register(star)
					GAME_BOARD.set_el(i,j,star)


			
		else:
			player.inventory.append(self)
			#changing sprite on item interaction
			player.sprite = change_sprite(player.inventory)
			
			GAME_BOARD.draw_msg("You just acquired an item!  You have %d items and your beard is growing!" % (len(player.inventory)))
			
		new_snake = AwesomePython()
		GAME_BOARD.register(new_snake)
		GAME_BOARD.set_el(random.randint(0,7), random.randint(0,7), new_snake)

####   End class definitions    ####

def initialize():
    """Put game initialization code here"""

    #### INITIALIZE ROCKS
    rock_positions = [
    	(random.randint (0,7), random.randint(0,7)),
    	(random.randint (0,7), random.randint(0,7)),
    	(random.randint (0,7), random.randint(0,7)),
    	(random.randint (0,7), random.randint(0,7)),
    	(random.randint (0,7), random.randint(0,7)),
    	(random.randint (0,7), random.randint(0,7)),
    	(random.randint (0,7), random.randint(0,7))
    ]
    rocks = []

    for pos in rock_positions:
    	rock = Rock()
    	GAME_BOARD.register(rock)
    	GAME_BOARD.set_el(pos[0], pos[1], rock)
    	rocks.append(rock)

    #### INITIALIZE PLAYER/S
    global PLAYER
    PLAYER = Player()
    #PLAYER.IMAGE = "Princess"
    GAME_BOARD.register(PLAYER)
    GAME_BOARD.set_el(2,2,PLAYER)



    ###INITIALIZE SNAKE
    global baddie_x 
    global baddie_y 
    global SNAKE
    global baddie_speed 

    baddie_x = random.randint(0 , GAME_WIDTH - 1) #initialize bad guy at random location
    baddie_y = random.randint(1 , GAME_HEIGHT - 1)

    SNAKE = AwesomePython() #snake is new instance of Awesome python
    GAME_BOARD.register(SNAKE)
    GAME_BOARD.set_el(baddie_x, baddie_y, SNAKE)
    baddie_speed = 1 

    pyglet.clock.schedule_interval(baddie_move, 1) #call bad guy function regularly




    #### INITIALIZE ITEM
    global ITEM
    global item_x 
    global item_y 
    ITEM = Items()
    GAME_BOARD.register(ITEM)
    item_x= random.randint(0 , GAME_WIDTH - 1)
    item_y= random.randint(0 , GAME_HEIGHT - 1)
    GAME_BOARD.set_el(item_x, item_y, ITEM)   
    
    pyglet.clock.schedule_interval(make_item_pop_up, 3)
    
	


def baddie_move(dt):
	global baddie_x
	global baddie_y
	global SNAKE
	global baddie_speed
	GAME_BOARD.del_el(baddie_x, baddie_y)


	if baddie_y == 0: #if y position is equal to 0)
		baddie_speed = (baddie_speed * -1) #then reverse the speed 
	elif baddie_y == 7:  
		baddie_speed = (baddie_speed * -1)
	else:
		baddie_speed = baddie_speed
	

	baddie_y += baddie_speed
	GAME_BOARD.set_el(baddie_x, baddie_y, SNAKE)

def make_item_pop_up(dt):
	global item_x 
	global item_y

	GAME_BOARD.del_el(item_x, item_y)
	
	ITEM.sprite = change_item_sprite()

	if PLAYER.x == item_x and PLAYER.y == item_y:
		GAME_BOARD.set_el(item_x, item_y, PLAYER)
	
	item_x = random.randint(0, GAME_WIDTH-1)
	item_y = random.randint(0, GAME_HEIGHT-1)
	GAME_BOARD.set_el(item_x, item_y , ITEM)	



def keyboard_handler():
	direction = None

	if KEYBOARD[key.UP]:
		direction = "up"
	if KEYBOARD[key.DOWN]:
		direction = "down"
	if KEYBOARD[key.LEFT]:
		direction = "left"
	if KEYBOARD[key.RIGHT]:
		direction = "right"

	
		
	if direction:
		next_location = PLAYER.next_pos(direction)
		next_x = next_location[0]
		next_y = next_location[1]

		if (-1 < next_x < GAME_WIDTH) and (-1 < next_y < GAME_HEIGHT):

			existing_el = GAME_BOARD.get_el(next_x, next_y) #Returns location of object

			if existing_el: #if this equals True (so there IS an object in the spot):
				existing_el.interact(PLAYER) #run the interact method on element that it stores
			#as existing_el

			if existing_el is None or not existing_el.SOLID:
				GAME_BOARD.del_el(PLAYER.x, PLAYER.y)
				GAME_BOARD.set_el(next_x, next_y, PLAYER)

def change_item_sprite():
	sprite_list =  [
					"cheetos.png",
					"sandal.png",
					"dice.png",
					"mtdew.png",
					"emacslogo.png"
				]
	new_item_sprite = pyglet.sprite.Sprite(pyglet.resource.image(sprite_list[random.randint(0,4)]))
	return new_item_sprite
    
def change_sprite(inventory):
	
	sprite_list = [
					"beard1.png",
					"beard1.png",
					"beard2.png",
					"beard2.png",
					"beard3.png",
					"beard3.png",
					"beard4.png",
					"beard4.png",
					"beard5.png",
					"beard5.png",
					"beard5.png",
					"beard5.png",
					"beard5.png",
					"beard5.png",
					"beard5.png",
					"beard5.png"
					]
	#if len(inventory) <= 5:
	new_sprite = pyglet.sprite.Sprite(pyglet.resource.image(
										 sprite_list[len(inventory)]))

	#else:
	#	GAME_BOARD.draw_msg("You win!")
	return new_sprite    



# def make_items_pop(dt):
# 	#first, make the item appear
# 	item = Items()
# 	GAME_BOARD.register(item)
# 	location = (random.randint(0,5), random.randint(0,5))
# 	print location
# 	GAME_BOARD.set_el(location[0], location[1], item)
# 	#then, add those coordinates to our list
# 	global item_list
# 	item_list.append(location)
# 	#then, if item list has more than one item on it, delete it
# 	if len(item_list) >= 1:
# 		GAME_BOARD.del_el((item_list[-1])[0], (item_list[-1])[1])
# 		print item_list[-1]

# 	