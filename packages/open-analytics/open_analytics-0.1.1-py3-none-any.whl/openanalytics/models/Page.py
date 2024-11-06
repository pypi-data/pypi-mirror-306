from openanalytics.models.BaseModel import BaseModel
from dataclasses import dataclass
from datetime import datetime


class Page(BaseModel):
    SIGNATURE = "page"

    name: str
    category: str
    properties: dict

    def __init__(
        self,
        name: str,
        category: str,
        properties: dict,
        metadata: dict = None,
        time=None,
        timestamp: datetime = None,
        type: str = None,
        messageId: str = None,
    ):
        super().__init__(metadata, time, timestamp, type, messageId)
        self.name = name
        self.category = category
        self.properties = properties
        self.metadata = metadata
        self.time = time
        self.timestamp = timestamp
        self.type = type
        self.messageId = messageId
