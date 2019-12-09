from django.db import transaction
from django.contrib.auth import get_user_model
from django.shortcuts import (
	render, redirect
)

from pecafes.grupo.models import (
	Uf, GrupoIndividual, EntidadeFisica, Grupo
)
from .forms import (
	UserForm, EntidadeForm, GrupoForm, EntidadeFisicaForm,
)

Usuario = get_user_model()


@transaction.atomic
def cadastro(request):
	
	if request.method == "POST": 
		
		userForm = UserForm(request.POST)
		entidadeForm = EntidadeForm(request.POST)
		entidadeFisicaForm = EntidadeFisicaForm(request.POST)

		if userForm.is_valid() and entidadeForm.is_valid() and entidadeFisicaForm.is_valid():

			entidadeFisica = entidadeFisicaForm.save(commit=False)
		
			usuario = userForm.save(commit=False)
			usuario.set_password(userForm.cleaned_data["password"])

			if request.POST.get("is_assistente_tecnico") is None:

				usuario.tipo_usuario = Usuario.EXTERNO
			else:
				usuario.tipo_usuario = Usuario.ASSISTENCIA_TECNICA	

			
			usuario.username = entidadeFisica.cpf
			usuario.save()

			entidade = entidadeForm.save(commit=False)
			entidade.usuario_id = usuario.pk		
			entidade.save()

			entidadeFisica.entidade_id = entidade.pk
			entidadeFisica.save()
 			
			return redirect("conta:cadastro-finalizado")

		else:
			contexto = {
			"userForm": userForm,
			"entidadeForm": entidadeForm,
			"entidadeFisicaForm": entidadeFisicaForm,
			}
	else:
		contexto = {
		"userForm": UserForm(),
		"entidadeForm": EntidadeForm(),
		"entidadeFisicaForm": EntidadeFisicaForm(),
		}
	
	return render(request, "conta/cadastro-externo/base.html", contexto)


def cadastroFinalizado(request):
	return render(request, "conta/cadastro-externo/cadastro-finalizado.html")


def ajudaCadastroGrupo(request):
	return render(request, "conta/cadastro-externo/ajuda.html")