from flask import Blueprint, request, jsonify
from app.models import db, Ocorrencia, Usuario, Secretaria
import time
import uuid
from app.services.email_svc import enviar_email_confirmacao
from app.services.ai_svc import analisar_ocorrencia_agente

cidadao_bp = Blueprint('cidadao', __name__)

@cidadao_bp.route('/registrar', methods=['POST'])
def registrar_ocorrencia():
    dados = request.get_json()
    
    tipo = dados.get('tipo')
    descricao = dados.get('descricao')
    latitude = dados.get('latitude')
    longitude = dados.get('longitude')
    
    if not all([tipo, descricao, latitude, longitude]):
        return jsonify({"erro": "Dados incompletos. Todos os campos são obrigatórios."}), 400

    try:
        # SIMULAÇÃO DE USUÁRIO (Já que o login real ainda não está pronto)
        usuario_atual = Usuario.query.first()
        if not usuario_atual:
            usuario_atual = Usuario(
                nome_completo="Cidadão Teste", 
                email="teste@repare.aqui", 
                cpf="00000000000"
            )
            db.session.add(usuario_atual)
            db.session.commit()

        # Gera o protocolo indestrutível
        timestamp_atual = int(time.time())
        protocolo_gerado = f"REP-{timestamp_atual}-{str(uuid.uuid4())[:4].upper()}"

        # Chama a IA
        resultado_ia = analisar_ocorrencia_agente(tipo, descricao)

        # Apenas UMA criação e inserção no banco (Sem duplicidade)
        nova_ocorrencia = Ocorrencia(
            protocolo=protocolo_gerado,
            usuario_id=usuario_atual.id,
            tipo=tipo,
            descricao=descricao,
            latitude=latitude,
            longitude=longitude,
            urgencia=resultado_ia.get('urgencia', 'Não avaliada'),
            secretaria_sugerida=resultado_ia.get('secretaria', 'Triagem Manual')
        )

        db.session.add(nova_ocorrencia)
        db.session.commit()

        # Envia e-mail de forma assíncrona/desacoplada
        enviar_email_confirmacao(
            destinatario=usuario_atual.email,
            protocolo=protocolo_gerado,
            tipo=tipo,
            descricao=descricao
        )
        
        return jsonify({
            "mensagem": "Ocorrência registrada com sucesso!",
            "protocolo": protocolo_gerado,
            "status": "Aberto"
        }), 201

    except Exception as e:
        db.session.rollback() # O "Escudo" que previne o travamento (Ghost Session)
        print(f"❌ Erro interno ao registrar ocorrência: {e}")
        return jsonify({"erro": "Falha interna ao processar sua solicitação."}), 500


@cidadao_bp.route('/ocorrencias', methods=['GET'])
def listar_ocorrencias():
    ocorrencias = Ocorrencia.query.all()
    
    lista_ocorrencias = [{
        "id": occ.id,
        "protocolo": occ.protocolo,
        "tipo": occ.tipo,
        "descricao": occ.descricao,
        "latitude": occ.latitude,
        "longitude": occ.longitude,
        "status": occ.status,
        "data_criacao": occ.data_criacao.isoformat() if occ.data_criacao else None
    } for occ in ocorrencias]
    
    return jsonify(lista_ocorrencias), 200


@cidadao_bp.route('/meu-historico', methods=['GET'])
def meu_historico():
    email_usuario = request.args.get('email')
    
    if not email_usuario:
        return jsonify({"erro": "E-mail não fornecido"}), 400
        
    usuario = Usuario.query.filter_by(email=email_usuario).first()
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404
        
    ocorrencias = Ocorrencia.query.filter_by(usuario_id=usuario.id).order_by(Ocorrencia.id.desc()).all()
    
    historico = []
    for occ in ocorrencias:
        secretaria_nome = "Aguardando triagem"
        
        if occ.secretaria_id:
            secretaria = Secretaria.query.get(occ.secretaria_id)
            secretaria_nome = secretaria.nome if secretaria else secretaria_nome
                
        historico.append({
            "protocolo": occ.protocolo,
            "tipo": occ.tipo,
            "status": occ.status,
            "secretaria_responsavel": secretaria_nome,
            "data_solicitacao": occ.data_criacao.strftime("%d/%m/%Y %H:%M") if occ.data_criacao else "N/A"
        })
        
    return jsonify(historico), 200