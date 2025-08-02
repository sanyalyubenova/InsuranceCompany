from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from InsuranceCompany.accounts.models import Profile

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'date_of_birth', 'get_profile_name')
    list_filter = ('date_of_birth',)
    search_fields = ('user__email', 'first_name', 'last_name')
    ordering = ('user__email',)
    
    def get_profile_name(self, obj):
        return obj.get_profile_name()
    get_profile_name.short_description = 'Full Name'
