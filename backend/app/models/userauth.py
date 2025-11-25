
from typing import Dict

class UserAuth:
    _username: str = ""
    _token: str = ""
    
    def __new__(cls, *args, **kwargs): # type: ignore
        raise TypeError("This is intended to be a static class")
    
    @staticmethod
    def get_auth() -> Dict[str, str]:
        return {
            "user": UserAuth._username,
            "token": UserAuth._token
        }
        
    @staticmethod
    def set_auth(auth: Dict[str, str]):
        UserAuth._username = auth["user"]
        UserAuth._token = auth["token"]
    
    