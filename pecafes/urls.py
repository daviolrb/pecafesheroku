from django.contrib import admin
from django.urls import path, include
from pecafes.core import urls as core_urls
from pecafes.conta import urls as conta_urls
from pecafes.administracao import urls as administracao_urls

urlpatterns = [
    path("pecafes/", include(core_urls, namespace="home")),
    path("pecafes/conta/", include(conta_urls, namespace="conta")),
    path("pecafes/administracao/", include(administracao_urls, namespace="administracao")),
    path('pecafes/admin/', admin.site.urls),
]
