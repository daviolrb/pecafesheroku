from django.contrib.auth import get_user_model
from django import forms
#from .models import CustomUser
from pecafes.grupo.models import (
	Uf, Cidade, Entidade, Uf, Grupo, 
	EntidadeFisica, EntidadeJuridica, 
	GrupoInformal, GrupoFormal, GrupoIndividual
)

from django.contrib.auth.forms import(
	UserCreationForm, UserChangeForm
)

#Customização de usuário:
class CustomUserCreationForm(UserCreationForm):

	class Meta:
		model = get_user_model()
		fields = ["username", "email", "tipo_usuario"]

		labels = {
		"username": "CPF"
		}

class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = get_user_model()

		fields = ["username", "email", "tipo_usuario"]


#Forms de cadastro(Externo)
class EntidadeFisicaForm(forms.ModelForm):

	class Meta:
		model = EntidadeFisica
		fields = ["cpf", "sexo"]
		
		widgets = {
		"cpf": forms.NumberInput(attrs={"class": "form-control", "aria-describedby": "cpfHelp"}),
		"sexo": forms.Select(attrs={"class": "form-control"},),
		}


class EntidadeJuridicaForm(forms.ModelForm):
	class Meta:
		model = EntidadeJuridica
		fields = ["cnpj"]

		widgets = {
		"cnpj": forms.NumberInput(attrs={"class": "form-control", "aria-describedby": "cnpjHelp", "placeholder": ""})
		}


class GrupoForm(forms.ModelForm):
	pass


class GrupoIndividualForm(forms.ModelForm):
	class Meta:
		model = GrupoIndividual
		fields = ["dap_fisica"]

		widgets = {
		"dap_fisica": forms.TextInput(attrs={"class": "form-control", "aria-describedby": "dapFisicaHelp", "placeholder": "Número da sua DAP"})
		}


class GrupoInformalForm(forms.ModelForm):

	AUX_EA_CHOICES = [('1', 'Sim'), ('0', 'Não')]
	has_entidade_articulada = forms.ChoiceField(widget=forms.RadioSelect(attrs={"class": "custom-control-input"}),choices=AUX_EA_CHOICES)

	class Meta:
		model = GrupoInformal
		fields = ["entidade_articulada", 
		"ano_formacao", 
		"reconhecimento_indigena", 
		"reconhecimento_quilombola",
		"reconhecimento_economia_solidaria",]

		REC_IQ_CHOICES = [('1', 'Sim'), ('0', 'Não')]

		widgets = {
		
		"entidade_articulada": forms.TextInput(
		attrs={"class": "form-control", "aria-describedby": "entidadeArticuladaHelp", "placeholder": ""}),
		
		"ano_formacao": forms.NumberInput(
		attrs={"class": "form-control","aria-describedby": "anoFormacaoHelp","placeholder": ""}),

		"reconhecimento_indigena": forms.RadioSelect(choices=REC_IQ_CHOICES,
		attrs={"class": "custom-control-input"}),
		
		"reconhecimento_quilombola": forms.RadioSelect(choices=REC_IQ_CHOICES,
		attrs={"class": "custom-control-input"}),

		"reconhecimento_economia_solidaria": forms.RadioSelect(choices=REC_IQ_CHOICES,
		attrs={"class": "custom-control-input"}),

		}


class UserForm(forms.ModelForm):

	password = forms.CharField(label="Senha",help_text="",min_length=6,max_length=30,
		widget=forms.PasswordInput(attrs={"class": "form-control", "aria-describedby": "senhaHelp", "placeholder": ""}))

	rPassword = forms.CharField(label="",help_text="Digite a senha novamente",min_length=6,max_length=30,
		widget=forms.PasswordInput(attrs={"class": "form-control", "aria-describedby": "r_senhaHelp", "placeholder": ""}))

	class Meta:
		model = get_user_model()
		
		fields = ["email"]

		widgets = {
		"email": forms.EmailInput(attrs={"class": "form-control", "aria-describedby": "emailHelp", "placeholder": ""}),
		}


class EntidadeForm(forms.ModelForm):

	uf = forms.ModelChoiceField(queryset=Uf.objects.all(),widget=forms.Select(attrs={"class": "form-control"}), required=False)

	class Meta:
		model = Entidade
		fields = ["nome", "municipio", "cep", "telefone_fixo", "telefone_celular"]

		widgets = {
		"nome": forms.TextInput(attrs={"class": "form-control", "aria-describedby": "nomeHelp", "placeholder": ""}),
		"telefone_celular": forms.NumberInput(attrs={"class": "form-control", "aria-describedby": "celularHelp", "placeholder": ""}),
		"telefone_fixo": forms.NumberInput(attrs={"class": "form-control", "aria-describedby": "fixoHelp", "placeholder": ""}),
		"cep": forms.NumberInput(attrs={"class": "form-control", "aria-describedby": "cepHelp", "placeholder": ""}),
		"municipio": forms.Select(attrs={"class": "form-control"})
		}


class GrupoFormalForm(forms.ModelForm):

	class Meta:
		model = GrupoFormal
		
		fields = [
		"reconhecimento_economia_solidaria", 
		"ano_fundacao", 
		"reconhecimento_quilombola", 
		"reconhecimento_indigena",
		"dap_juridica"]

		RECONHECIMENTO_CHOICES = [('1', 'Sim'), ('0', 'Não')]

		widgets = {
		
		"ano_fundacao": forms.NumberInput(
		attrs={"class": "form-control","aria-describedby": "anoFundacaoHelp","placeholder": ""}),

		"dap_juridica": forms.TextInput(attrs={"class": "form-control", "aria-describedby": "dapFisicaHelp", "placeholder": "Número da sua DAP"}),

		"reconhecimento_economia_solidaria": forms.RadioSelect(choices=RECONHECIMENTO_CHOICES,
		attrs={"class": "custom-control-input"}),

		"reconhecimento_indigena": forms.RadioSelect(choices=RECONHECIMENTO_CHOICES,
		attrs={"class": "custom-control-input"}),
		
		"reconhecimento_quilombola": forms.RadioSelect(choices=RECONHECIMENTO_CHOICES,
		attrs={"class": "custom-control-input"}),

		}