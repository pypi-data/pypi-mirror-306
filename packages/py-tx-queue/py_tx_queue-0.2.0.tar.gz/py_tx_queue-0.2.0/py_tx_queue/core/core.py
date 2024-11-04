from alembic.config import Config, command
from pathlib import Path

_alembic_path = Path(__file__).parent.parent / "migrations"

class PyTxQueueConfig:
    _database_url: str
    _alembic_cfg: Config

    def __init__(self, database_url: str):
        self._database_url = database_url

        self._alembic_cfg = Config(_alembic_path / "alembic.ini")

        self._alembic_cfg.set_main_option("script_location", str(_alembic_path))
        self._alembic_cfg.set_main_option("schalchemy.url", database_url)


class PyTxQueue:
    _config: PyTxQueueConfig

    def __init__(self, config: PyTxQueueConfig):
        self._config = config
        command.upgrade(self._config._alembic_cfg, "head")

    def setup(self):
        ...
