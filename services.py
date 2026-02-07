from datetime import datetime
from requests import session
from schemas import AgendCancelarSchema, AgendamentoSchema, ConfirmarPedidoSchema, LoginSchema, ServicoSchema, UsuarioSchema, UsuarioSchemaAdm
from models import Usuario, Servico, Agendamento
from dependency import iniciar_sessao, Session, db, verificar_token  
from fastapi import Depends, HTTPException
from security import SECRET_KEY, bcrypt_context, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone

def criar_token(id_usuario, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_codificado

def achar_duracao(servico_id, session: Session = Depends(iniciar_sessao)):
    duracao = session.query(Servico.duracao).filter(Servico.id == servico_id).first()
    return duracao

class UsuarioService:
    @staticmethod
    def cadastrar_usuario_admin(usuario_schema: UsuarioSchemaAdm, session: Session, usuario_logado: Usuario):
        usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
        if usuario:
            raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")   
        print(usuario_logado.admin)
        if usuario_schema.admin == True and usuario_logado.admin == False:
            raise HTTPException(status_code=403, detail="Apenas usuários administradores podem criar contas administradoras.")
        else:
            senha_hash = bcrypt_context.hash(usuario_schema.senha)
            novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_hash, admin=usuario_schema.admin == True) 
            session.add(novo_usuario)
            session.commit()
            return {"mensagem": f"Usuário cadastrado com sucesso! "}
        
    @staticmethod
    def cadastrar_usuario(usuario_schema: UsuarioSchema, session: Session):
        usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
        if usuario:
            raise HTTPException(status_code=400, detail="E-mail do usuário já cadastrado")   
        else:
            senha_hash = bcrypt_context.hash(usuario_schema.senha)
            novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_hash, admin=False) 
            session.add(novo_usuario)
            session.commit()
            return {"mensagem": f"Usuário cadastrado com sucesso! "}    
        
    @staticmethod
    def login_usuario(login_schema: LoginSchema, session: Session):
        usuario = session.query(Usuario).filter(Usuario.email == login_schema.email).first()
        if not usuario:
            raise HTTPException(status_code=400, detail="E-mail ou senha incorretos")
        elif not bcrypt_context.verify(login_schema.senha, usuario.senha):
            raise HTTPException(status_code=400, detail="E-mail ou senha incorretos")
        else:
            access_token = criar_token(usuario.id)
            refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
            return{
                "access_token": access_token,
                "refresh_token": refresh_token,
                "token_type": "Bearer"
            }
        
    @staticmethod
    def login_form_usuario(login_schema: LoginSchema, session: Session):
        usuario = session.query(Usuario).filter(Usuario.email == login_schema.email).first()
        if not usuario:
            raise HTTPException(status_code=400, detail="E-mail ou senha incorretos")
        elif not bcrypt_context.verify(login_schema.senha, usuario.senha):
            raise HTTPException(status_code=400, detail="E-mail ou senha incorretos")
        else:
            access_token = criar_token(usuario.id)
            return{
                "access_token": access_token,
                "token_type": "Bearer"
            }
        
class AgendamentoService:
    @staticmethod
    def criar_agendamento(agendamento_schema: AgendamentoSchema, session: Session, usuario_logado: Usuario):       
        inicio_dt = datetime.combine(agendamento_schema.dia, agendamento_schema.hora)
        duracao_dt = achar_duracao(agendamento_schema.servico_id, session).duracao
        fim_dt = inicio_dt + duracao_dt
        hora_fim = fim_dt.time()
        conflito = session.query(Agendamento).filter(
            Agendamento.dia == agendamento_schema.dia,
            Agendamento.hora_comeco < hora_fim,
            Agendamento.hora_fim > agendamento_schema.hora
        ).first()
        if conflito:
            raise HTTPException(status_code=400, detail="Conflito de horário. Por favor, escolha outro horário.")
        novo = Agendamento(
            servico_id=agendamento_schema.servico_id,
            usuario_id=usuario_logado.id,
            dia=agendamento_schema.dia,
            hora_comeco=agendamento_schema.hora,
            hora_fim=hora_fim,
            nome_completo=agendamento_schema.nome_completo
        )
        session.add(novo)
        session.commit()
        session.refresh(novo)
        return {
            'mensagem': 'Agendamento criado com sucesso.',
        }

    @staticmethod
    def cancelar_agendamento(agendamento_cancelar: AgendCancelarSchema, session: Session, usuario_logado: Usuario):
        agendamento = session.query(Agendamento).filter(Agendamento.id == agendamento_cancelar.agendamento_id).first()
        if not agendamento:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
        if agendamento.usuario_id != usuario_logado.id:
            raise HTTPException(
                status_code=403, 
                detail="Você não tem permissão para cancelar este agendamento pois pertence a outro usuário."
            )
        session.delete(agendamento)
        session.commit()
        return {"mensagem": "Agendamento cancelado com sucesso."}
    
    @staticmethod
    def confirmar_agendamento_admin(agendamento_id: int, session: Session, usuario_logado: Usuario):
        if not usuario_logado.admin:
            raise HTTPException(status_code=403, detail="Você não tem permissão para confirmar este agendamento.")
        agendamento = session.query(Agendamento).filter(Agendamento.id == agendamento_id).first()
        if not agendamento:
            raise HTTPException(status_code=404, detail="Agendamento não encontrado.")
        agendamento.status = 'confirmado'
        session.commit()
        return {"mensagem": "Agendamento confirmado com sucesso."}
        
class SrvService:
    @staticmethod
    def listar_servicos(session: Session):
        servicos = session.query(Servico).all()
        if not servicos:
            raise HTTPException(status_code=404, detail="Nenhum serviço cadastrado.")
        return servicos
    
    @staticmethod
    def criar_servico(servico_schema: ServicoSchema, session: Session, usuario_logado: Usuario):
        if not usuario_logado.admin:
            raise HTTPException(status_code=403, detail="Você não tem permissão para criar um serviço.")
        conflito = session.query(Servico).filter(Servico.modalidade == servico_schema.modalidade).first()
        if conflito:
            raise HTTPException(status_code=400, detail="Já existe um serviço com essa modalidade!")                 
        novo_servico = Servico(
            modalidade=servico_schema.modalidade,
            duracao=servico_schema.duracao,
            preco=servico_schema.preco
        )
        session.add(novo_servico)
        session.commit()
        session.refresh(novo_servico)
        return novo_servico
