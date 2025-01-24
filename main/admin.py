from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = ('username', "email", 'name', 'date_joined', 'slug', "is_staff", "is_active",)
    list_filter = ("is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ('username', "email", "password", 'name', 'slug')}),
        ("Permissions", {"fields": (
            "is_active", "is_staff", 'is_superuser', "groups", "user_permissions", 'date_joined', 'updated', 'last_login', 'data')}
         ),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                'username', "email", 'slug', "password1", "password2", "is_active",
                "groups", "user_permissions",
            )}),
    )
    search_fields = ('username', 'email')
    ordering = ("-date_joined",)
    readonly_fields = ('last_login', 'date_joined', 'updated')
    prepopulated_fields = {'slug': ('username',)}


admin.site.register(CustomUser, CustomUserAdmin)
