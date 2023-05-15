from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm
from django import forms

# Register your models here.



class CustomUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label=_('Password'), help_text=_('Enter a new password to change this user\'s password, or leave this field blank to keep the current password.'))

    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserAdminForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        # exclude = ('is_staff', 'is_superuser', 'groups', 'user_permissions')

class CustomUserAdmin(UserAdmin):
    form = CustomUserAdminForm

    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'city', 'state', 'zip_code', 'country', 'is_staff')
    list_filter = ('is_staff', 'is_active', 'groups')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'city', 'state', 'zip_code', 'country')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'city', 'state', 'zip_code', 'country', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'first_name', 'last_name', 'phone_number', 'city', 'state', 'zip_code', 'country')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(CustomUser, CustomUserAdmin)