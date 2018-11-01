from pygame.locals import *
import pygame
import time
import math
from random import randint

pixel=10
def text_to_screen(screen, text, x, y, size = 50, color = (200, 000, 000), font_type = 'Comic Sans MS'):
	text = str(text)
	font = pygame.font.SysFont(font_type, size)
	text = font.render(text, True, color)
	screen.blit(text, (x, y))

def isCollision(x1,y1,x2,y2,bsize):
	if x1 >= x2 and x1 < x2 + bsize:
		if y1 >= y2 and y1 < y2 + bsize:
			return True
	return False

class Apple:
	x = 0
	y = 0
	step = pixel
 
	def __init__(self,x=5,y=5,offset=[0,0]):
		self.x = x * pixel
		self.y = y * pixel
		self.offset=offset
 
	def draw(self, surface, image):
		surface.blit(image,(self.x+self.offset[0], self.y+self.offset[1])) 


class Player:
	def __init__(self,length=3, offset=[0,0]):
		self.offset=offset
		self.dead=False
		self.score=0
		self.x=[0]
		self.y=[0]
		self.direction=0
		self.updateCountMax = 2
		self.updateCount = 0
		self.step = pixel
		self.length=length
		for i in range(0,2000):
			self.x.append(-100)
			self.y.append(-100)
		self.x[1] = 1*pixel+self.offset[0]
		self.x[2] = 2*pixel+self.offset[0]


	def update(self):
 
		self.updateCount = self.updateCount + 1
		if self.updateCount > self.updateCountMax:
 
			# update previous positions
			for i in range(self.length-1,0,-1):
				self.x[i] = self.x[i-1]
				self.y[i] = self.y[i-1]
 
			# update position of head of snake
			if not self.dead:
				if self.direction == 0:
					self.x[0] = self.x[0] + self.step
				if self.direction == 1:
					self.x[0] = self.x[0] - self.step
				if self.direction == 2:
					self.y[0] = self.y[0] - self.step
				if self.direction == 3:
					self.y[0] = self.y[0] + self.step
 
			self.updateCount = 0
	
	def moveRight(self):
		if not self.direction==1:
			self.direction = 0
 
	def moveLeft(self):
		if not self.direction==0:
			self.direction = 1
 
	def moveUp(self):
		if not self.direction==3:
			self.direction = 2
 
	def moveDown(self):
		if not self.direction==2:
			self.direction = 3

	def draw(self, surface, image):
		for i in range(0,self.length):
			surface.blit(image,(self.x[i]+self.offset[0],self.y[i]+self.offset[1])) 


class App:


	def __init__(self,draw=False,keys_control=False,name="input",offset=[0,0], numPlayers=3, polje_x=10, polje_y=10):
		self.offset=offset
		self.numPlayers=numPlayers
		self._display_surf=None
		self._image_surf = []
		self._apple_surf = []
		self._running=True
		self.player= []
		self.apple=[]
		self.filename=name
		off1=self.getStacked(resx=1366, resy=768, poljex=polje_x, poljey=polje_y)
		self.windowWidth=polje_x*pixel
		self.windowHeight=polje_y*pixel
		self.dead=0

		self.is_drawing=draw		
		if not self.is_drawing:
			self.keyboard_control=self.is_drawing
		else: self.keyboard_control=keys_control
		for i in range (self.numPlayers): 
			off=off1[i]
			self.player.append(Player(offset=off)) 
			self.apple.append(Apple(x=randint(1,int(math.floor(self.windowWidth /pixel))-1 ),y=randint(1,int(math.floor(self.windowHeight /pixel))-1 ),offset=off)) 
		print (int(math.floor(self.windowHeight /pixel) ))

	def getStacked (self, resx=1366, resy=768, poljex=10, poljey=10):
		out=[]
		global pixel
		p1=math.floor(pixel*(resx/(math.ceil(math.sqrt(self.numPlayers) )*poljex*pixel) ) )
		p2=math.floor(pixel*(resy/(math.ceil(math.sqrt(self.numPlayers) )*poljey*pixel) ) )
		if p1<p2:
			pixel=int(p1)
		else: pixel=int(p2)
		k=0
		i=0
		j=0
		while k<self.numPlayers:
			out.append ([poljex*pixel*i,poljey*pixel*j])
			i+=1
			if i == (math.ceil(math.sqrt(self.numPlayers))):
				i=0
				j+=1
			k+=1
		return out



	
	def keys_control(self,i):
		file=open (self.filename+str(i)+".txt", "w")
		pygame.event.pump()
		keys = pygame.key.get_pressed() 
		if (keys[K_d]):
			self.player[i].moveRight()
			file.write("d")
 
		elif (keys[K_a]):
			self.player[i].moveLeft()
			file.write("a")

		elif (keys[K_w]):
			self.player[i].moveUp()
			file.write("w")
 
		elif (keys[K_s]):
			self.player[i].moveDown()
			file.write("s")
 
		elif (keys[K_ESCAPE]) or (keys[K_q]):
			self._running = False
			file.write("q")
		file.close()

	def file_control (self,i):
		with open (self.filename+str(i)+".txt", "r") as file:
			input=file.read()
			if (input=="d"):
				self.player[i].moveRight()
 
			elif (input=="a"):
				self.player[i].moveLeft()
 
			elif (input=="w"):
				self.player[i].moveUp()
 
			elif (input=="s"):
				self.player[i].moveDown()
 
			elif (input=="q"):
				self._running = False

	def on_init (self):
		if self.is_drawing:
			pygame.init()
			self._display_surf=pygame.display.set_mode ((0,0),pygame.FULLSCREEN)#((self.windowWidth*(math.ceil(math.sqrt(self.numPlayers))), self.windowHeight*(math.ceil(math.sqrt(self.numPlayers)))))
			pygame.display.set_caption('AI_Test_SNAKE')
			for i in range (self.numPlayers): 
				p=pygame.Surface((pixel, pixel))
				p.fill((255, 255, 255))
				self._image_surf.append (p)
				a =pygame.Surface((pixel, pixel))
				a.fill((255, 0, 0))
				self._apple_surf.append(a)
			self._running=True

	def on_render(self,i):
		if not self.player[i].dead: 
			self.player[i].draw(self._display_surf, self._image_surf[i])
			self.apple[i].draw(self._display_surf, self._apple_surf[i])
			text_to_screen(self._display_surf, "Snake"+str(i)+": "+str(self.player[i].score), self.player[i].offset[0], self.player[i].offset[1], size = pixel)	
		else: text_to_screen(self._display_surf, "Snake"+str(i)+" DEAD", self.player[i].offset[0], self.player[i].offset[1]+int(self.windowHeight/2), size = pixel)
		pygame.draw.rect(self._display_surf, (255, 0, 0), pygame.Rect(0+self.player[i].offset[0], 0+self.player[i].offset[1], self.windowWidth, self.windowHeight), 1)
	
	def on_loop(self,j):
		self.player[j].update()
 
		# does snake eat apple?
		for i in range(0,self.player[j].length):
			if isCollision(self.apple[j].x, self.apple[j].y, self.player[j].x[i], self.player[j].y[i], pixel):
				self.apple[j].x = randint(1,int(self.windowWidth /pixel)-1 ) * pixel
				self.apple[j].y = randint(1,int(self.windowHeight/pixel)-1 ) * pixel
				self.player[j].length = self.player[j].length + 1
				self.player[j].score+=1
 
 
		# does snake collide with itself?
		for i in range(2,self.player[j].length):
			if isCollision(self.player[j].x[0],self.player[j].y[0],self.player[j].x[i], self.player[j].y[i], pixel-1):
				if not self.player[j].dead:
					self.dead+=1
					print("SNAKE "+str(j)+" dead, ate tail, SCORE:"+str (self.player[j].score))
					self.player[j].dead=True

		#does snake collide with wall?
		if (self.player[j].x[0]>=self.windowWidth) or (self.player[j].x[0]<0) or (self.player[j].y[0]>=self.windowHeight) or (self.player[j].y[0]<0):
			if not self.player[j].dead:
				self.dead+=1
				self.player[j].dead=True
				print ("SNAKE "+ str(j) + " dead, hit wall, SCORE:"+str (self.player[j].score))
 
		pass

	def on_execute(self,tick=30.0/1000.0):
		if self.on_init() == False:
			self._running = False
		while( self._running ):
			if self.is_drawing:
				self._display_surf.fill((0,0,0))
			for i in range (self.numPlayers):
				if self.keyboard_control:
					self.keys_control(i)
				self.file_control (i)
				self.on_loop(i)
				if self.is_drawing:
					self.on_render(i)
			if self.is_drawing:
				pygame.display.flip()
				time.sleep (tick);
			if self.dead>=self.numPlayers:
				#self._running=False
				pass

if __name__ == "__main__" :
	theApp = App(draw=True, keys_control=True, numPlayers=3).on_execute()