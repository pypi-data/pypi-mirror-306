
from typing import List, Optional, Any


class BFloatError(Exception):
    def __init__(self, message: str, status: Optional[int] = None, response: Any = None):
        super().__init__(message)
        self.status = status
        self.response = response
