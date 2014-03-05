import robot
'''
provides access to robot constructor.
'''

from random import shuffle
'''
Import shuffle function to randomize turn order.
'''

class Board:
	'''
	A representation of the game board.
	
	Keeps a collection of the robots in play
	and performs the logic for updating the board each tick.
	'''
	
	BOARD_SIZE = 10
	'''
	The size of the board, specifically the number of tiles on the side of a square board.
	
	If BOARD_SIZE is 0, the board is unbounded.
	'''
	
	actors = {}
	'''
	A dict containing the active actors on the board.
	'''

	destroyed = {}
	'''
	A dict for stashing destroyed actors.
	'''
	
	def __init__(self, scripts):
		'''
		Initializes robot.actors to add to Board
		
		@param scripts: function pointers to the scripts which define the robot behaviors.
		One robot will be created for each script provided.
		'''
		
		print("initializing board")
		
		for i in range(len(scripts)):
			robotName = "Robot_" + str(i)
			self.actors[robotName] = robot.Robot(5, 5, 0, scripts[i], robotName)

	def update(self):
		'''
		Updates the positions of all actors and performs all other simulation logic.
		'''
		
		# make a copy of the list of keys so python doesn't freak out if a robot gets deleted
		keys = list(self.actors.keys())

		# shuffle list for random turn order
		shuffle(keys)

		for key in keys:

			# double check that actors[key] has not been destroyed
			if key not in self.actors:
				continue

			# Have robot act
			self.actors[key].takeAction(self)

			# check to see if any robot has been destroyed
			keys2 = list(self.actors.keys())
			for key2 in keys2:

				if self.actors[key2].health == 0:

					print(self.actors[key2], " destroyed")

					# stash destroyed robot
					self.destroyed[key2] = self.actors[key2]

					# remove destroyed robot from robot list
					del self.actors[key2]

	def occupied(self, x, y):
		'''
		Returns true is board[x, y] is occupied.

		@returns true if there is an actor at coordinates (x,y).
		'''

		for key in self.actors:
			actor = self.actors[key]
			if x == actor.x and y == actor.y:
				return True

		return False