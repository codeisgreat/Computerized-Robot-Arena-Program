from actor import Actor

from math import cos, sin, radians

from utility import forwardCoords

import copy
'''
Import copy module for creating safe copies of board to pass to scripts.
'''

import logging
''' Import logging module. '''

class Robot(Actor):
	'''
	The parent class for all robot scripts.

	Each robot is given an x and y coordinate,
	a value for theta representing rotation,
	and a string with a unique identifying name for the robot.
	'''

	DEFAULT_HEALTH = 1
	'''
	The starting health value for robots on the field.
	'''
	
	script = None
	'''
	A function pointer to the script defining the behavior of the robot.
	'''

	def __init__(self, x, y, theta, script=None, name=None, health=DEFAULT_HEALTH):
		'''
		Constructor method.
		
		@param x: The starting x coordinate of the robot.
		
		@param y: The starting y coordinate of the robot.
		
		@param theta: The starting theta of the robot.
		
		@param script: A function pointer to the script defining the behavior of the robot.
		
		@param name: The name of the robot. If no name is provided a unique, random name will be provided.

		@param health: The starting health of the robot. Defaults to Robot::DEFAULT_HEALTH
		'''
		
		# set parameter values
		self.xPosition = x
		self.yPosition = y
		self.rotation = theta
		self.script = script
		self.health = health
		
		# if no name provided, create unique name
		if name is None:
			
			# name is the default string of the object,
			# which includes the memory address,
			# guaranteeing that the string is unique.
			name = id(self);
			
		self.name = name

	def takeAction(self, board):
		'''
		Call the behavior script and then take the chosen action.
		'''
		
		# call behavior script, passing in copies of self and board
		# behavior script returns the key of the action in Robot.ACTIONS
		action = self.script.decideAction(copy.copy(self), copy.deepcopy(board), list(Robot.ACTIONS.keys()))
		
		if (action in Robot.ACTIONS.keys()):
# 			logging.info("%s is going to %s" % (self.name, str(action)))
			
			action = Robot.ACTIONS[action]
			action(self, board)
		else:
			pass

	def turnLeft(self, board):
		'''
		Rotate the robot 90 degrees to the left.
		'''
		self.rotation = (self.rotation - 90) % 360
	
	def turnRight(self, board):
		'''
		Rotate the robot 90 degrees to the right
		'''
		self.rotation = (self.rotation + 90) % 360
		
	def shootProjectile(self, board):
		'''
		Creates a projectile in front and adds it to the board
		
		@param board: A reference to the board object. This is used for checking bounds and collisions.
		'''
		
		# get coordinates of space in front of robot
		# same code as in moveForward()
		targetX = self.xPosition + cos(radians(self.rotation))
		targetY = self.yPosition + sin(radians(self.rotation))
		
		board.spawnProjectile(targetX, targetY, self.rotation)
		
	def moveForward(self, board):
		'''
		Moves the robot forward one space in the current direction.
		If it runs into a wall, it will simply not move.
		
		@param board: A reference to the board object. This is used for checking bounds and collisions.
		'''
		
# 		logging.debug("%s is moving forward" % (self.name))

		# get the coordinates in front of the robot
		coords = forwardCoords(self.xPosition, self.yPosition, self.rotation, board)

		# if out of bounds, do nothing
		if coords is None:
			
# 			logging.debug('{} is off the board'.format(self.name)) # debugging output
			
			# exit
			return
		
		# ===================
		# TEST FOR COLLISIONS
		# ===================
		
		# retrieve list of actors in new space
		collidingActors = board.occupied(coords[0], coords[1])
		
		# if there are one or more actors in the new space
		if len(collidingActors) > 0:
			
			# debugging output
# 			logging.debug('actors in front of {}: {}'.format(self.name, str(collidingActors)))
			
			# iterate over actors in space
			for actor in collidingActors:
				
				# debugging output
# 				logging.debug(self.name + " to collide with actor " + actor)
				
				# if actor is robot, damage robot and destroy self
				if actor in board.getRobots():
					
					# debugging output
# 					logging.debug(self.name + " colliding with robot " + actor)
					
					# run collision logic
					board.collision(self.name, actor)
					
					# exit without moving
					return
		
		# no collisions, move to new coords
		if (self.health > 0):
			self.xPosition = coords[0]
			self.yPosition = coords[1]
	
	ACTIONS = {	'MOVE_FORWARD': moveForward,
				'TURN_RIGHT': turnRight,
				'TURN_LEFT': turnLeft,
				'SHOOT_PROJECTILE': shootProjectile }
	
	def __copy__(self):
		'''
		Create a safe copy of the robot, containing only positional and type info.
		'''
		
		return Robot(self.xPosition, self.yPosition, self.rotation, self.script, self.name, self.health)
