import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

def analisar_ocorrencia_agente(tipo, descricao):
    api_key = os.getenv("GOOGLE_API_KEY")
    
    # Fallback caso a chave não esteja configurada
    if not api_key:
        print("⚠️ Chave GOOGLE_API_KEY não encontrada. IA desativada.")
        return {"urgencia": "Não avaliada", "secretaria": "Triagem Manual"}
        
    # Inicializa o modelo (Flash é extremamente rápido e barato para triagens)
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1, google_api_key=api_key)
    
    template = """
    Você é um agente de inteligência artificial da prefeitura de Salvador.
    Sua missão é atuar como um despachante urbano. Analise o problema relatado pelo cidadão:
    
    Tipo de Problema: {tipo}
    Descrição do Cidadão: {descricao}
    
    Classifique a urgência (Baixa, Média, Alta) e sugira a secretaria ou órgão municipal responsável:
    - SEMAN (Secretaria de Manutenção da Cidade)
    - TRANSALVADOR (Trânsito e semáforos)
    - LIMPURB (Limpeza e entulho)
    - DESAL (Companhia de Desenvolvimento Urbano de Salvador)
    
    Responda APENAS em formato JSON válido, contendo as chaves "urgencia" e "secretaria". Não escreva mais nada.
    """
    
    prompt = PromptTemplate(template=template, input_variables=["tipo", "descricao"])
    chain = prompt | llm
    
    try:
        resposta = chain.invoke({"tipo": tipo, "descricao": descricao})
        # Limpa formatações Markdown que o LLM possa retornar (ex: ```json ... ```)
        texto_limpo = resposta.content.replace("```json", "").replace("```", "").strip()
        dados_ia = json.loads(texto_limpo)
        
        print(f"🤖 [AGENTE IA] Triagem concluída: {dados_ia}")
        return dados_ia
        
    except Exception as e:
        print(f"❌ Erro no Agente de IA: {e}")
        return {"urgencia": "Não avaliada", "secretaria": "Triagem Manual"}