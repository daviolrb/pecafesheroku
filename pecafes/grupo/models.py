from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Uf(models.Model):
	sigla = models.CharField(max_length=2, null=False,blank=False,unique=True)
	nome = models.CharField(max_length=255, null=False,blank=False)

	def __str__(self):
		return ("({}) - {}".format(self.sigla, self.nome))


class CidadeManager(models.Manager):
	def getCidadeByUf(self, uf_pk):
		return self.get_queryset().filter(uf__pk=uf_pk)


class Cidade(models.Model):
	uf = models.ForeignKey(Uf, on_delete=models.CASCADE)
	municipio = models.CharField(max_length=255, null=False,blank=False)
	
	objects = CidadeManager()

	def __str__(self):
		return ("({}) - {}".format(self.uf.sigla, self.municipio))


class Entidade(models.Model):
	
	usuario = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
	nome = models.CharField(max_length=255, null=False,blank=False,unique=False)
	
	municipio = models.ForeignKey(Cidade,on_delete=models.PROTECT)
	cep = models.CharField(max_length=8, null=False,blank=False,unique=False)
	bairro = models.CharField(max_length=255, null=False,blank=True,unique=False)
	rua    = models.CharField(max_length=255, null=False,blank=True,unique=False)
	numero = models.CharField(max_length=255, null=False,blank=True,unique=False)
	
	telefone_fixo    = models.CharField(max_length=255, null=False,blank=True,unique=False)
	telefone_celular = models.CharField(max_length=255, null=False,blank=False,unique=False)

	data_adicionado = models.DateTimeField(auto_now_add=True)
	data_atualizado = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.nome


class EntidadeFisica(models.Model):

	MASCULINO = 'M'
	FEMININO = 'F'
	DESCONHECIDO = 'N'

	SEXO_CHOICES = [
	('M', 'Masculino'),
	('F', 'Feminino'),
	('N', 'Desconhecido'),
    ]

	entidade = models.OneToOneField(Entidade, on_delete=models.CASCADE)
	sexo = models.CharField(max_length=1,choices=SEXO_CHOICES, null=False, blank=True, default=DESCONHECIDO)
	data_nascimento = models.DateField(null=True, blank=True)
	cpf = models.CharField(max_length=11, help_text="Sem pontos e traço, apenas números.",null=False,blank=False, unique=True)

	def __str__(self):
		return self.entidade.nome


class EntidadeJuridica(models.Model):
	entidade = models.OneToOneField(Entidade, on_delete=models.CASCADE)
	cnpj = models.CharField(max_length=14, null=False,blank=False, unique=True)

	def __str__(self):
		return self.entidade.nome


class Grupo(models.Model):

	INDIVIDUAL = 1
	INFORMAL = 2
	FORMAL = 3

	is_individual = models.BooleanField(default=False)
	is_informal = models.BooleanField(default=False)
	is_formal = models.BooleanField(default=False)

	cadastro_individual_iniciado = models.BooleanField(default=False)
	cadastro_individual_finalizado = models.BooleanField(default=False)
	entidade_individual = models.OneToOneField(Entidade, 
		on_delete=models.CASCADE, blank=True, null=True, related_name="entidade_individual")


	cadastro_formal_iniciado = models.BooleanField(default=False)
	cadastro_formal_finalizado = models.BooleanField(default=False)
	entidade_formal = models.OneToOneField(Entidade, 
		on_delete=models.CASCADE, blank=True, null=True,related_name="entidade_formal")


	cadastro_informal_iniciado = models.BooleanField(default=False)
	cadastro_informal_finalizado = models.BooleanField(default=False)
	entidade_informal = models.OneToOneField(Entidade, 
		on_delete=models.CASCADE, blank=True, null=True, related_name="entidade_informal")

	
	usuario = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
	
	
	data_adicionado = models.DateTimeField(auto_now_add=True)
	data_atualizado = models.DateTimeField(auto_now=True)
 

class GrupoIndividual(models.Model):

	grupo = models.OneToOneField(Grupo, on_delete=models.CASCADE)	
	dap_fisica = models.CharField(max_length=255, null=True,blank=False, unique=True)

	data_adicionado = models.DateTimeField(auto_now_add=True)
	data_atualizado = models.DateTimeField(auto_now=True)

	def __str__(self):
		if self.grupo.entidade_individual is None:
			return "Indisponivel"
		
		return self.grupo.entidade_individual.nome

	class Meta:
		verbose_name = 'Grupo Individual'
		verbose_name_plural = 'Grupos Individuais'


class GrupoInformal(models.Model):

	grupo = models.OneToOneField(Grupo, on_delete=models.CASCADE)
	entidade_articulada = models.CharField(max_length=255, null=True, blank=True)
	reconhecimento_economia_solidaria = models.BooleanField()
	ano_formacao = models.PositiveSmallIntegerField()
	reconhecimento_indigena = models.BooleanField()
	reconhecimento_quilombola = models.BooleanField()

	data_adicionado = models.DateTimeField(auto_now_add=True)
	data_atualizado = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.grupo.entidade_informal.nome

	class Meta:
		verbose_name = 'Grupo Informal'
		verbose_name_plural = 'Grupos Informais'


class GrupoFormal(models.Model):

	TIPOGRUPO_CHOICES = [
	('AS', 'Associação'),
	('CO', 'Cooperativa'),
	('N', 'Não Informado'),
    ]

	grupo = models.OneToOneField(Grupo, on_delete=models.CASCADE)
	dap_juridica = models.CharField(max_length=255, null=False,blank=False, unique=True)
	ano_fundacao = models.PositiveSmallIntegerField()
	tipo_formal = models.CharField(max_length=2,choices=TIPOGRUPO_CHOICES,default='N')
	
	reconhecimento_economia_solidaria = models.BooleanField()
	reconhecimento_indigena = models.BooleanField()
	reconhecimento_quilombola = models.BooleanField()
	
	representante_legal = models.OneToOneField(Entidade, on_delete=models.CASCADE)

	data_adicionado = models.DateTimeField(auto_now_add=True)
	data_atualizado = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.grupo.entidade_formal.nome

	class Meta:
		verbose_name = 'Grupo Formal'
		verbose_name_plural = 'Grupos Formais'


class Produto(models.Model):
	
	nome = models.CharField(max_length=255, null=False, blank=False)
	unidade = models.CharField(max_length=255,null=False, blank=False)

	validado = models.BooleanField(default=True)

	def __str__(self):
			return self.nome

class ProdutoSugerido(models.Model):

	usuario = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
	produto = models.ForeignKey(Produto, on_delete=models.CASCADE)

	data_adicionado = models.DateTimeField(auto_now_add=True)

class ProdutoGrupo(models.Model):

	produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
	participante = models.ForeignKey(Entidade,on_delete=models.CASCADE)
	grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
	tipo_grupo = models.PositiveSmallIntegerField()
	
	quantidade = models.PositiveIntegerField()

	sazonalidade_janeiro = models.BooleanField(help_text="Janeiro",default=False)
	sazonalidade_fevereiro = models.BooleanField(help_text="Fevereiro",default=False)
	sazonalidade_marco = models.BooleanField(help_text="Março",default=False)
	sazonalidade_abril = models.BooleanField(help_text="Abril",default=False)
	sazonalidade_maio = models.BooleanField(help_text="Maio",default=False)
	sazonalidade_junho = models.BooleanField(help_text="Junho",default=False)
	sazonalidade_julho = models.BooleanField(help_text="Julho",default=False)
	sazonalidade_agosto = models.BooleanField(help_text="Agosto",default=False)
	sazonalidade_setembro = models.BooleanField(help_text="Setembro",default=False)
	sazonalidade_outubro = models.BooleanField(help_text="Outubro",default=False)
	sazonalidade_novembro = models.BooleanField(help_text="Novembro",default=False)
	sazonalidade_dezembro = models.BooleanField(help_text="Dezembro",default=False)


	validado = models.BooleanField(default=False)

	data_adicionado = models.DateTimeField(auto_now_add=True)
	data_atualizado = models.DateTimeField(auto_now=True)

class ParticipanteGrupo(models.Model):
	
	grupo = models.ForeignKey(Grupo,on_delete=models.CASCADE,related_name="grupo")
	tipo_grupo = models.PositiveSmallIntegerField()

	participante = models.ForeignKey(Entidade,on_delete=models.CASCADE,related_name="participante_grupo")

	validado = models.BooleanField(default=False)

	data_adicionado = models.DateTimeField(auto_now_add=True)
	data_atualizado = models.DateTimeField(auto_now=True)