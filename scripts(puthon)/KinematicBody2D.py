from godot import exposed
from godot import *

@exposed
class Player(KinematicBody2D):

	speed = 200
	jump_force = -350
	gravity = 900
	
	velocity = Vector2()
	
	def _ready(self):
		#instantiete
		self.sprite = self.get_node("AnimatedSprite")
	
	def _physics_process(self, delta):
		direction = 0
		#направление и инпут 
		if Input.is_action_pressed("ui_right"):
			direction += 1
		if Input.is_action_pressed("ui_left"):
			direction -= 1
	
		#run
		self.velocity.x = direction * self.speed
	
		#verticale gravity
		self.velocity.y += self.gravity * delta
	
		#jump
		if self.is_on_floor():
			if Input.is_action_just_pressed("ui_accept"):
				self.velocity.y = self.jump_force
				
	
		#move and slide from gd
		self.velocity = self.move_and_slide(self.velocity, Vector2.UP)
	
		#flip H
		if direction != 0:
			self.sprite.flip_h = direction < 0
	
		#anim_player
		if not self.is_on_floor():
			self.sprite.play("jump")
		elif direction != 0:
			self.sprite.play("run")
		else:
			self.sprite.play("idle")
