import pygame
import pygame.font as pygfont
import pygame.mouse as pymouse
import pygame.draw as pygdraw
pygfont.init()

font = pygfont.SysFont("Arial",16)

class Button():
	def __init__(self,x,y,w,h,text,callback,colorBase=(175,175,175),colorOutlineBase=(100,100,100),colorOutlineHighlight=(255,255,255),textColor=(0,0,0)):
		self.pos = [x,y]
		self.size = [w,h]
		self.Rect = pygame.Rect(x,y,w,h)

		self.colorBase = colorBase
		self.colorOutlineBase = colorOutlineBase
		self.colorOutlineHighlight = colorOutlineHighlight
		self.textColor = textColor

		self.callback = callback
		self.text = text

		self.mouseStop = False

		self.fontSize = 72
		self.font = pygfont.SysFont("Arial",self.fontSize)
		while self.font.size(self.text)[0] > self.size[0]:
			self.fontSize -= 1
			self.font = pygfont.SysFont("Arial",self.fontSize)
			
		while self.font.size(self.text)[1] > self.size[1]:
			self.fontSize -= 1
			self.font = pygfont.SysFont("Arial",self.fontSize)

	def render(self,surface,mousePos,mouseButton):
		pygdraw.rect(surface,self.colorBase,self.Rect)
		mouseInArea = False

		text = self.font.render(self.text, False, self.textColor)
		surface.blit(text,self.Rect)

		if(mousePos[0] in range(self.pos[0],self.pos[0]+self.size[0])):
			if(mousePos[1] in range(self.pos[1],self.pos[1]+self.size[1])):
				mouseInArea = True

		if(mouseInArea):
			pygdraw.rect(surface,self.colorOutlineHighlight,self.Rect,width=2)
			if(mouseButton[1] and not self.mouseStop):
				self.callback()
				self.mouseStop = True
			elif(not mouseButton[1]):
				self.mouseStop = False
		else:
			pygdraw.rect(surface,self.colorOutlineBase,self.Rect,width=2)
			self.mouseStop = False

	def getX(self):
		return self.pos[0]

	def getY(self):
		return self.pos[1]