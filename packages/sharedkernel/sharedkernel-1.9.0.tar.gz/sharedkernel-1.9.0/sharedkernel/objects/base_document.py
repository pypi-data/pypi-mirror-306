from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BaseDocument(BaseModel):
    id: Optional[str]
    is_deleted: bool = False
    created_on: datetime = Field(default_factory=datetime.now)
    updated_on: datetime = Field(default_factory=datetime.now)