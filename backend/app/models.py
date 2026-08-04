from . import db
from datetime import datetime, timezone, timedelta
import uuid

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    cpf = db.Column(db.String(11), unique=True, nullable=True)
    nome_completo = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    tipo_perfil = db.Column(db.String(20), nullable=False, default='cidadao') # 'cidadao' ou 'corporativo'

class Secretaria(db.Model):
    __tablename__ = 'secretarias'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email_contato = db.Column(db.String(150), nullable=True)

class Ocorrencia(db.Model):
    __tablename__ = 'ocorrencias'
    id = db.Column(db.Integer, primary_key=True)
    protocolo = db.Column(db.String(50), unique=True, nullable=False)
    usuario_id = db.Column(db.String(36), db.ForeignKey('usuarios.id'), nullable=False)
    secretaria_id = db.Column(db.Integer, db.ForeignKey('secretarias.id'), nullable=True)
    tipo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    endereco_aproximado = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(30), nullable=False, default='Aberto')
    data_criacao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    urgencia = db.Column(db.String(50), default='Pendente')
    secretaria_sugerida = db.Column(db.String(100), nullable=True)

class HistoricoStatus(db.Model):
    __tablename__ = 'historico_status'
    id = db.Column(db.Integer, primary_key=True)
    ocorrencia_id = db.Column(db.Integer, db.ForeignKey('ocorrencias.id'), nullable=False)
    novo_status = db.Column(db.String(30), nullable=False)
    data_alteracao = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    observacao = db.Column(db.Text, nullable=True)

class TokenAcesso(db.Model):
    __tablename__ = 'tokens_acesso'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    codigo = db.Column(db.String(6), nullable=False)
    data_expiracao = db.Column(db.DateTime, nullable=False)