from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):

	EXTERNO = 1
	GESTOR = 2
	ASSISTENCIA_TECNICA = 3
	ADMINISTRADOR = 4
	GESTOR_PUBLICO = 5

	TIPO_USUARIO = [
	(1, 'EXTERNO'),
	(2, 'GESTOR'),
	(3, 'ASSISTENCIA_TECNICA'),
	(4, 'ADMINISTRADOR'),
	(5, 'GESTOR_PUBLICO'),
	]

	tipo_usuario = models.PositiveSmallIntegerField(choices=TIPO_USUARIO,default=ADMINISTRADOR)

