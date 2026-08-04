import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def enviar_email_confirmacao(destinatario, protocolo, tipo, descricao):
    remetente = os.getenv('EMAIL_USER')
    senha = os.getenv('EMAIL_PASS')
    
    # Se você ainda não configurou as senhas no .env, o sistema não quebra e simula o envio no terminal
    if not remetente or not senha:
        print(f"\n✅ [SIMULAÇÃO DE EMAIL] Enviado para: {destinatario}")
        print(f"Assunto: RepareAqui - Confirmação de Registro ({protocolo})")
        print(f"Mensagem: Ocorrência do tipo '{tipo}' registrada com sucesso!\n")
        return True

    msg = MIMEMultipart()
    msg['From'] = remetente
    msg['To'] = destinatario
    msg['Subject'] = f"RepareAqui - Confirmação de Solicitação ({protocolo})"

    corpo = f"""
    Olá, Cidadão!
    
    Sua solicitação foi registrada com sucesso no portal RepareAqui.
    
    Protocolo: {protocolo}
    Tipo: {tipo}
    Descrição: {descricao}
    Status: Aberto
    
    Você pode acompanhar o andamento do seu pedido através do nosso portal (Meu Histórico).
    
    Atenciosamente,
    Equipe RepareAqui - Prefeitura de Salvador
    """
    msg.attach(MIMEText(corpo, 'plain', 'utf-8'))

    try:
        # Configuração padrão para o Gmail (requer criar uma "Senha de App" na conta do Google)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente, senha)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Erro real ao enviar e-mail: {e}")
        return False