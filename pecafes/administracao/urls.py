from django.urls import path

from .views import (
	dashboardGestao, homologarCadastro, cadastroExterno, 
	listaHomologar,homologarCadastroExterno
)

app_name = 'administracao'


urlpatterns = [

	path("dashboard/gestao/", dashboardGestao, 	name="dashboard-gestao"),

	path("dashboard/gestao/homologar/<str:tipo_lista>/", listaHomologar, 	name="lista-homologar"),
	path("dashboard/gestao/homologar/<str:tipo_grupo>/<int:grupo_id>/", homologarCadastroExterno, 	name="homologar-cadatro-externo"),
	path("dashboard/gestao/homologar/finalizar/<int:tipo_grupo>/<int:grupo_id>/", homologarCadastro, 	name="finalizar-homologar-cadastro"),

	path("dashboard/assistente-tecnico/", cadastroExterno, 	name="dashboard-assistente-tecnico"),
]