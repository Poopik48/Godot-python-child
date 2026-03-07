from godot import exposed, export
from godot import *

@exposed
class Player(KinematicBody):

	speed = export(float, default=10.0)       # скорость движения
	jump_force = export(float, default=20.0)  # сила прыжка
	gravity = export(float, default=40.0)     # гравитация
	coyote_time = export(float, default=0.1)  # время после схода с платформы, когда можно прыгнуть
	jump_buffer_time = export(float, default=0.1)  # буфер прыжка
	
	velocity = Vector3()       # текущая скорость персонажа
	on_ground_timer = 0.0
	jump_buffer_timer = 0.0
	can_double_jump = True
	
	def _ready(self):
		self.mesh = self.get_node("MeshInstance")  # ссылка на меш в кинематик бади
	
	def _physics_process(self, delta):
		# управление
		direction = Vector3()
		if Input.is_action_pressed("ui_right"):
			direction.x += 1
		if Input.is_action_pressed("ui_left"):
			direction.x -= 1
		if Input.is_action_pressed("ui_up"):
			direction.z -= 1
		if Input.is_action_pressed("ui_down"):
			direction.z += 1
		
		# движение
		if direction.length() > 0:
			direction = direction.normalized() * self.speed
		else:
			direction = Vector3()
		# обьявление позиции
		self.velocity.x = direction.x
		self.velocity.z = direction.z

		# гравитация
		if not self.is_on_floor():
			self.velocity.y -= self.gravity * delta
			self.on_ground_timer -= delta
		else:
			self.on_ground_timer = self.coyote_time
			self.can_double_jump = True

		# буфер прыжка
		if Input.is_action_just_pressed("ui_accept"):
			self.jump_buffer_timer = self.jump_buffer_time
		else:
			self.jump_buffer_timer -= delta
		
		# условия приыжка и дабл джамп
		if self.jump_buffer_timer > 0:
			if self.on_ground_timer > 0:
				self.velocity.y = self.jump_force
				self.jump_buffer_timer = 0
			elif self.can_double_jump:
				self.velocity.y = self.jump_force
				self.can_double_jump = False
				self.jump_buffer_timer = 0

		# прыжок покруче (под вопросом)
		if Input.is_action_pressed("ui_accept") and Input.is_action_pressed("ui_select"):  # ui_select = Ctrl
			if self.is_on_floor():
				self.velocity.y = self.jump_force * 10

		# движение с проверкой столкновений
		self.velocity = self.move_and_slide(self.velocity, Vector3.UP)
