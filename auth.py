import hashlib
import secrets

from fastapi.requests import Request
from fastapi.responses import Response 


USERS = {
    "admin": hashlib.sha256("12345".encode()).hexdigest(),
}

SESSIONS = {}

def hash_password(password: str):

    return hashlib.sha256(password.encode()).hexdigest()

def check_credentials(username: str, password: str) -> bool:

    if username in USERS:
        if USERS[username] == hash_password(password):

            return True
    
    return False

def login_user(response: Response, username: str): 

    session_id = secrets.token_hex(16) 
    SESSIONS[session_id] = username
    response.set_cookie("session_id", session_id)

    return session_id

def get_current_user(request: Request):

    session_id = request.cookies.get("session_id")

    if not session_id: 

        return None

    return SESSIONS.get(session_id)

def logout_user(request: Request, response: Response):

    session_id = request.cookies.get("session_id")

    if session_id is not None:

        SESSIONS.pop(session_id, None)

    response.delete_cookie("session_id")
