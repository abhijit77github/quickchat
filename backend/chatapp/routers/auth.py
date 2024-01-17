"""This router contains all auth related routes"""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from ..models.auth_model import TokenRequest, User, UserDb
from ..utils.user_util import UserUtl
from ..utils.pass_util import PassUtil, generate_access_token
from ..dependencies import Getdb, ValidateToken


router = APIRouter()


@router.post("/register", tags=['auth'], status_code=status.HTTP_201_CREATED)
async def register_user(user: User, db=Depends(Getdb)):
    usrutl = UserUtl(db) 
    # raise exception if user exist
    if usrutl.get_user_by_mail(user.mail):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                            detail='Email already in use')

    # else add user
    passutl = PassUtil()
    new_usr = UserDb(mail=user.mail, name=user.name, hashed_pass=passutl.hash_pass(user.password))
    usrutl.add_user(new_usr)
    return {"msg": "User added"}



@router.post("/token", tags=["auth"])
async def create_access_token(user: TokenRequest, db=Depends(Getdb)):
    """returns token for vallid request"""
    usrutl = UserUtl(db) 
    # validate user is already registered
    user_db = usrutl.get_user_by_mail(user.mail)
    if user_db is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='User does not exist')
    
    # validate password
    passutl = PassUtil()
    if not passutl.verify_pass(user.password, user_db.hashed_pass):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Password incorrect')
    
    # generate token
    token = generate_access_token(data={"name": user_db.name, "mail": user_db.mail})
    print(f"acces_token = {token}")
    return {"access_token": token, "token_type": "bearer"}
