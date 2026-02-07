from fastapi import APIRouter, Depends
from models import Agendamento
from schemas import AgendCancelarSchema, AgendamentoSchema
from dependency import iniciar_sessao, Session
from services import AgendamentoService
from dependency import verificar_token

agendamento_router = APIRouter(prefix="/agendamento", tags=["agendamento"], dependencies=[Depends(verificar_token)])

@agendamento_router.post("/agendamento")
async def criar_agendamento(agendamento_schema: AgendamentoSchema, session: Session = Depends(iniciar_sessao), usuario_logado = Depends(verificar_token)):
    resultado = AgendamentoService.criar_agendamento(agendamento_schema, session, usuario_logado)
    return resultado

@agendamento_router.delete("/cancelar")
async def cancelar_agendamento(agendamento_cancelar: AgendCancelarSchema, session: Session = Depends(iniciar_sessao), usuario_logado = Depends(verificar_token)):
    resultado = AgendamentoService.cancelar_agendamento(agendamento_cancelar, session, usuario_logado)
    return resultado
    
@agendamento_router.post('confirmar_agendamento_admin')
async def confirmar_agendamento_admin(agendamento_id: int, session: Session = Depends(iniciar_sessao), usuario_logado = Depends(verificar_token)):
    resultado = AgendamentoService.confirmar_agendamento_admin(agendamento_id, session, usuario_logado)
    return resultado
