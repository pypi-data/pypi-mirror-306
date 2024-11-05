from dataclasses import dataclass, field
from datetime import datetime


class BaseModel:

    metadata: dict = None
    time = None
    timestamp: datetime = None
    type: str
    messageId: str

    def __init__(
        self,
        metadata: dict = None,
        time=None,
        timestamp: datetime = None,
        type: str = None,
        messageId: str = None,
    ):
        self.metadata = metadata
        self.time = time
        self.timestamp = timestamp
        self.type = type
        self.messageId = messageId
        pass
