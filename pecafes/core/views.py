from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.core import serializers
from django.http import HttpResponse
 

from pecafes.grupo.models import (
	Produto, ProdutoGrupo, Grupo,
	ParticipanteGrupo, Cidade
)

from pecafes.conta.forms import (
	EntidadeFisicaForm, GrupoIndividualForm, 
	EntidadeForm, GrupoInformalForm, EntidadeJuridicaForm,
	GrupoFormalForm,
)
 
from .forms import ProdutoGrupoForm

# Create your views here.
def home(request):
	return render(request, "base.html")

def listaCidadeByUf(request, id_uf):
	cidadesByUf = Cidade.objects.getCidadeByUf(id_uf)
	json_cidades = serializers.serialize('json', cidadesByUf)
	return HttpResponse(json_cidades, content_type="application/json")


def selecionaPerfilFormal(request):
	return render(request, "core/dashboard/cadastro-grupo/seleciona-formal.html")

def addParticipanteToGrupo(request, tipo_grupo):

	try:

		if tipo_grupo == Grupo.FORMAL:
			usuario = get_user_model().objects.get(pk=request.user.pk)
			grupoFormal = usuario.grupo.grupoformal

		elif tipo_grupo == Grupo.INFORMAL:
			usuario = get_user_model().objects.get(pk=request.user.pk)
			grupoInformal = usuario.grupo.grupoinformal

		else:
			raise AttributeError

	except AttributeError:
		return redirect("core:dashboard")

	if request.method == "POST":

		entidadeForm = EntidadeForm(request.POST)
		entidadeFisicaForm = EntidadeFisicaForm(request.POST)
		grupoIndividualForm = GrupoIndividualForm(request.POST)

		if entidadeForm.is_valid() and entidadeFisicaForm.is_valid():

			entidade = entidadeForm.save(commit=False)
			entidade.save()

			entidadeFisica = entidadeFisicaForm.save(commit=False)
			entidadeFisica.entidade_id = entidade.pk
			entidadeFisica.save()

			# A situação onde "grupoIndividualForm" não é 
			# valido ocorre quando o participante
			# pertence a economia solidaria(SEM DAP)
			if grupoIndividualForm.is_valid():

				grupo = Grupo()
				grupo.entidade_individual_id = entidade.pk
				grupo.save()

				grupoIndividual = grupoIndividualForm.save(commit=False)
				grupoIndividual.grupo_id = grupo.pk
				grupoIndividual.save()

			participanteGrupo = ParticipanteGrupo()
			participanteGrupo.grupo_id = request.user.grupo.pk

			if tipo_grupo == Grupo.FORMAL:
				participanteGrupo.tipo_grupo = Grupo.FORMAL

			elif tipo_grupo == Grupo.INFORMAL:
				participanteGrupo.tipo_grupo = Grupo.INFORMAL

			
			participanteGrupo.participante_id = entidade.pk
			participanteGrupo.save()

			if tipo_grupo == Grupo.FORMAL:
				addProduto = adicionarProduto(request, Grupo.INFORMAL, entidade.pk, 'cadastro-grupo-formal-add-participante')

			elif tipo_grupo == Grupo.INFORMAL:
				addProduto = adicionarProduto(request, Grupo.FORMAL, entidade.pk, 'novo-participante-informal')
				

			
			return addProduto

		else:
			context = {
			"entidadeForm": entidadeForm,
			"entidadeFisicaForm": entidadeFisicaForm,
			"grupoIndividualForm": GrupoIndividualForm(),
			"produtos": Produto.objects.all(),
			}	


	else:
		context = {
		"entidadeForm": EntidadeForm(),
		"entidadeFisicaForm": EntidadeFisicaForm(),
		"grupoIndividualForm": GrupoIndividualForm(),
		"produtos": Produto.objects.all()
		}

	if tipo_grupo == Grupo.FORMAL:
		return render(request, "core/dashboard/cadastro-grupo/formal-add-participante.html", context)
	elif tipo_grupo == Grupo.INFORMAL:
		return render(request, "core/dashboard/cadastro-grupo/informal-add-participante.html", context)


@login_required
@transaction.atomic
def cadastroGrupoFormal(request):

	EntidadeFormSet = formset_factory(EntidadeForm,extra=2)

	if request.method == "POST":
		#submitForm
		selecionaFormal = request.POST.get("seleciona-formal")

		if selecionaFormal is None: 
			
			isRepresentante = request.POST.get("is_representante")
 
			try: 
				grupo = request.user.grupo 
			except AttributeError: 
				grupo = Grupo()
				grupo.usuario_id = request.user.pk
 
			if grupo.cadastro_formal_finalizado:
				return render(request, "core/dashboard/base-dashboard.html", 
						{"message": "Cadastro no grupo de associações e cooperativa já foi concluido.",
						"is_error": False})

			if grupo.cadastro_formal_iniciado:
				return redirect("core:cadastro-grupo-formal-add-participante", tipo_grupo=Grupo.FORMAL)

			entidadeJuridicaForm = EntidadeJuridicaForm(request.POST)
			grupoFormalForm = GrupoFormalForm(request.POST)

			if isRepresentante == "yes":
				#Cadastro é representante
				entidadeForm = EntidadeForm(request.POST)

				if entidadeJuridicaForm.is_valid() and  grupoFormalForm.is_valid() and entidadeForm.is_valid():
					
					entidadeGrupo = entidadeForm.save()
					entidadeJuridica = entidadeJuridicaForm.save(commit=False)
					entidadeJuridica.entidade_id = entidadeGrupo.pk
					entidadeJuridica.save()

					grupo.entidade_formal_id = entidadeGrupo.pk
					grupo.cadastro_formal_iniciado = True
					grupo.save()

					grupoFormal = grupoFormalForm.save(commit=False)
					grupoFormal.grupo_id = grupo.pk
					grupoFormal.representante_legal_id = request.user.entidade.pk
					grupoFormal.save()

					return redirect("core:cadastro-grupo-formal-add-participante", tipo_grupo=Grupo.FORMAL)
					
				else:
					context = {
					"entidadeJuridicaForm": entidadeJuridicaForm,
					"grupoFormalForm": grupoFormalForm,
					"entidadeForm": entidadeForm,
					"is_representante": "yes",
					}

					return render(request, "core/dashboard/cadastro-grupo/formal.html", context)


			else: 
		
				entidadeFormSet = EntidadeFormSet(request.POST)
				entidadeFisicaForm = EntidadeFisicaForm(request.POST)

				if entidadeJuridicaForm.is_valid() and grupoFormalForm.is_valid() and entidadeFormSet.is_valid() and entidadeFisicaForm.is_valid():
					
					entidadeGrupoForm = entidadeFormSet[0]
					entidadeRepresentanteForm = entidadeFormSet[1]

					#Cadastrando o representante
					entidadeRepresentante = entidadeRepresentanteForm.save()
					entidadeFisica = entidadeFisicaForm.save(commit=False)
					entidadeFisica.entidade_id = entidadeRepresentante.pk
					entidadeFisica.save()


					#Cadastro Entidade Juridica de Grupo
					entidadeGrupo = entidadeGrupoForm.save()
					entidadeJuridica = entidadeJuridicaForm.save(commit=False)
					entidadeJuridica.entidade_id = entidadeGrupo.pk
					entidadeJuridica.save()

					#Cadastro de Grupo e sua parte Formal
					grupo.cadastro_formal_iniciado = True
					grupo.entidade_formal_id = entidadeGrupo.pk
					grupo.save()

					grupoFormal = grupoFormalForm.save(commit=False)
					grupoFormal.representante_legal_id = entidadeRepresentante.pk
					grupoFormal.grupo_id = grupo.pk
					grupoFormal.save()
					
					return redirect("core:cadastro-grupo-formal-add-participante", tipo_grupo=Grupo.FORMAL)

				else:
					context = {
					"entidadeJuridicaForm": entidadeJuridicaForm,
					"grupoFormalForm": grupoFormalForm,
					"entidadeFormSet": entidadeFormSet,
					"entidadeFisicaForm": entidadeFisicaForm,
					"is_representante": "no",
					}
					return render(request, "core/dashboard/cadastro-grupo/formal.html", context)



		else:
			#Cria formulario de cadastro
			context = {
			"entidadeJuridicaForm": EntidadeJuridicaForm(),
			"grupoFormalForm": GrupoFormalForm(),
			}

			if selecionaFormal == "no":
				#Usuário não é representante
				context = {
				"entidadeJuridicaForm": EntidadeJuridicaForm(),
				"grupoFormalForm": GrupoFormalForm(),
				"entidadeFormSet": EntidadeFormSet(),
				"entidadeFisicaForm": EntidadeFisicaForm(),
				"is_representante": "no",
				}
				return render(request, "core/dashboard/cadastro-grupo/formal.html", context)

			else:
				#Usuario e o representante
				context = {
				"entidadeJuridicaForm": EntidadeJuridicaForm(),
				"grupoFormalForm": GrupoFormalForm(),
				"entidadeForm": EntidadeForm(),
				"is_representante": "yes",
				}
				return render(request, "core/dashboard/cadastro-grupo/formal.html", context)

			return render(request, "core/dashboard/base-dashboard.html", 
				{"success_message": "Cadastro como grupo informal concluido, aguada a equipe PECAFES homologar seu cadastro."})

	else:
		return render(request, "core/dashboard/cadastro-grupo/seleciona-formal.html")

	return render(request, "core/dashboard/cadastro-grupo/seleciona-formal.html")


def finalizaCadastroFormal(request):

	try:

		grupo = request.user.grupo

		if grupo.cadastro_formal_iniciado and not grupo.cadastro_formal_finalizado:
			grupo.cadastro_formal_finalizado = True
			grupo.save() 
			return render(request, "core/dashboard/cadastro-grupo/cadastro-concluido.html", 
				{"cadastro_formal": True} )

	except AttributeError:
		return redirect("core:dashboard")

	return redirect("core:dashboard")

def finalizaCadastroInformal(request):

	try:

		grupo = request.user.grupo

		if grupo.cadastro_informal_iniciado and not grupo.cadastro_informal_finalizado:
			grupo.cadastro_informal_finalizado = True
			grupo.save() 
			return render(request, "core/dashboard/cadastro-grupo/cadastro-concluido.html", 
				{"cadastro_informal": True} )

	except AttributeError:
		return redirect("core:dashboard")

	return redirect("core:dashboard")


@login_required
@transaction.atomic
def cadastroGrupoIndividual(request):

	if request.method == "POST":
			
		grupoIndividualForm = GrupoIndividualForm(request.POST)

		if grupoIndividualForm.is_valid(): 

			try:

				grupo = request.user.grupo

			except AttributeError:
				grupo = Grupo()
				grupo.usuario_id = request.user.pk

			#Questão a ser tratada
			if hasattr(grupo, 'grupoindividual'):
				return redirect("core:seleciona-produto")		

			grupo.cadastro_individual_iniciado = True
			grupo.entidade_individual_id = request.user.entidade.pk
			grupo.save()

			grupoIndividual = grupoIndividualForm.save(commit=False)
			grupoIndividual.grupo_id = grupo.pk
			grupoIndividual.save()

			addProduto = adicionarProduto(request, Grupo.INDIVIDUAL, request.user.entidade.pk, 'finaliza-cadastro-individual')
			
			return addProduto

		else:
			context = {
			"grupoIndividualForm": grupoIndividualForm,
			"produtos": Produto.objects.all(),
			}			

	else:
		context = {
		"grupoIndividualForm": GrupoIndividualForm(),
		"produtos": Produto.objects.all(),
		}

	return render(request, "core/dashboard/cadastro-grupo/individual.html", context)


def finalizaCadastroIndividual(request):

	try:

		grupo = request.user.grupo

		if grupo.cadastro_individual_iniciado and not grupo.cadastro_individual_finalizado:
			grupo.cadastro_individual_finalizado = True
			grupo.save() 
			return render(request, "core/dashboard/cadastro-grupo/cadastro-concluido.html", 
				{"cadastro_individual": True} )

	except AttributeError:
		return redirect("core:dashboard")

	return redirect("core:dashboard")


@login_required
@transaction.atomic
def cadastroGrupoInformal(request): 

	if request.method == "POST":
			
		grupoInformalForm = GrupoInformalForm(request.POST)
		entidadeForm = EntidadeForm(request.POST)

		if grupoInformalForm.is_valid() and entidadeForm.is_valid(): 

			try:

				grupo = request.user.grupo 

			except AttributeError: 
				grupo = Grupo()
				grupo.usuario_id = request.user.pk 
 
			if hasattr(grupo, 'grupoinformal'):
				if grupo.cadastro_informal_finalizado:
					return redirect("core:dashboard")
				else:
					return redirect("core:cadastro-grupo-informal-add-participante", 
						tipo_grupo=Grupo.INFORMAL)
 
			entidade = entidadeForm.save()

			grupo.entidade_informal_id = entidade.pk
			grupo.cadastro_informal_iniciado = True 
			
			grupo.save()
 
			try:
				
				grupoInformal = grupoInformalForm.save(commit=False)
				grupoInformal.grupo_id = grupo.pk
				grupoInformal.save()				
			
			except IntegrityError:
				return redirect("core:dashboard")


			return redirect("core:cadastro-grupo-informal-add-participante", tipo_grupo=Grupo.INFORMAL)

		else:
			context = {
			"grupoInformalForm": grupoInformalForm,
			"entidadeForm": entidadeForm,
			}			

	else:
		context = {
		"grupoInformalForm": GrupoInformalForm(),
		"entidadeForm": EntidadeForm(),
		}

	return render(request, "core/dashboard/cadastro-grupo/informal.html", context)


@login_required
def dashboard(request):
	return render(request, "core/dashboard/base-dashboard.html")


@login_required
def selecionaProduto(request):
	produtos = Produto.objects.all()
	return render(request, "core/dashboard/produto/seleciona.html", {'produtos': produtos})


@login_required
def adicionarProduto(request, tipo_grupo, entidade_participante_id, redirect_to):
	
	if request.method == "POST":

		idProdutos = request.POST.getlist("produtos")

		if idProdutos is None:
			return redirect("core:dashboard")

		if len(idProdutos) < 1:
			return redirect("core:seleciona-produto")

		ProdutoGrupoFormSet = formset_factory(ProdutoGrupoForm,extra=len(idProdutos))
		produtoGrupoFormSet = ProdutoGrupoFormSet()

		listaProdutos  = []

		count = 0
		for idProduto in idProdutos:

			produto = Produto.objects.get(pk=int(idProduto))

			listaProdutos.append(produto)
			produtoGrupoForm = produtoGrupoFormSet[count]
			produtoGrupoForm["codigo"].initial = produto.pk
			produtoGrupoForm["nome"].initial = produto.nome
			produtoGrupoForm["unidade"].initial = produto.unidade
			count += 1

		template = "core/dashboard/produto/adiciona.html"

		return render(request, template, 
			{"produtoGrupoFormSet": produtoGrupoFormSet, 
			"entidade_participante": entidade_participante_id,
			"tipo_grupo": tipo_grupo,
			"redirect_to": redirect_to})
	else:
		return redirect("core:seleciona-produto")


@login_required
@transaction.atomic
def processarAdicionarProduto(request):

	if request.method == "POST":
		
		redirect_to = request.POST.get("redirect_to")

		totalItens = int(request.POST.get("form-TOTAL_FORMS"))
		if totalItens is None:
			return redirect("core:seleciona-produto")

		tipo_grupo = int(request.POST.get("tipo_grupo"))

		if tipo_grupo is None:
			return redirect("core:dashboard")

		if tipo_grupo != Grupo.INFORMAL and tipo_grupo != Grupo.FORMAL and tipo_grupo != Grupo.INDIVIDUAL:
			return redirect("core:dashboard")

		participante = int(request.POST.get("participante"))

		#Adicionar validação de segurança para
		#impedir o cadastro de pordutos
		#de outros grupos
		if participante is None:
			return redirect("core:dashboard")
		 
		ProdutoGrupoFormSet = formset_factory(ProdutoGrupoForm,extra=totalItens)
		produtoGrupoFormSet = ProdutoGrupoFormSet(request.POST)

		if produtoGrupoFormSet.is_valid():
			
			for produtoGrupoForm in produtoGrupoFormSet:

				produtoGrupo = produtoGrupoForm.save(commit=False)

				idProduto = produtoGrupoForm.cleaned_data["codigo"]
				idGrupo = request.user.grupo.pk

				#impedir duplicados
				hasDuplicado = ProdutoGrupo.objects.filter(produto_id=idProduto,
					participante_id=participante,
					tipo_grupo=tipo_grupo).count()

				if hasDuplicado > 0:
					print("Já possui!\n")
					continue

				produtoGrupo.grupo_id = idGrupo
				produtoGrupo.produto_id = idProduto
				produtoGrupo.participante_id = participante
				produtoGrupo.tipo_grupo = tipo_grupo
				produtoGrupo.save()


			if redirect_to == 'novo-participante-informal':
				
				return redirect("core:cadastro-grupo-informal-add-participante",
					tipo_grupo=Grupo.INFORMAL)
				
				response = addParticipanteToGrupo(request, tipo_grupo)
				return response
			
			elif redirect_to == 'finaliza-cadastro-individual':
				return redirect("core:finaliza-cadastro-individual")

			elif redirect_to == 'cadastro-grupo-formal-add-participante':
				return redirect("core:cadastro-grupo-formal-add-participante", 
					tipo_grupo=Grupo.FORMAL)

			
			else:
				return redirect("core:meus-produtos")
			 
		else:
			return render(request, 
				"core/dashboard/produto/adiciona.html", 
				{'produtoGrupoFormSet': produtoGrupoFormSet,
				"tipo_grupo": tipo_grupo,
				"participante": participante,})

	return redirect("core:seleciona-produto")


@login_required
def listaProduto(request):
	produtos = ProdutoGrupo.objects.filter(grupo_id=request.user.grupo.pk)
	return render(request, "core/dashboard/produto/minha-lista.html", {'produtos': produtos})


@login_required
@transaction.atomic
def cadastroParticipante(request):

	if request.method == "POST":
		
		entidadeForm = EntidadeForm(request.POST)
		entidadeFisicaForm = EntidadeFisicaForm(request.POST)

		#Só valida se tem dap
		grupoIndividualForm = GrupoIndividualForm(request.POST)

		if entidadeForm.is_valid() and entidadeFisicaForm.is_valid():

			entidade = entidadeForm.save(commit=False)
			entidade.save()

			entidadeFisica = entidadeFisicaForm.save(commit=False)
			entidadeFisica.entidade_id = entidade.pk
			entidadeFisica.save()

			if grupoIndividualForm.is_valid():

				grupo = Grupo()
				grupo.entidade_id = entidade.pk
				grupo.save()

				grupoIndividual = grupoIndividualForm.save(commit=False)
				grupoIndividual.grupo_id = grupo.pk
				grupoIndividual.save()

			#
			participanteGrupo = ParticipanteGrupo()
			participanteGrupo.grupo_id = request.user.entidade.grupo.pk
			participanteGrupo.participante_id = entidade.pk
			participanteGrupo.save()

			participantes = ParticipanteGrupo.objects.filter(grupo_id=request.user.entidade.grupo.pk)
			context = {
			"msg_participante_criado": "msg_participante_criado",
			"participantes":participantes,
			}

			return render(request, "core/dashboard/participante/minha-lista.html",context)
		else:
			context = {
			"entidadeForm": entidadeForm,
			"entidadeFisicaForm": entidadeFisicaForm,
			"grupoIndividualForm": GrupoIndividualForm(),
			}
	else:
		context = {
		"entidadeForm": EntidadeForm(),
		"entidadeFisicaForm": EntidadeFisicaForm(),
		"grupoIndividualForm": GrupoIndividualForm(),
		}

	return render(request, "core/dashboard/participante/cadastro.html", context)


@login_required
def listaParticipanteGrupo(request):
	participantes = ParticipanteGrupo.objects.filter(grupo_id=request.user.entidade.grupo.pk)
	return render(request, "core/dashboard/participante/minha-lista.html", {'participantes': participantes})

def errorOperation(request, context):
	return render(request, "core/error.html", context)