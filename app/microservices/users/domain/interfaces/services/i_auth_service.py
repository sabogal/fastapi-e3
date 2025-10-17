from typing import Protocol, Optional

class IAuthService(Protocol):
    
    async def login_with_email(self, email: str, password: str) -> str:
        raise NotImplementedError
