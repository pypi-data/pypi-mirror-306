from pydantic import BaseModel, Field
from nonebot import get_driver, get_plugin_config

class Config(BaseModel):
    """Plugin Config Here"""
    group_whitelist: list = Field(default_factory=list, description="群聊白名单")
    repeat_frequency:int = Field(default=5, description="复读频率")

config = get_plugin_config(Config)
repeat_frequency = config.repeat_frequency