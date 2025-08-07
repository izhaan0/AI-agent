from pydantic import BaseModel
from typing import List

class UserProfile(BaseModel):
    user_id: str
    skills: List[str]
    experience: List[str]
    interests: List[str]

class PostContent(BaseModel):
    content: str
    scheduled_time: str