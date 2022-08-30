from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account


class CustonUserAdmin(UserAdmin):
    readonly_fields = ("updated_at", "date_joined", "last_login")

    fieldsets = (
        ("Credentials", {"fields": ("username", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "email", "birthdate", "bio")}),
        ("Permissions", {"fields": ("is_superuser", "is_critic", "is_active", "is_staff")}),
        ("Important Dates", {"fields": ("updated_at", "date_joined", "last_login")}),
    )


admin.site.register(Account, CustonUserAdmin)