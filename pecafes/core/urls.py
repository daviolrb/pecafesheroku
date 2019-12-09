from django.urls import path
from .views import (
	home, listaCidadeByUf, dashboard, 
	selecionaProduto, adicionarProduto, 
	processarAdicionarProduto, listaProduto,
	cadastroParticipante, listaParticipanteGrupo,
	cadastroGrupoIndividual, cadastroGrupoInformal,
	selecionaPerfilFormal, cadastroGrupoFormal,
	finalizaCadastroFormal,
	addParticipanteToGrupo,
	finalizaCadastroInformal,
	finalizaCadastroIndividual,
)

app_name = 'core'

urlpatterns = [
	path("", home, 	name="index"),
	path("home/", home, 	name="index"),
	path("home/dashboard/", dashboard, 	name="dashboard"),

	#cadastro de grupo formal
	path("home/dashboard/cadastro-formal/", cadastroGrupoFormal, 	name="cadastro-formal"),
	path("home/dashboard/seleciona-formal/", selecionaPerfilFormal, 	name="seleciona-formal"),
	path("home/dashboard/cadastro-formal-finalizado/", finalizaCadastroFormal, 	name="finaliza-cadastro-formal"),
	path("home/dashboard/cadastro-grupo-formal-add-participante/<int:tipo_grupo>", 
		addParticipanteToGrupo, 	name="cadastro-grupo-formal-add-participante"),

	#Cadastro Informal
	path("home/dashboard/cadastro-informal/", cadastroGrupoInformal, 	name="cadastro-informal"),
	path("home/dashboard/cadastro-grupo-informal-add-participante/<int:tipo_grupo>", 
		addParticipanteToGrupo, 	name="cadastro-grupo-informal-add-participante"),
	path("home/dashboard/cadastro-informal-finalizado/", finalizaCadastroInformal, 	name="finaliza-cadastro-informal"),

	#Individual
	path("home/dashboard/cadastro-individual/", cadastroGrupoIndividual, 	name="cadastro-individual"),
	path("home/dashboard/cadastro-individual-finalizado/", finalizaCadastroIndividual, 	name="finaliza-cadastro-individual"),
	


	#formal-adiciona-participante
	path("home/dashboard/meus-produtos/", listaProduto, 	name="meus-produtos"),
	path("home/dashboard/cadastro-participante/", cadastroParticipante, 	name="cadastro-participante"),
	path("home/dashboard/lista-participantes/", listaParticipanteGrupo, 	name="lista-grupo-participante"),
	path("home/dashboard/processar-produto/", processarAdicionarProduto, 	name="processar-adicionar-produto"),
	path("home/dashboard/seleciona-produto/", selecionaProduto, 	name="seleciona-produto"),
	path("home/dashboard/adicionar-produto/", adicionarProduto, 	name="adicionar-produto"),

	

	
	


	path("lista-cidade/<int:id_uf>", listaCidadeByUf, 	name="lista-cidade-by-uf"),
]