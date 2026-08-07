from enum import Enum


class ContentType(str, Enum):
    URL = "url"
    PDF = "pdf"
    TEXT = "text"
