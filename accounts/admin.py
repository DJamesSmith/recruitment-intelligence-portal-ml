from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import EmailOTP, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display: tuple[str, ...] = (
        "email",
        "role",
        "is_email_verified",
        "is_staff",
        "is_active",
    )
    list_filter: tuple[str, ...] = ("role", "is_email_verified", "is_staff", "is_active")
    search_fields: tuple[str, ...] = ("email", "first_name", "last_name")
    ordering: tuple[str, ...] = ("email",)
    fieldsets: tuple[tuple[str, dict[str, tuple[str, ...]]], ...] = (
        (None, {"fields": ("email", "password")}),
        ("Personal", {"fields": ("first_name", "last_name", "phone")}),
        ("Role", {"fields": ("role", "is_email_verified")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets: tuple[tuple[None | str, dict[str, tuple[str, ...]]], ...] = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2", "role")}),
    )


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display: tuple[str, ...] = ("user", "code", "expires_at", "is_used", "created_at")
    list_filter: tuple[str, ...] = ("is_used",)
    search_fields: tuple[str, ...] = ("user__email",)
