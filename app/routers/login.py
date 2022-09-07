from fastapi import APIRouter, status, HTTPException, Response,Depends
from .. import schemas,utils,database,oauth
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router=APIRouter(prefix="/login",tags=["Login"])
conn,cursor=database.run()

@router.post("/",response_model=schemas.Token)
def login(user_cred: OAuth2PasswordRequestForm = Depends()):
    cursor.execute('''SELECT * FROM USERS WHERE email = %s''',(user_cred.username,))

    db_user=cursor.fetchone()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_cred.password,db_user['password']):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    access_to = oauth.create_access_token(data= {"user_id": int(db_user["id"])})
    return {"access_token":access_to,"token_type":"bearer"}
