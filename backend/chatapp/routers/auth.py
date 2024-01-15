"""This router contains all auth related routes"""

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from ..models.auth_model import User, UserDb
from ..utils.user_util import UserUtl
from ..utils.pass_util import PassUtil
from ..dependencies import Getdb


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



@router.get("/token", tags=["auth"])
async def read_users():
    """returns token for vallid request"""
    return [{"username": "Rick"}, {"username": "Morty"}]
