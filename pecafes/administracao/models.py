from django.db import models
from pecafes.grupo.models import Grupo
from django.contrib.auth import get_user_model

class AssistenciaTecnica(models.Model):

	usuario = models.OneToOneField(get_user_model(), on_delete=models.PROTECT)
	grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)