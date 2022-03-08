import pygame
import time

from pygame.locals import*
from time import sleep

class Sprite():
	def __init__(self, xPos, yPos, width, height, im):
		self.image = pygame.image.load(im)
		self.x = xPos
		self.y = yPos
		self.w = width
		self.h = height
		self.spawnX = xPos
		self.spawnY = yPos

	def changeImage(self, newIm):
		self.image = pygame.image.load(newIm)

	def storePrevPos(self):
		self.px = self.x
		self.py = self.y


class Mario(Sprite):
	def __init__(self, xPos, yPos):
		super(Mario, self).__init__(xPos, yPos, 60, 95, "mario0.png")
		self.vertVelocity = 2.0
		self.jump = False
		self.movement = False
		self.inAir = False
		self.onSurface = False
		self.airTime = 0
		self.imageNum = 0
		self.attack = False

	def collisionExit(self, sprite):
		if self.x + self.w > sprite.x and self.px + self.w <= sprite.x:
			self.x = sprite.x - self.w
		if self.x <= sprite.x + sprite.w and self.px >= sprite.x + sprite.w:
			self.x = sprite.x + sprite.w
		if self.y + self.h >= sprite.y and self.py + self.h <= sprite.y:
			self.y = sprite.y - self.h
			self.onSurface = True
		if self.y <= sprite.y + sprite.h and self.py >= sprite.y + sprite.h:
			self.y = sprite.y + sprite.h

	def attack(self):
		self.attack = true

	def update(self):
	#gravity acceleration
		self.vertVelocity += 1.3

	#stop gravity on surface
		if self.onSurface or self.y >= 500 - self.h:
			self.vertVelocity = 0.0
			self.inAir = False
			self.airTime = 0
			if self.y > 500 - self.h:
				self.y = 500 - self.h
		else:
			self.inAir = True

	#jumping
		if self.jump and self.airTime <= 5:
			self.vertVelocity += -5.0
			self.airTime += 1
			self.inAir = True

	#image change
		if self.movement == False and self.jump == False:
			self.changeImage("mario0.png")
		elif self.movement == True and self.jump == False:
			self.imageNum = (self.imageNum + 1)%6
			if self.imageNum == 0:
				self.imageNum += 1
			self.changeImage("mario" + str(self.imageNum) + ".png")

	#cleanup
		self.y += self.vertVelocity
		self.onSurface = False
		self.attack = False

class Goomba(Sprite):
	def __init__(self, xPos, yPos):
		super(Goomba, self).__init__(xPos, yPos, 99, 118, "goomba1.png")
		self. speed = 5
		self.collide = False
		self.fire = False
		self.burn = 0
		self.rem = False

	def collisionExit(self, sprite):
		if self.x + self.w >= sprite.x:
			self.collide = True
			if isinstance(sprite, Fireball):
				self.fire = True
		if self.x <= sprite.x + sprite.w:
			self.collide = True
			if isinstance(sprite, Fireball):
				self.fire = True

	def update(self):
		if self.fire == True:
			self.changeImage("goomba2.png")
			self.speed = 0
			self.burn += 1

		if self.burn > 50:
			self.rem = True

		if self.collide == True:
			self.speed = -1* self.speed
			self.collide = False
		self.x += self.speed

class Fireball(Sprite):
	def __init__(self, xPos, yPos):
		super(Fireball, self).__init__(xPos, yPos, 47, 47, "fireball.png")
		self.xSpeed = 8
		self.vertVelocity = 1.2
		self.collide = False
		self.rem = False

	def update(self):
		if self.y >= 500 - self.h:
			self.vertVelocity += -30.0
		else:
			self.vertVelocity += 5.0

		self.x += self.xSpeed
		self.y += self.vertVelocity

	def collisionExit(self, sprite):
		if self.x + self.w > sprite.x:
			self.collide = True
			if isinstance(sprite, Goomba):
				self.rem = True
		if self.x < sprite.x + sprite.w:
			self.collide = True
			if isinstance(sprite, Goomba):
				self.rem = True

class Tube(Sprite):
	def __init__(self, xPos, yPos):
		super(Tube, self).__init__(xPos, yPos, 55, 400, "tube.png")
	def update(self):
		pass

class Model():
	def __init__(self):
		self.dest_x = 0
		self.dest_y = 0
		self.mario = Mario(200,405)
		#self.lettuce = Lettuce (500, 400)
		self.sprites = []
		self.sprites.append(self.mario)
		self.sprites.append(Tube(400, 450))
		self.sprites.append(Tube(650, 350))
		self.sprites.append(Goomba(470, 382))

	def collision(self, sprite):
		for i in self.sprites:
			if isinstance(i, Tube):
				if sprite.x + sprite.w <= i.x:
					continue
				elif sprite.x >= i.x + i.w:
					continue
				elif sprite.y + sprite.h <= i.y:
					continue
				elif sprite.y >= i.y + i.h:
					continue
				else:
					sprite.collisionExit(i)
			if sprite.y +sprite.h <= 500:
				continue
			else:
				sprite.y = 500 -sprite.h

		if isinstance(sprite, Goomba):
			for i in self.sprites:
				if isinstance(i, Fireball):
					if sprite.x + sprite.w <= i.x:
						continue
					elif sprite.x >= i.x + i.w:
						continue
					elif sprite.y + sprite.h <= i.y:
						continue
					elif sprite.y >= i.y + i.h:
						continue
					else:
						sprite.collisionExit(i)

		if isinstance(sprite, Fireball):
			for i in self.sprites:
				if isinstance(i, Goomba):
					if sprite.x + sprite.w <= i.x:
						continue
					elif sprite.x >= i.x + i.w:
						continue
					elif sprite.y + sprite.h <= i.y:
						continue
					elif sprite.y >= i.y + i.h:
						continue
					else:
						sprite.collisionExit(i)

	def update(self):
		if self.mario.attack == True:
			self.sprites.append(Fireball(self.mario.x - (self.mario.w/2), self.mario.y + (self.mario.h /3)))
		for sprite in self.sprites:
			sprite.update()

#goomba/fireball removal
			if isinstance(sprite, (Goomba, Fireball)):
				if isinstance(sprite, Fireball):
					if sprite.x - (self.mario.x - self.mario.spawnX) >= 800:
						self.sprites.remove(sprite)
						self.update()
						break
				if sprite.rem == True:
					self.sprites.remove(sprite)
					self.update()
					break

#collision check
			if isinstance(sprite,( Mario, Goomba, Fireball)):
				self.collision(sprite)



class View():
	def __init__(self, model):
		screen_size = (800,600)
		self.screen = pygame.display.set_mode(screen_size, 32)
		self.model = model
		self.ground = pygame.image.load("ground.png")

	def update(self):    
		self.screen.fill([128,255,255])

		for i in range(0, 800, 16):
			self.screen.blit(self.ground, (i, 500))
			for j in range(516, 600, 16):
				self.screen.blit(self.ground, (i, j))

		#self.screen.blit(self.model.turtle.image, (self.model.turtle.x, self.model.turtle.y))
		#self.screen.blit(self.model.lettuce.image, (self.model.lettuce.x, self.model.lettuce.y))

		for sprite in self.model.sprites:
			self.screen.blit(sprite.image, (sprite.x - (self.model.mario.x - self.model.mario.spawnX), sprite.y))

		pygame.display.flip()

class Controller():
	def __init__(self, model):
		self.model = model
		self.keep_going = True

	def update(self):
		self.model.mario.storePrevPos()
		for event in pygame.event.get():
			if event.type == QUIT:
				self.keep_going = False
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.keep_going = False
				if event.key == K_LCTRL:
					self.model.sprites.append(Fireball(self.model.mario.x - (self.model.mario.w/2), self.model.mario.y + (self.model.mario.h /3)))

		keys = pygame.key.get_pressed()
		if keys[K_LEFT]:
			self.model.mario.x -= 10
			self.model.mario.movement = True
		elif keys[K_RIGHT]:
			self.model.mario.x += 10
			self.model.mario.movement = True
		else:
			self.model.mario.movement = False

		if keys[K_SPACE]:
			self.model.mario.jump = True
		elif keys[K_UP]:
			self.model.mario.jump = True
		else:
			self.model.mario.jump = False

print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
	c.update()
	m.update()
	v.update()
	sleep(0.04)
print("Goodbye")