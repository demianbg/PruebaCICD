from django.apps import AppConfig


class AppConfig(AppConfig):
    """
    Configuración de la aplicación 'app'.

    Esta clase configura la aplicación y define los ajustes predeterminados
    para la aplicación 'app' en un proyecto Django.

    Args:
        default_auto_field (str): Especifica el tipo de campo automático por defecto.
        name (str): Nombre de la aplicación.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "app"
