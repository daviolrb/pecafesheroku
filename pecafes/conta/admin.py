from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import(
	CustomUserCreationForm, CustomUserChangeForm
)

from .models import Usuario
# Register your models here.

class CustomUserAdmin(UserAdmin):
	
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm
	model = get_user_model()
	list_display = ["username", "email", "tipo_usuario"]

	fieldsets = UserAdmin.fieldsets + (
		(None, {'fields': ('tipo_usuario',)}),
		)

admin.site.register(get_user_model(), CustomUserAdmin)
