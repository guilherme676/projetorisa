from typing import Optional
from fastapi.params import Depends
from pydantic import BaseModel
from datetime import datetime, date, timedelta, time   

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    
    class Config:
        from_attributes = True

class UsuarioSchemaAdm(BaseModel):
    nome: str
    email: str
    senha: str
    admin: Optional[bool] = False

    class Config:
        from_attributes = True

class AgendamentoSchema(BaseModel):
    hora: time
    dia: date
    servico_id: int
    nome_completo: str
    usuario_id: int 
    
    class Config:
        from_attributes = True

class ServicoSchema(BaseModel):
    modalidade: str
    duracao: timedelta
    preco: float

    class Config:
        from_attributes = True

class ConfirmarPedidoSchema(BaseModel):
    usuario_id: int
    agendamento_id: int
    servico_id: int
    
    class Config:
        from_attributes = True

class AgendCancelarSchema(BaseModel):
    agendamento_id: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_attributes = True