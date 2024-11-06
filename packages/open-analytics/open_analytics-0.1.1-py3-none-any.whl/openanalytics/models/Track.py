from openanalytics.models.BaseModel import BaseModel
from dataclasses import dataclass
from datetime import datetime


class Track(BaseModel):
    SIGNATURE = "track"

    endpoint: str
    event: str
    properties: dict

    def __init__(
        self,
        endpoint: str,
        event: str,
        properties: dict,
        metadata: dict = None,
        time=None,
        timestamp: datetime = None,
        type: str = None,
        messageId: str = None,
    ):
        super().__init__(metadata, time, timestamp, type, messageId)
        self.endpoint = endpoint
        self.event = event
        self.properties = properties
        self.metadata = metadata
        self.time = time
        self.timestamp = timestamp
        self.type = type
        self.messageId = messageId
