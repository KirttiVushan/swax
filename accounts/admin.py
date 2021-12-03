from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser




class UserAdminConfig(UserAdmin):

    model = CustomUser

    search_fields=('email','username')
    ordering = ('-creation_date',)
    list_display =('email','username','creation_date','is_active','is_staff')
    fieldsets = (
        (None, {'fields': ('email','username',)}),
        ('Permissions', {'fields': ('is_staff','is_active')}),
        ('Personal', {'fields': ('creation_date',)}),
        )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2','is_staff','is_active'),
        }),
    )
    



admin.site.register(CustomUser,UserAdminConfig)
