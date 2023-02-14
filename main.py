import pygame, sys, time
import pygame.draw as pygdraw
import pygame.font as pygfont

import datetime
from cellboard import Board
from userInputs import Button

boardSize = 7
mines = int(boardSize**2*.15)
board = Board(boardSize)
board.generate(mines)

pygfont.init()

numericFont = pygfont.SysFont("Arial",14)
minesFont = pygfont.SysFont("Arial",26)

pygame.init()
screenSize = [640,480]
window = pygame.display.set_mode(screenSize,flags=pygame.RESIZABLE)
pygame.display.set_caption("PYпер")


mouse = [0,0]
mouseButtons = {1:False,2:False,3:False}
numericColor = {1:(0,255,0),2:(111,255,0),3:(171,255,0),4:(213,255,0),5:(255,213,0),6:(255,162,0),7:(255,119,0),8:(255,56,0),9:(255,0,0)}

highligthedCellIndex = -1
canReveal = True
canFlag = True
#game states
# 0 - gaming
# 1 - win
# 2 - lose
# 3 - generating
gameState = 0

currentTime = datetime.datetime.now().time()
gameStartTime = datetime.timedelta(hours=currentTime.hour,minutes=currentTime.minute,seconds=currentTime.second)
IGTime = gameStartTime

def resetField():
	global board, gameState,highligthedCellIndex, gameStartTime, IGTime
	highligthedCellIndex = -1
	gameState = 0
	canReveal = True
	canFlag = True
	board.resetReveal = True
	board.generate(mines)

	currentTime = datetime.datetime.now().time()
	gameStartTime = datetime.timedelta(hours=currentTime.hour,minutes=currentTime.minute,seconds=currentTime.second)
	IGTime = gameStartTime

def resizeField(offsetx=0,offsety=0):
	global board,mines, highligthedCellIndex
	highligthedCellIndex = -1
	if((board.size[0]+offsetx > 0) and (board.size[1]+offsety > 0)):
		board.size = [board.size[0]+offsetx,board.size[1]+offsety]
	board.generate(mines)

def resetMines():
	global board,mines
	mines = int((board.size[0]*board.size[1]) * .15)
	board.mines = mines

def offsetMines(offset=0):
	global board,mines
	mines += offset
	board.mines = mines

buttons = [
			Button(0,0,128,32,"Сбросить поле",resetField),
			Button(128,0,128,32,"Сбросить кол-во мин",resetMines),
			Button(256,0,64,16,"Мины: +1",lambda: offsetMines(1)),
			Button(256,16,64,16,"Мины: -1",lambda: offsetMines(-1)),
			Button(320,0,128,16,"Поле: ширина +1",lambda: resizeField(offsetx=1)),
			Button(320,16,128,16,"Поле: ширина -1",lambda: resizeField(offsetx=-1)),
			Button(448,0,128,16,"Поле: высота +1",lambda: resizeField(offsety=1)),
			Button(448,16,128,16,"Поле: высота -1",lambda: resizeField(offsety=-1))
		  ]


while True:
	if(gameState == 0):
		currentTime = datetime.datetime.now().time()
		IGTime = datetime.timedelta(hours=currentTime.hour,minutes=currentTime.minute,seconds=currentTime.second)

	window.fill((25,25,25))
	
	while pygame.event.peek():
		event = pygame.event.poll()
		if(event.type == pygame.WINDOWCLOSE):
			pygame.quit()
			sys.exit()
		if(event.type == pygame.MOUSEMOTION):
			mouse = [event.__dict__["pos"][0],event.__dict__["pos"][1]]
		if(event.type == pygame.MOUSEBUTTONDOWN):
			mouseButtons[event.__dict__["button"]] = True
		if(event.type == pygame.MOUSEBUTTONUP):
			mouseButtons[event.__dict__["button"]] = False
		if(event.type == pygame.WINDOWRESIZED):
			screenSize = [event.__dict__["x"],event.__dict__["y"]]


	#render cycle
	cellWidth = screenSize[0] // board.size[0]
	menuHeight = screenSize[1] // 6
	cellHeight = (screenSize[1] - menuHeight) // board.size[1]
	minesFont = pygfont.SysFont("Arial",menuHeight//3)
	numericFont = pygfont.SysFont("Arial",min(cellHeight//2,cellWidth//2))
	

	for cell in board.cells:
		cell.fix()

		rect = pygame.Rect(cell.getX()*cellWidth, cell.getY()*cellHeight+menuHeight, cellWidth, cellHeight)
		insideRect = pygame.Rect(rect.x+2, rect.y+2, cellWidth-4, cellHeight-4)

		mouserect = pygame.Rect(mouse[0], mouse[1], 1, 1)

		if(rect.colliderect(mouserect)):
			pygdraw.rect(window, (255,0,0), rect, width=2)
			highligthedCellIndex = board.cells.index(cell)
		else:
			pygdraw.rect(window, (0,0,0), rect, width=2)

		
		if(cell.cellType == 1): #bomb cell
			middleX = (rect.x + (rect.x+cellWidth)) // 2
			middleY = (rect.y + (rect.y+cellHeight)) // 2
			pygdraw.circle(window,(0,0,0),(middleX,middleY),min(cellHeight/4,cellWidth/4))
			if(gameState == 0):
				if(not cell.flagged):
					pygdraw.rect(window,(155,155,155),insideRect)
				else:
					pygdraw.rect(window,(56,144,56),insideRect)
			else:
				if(not cell.flagged):
					pygdraw.line(window,(255,0,0),(insideRect.x,insideRect.y),(insideRect.x+insideRect.w,insideRect.y+insideRect.h))
					pygdraw.line(window,(255,0,0),(insideRect.x,insideRect.y+insideRect.h),(insideRect.x+insideRect.w,insideRect.y))
				else:
					pygdraw.rect(window,(0,255,0),insideRect,width=2)

		elif(cell.cellType == 2): #numeric cell
			middleX = (rect.x + (rect.x+cellWidth)) // 2
			middleY = (rect.y + (rect.y+cellHeight)) // 2
			text = numericFont.render(str(cell.minesNear),False,numericColor[cell.minesNear])
			middleX -= text.get_size()[0]//2
			middleY -= text.get_size()[1]//2
			window.blit(text,(middleX,middleY))
			if(not cell.revealed):
				if(cell.flagged):
					pygdraw.rect(window,(56,144,56),insideRect)
				else:
					pygdraw.rect(window,(155,155,155),insideRect)

		else: #none cell
			if(not cell.revealed):
				if(cell.flagged):
					pygdraw.rect(window,(56,144,56),insideRect)
				else:
					pygdraw.rect(window,(155,155,155),insideRect)

	if(gameState == 0):
		minesLeft = board.mines - board.getFlaggedCells()
		text = minesFont.render("Мин осталось:" + str(minesLeft),False,(255,255,255))
		window.blit(text,(screenSize[0]/16,screenSize[1]/14))

	timeText = minesFont.render(str(IGTime - gameStartTime),False,(255,255,255))
	window.blit(timeText,(screenSize[0] - screenSize[0]/4,screenSize[1]/16))

	if(gameState == 1):
		text = minesFont.render("Вы победили!",True,(255,255,255))
		window.blit(text,(screenSize[0]/16,screenSize[1]/16))
	if(gameState == 2):
		text = minesFont.render("Вы проиграли!",True,(255,255,255))
		window.blit(text,(screenSize[0]/16,screenSize[1]/16))

	for button in buttons:
		button.render(window,mouse,mouseButtons)
			

	#gaming cycle

	if(mouseButtons[1] and gameState == 0):
		if(highligthedCellIndex > -1 and canReveal):
			cell = board.cells[highligthedCellIndex]
			cell.revealed = True
			canReveal = False
			if(cell.cellType == 1):
				gameState = 2
			else:
				board.revealArea(cell.pos)
	else:
		canReveal = True

	if(mouseButtons[3] and gameState == 0):
		if(highligthedCellIndex > -1 and canFlag):
			cell = board.cells[highligthedCellIndex]
			cell.flagged = not cell.flagged
			canFlag = False
	else:
		canFlag = True

	IGmines = board.getMinesLeft()
	if(IGmines[1] == 0):
		gameState = 1

	pygame.display.flip()

		


