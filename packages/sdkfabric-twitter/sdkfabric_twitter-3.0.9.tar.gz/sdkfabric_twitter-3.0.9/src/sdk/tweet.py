"""
tweet automatically generated by SDKgen please do not edit this file manually
https://sdkgen.app
"""

from pydantic import BaseModel, Field, GetCoreSchemaHandler
from pydantic_core import CoreSchema, core_schema
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union
from .tweet_geo import TweetGeo
from .tweet_media import TweetMedia
from .tweet_poll import TweetPoll
from .tweet_reply import TweetReply
class Tweet(BaseModel):
    direct_message_deep_link: Optional[str] = Field(default=None, alias="direct_message_deep_link")
    for_super_followers_only: Optional[bool] = Field(default=None, alias="for_super_followers_only")
    geo: Optional[TweetGeo] = Field(default=None, alias="geo")
    media: Optional[TweetMedia] = Field(default=None, alias="media")
    poll: Optional[TweetPoll] = Field(default=None, alias="poll")
    quote_tweet_id: Optional[str] = Field(default=None, alias="quote_tweet_id")
    reply: Optional[TweetReply] = Field(default=None, alias="reply")
    reply_settings: Optional[str] = Field(default=None, alias="reply_settings")
    text: Optional[str] = Field(default=None, alias="text")
    possibly_sensitive: Optional[bool] = Field(default=None, alias="possibly_sensitive")
    lang: Optional[str] = Field(default=None, alias="lang")
    pass
