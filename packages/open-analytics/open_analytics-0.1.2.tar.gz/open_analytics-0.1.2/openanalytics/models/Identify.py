from openanalytics.models.BaseModel import BaseModel
from dataclasses import dataclass
from datetime import datetime


class Identify(BaseModel):
    SIGNATURE = "identify"

    userId: str
    event: str

    def __init__(
        self,
        userID: str,
        event: str,
        metadata: dict,
        time=None,
        timestamp: datetime = None,
        type: str = None,
        messageId: str = None,
    ):
        super().__init__(metadata, time, timestamp, type, messageId)
        self.userId = userID
        self.event = event
        self.metadata = metadata
        self.time = time
        self.timestamp = timestamp
        self.type = type
        self.messageId = messageId
