from enum import Enum

class Event(str,Enum):
    """Nombre de los eventos del patro Observer."""

    CONFIG_CHANGED = "config_changed"
    GENERATING_START = "generating_start"
    GENERATING_DONE = "generating_done"
    GENERATING_ERROR = "generating_error"
    MESSAGES_UPDATED = "messages_updated"
    EXPORT_DONE = "export_done"