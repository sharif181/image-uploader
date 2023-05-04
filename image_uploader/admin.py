from .models import User
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import FileUpload, ArbitaryTier, GenerateLink


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_active']
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('email', 'is_active')
        }),
        ('Tier info', {
            'fields': ('build_in_tier', 'arbitary_tier')
        }),
        ('Permissions', {
            'fields': (
                'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'build_in_tier', 'arbitary_tier')
        }),
    )

    list_per_page = 25



@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    pass

@admin.register(ArbitaryTier)
class ArbitaryTierAdmin(admin.ModelAdmin):
    pass

@admin.register(GenerateLink)
class GenerateLinkAdmin(admin.ModelAdmin):
    pass