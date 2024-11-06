from nautobot.apps import NautobotAppConfig, nautobot_database_ready
from nautobot_move.signals import create_custom_field


class MoveConfig(NautobotAppConfig):
    name = "nautobot_move"
    verbose_name = "Move"
    description = "A plugin for installing planned and replacing failed devices"
    version = "1.0.0"
    author = "Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen"
    author_email = "netzadmin@gwdg.de"
    base_url = "nautobot-move"
    required_settings = []
    default_settings = {}
    middleware = []

    def ready(self):
        super().ready()
        nautobot_database_ready.connect(create_custom_field, sender=self)


config = MoveConfig
