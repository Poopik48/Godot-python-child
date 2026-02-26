from godot import exposed
from godot import *

@exposed
class Enemy(KinematicBody2D):

	speed = 100
	direction = 1 
	velocity = Vector2()

	def _ready(self):
		self.sprite = self.get_node("AnimatedSprite") 
		self.player = self.get_tree().get_root().get_node("res://scenes/Player.tscn")
	
	def _physics_process(self, delta):
		self.velocity.x = self.speed * self.direction
		self.velocity.y += 900 * delta  
		
		self.velocity = self.move_and_slide(self.velocity, Vector2.UP)
		
		if self.is_on_wall():
			self.direction *= -1
			self.sprite.flip_h = self.direction < 0
		
		
		if self.player:
			if self.get_collision_with_player():
				self.player.reload_scene()
	
	
	def get_collision_with_player(self):
		#AABB
		return self.get_node("CollisionShape2D").get_global_rect().intersects(
			self.player.get_node("CollisionShape2D").get_global_rect()
		)
