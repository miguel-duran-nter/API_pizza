from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    password: str


users_db = {
    "draco": {
        "username": "draco",
        "full_name": "drack",
        "email": "pr@pr.es",
        "disabled": False,
        "password": "123456",
    },
    "draco2": {
        "username": "draco2",
        "full_name": "dracki",
        "email": "pr@pr.es",
        "disabled": True,
        "password": "123",
    },
}


def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"www-authenticate": "Bearer"},
        )
    
    if user.disabled:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Usario inactivo")
    
    return user


@app.get("/")
async def get(username: str):
    return search_user(username)


@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto"
        )
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta",
        )
    
    if user.disabled:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail = "Usario inactivo")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def my_user(user: User = Depends(current_user)):
    return user
