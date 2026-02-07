from fastapi import APIRouter, Depends
from dependency import iniciar_sessao, Session, verificar_token
from services import SrvService
from schemas import ServicoSchema

srv_router = APIRouter(prefix="/srv", tags=["srv"])

@srv_router.get("/listar")
async def listar_servicos(session: Session = Depends(iniciar_sessao)):
    resultado = SrvService.listar_servicos(session)
    return resultado

@srv_router.post("/criar", dependencies=[Depends(verificar_token)])
async def criar_servicos(servico_schema: ServicoSchema, session: Session = Depends(iniciar_sessao), usuario_logado = Depends(verificar_token)):
    resultado = SrvService.criar_servico(servico_schema, session, usuario_logado)
    return resultado

