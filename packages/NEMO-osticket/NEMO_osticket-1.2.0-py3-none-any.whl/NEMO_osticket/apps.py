from django.apps import AppConfig


class OsTicketConfig(AppConfig):
    name = "NEMO_osticket"
    verbose_name = "osTicket"
    default_auto_field = "django.db.models.AutoField"

    def ready(self):
        """
        This code will be run when Django starts.
        """
        pass
