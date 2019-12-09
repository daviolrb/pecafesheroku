from django.contrib import admin
from pecafes.grupo.models import (
	Uf, Cidade, Entidade, EntidadeFisica, 
	EntidadeJuridica, Grupo, GrupoIndividual, 
	GrupoInformal, GrupoFormal, Produto, Grupo, 
	ProdutoGrupo, ParticipanteGrupo
)

# Register your models here. 
admin.site.register(Uf)
admin.site.register(Cidade)
admin.site.register(Entidade)
admin.site.register(EntidadeJuridica)
admin.site.register(EntidadeFisica)
admin.site.register(Grupo)
admin.site.register(GrupoIndividual)
admin.site.register(GrupoInformal)
admin.site.register(GrupoFormal)
admin.site.register(Produto)
admin.site.register(ProdutoGrupo)
admin.site.register(ParticipanteGrupo)