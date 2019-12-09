from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import (
	cadastro, cadastroFinalizado
)


app_name = 'conta'


urlpatterns = [ 

	path("cadastro/", cadastro, name="cadastro"),
	path("cadastro-finalizado/", cadastroFinalizado, name="cadastro-finalizado"),	
	path("sair/", LogoutView.as_view(), name="sair"), 
	path("entrar/", LoginView.as_view(template_name="conta/autenticacao/login.html"), name="entrar"),
]