from openanalytics.models.BaseModel import BaseModel
from dataclasses import dataclass
from datetime import datetime


class Log(BaseModel):
    SIGNATURE = "log"

    summary: str
    level: str
    event: str

    def __init__(
        self,
        summary: str,
        level: str,
        event: str,
        metadata: dict = None,
        time=None,
        timestamp: datetime = None,
        type: str = None,
        messageId: str = None,
    ):
        super().__init__(metadata, time, timestamp, type, messageId)
        self.summary = summary
        self.level = level
        self.event = event
        self.metadata = metadata
        self.time = time
        self.timestamp = timestamp
        self.type = type
        self.messageId = messageId
