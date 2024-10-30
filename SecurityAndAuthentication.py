from fastapi import (
    FastAPI, 
    status,
    Depends,
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt

app = FastAPI()


## video - 27 - Security, OAuth2 with Password, Bearer with JWT(JSON Web Tokens)
SECRET_KEY="thequickbrownfoxjumpsoverthelazydog"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_user_db = {
    "johndoe": dict(
        username = "johndoe",
        full_name = "John Doe",
        email = "johndoe@example.com",
        hashed_password = "$2b$12$GghkJyJfm6hq0DpqPnttVOS.hNcKOH5nhLGh7F5Wl9DmiK8FEM8pG",
        disabled = False
    ),
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str]= None
    full_name: Optional[str] = None
    disabled:bool = False

class UserInDB(User):
    hashed_password:str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated= "auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def authenticate_user(fake_db, username: str, password: str):
    user = get_user(db=fake_db, username= username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data:dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc)+ expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm= ALGORITHM)
    return encoded_jwt

@app.post("/token", response_model= Token)
async def login_for_access(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub": user.username},
        expires_delta = access_token_expires,
        )
    return {"access_token":access_token, "token_type":"bearer"}

async def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

    try:
        payload = jwt.decode(token=token, key=SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_user_db, username= token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/users/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_active_user)):
    return current_user

@app.get("/users/me/items")
async def read_own_items(current_user:User = Depends(get_current_active_user)):
    return [{"Item_id":"Foo", "Owner":current_user.username}]