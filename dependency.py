from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session 
from models import db, Usuario 
from jose import JWTError, jwt
from security import SECRET_KEY, ALGORITHM, oauth2_scheme

def iniciar_sessao():
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()

def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(iniciar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        id_usuario = int(dic_info.get("sub"))
    except JWTError as erro:
        print(erro)
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    return usuario 