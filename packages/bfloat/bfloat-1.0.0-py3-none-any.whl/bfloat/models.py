from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class BrowserSettings:
    os: Optional[List[str]] = None
    devices: Optional[List[str]] = None
    screen: Optional[Dict[str, int]] = None
    locales: Optional[List[str]] = None

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if v is not None}

@dataclass
class BrowserConfig:
    type: str
    settings: Optional[BrowserSettings] = None
    block_ads: Optional[bool] = None
    proxy: Optional[bool] = None

    def to_dict(self) -> dict:
        result = {'type': self.type}
        if self.settings:
            result['settings'] = self.settings.to_dict()
        if self.block_ads is not None:
            result['block_ads'] = self.block_ads
        if self.proxy is not None:
            result['proxy'] = self.proxy
        return result

@dataclass
class SessionConfig:
    browser: BrowserConfig
    lifetime: Optional[int] = None
    keep_alive: Optional[bool] = None

    def to_dict(self) -> dict:
        result = {'browser': self.browser.to_dict()}
        if self.lifetime is not None:
            result['lifetime'] = self.lifetime
        if self.keep_alive is not None:
            result['keep_alive'] = self.keep_alive
        return result

@dataclass
class DebugInfo:
    ws_endpoint: str
    ws_debugger_url: str
    devtools_frontend_url: str

    def to_dict(self) -> dict:
        return self.__dict__

@dataclass
class Session:
    id: str
    status: str
    project_id: str
    updated_at: str
    created_at: str
    debug_info: DebugInfo
    duration: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Session':
        debug_info = DebugInfo(**data.pop('debug_info'))
        return cls(debug_info=debug_info, **data)

    def to_dict(self) -> dict:
        return {
            **self.__dict__,
            'debug_info': self.debug_info.to_dict()
        }

@dataclass
class StopSessionResponse:
    message: str
    status: str

    def to_dict(self) -> dict:
        return self.__dict__
