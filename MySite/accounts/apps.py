from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'Аккаунты'

    def ready(self) -> None:
        """
        метод конфигурации пользовательского приложения для выполнения 
        задачи инициализации, которая регистрирует сигналы.
        """
        import accounts.signals
