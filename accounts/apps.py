from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "accounts"

    def ready(self: "AccountsConfig") -> None:
        import accounts.signals