from dataclasses import dataclass
from typing import Optional


@dataclass
class TokenResponseDto:
    token: Optional[str] = None