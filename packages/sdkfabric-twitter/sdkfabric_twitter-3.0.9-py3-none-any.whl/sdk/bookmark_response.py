"""
bookmark_response automatically generated by SDKgen please do not edit this file manually
https://sdkgen.app
"""

from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from .bookmark import Bookmark
class BookmarkResponse(BaseModel):
    data: Optional[Bookmark] = Field(default=None, alias="data")
    pass
