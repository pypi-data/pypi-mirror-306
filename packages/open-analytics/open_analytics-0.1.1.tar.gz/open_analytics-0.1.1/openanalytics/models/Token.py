from openanalytics.models.BaseModel import BaseModel
from dataclasses import dataclass
from datetime import datetime


class Token(BaseModel):
    SIGNATURE = "token"

    event: str
    action: str
    count: int

    def __init__(
        self,
        event: str,
        action: str,
        count: int,
        metadata: dict = None,
        time=None,
        timestamp: datetime = None,
        type: str = None,
        messageId: str = None,
    ):
        super().__init__(metadata, time, timestamp, type, messageId)
        self.event = event
        self.action = action
        self.count = count
        self.metadata = metadata
        self.time = time
        self.timestamp = timestamp
        self.type = type
        self.messageId = messageId
