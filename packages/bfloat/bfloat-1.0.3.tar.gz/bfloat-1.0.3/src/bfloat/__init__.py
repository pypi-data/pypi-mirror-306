"""BFloat.ai Python SDK

A powerful and intuitive Python SDK for interacting with the bfloat.ai API.
"""

from .client import BfloatSDK
from .models import (
    BrowserConfig,
    BrowserSettings,
    SessionConfig,
    Session,
    StopSessionResponse,
    DebugInfo,
)
from .exceptions import BFloatError
from .constants import DEFAULT_BROWSER_CONFIG

__version__ = "1.0.0"
__all__ = [
    "BfloatSDK",
    "BFloatError",
    "BrowserConfig",
    "BrowserSettings",
    "SessionConfig",
    "Session",
    "StopSessionResponse",
    "DebugInfo",
    "DEFAULT_BROWSER_CONFIG",
]