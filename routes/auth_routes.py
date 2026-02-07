from dependency import iniciar_sessao, Session  
from fastapi import APIRouter, Depends 
from schemas import LoginSchema, UsuarioSchema, UsuarioSchemaAdm
from services import UsuarioService
from models import Usuario
from dependency import verificar_token
from services import criar_token
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.post("/criar_conta")   
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(iniciar_sessao)):
    resultado = UsuarioService.cadastrar_usuario(usuario_schema, session)
    return resultado

@auth_router.post("/criar_conta_admin")   
async def criar_conta_admin(usuario_schema: UsuarioSchemaAdm, session: Session = Depends(iniciar_sessao), usuario_logado: Usuario = Depends(verificar_token)):
    resultado = UsuarioService.cadastrar_usuario_admin(usuario_schema, session, usuario_logado)
    return resultado

@auth_router.post("/login") 
async def login(login_schema: LoginSchema, session: Session = Depends(iniciar_sessao)):
    resultado = UsuarioService.login_usuario(login_schema, session)
    return resultado

@auth_router.post("/login-form") 
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(iniciar_sessao)):
    login_schema = LoginSchema(email=dados_formulario.username, senha=dados_formulario.password)  
    resultado = UsuarioService.login_form_usuario(login_schema, session)
    return resultado

@auth_router.get('/refresh')
async def user_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return{
        "access_token": access_token,
        "token_type": "Bearer"
    }