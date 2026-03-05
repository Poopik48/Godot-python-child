from godot import exposed, export
from godot import *
from godot import lerp

@exposed
class Player(KinematicBody):
	
	speed = export(int, default=200)  # скорость
	jump_force = export(int, default=400)  # сила прыжка
	gravity = export(int, default=900)  # гравитация
	friction = export(float, default=0.1)  # торможение
	max_fall_speed = export(int, default=1000)  # макс падение
	coyote_time = export(float, default=0.1)  # прыжок после схода с края
	jump_buffer_time = export(float, default=0.1)  # нажатие чуть раньше срабатывает
	
	velocity = Vector2() #velociti righy now
	on_ground_timer = 0.0 
	jump_buffer_timer = 0.0
	can_double_jump = True
	
	def _ready(self):
		
		self.mesh = self.get_node("../MeshInstance")  # спрайт для анимаций
	
	def _physics_process(self, delta):
		direction = 0	#начальный вектор
		if Input.is_action_pressed("ui_right"):
			direction += 1
		if Input.is_action_pressed("ui_left"):
			direction -= 1
		self.velocity.x = lerp(self.velocity.x, direction * self.speed, self.friction)#плавное движение(линейная интерполяция для скольжения)
		
		
		self.velocity.y += self.gravity * delta 	# что бы от частоты кадров не менялось ничего
		if self.velocity.y > self.max_fall_speed:	# не падаем слишком быстро
			self.velocity.y = self.max_fall_speed  # не падаем слишком быстро
		
		
		if self.is_on_floor():
			self.on_ground_timer = self.coyote_time 	# таймер койота
			self.can_double_jump = True 				# условие дабл джампа
		else:
			self.on_ground_timer -= delta
		
		
		if Input.is_action_just_pressed("ui_up"):	# JUMP
			self.jump_buffer_timer = self.jump_buffer_time
		else:
			self.jump_buffer_timer -= delta
		
		
		if self.jump_buffer_timer > 0:
			if self.on_ground_timer > 0:
				self.velocity.y = -self.jump_force  # прыгаем с пола
				self.jump_buffer_timer = 0
			elif self.can_double_jump:
				self.velocity.y = -self.jump_force  # двойной прыжок
				self.can_double_jump = False
				self.jump_buffer_timer = 0
		
		
		if Input.is_action_pressed("ui_up") and Input.is_action_pressed("ui_select"):  # Ctrl + пробел
			if self.is_on_floor():
				self.velocity.y = -self.jump_force * 10  # супер-прыжок
		
		self.velocity = self.move_and_slide(self.velocity, Vector2(0, -1))  # двигаемся
		
		if not self.is_on_floor():
			self.sprite.play("jump")
		elif direction != 0:
			self.sprite.play("run")
			self.sprite.flip_h = direction < 0
		else:
			self.sprite.play("idle")
