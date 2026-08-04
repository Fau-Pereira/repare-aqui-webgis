from flask import Blueprint, request, jsonify
from app.models import db, Ocorrencia, Secretaria

corporativo_bp = Blueprint('corporativo', __name__)

@corporativo_bp.route('/ocorrencias', methods=['GET'])
def listar_todas_ocorrencias():
    # Busca todas as ocorrências, ordenando das mais recentes para as mais antigas
    ocorrencias = Ocorrencia.query.order_by(Ocorrencia.data_criacao.desc()).all()
    
    dados = []
    for occ in ocorrencias:
        dados.append({
            "id": occ.id,
            "protocolo": occ.protocolo,
            "tipo": occ.tipo,
            "descricao": occ.descricao,
            "status": occ.status,
            "latitude": occ.latitude,
            "longitude": occ.longitude,
            "data_criacao": occ.data_criacao.strftime("%d/%m/%Y %H:%M") if occ.data_criacao else "N/A"
        })
        
    return jsonify(dados), 200

@corporativo_bp.route('/ocorrencias/<id_ocorrencia>/status', methods=['PUT'])
def atualizar_status(id_ocorrencia):
    dados = request.get_json()
    novo_status = dados.get('status')
    
    if not novo_status:
        return jsonify({"erro": "O campo 'status' é obrigatório."}), 400
        
    # Busca a ocorrência específica no banco
    ocorrencia = Ocorrencia.query.get(id_ocorrencia)
    
    if not ocorrencia:
        return jsonify({"erro": "Ocorrência não encontrada."}), 404
        
    # Atualiza o status e salva no banco de dados
    ocorrencia.status = novo_status
    db.session.commit()
    
    return jsonify({
        "mensagem": "Status atualizado com sucesso!",
        "protocolo": ocorrencia.protocolo,
        "novo_status": ocorrencia.status
    }), 200