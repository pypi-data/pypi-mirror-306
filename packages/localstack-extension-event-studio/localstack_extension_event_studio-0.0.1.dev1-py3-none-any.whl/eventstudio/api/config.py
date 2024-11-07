from pathlib import Path


class Config:
    BASE_URL = "http://localhost:4566/_extension/eventstudio"
    API_PREFIX = "/api"  # required to avoid collisions with frontend

    EVENTS = "/events"
    ALL_EVENTS = "/events/all"
    TRACES = "/traces"
    REPLAY = "/replay"

    PACKAGE_ROOT = Path(__file__).parents[2]
    DATABASE_NAME = "event_studio.db"

    DATABASE_PATH = DATABASE_NAME if DATABASE_NAME == "" else PACKAGE_ROOT / DATABASE_NAME

    @staticmethod
    def get_full_url(endpoint):
        return f"{Config.BASE_URL}{Config.API_PREFIX}{endpoint}"

    @staticmethod
    def get_relative_url(endpoint):
        return f"{Config.API_PREFIX}{endpoint}"
