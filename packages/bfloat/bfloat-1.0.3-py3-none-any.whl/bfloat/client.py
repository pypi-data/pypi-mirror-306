"""
BFloat.ai Python SDK
Version: 1.0.0
License: bfloat

A Python SDK for interacting with the bfloat.ai API.
This SDK provides a simple interface for managing browser automation sessions
through the bfloat.ai platform.

Features:
- Full type hinting support
- Async support using asyncio and aiohttp
- Comprehensive error handling
- Session management (create, list, get, stop)
- Browser configuration utilities
"""

from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import requests
import aiohttp
import json
from datetime import datetime
from .models import BrowserSettings, BrowserSettings, BrowserConfig, SessionConfig, DebugInfo, Session, StopSessionResponse
from .exceptions import BFloatError


class BfloatSDK:
    def __init__(self, api_key: str, base_url: str = "https://api.bfloat.ai/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self._session = None

    async def _ensure_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(headers={
                'x-api-key': self.api_key,
                'Content-Type': 'application/json'
            })
        return self._session

    async def _make_request(self, method: str, endpoint: str, data: Optional[dict] = None) -> Any:
        session = await self._ensure_session()
        url = f"{self.base_url}{endpoint}"

        try:
            async with session.request(method, url, json=data) as response:
                response_data = await response.json()

                if not response.ok:
                    raise BFloatError(
                        response_data.get('message', 'Request failed'),
                        response.status,
                        response_data
                    )

                return response_data
        except aiohttp.ClientError as e:
            raise BFloatError(str(e))

    async def list_sessions(self) -> List[Session]:
        data = await self._make_request('GET', '/sessions')
        return [Session.from_dict(session_data) for session_data in data]

    async def get_session(self, session_id: str) -> Session:
        data = await self._make_request('GET', f'/sessions/{session_id}')
        return Session.from_dict(data)

    async def create_session(self, config: SessionConfig) -> Session:
        data = await self._make_request('POST', '/sessions', data=config.to_dict())
        return Session.from_dict(data)

    async def stop_session(self, session_id: str) -> StopSessionResponse:
        data = await self._make_request('POST', f'/sessions/{session_id}/stop')
        return StopSessionResponse(**data)

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
