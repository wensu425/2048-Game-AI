from __future__ import absolute_import, division, print_function
import copy
import random
import numpy as np
import math
MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
ACTIONS = [(0, -1), (-1, 0), (0, 1), (1, 0)]
BLACK = (0, 0, 0)
RED = (244, 67, 54)
PINK = (234, 30, 99)
PURPLE = (156, 39, 176)
DEEP_PURPLE = (103, 58, 183)
BLUE = (33, 150, 243)
TEAL = (0, 150, 136)
L_GREEN = (139, 195, 74)
GREEN = (60, 175, 80)
ORANGE = (255, 152, 0)
DEEP_ORANGE = (255, 87, 34)
BROWN = (121, 85, 72)
COLORS = { 0:BLACK, 2:RED, 4:PINK, 8:PURPLE, 16:DEEP_PURPLE,
               32:BLUE, 64:TEAL, 128:L_GREEN, 256:GREEN,
               512:ORANGE, 1024: DEEP_ORANGE, 2048:BROWN, 
               4096:DEEP_PURPLE, 8192:DEEP_ORANGE, 16384:BROWN, 32768:TEAL}
w =[[4**15, 4**14, 4**13, 4**12],
	[4**8, 4**9,  4**10,  4**11],
	[4**7,  4**6,  4**5,  4**4],
	[ 4**0,  4**1,  4**2,  4**3]]

class GameTreeNode:
	def __init__(self,state,score):
		self.ismax=True
		self.state=state
		self.depth=0
		self.child=[]
		self.parent=None
		self.move=None
		self.score=score
	def is_chance(self):
		self.ismax=False
	def is_max(self):
		self.ismax=True

class Gametree:
	"""main class for the AI"""
	# Hint: Two operations are important. Grow a game tree, and then compute minimax score.
	# Hint: To grow a tree, you need to simulate the game one step.
	# Hint: Think about the difference between your move and the computer's move.
	def __init__(self, root_state, depth_of_tree, current_score): 
		self.root_state=root_state
		self.depth_of_tree=depth_of_tree
		self.current_score=current_score
	# expectimax for computing best move
	def expectimax(self, gtnode):
		#if the node is a terminal, return the value of state
		if(gtnode.depth==3):
			score=0
			for i in range(4):
				for j in range(4):
					score += w[i][j] * gtnode.state[i][j]
			penalty = 0
			for i in range(0,4):
				for j in range(0,4):
					if( (i+1)>=0 and (i+1)<=3 ):
						penalty += abs(gtnode.state[i][j] - gtnode.state[i+1][j])
					if( (i-1)>=0 and (i-1)<=3 ):
						penalty += abs(gtnode.state[i][j] - gtnode.state[i-1][j])
					if( (j+1)>=0 and (j+1)<=3 ):
						penalty += abs(gtnode.state[i][j] - gtnode.state[i][j+1])
					if( (j-1)>=0 and (j-1)<=3 ):
						penalty += abs(gtnode.state[i][j] - gtnode.state[i][j-1])
			return score-penalty
		#if the node has ismax flag, view it as a max player
		elif(gtnode.ismax):
			#set value to infinity
			value=float ("-inf")
			for i in range (len(gtnode.child)):
				value=max(value,self.expectimax(gtnode.child[i]))
			return value
		#if the node does not have ismax flag, view it as a chance player
		elif(gtnode.ismax==False):
			value=0
			for i in range (len(gtnode.child)):
				value=value+self.expectimax(gtnode.child[i])*(1/len(gtnode.child))
			return value
	# function to return best decision to game
	def compute_decision(self):
		#change this return value when you have implemented the function
		#grow the starting from your root node to the specified depth
		gtnode=GameTreeNode(copy.deepcopy(self.root_state),self.current_score)
		self.growTree(gtnode)
		#after growing tree to specified depth, run the expectimax algorithms to find optimal move
		#and return that move
		maxval=-1
		returnval=-1
		#print("The root node is: \n", np.asmatrix(gtnode.state))
		#print("The number of child node: ", len(gtnode.child))
		for i in range (len(gtnode.child)):
			cur=self.expectimax(gtnode.child[i])
			#print("The expectimax value of move ", i, " is: ",cur)
			if(cur>maxval):
				maxval=cur
				returnval=gtnode.child[i].move
		#print("The max expectimax value is: ", maxval)
		if(returnval<0):
			return -1
		else:
			return returnval
	
	def growTree(self,gtnode):
		#print("The gtnode depth is: ", gtnode.depth)
		#print("TileMatrix of gtnode: \n", np.asmatrix(gtnode.state))
		while(gtnode.depth<self.depth_of_tree):
			#Create a deepcopy of the input node
			copynode=copy.deepcopy(gtnode)
			#check if the GameTreeNode is a max player
			if(gtnode.ismax):
				#Simulate at most 4 moves for a max player node
				for i in range(4):
					max_simulator=Simulator(copy.deepcopy(copynode.state),gtnode.score)
					max_simulator.move(i)
					#check if gameover and childnode equal to parent node
					if(max_simulator.checkIfCanGo() and copynode.state!=max_simulator.tileMatrix):
						#Create chance_childnode and set up the node
						chance_childnode=GameTreeNode(copy.deepcopy(max_simulator.tileMatrix),max_simulator.total_points)
						chance_childnode.is_chance()
						chance_childnode.depth=copynode.depth+1
						gtnode.child.append(chance_childnode)
						chance_childnode.move=i
						chance_childnode.score=max_simulator.total_points
						#print("The chance node depth is: ", chance_childnode.depth)
						#print("Move in direction: ", i)
						#print("The chance node state is: \n", np.asmatrix(chance_childnode.state), "\n")
						#recursion
						self.growTree(chance_childnode)
			#check if the GameTreeNode is chance player node
			if(gtnode.ismax==False):
				#Find tile equals '0' through matrix
				for i in range(4):
					for j in range(4):
						chance_simulator=Simulator(copy.deepcopy(copynode.state),gtnode.score)
						if chance_simulator.tileMatrix[i][j]==0:
							chance_simulator.tileMatrix[i][j]=2
							#Create max_childnode and set up the node
							max_childnode=GameTreeNode(copy.deepcopy(chance_simulator.tileMatrix),chance_simulator.total_points)
							max_childnode.is_max()
							max_childnode.depth=copynode.depth+1
							gtnode.child.append(max_childnode)
							max_childnode.score=chance_simulator.total_points
							#print("The max node depth is: ", max_childnode.depth)
							#print("The max node state is: \n", np.asmatrix(max_childnode.state),"\n")
							#recursion
							if(max_childnode.depth<3):
								self.growTree(max_childnode)
			return copynode

class Simulator:
	def __init__(self,tileMatrix,score):
		self.total_points = score
		self.default_tile = 2
		self.board_size = 4
		self.tileMatrix = tileMatrix
		self.undoMat = []
	def move(self, direction):
		for i in range(0, direction):
			self.rotateMatrixClockwise()
		if self.canMove():
			self.moveTiles()
			self.mergeTiles()
		for j in range(0, (4 - direction) % 4):
			self.rotateMatrixClockwise()
	def moveTiles(self):
		tm = self.tileMatrix
		for i in range(0, self.board_size):
			for j in range(0, self.board_size - 1):
				while tm[i][j] == 0 and sum(tm[i][j:]) > 0:
					for k in range(j, self.board_size - 1):
						tm[i][k] = tm[i][k + 1]
					tm[i][self.board_size - 1] = 0
	def mergeTiles(self):
		tm = self.tileMatrix
		for i in range(0, self.board_size):
			for k in range(0, self.board_size - 1):
				if tm[i][k] == tm[i][k + 1] and tm[i][k] != 0:
					tm[i][k] = tm[i][k] * 2
					tm[i][k + 1] = 0
					self.total_points += tm[i][k]
					self.moveTiles()
	def checkIfCanGo(self):
		tm = self.tileMatrix
		for i in range(0, self.board_size ** 2):
			if tm[int(i / self.board_size)][i % self.board_size] == 0:
				return True
		for i in range(0, self.board_size):
			for j in range(0, self.board_size - 1):
				if tm[i][j] == tm[i][j + 1]:
					return True
				elif tm[j][i] == tm[j + 1][i]:
					return True
		return False
	def canMove(self):
		tm = self.tileMatrix
		for i in range(0, self.board_size):
			for j in range(1, self.board_size):
				if tm[i][j-1] == 0 and tm[i][j] > 0:
					return True
				elif (tm[i][j-1] == tm[i][j]) and tm[i][j-1] != 0:
					return True
		return False
	def rotateMatrixClockwise(self):
		tm = self.tileMatrix
		for i in range(0, int(self.board_size/2)):
			for k in range(i, self.board_size- i - 1):
				temp1 = tm[i][k]
				temp2 = tm[self.board_size - 1 - k][i]
				temp3 = tm[self.board_size - 1 - i][self.board_size - 1 - k]
				temp4 = tm[k][self.board_size - 1 - i]
				tm[self.board_size - 1 - k][i] = temp1
				tm[self.board_size - 1 - i][self.board_size - 1 - k] = temp2
				tm[k][self.board_size - 1 - i] = temp3
				tm[i][k] = temp4
