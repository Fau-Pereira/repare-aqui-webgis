from flask import Blueprint, request, jsonify
from app.models import db, Usuario, TokenAcesso
from datetime import datetime, timezone, timedelta
import random

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/solicitar-token', methods=['POST'])
def solicitar_token():
    dados = request.get_json()
    email = dados.get('email')

    if not email:
        return jsonify({"erro": "E-mail é obrigatório"}), 400

    # Verifica se o usuário existe, se não, cria um cadastro básico
    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        usuario = Usuario(nome_completo="Novo Cidadão", email=email, cpf=None)
        db.session.add(usuario)
        db.session.commit()

    # Gera um código de 6 dígitos numéricos
    codigo_gerado = str(random.randint(100000, 999999))
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=10) # Válido por 10 min

    # Salva o token no banco
    novo_token = TokenAcesso(email=email, codigo=codigo_gerado, data_expiracao=expiracao)
    db.session.add(novo_token)
    db.session.commit()

    # Aqui no futuro você conectará com o email_svc.py para disparar o código.
    # Por enquanto, vamos imprimir no terminal para facilitar o teste.
    print(f"\n🔐 [SIMULAÇÃO GOV.BR] Token para {email}: {codigo_gerado}\n")

    return jsonify({"mensagem": "Token enviado para o seu e-mail!"}), 200

@auth_bp.route('/validar-token', methods=['POST'])
def validar_token():
    dados = request.get_json()
    email = dados.get('email')
    codigo = dados.get('codigo')

    # Busca o token mais recente desse e-mail
    token_salvo = TokenAcesso.query.filter_by(email=email, codigo=codigo).order_by(TokenAcesso.id.desc()).first()

    if not token_salvo:
        return jsonify({"erro": "Código inválido."}), 401
    
    # Tornar os datetimes compatíveis (ambos *aware* de fuso horário)
    agora = datetime.now(timezone.utc)
    expiracao_token = token_salvo.data_expiracao
    
    if expiracao_token.tzinfo is None:
        expiracao_token = expiracao_token.replace(tzinfo=timezone.utc)

    if agora > expiracao_token:
        return jsonify({"erro": "O código expirou. Solicite um novo."}), 401

    usuario = Usuario.query.filter_by(email=email).first()

    # Se validou com sucesso, apagamos o token por segurança
    db.session.delete(token_salvo)
    db.session.commit()

    # Devolvemos os dados do usuário. Na próxima evolução, devolveremos um JWT real aqui.
    return jsonify({
        "mensagem": "Login realizado com sucesso!",
        "usuario": {
            "id": usuario.id,
            "nome": usuario.nome_completo,
            "email": usuario.email,
            "perfil": usuario.tipo_perfil
        }
    }), 200