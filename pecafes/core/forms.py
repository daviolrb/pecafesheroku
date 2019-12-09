from django import forms
from pecafes.grupo.models import ProdutoGrupo

class ProdutoGrupoForm(forms.ModelForm):

	codigo = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
	nome = forms.CharField(max_length="255",widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))
	unidade = forms.CharField(max_length="255",widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}))

	class Meta:
		model = ProdutoGrupo
		fields = [
		"quantidade",
		"sazonalidade_janeiro",
		"sazonalidade_fevereiro",
		"sazonalidade_marco",
		"sazonalidade_abril",
		"sazonalidade_maio",
		"sazonalidade_junho",
		"sazonalidade_julho",
		"sazonalidade_agosto",
		"sazonalidade_setembro",
		"sazonalidade_outubro",
		"sazonalidade_novembro",
		"sazonalidade_dezembro",
		]

		widgets = {
		"quantidade": forms.NumberInput(attrs={"class": "form-control"}),
		"sazonalidade_janeiro": forms.CheckboxInput(),
		}

