from django.apps import AppConfig


class CatalogConfig(AppConfig):
    name = 'locallibrary.catalog'
    verbose_name = "Catalog"

    def ready(self):
        """Override this to put in:
            Users system checks
            Users signal registration
        """
        pass
