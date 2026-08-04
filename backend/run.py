from app import create_app, db
# Importamos os modelos para o SQLAlchemy reconhecê-los antes de criar as tabelas
from app.models import Usuario, Secretaria, Ocorrencia, HistoricoStatus

app = create_app()

if __name__ == '__main__':
    # Cria as tabelas automaticamente no banco se elas não existirem
    with app.app_context():
        db.create_all()
        print("✅ Tabelas verificadas/criadas com sucesso!")
        
    app.run(debug=True, host='0.0.0.0', port=5000)