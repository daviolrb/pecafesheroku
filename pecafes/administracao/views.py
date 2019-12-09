from django.shortcuts import render, redirect
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required

from pecafes.grupo.models import (
	Grupo, GrupoIndividual, GrupoInformal, 
	GrupoFormal, ParticipanteGrupo, ProdutoGrupo
)

# Create your views here.

def dashboardGestao(request):
	return render(request, "administracao/gestao/dashboard.html")


def cadastroExterno(request):
	return render(request, "administracao/gestao/dashboard.html")


@login_required
@transaction.atomic
def homologarCadastro(request, tipo_grupo, grupo_id):
	
	grupo = Grupo.objects.get(pk=grupo_id)
	
	if tipo_grupo == Grupo.INDIVIDUAL:
		grupo.is_individual = True

	elif tipo_grupo == Grupo.FORMAL:
		grupo.is_formal = True

	elif tipo_grupo == Grupo.INFORMAL:
		grupo.is_informal = True

	else:
		return redirect("administracao:dashboard-gestao")

	produtosGrupo = ProdutoGrupo.objects.filter(grupo_id=grupo_id,tipo_grupo=tipo_grupo)
	
	for produto in produtosGrupo:
		produto.validado = True
		produto.save()

	grupo.save()

	return render(request, "administracao/gestao/homologar/cadastro-externo/homologado-finalizado.html")


def homologarCadastroExterno(request, tipo_grupo, grupo_id):
	print(tipo_grupo, grupo_id)
	grupo = Grupo.objects.get(pk=grupo_id)

	if tipo_grupo == 'individual':

		entidadeGrupo = grupo.entidade_individual
		template = "administracao/gestao/homologar/cadastro-externo/individual.html"

		produtosParticipantesGrupo = grupo.produtogrupo_set.filter(participante_id=grupo.entidade_individual_id)

		context = {
		"produtosParticipantesGrupo": produtosParticipantesGrupo, 
		"entidadeGrupo": entidadeGrupo,
		"grupo_id": grupo.pk,
		"tipo_grupo": Grupo.INDIVIDUAL
		} 

	elif tipo_grupo == 'informal':

		entidadeGrupo = grupo.entidade_informal
		template = "administracao/gestao/homologar/cadastro-externo/informal.html"

		participantes = ParticipanteGrupo.objects.filter(grupo_id=grupo_id,tipo_grupo=Grupo.INFORMAL)

		context = {
		"entidadeGrupo": entidadeGrupo, 
		"participantes": participantes,
		"grupo_id": grupo.pk,
		"tipo_grupo": grupo.INFORMAL
		} 

	elif tipo_grupo == 'formal':

		entidadeGrupo = grupo.entidade_formal
		template = "administracao/gestao/homologar/cadastro-externo/formal.html"

		participantes = ParticipanteGrupo.objects.filter(grupo_id=grupo_id,tipo_grupo=Grupo.FORMAL)

		context = {
		"entidadeGrupo": entidadeGrupo, 
		"participantes": participantes,
		"grupo_id": grupo_id,
		"tipo_grupo": Grupo.FORMAL
		}
	else:
		return None

	return render(request, template, context)

 

def listaHomologar(request, tipo_lista):

	if tipo_lista == 'lista-individual':
		
		cadastros = Grupo.objects.filter(cadastro_individual_finalizado=True, is_individual=False)
		template = "administracao/gestao/homologar/cadastro-externo/lista-individual.html"
		context = {"cadastros": cadastros,}
		
	elif tipo_lista == 'lista-informal':
	
		cadastros = Grupo.objects.filter(cadastro_informal_finalizado=True, is_informal=False)
		template = "administracao/gestao/homologar/cadastro-externo/lista-informal.html"
		context = {"cadastros": cadastros,}

	elif tipo_lista == 'lista-formal':

		cadastros = Grupo.objects.filter(cadastro_formal_finalizado=True, is_formal=False)
		template = "administracao/gestao/homologar/cadastro-externo/lista-formal.html"
		context = {"cadastros": cadastros,}
	else:
		return None

	return render(request, template, context)
