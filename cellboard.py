import random

class Board():
	def __init__(self,size):
		self.size = [size,size]
		self.cells = []
		self.mines = 0

		self.resetReveal = False

	def generate(self,mines):
		self.cells = []
		self.mines = mines
		self.resetReveal = True

		while(self.mines >= (self.size[0] * self.size[1])):
			print("mines too big",self.mines)
			self.mines = self.mines // 2

		for x in range(self.size[0]):
			for y in range(self.size[1]):
				self.cells.append(Cell([x,y]))

		minesGenerated = 0
		while minesGenerated < self.mines:
			print("generating mines: ",str(int((minesGenerated/mines)*10)))
			cell = random.choice(self.cells)
			if(cell.pos != [0,0]):
				if(cell.cellType != 1):
					cell.cellType = 1
					minesGenerated += 1
		print("--")

		for i in range(len(self.cells)):
			cell = self.cells[i]
			pos = cell.pos
			#get cell indexes
			topCell = self.getCellByPos([pos[0],pos[1]-1])
			rightCell = self.getCellByPos([pos[0]+1,pos[1]])
			bottomCell = self.getCellByPos([pos[0],pos[1]+1])
			leftCell = self.getCellByPos([pos[0]-1,pos[1]])

			topRightCell = self.getCellByPos([pos[0]+1,pos[1]-1])
			topLeftCell = self.getCellByPos([pos[0]-1,pos[1]-1])

			bottomRightCell = self.getCellByPos([pos[0]+1,pos[1]+1])
			bottomLeftCell = self.getCellByPos([pos[0]-1,pos[1]+1])

			#if exists (not None) get object
			if(topCell):
				topCell = self.cells[topCell]
			if(rightCell):
				rightCell = self.cells[rightCell]
			if(bottomCell):
				bottomCell = self.cells[bottomCell]
			if(leftCell):
				leftCell = self.cells[leftCell]

			if(topRightCell):
				topRightCell = self.cells[topRightCell]
			if(topLeftCell):
				topLeftCell = self.cells[topLeftCell]
			if(bottomRightCell):
				bottomRightCell = self.cells[bottomRightCell]
			if(bottomLeftCell):
				bottomLeftCell = self.cells[bottomLeftCell]

			#check for mines
			if(topCell and topCell.cellType == 1):
				cell.minesNear += 1
			if(rightCell and rightCell.cellType == 1):
				cell.minesNear += 1
			if(bottomCell and bottomCell.cellType == 1):
				cell.minesNear += 1
			if(leftCell and leftCell.cellType == 1):
				cell.minesNear += 1

			if(topRightCell and topRightCell.cellType == 1):
				cell.minesNear += 1
			if(topLeftCell and topLeftCell.cellType == 1):
				cell.minesNear += 1
			if(bottomRightCell and bottomRightCell.cellType == 1):
				cell.minesNear += 1
			if(bottomLeftCell and bottomLeftCell.cellType == 1):
				cell.minesNear += 1
			#if mines > 0 and cell is not determined then set to numeric block
			if(cell.minesNear > 0 and cell.cellType == 0):
				cell.cellType = 2

	def getCellByPos(self,pos):
		for i in range(len(self.cells)):
			if(self.cells[i].pos == pos):
				return i
		return None

	def getMinesLeft(self):
		countFlagged = 0
		countUnflagged = 0
		for cell in self.cells:
			if(cell.cellType == 1):
				if(not cell.flagged):
					countUnflagged += 1
				else:
					countFlagged += 1
		return (countFlagged,countUnflagged)

	def getFlaggedCells(self):
		count = 0
		for cell in self.cells:
			if(cell.flagged):
				count += 1
		return count

	def getCellObjectByPos(self,pos):
		i = self.getCellByPos(pos)
		if(i):
			return self.cells[i]
		else:
			return None

	def revealArea(self,cellPos,revealedCells=[],depth=0):
		try:
			if(depth == 0):
				revealedCells = []
			currentCell = self.cells[self.getCellByPos(cellPos)]

			if(currentCell.cellType == 1): return # if bomb do nothing
 
			if(cellPos in revealedCells): return #if revealed do nothing

			if(currentCell.cellType == 0 or currentCell.cellType == 2): #if empty or numeric, reveal
				currentCell.revealed = True

			revealedCells.append(cellPos)

			if(currentCell.cellType == 2): return #if numeric, do not reveal further

			if(cellPos[0] == 0): #if x == 0
				self.revealArea([cellPos[0] + 1,cellPos[1]],revealedCells=revealedCells,depth=depth+1) #expose right
				if(cellPos[1] == 0): #if y == 0
					self.revealArea([cellPos[0],cellPos[1]+1],revealedCells=revealedCells,depth=depth+1) #expose down
					self.revealArea([cellPos[0] + 1,cellPos[1] + 1],revealedCells=revealedCells,depth=depth+1) #expose right-down
				elif(cellPos[1] == self.size[1]-1): #if y == size.y
					self.revealArea([cellPos[0],cellPos[1]-1],revealedCells=revealedCells,depth=depth+1) #expose up
					self.revealArea([cellPos[0] + 1,cellPos[1] - 1],revealedCells=revealedCells,depth=depth+1) #expose right-up
				else:
					self.revealArea([cellPos[0],cellPos[1]+1],revealedCells=revealedCells,depth=depth+1) #expose down
					self.revealArea([cellPos[0],cellPos[1]-1],revealedCells=revealedCells,depth=depth+1) #expose up

			elif(cellPos[0] == self.size[0]-1): #if x == size.x
				self.revealArea([cellPos[0] - 1,cellPos[1]],revealedCells=revealedCells,depth=depth+1) #expose left
				if(cellPos[1] == 0): #if y == 0
					self.revealArea([cellPos[0],cellPos[1]+1],revealedCells=revealedCells,depth=depth+1) #expose down
					self.revealArea([cellPos[0] - 1,cellPos[1] + 1],revealedCells=revealedCells,depth=depth+1) #expose left-down
				elif(cellPos[1] == self.size[1]-1): #if y == size.y
					self.revealArea([cellPos[0],cellPos[1]-1],revealedCells=revealedCells,depth=depth+1) #expose up
					self.revealArea([cellPos[0] - 1,cellPos[1] - 1],revealedCells=revealedCells,depth=depth+1) #expose left-up
				else:
					self.revealArea([cellPos[0],cellPos[1]+1],revealedCells=revealedCells,depth=depth+1) #expose down
					self.revealArea([cellPos[0],cellPos[1]-1],revealedCells=revealedCells,depth=depth+1) #expose up

			elif(cellPos[1] == 0): #if y == 0
					self.revealArea([cellPos[0],cellPos[1]+1],revealedCells=revealedCells,depth=depth+1) #expose down
					if(cellPos[0] == 0): #if x == 0
						self.revealArea([cellPos[0] + 1,cellPos[1]],revealedCells=revealedCells,depth=depth+1) #expose right
						self.revealArea([cellPos[0] + 1,cellPos[1] + 1],revealedCells=revealedCells,depth=depth+1) #expose right-down
					elif(cellPos[0] == self.size[0]-1): #if x == size.x
						self.revealArea([cellPos[0] - 1,cellPos[1]],revealedCells=revealedCells,depth=depth+1) #expose left
						self.revealArea([cellPos[0] - 1,cellPos[1] + 1],revealedCells=revealedCells,depth=depth+1) #expose left-down
					else:
						self.revealArea([cellPos[0] + 1,cellPos[1]],revealedCells=revealedCells,depth=depth+1) #expose right
						self.revealArea([cellPos[0] - 1,cellPos[1]],revealedCells=revealedCells,depth=depth+1) #expose left

			elif(cellPos[1] == self.size[1]-1): #if y == size.y
					self.revealArea([cellPos[0],cellPos[1]-1],revealedCells=revealedCells,depth=depth+1) #expose up
					if(cellPos[0] == 0): #if x == 0
						self.revealArea([cellPos[0] + 1,cellPos[1]],revealedCells=revealedCells,depth=depth+1) #expose right
						self.revealArea([cellPos[0] + 1,cellPos[1] - 1],revealedCells=revealedCells,depth=depth+1) #expose right-up
					elif(cellPos[0] == self.size[0]-1): #if x == size.x
						self.revealArea([cellPos[0] - 1,cellPos[1]],revealedCells=revealedCells,depth=depth+1) #expose left
						self.revealArea([cellPos[0] - 1,cellPos[1] - 1],revealedCells=revealedCells,depth=depth+1) #expose left-up
					else:
						self.revealArea([cellPos[0] + 1,cellPos[1]],revealedCells=revealedCells,depth=depth+1) #expose right
						self.revealArea([cellPos[0] - 1,cellPos[1]],revealedCells=revealedCells,depth=depth+1) #expose left

			elif(cellPos[0] in range(1,self.size[0])):
				if(cellPos[1] in range(1,self.size[1])):
					self.revealArea([cellPos[0] + 1,cellPos[1]],revealedCells=revealedCells,depth=depth+1) #expose right
					self.revealArea([cellPos[0],cellPos[1]+1],revealedCells=revealedCells,depth=depth+1) #expose down
					self.revealArea([cellPos[0],cellPos[1]-1],revealedCells=revealedCells,depth=depth+1) #expose up
					self.revealArea([cellPos[0] - 1,cellPos[1]],revealedCells=revealedCells,depth=depth+1) #expose left
					self.revealArea([cellPos[0] - 1,cellPos[1] - 1],revealedCells=revealedCells,depth=depth+1) #expose left-up
					self.revealArea([cellPos[0] - 1,cellPos[1] + 1],revealedCells=revealedCells,depth=depth+1) #expose left-down
					self.revealArea([cellPos[0] + 1,cellPos[1] + 1],revealedCells=revealedCells,depth=depth+1) #expose right-down
					self.revealArea([cellPos[0] + 1,cellPos[1] - 1],revealedCells=revealedCells,depth=depth+1) #expose right-up
		except Exception as e:
			pass



# cellTypes:
# 0 - none
# 1 - mine
# 2 - numeric
class Cell():
	def __init__(self,pos):
		self.pos = pos
		self.cellType = 0
		self.minesNear = 0
		self.revealed = False
		self.flagged = False

	def __repr__(self):
		if(self.cellType == 0):
			return f"None at [{self.pos[0]},{self.pos[1]}]" + (", flagged" if self.flagged else "") + (", revealed" if self.revealed else "")
		elif(self.cellType == 1):
			return f"Mine at [{self.pos[0]},{self.pos[1]}]" + (", flagged" if self.flagged else "") + (", revealed" if self.revealed else "")
		elif(self.cellType == 2):
			return f"Empty at [{self.pos[0]},{self.pos[1]}]" + (", flagged" if self.flagged else "") + (", revealed" if self.revealed else "")
		elif(self.cellType == 3):
			return f"Numeric at [{self.pos[0]},{self.pos[1]}]" + (", flagged" if self.flagged else "") + (", revealed" if self.revealed else "")

	def fix(self):
		if(self.flagged and self.revealed):
			self.flagged = False

	def getX(self):
		return self.pos[0]

	def getY(self):
		return self.pos[1]

