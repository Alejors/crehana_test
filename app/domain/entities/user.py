from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    email: str
    password: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    username: Optional[str] = None
    id: Optional[int] = None
