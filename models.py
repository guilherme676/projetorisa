from sqlalchemy import Column, ForeignKey, Integer, Interval, String, Boolean, create_engine, Time, Date, Enum
from sqlalchemy.orm import declarative_base

db = create_engine('sqlite:///banco.db')
Base = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)       
    email = Column(String, unique=True)
    senha = Column(String)
    admin = Column(Boolean, default=False)

    def __init__(self, nome, email, senha, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.admin = admin

class Servico(Base):
    __tablename__ = "servicos"
    id = Column(Integer, primary_key=True, index=True)
    modalidade = Column(String)       
    duracao = Column(Interval)
    preco = Column(Integer)

    def __init__(self, modalidade, preco, duracao):
        self.modalidade = modalidade
        self.preco = preco
        self.duracao = duracao

class Agendamento(Base):
    __tablename__ = "agendamentos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(ForeignKey('usuarios.id'))
    nome_completo= Column(String)
    servico_id = Column(ForeignKey('servicos.id'))       
    hora_comeco = Column(Time)
    hora_fim = Column(Time)
    dia = Column(Date)
    status = Column(Enum('pendente', 'confirmado', 'cancelado'), default='pendente')

    def __init__(self, usuario_id, nome_completo, servico_id, hora_comeco, hora_fim, dia):
        self.usuario_id = usuario_id
        self.nome_completo = nome_completo
        self.servico_id = servico_id
        self.hora_comeco = hora_comeco
        self.hora_fim = hora_fim
        self.dia = dia
        self.status = 'pendente'