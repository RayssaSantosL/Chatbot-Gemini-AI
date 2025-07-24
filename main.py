# main.py
from fastapi import FastAPI, Request, Response
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import logging

# Configura o logger para exibir mensagens no console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Verifica se as variáveis de ambiente estão carregadas (para depuração)
logging.info(f"GOOGLE_API_KEY carregada: {'Sim' if os.getenv('GOOGLE_API_KEY') else 'Não'}")
logging.info(f"TWILIO_ACCOUNT_SID carregado: {'Sim' if os.getenv('TWILIO_ACCOUNT_SID') else 'Não'}")

# Inicializa o aplicativo FastAPI
app = FastAPI()

# Rota para a raiz do aplicativo (apenas para verificar se está online)
@app.get("/")
async def root():
    logging.info("Requisição GET recebida na raiz.")
    return {"message": "Chatbot da Farmácia está online e aguardando mensagens!"}

# Rota para o webhook do Twilio
@app.post("/webhook")
async def handle_whatsapp_message(request: Request):
    form_data = await request.form()
    incoming_msg = form_data.get('Body')
    sender_id = form_data.get('From')

    logging.info(f"Mensagem recebida de {sender_id}: {incoming_msg}")

    resp = MessagingResponse()

    if not incoming_msg:
        logging.warning("Mensagem vazia recebida.")
        resp.message("Desculpe, não recebi nenhuma mensagem. Poderia tentar novamente?")
        return Response(content=str(resp), media_type="application/xml")

    try:
    # Chama a função do chatbot para obter a resposta
    # Agora get_chatbot_response está no mesmo arquivo
        bot_response = get_chatbot_response(incoming_msg)
        logging.info(f"Resposta gerada pelo bot: {bot_response}")
        resp.message(bot_response)
    except Exception as e:
        logging.error(f"Erro ao processar mensagem: {e}")
        resp.message("Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde.")

    return Response(content=str(resp), media_type="application/xml")

    # --- INÍCIO DO CÓDIGO DE chatbot_logic.py ---

    # Importações que estavam em chatbot_logic.py (mantenha se não estiverem em main.py)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Inicializa o modelo Gemini
llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY"))

# Define o prompt do sistema para o chatbot
system_prompt = (
    "Você é um assistente de chatbot prestativo e amigável para uma farmácia de manipulação."
    "Seu objetivo é fornecer informações precisas e úteis sobre os serviços da farmácia, produtos,"
    "horários de funcionamento, localização e como enviar receitas."
    "Mantenha as respostas concisas e diretas ao ponto."
    "Se a pergunta estiver fora do seu escopo ou exigir consulta médica, peça para o usuário entrar em contato direto com a farmácia."
    "Exemplos de informações que você pode fornecer:"
    "- Horário de funcionamento: De segunda a sexta, das 8h às 18h, e sábados das 9h às 13h."
    "- Endereço: Rua da Manipulação, 123, Centro, Cidade."
    "- Telefone: (XX) XXXX-XXXX"
    "- Como enviar receita: Você pode enviar sua receita por e-mail (receita@farmacia.com), WhatsApp (mesmo número que você está usando) ou trazer pessoalmente."
    "- Produtos: Mencione que a farmácia trabalha com manipulação personalizada de medicamentos, cosméticos e suplementos."
    "Sempre seja educado e prestativo."
    )

    # Cria o template do prompt
prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("user", "{user_message}"),
        ]
    )

    # Cria a cadeia de processamento
chain = prompt | llm | StrOutputParser()

def get_chatbot_response(user_message: str) -> str:
    """
    Obtém uma resposta do chatbot usando o modelo Gemini.
    """
    try:
        response = chain.invoke({"user_message": user_message})
        return response
    except Exception as e:
        logging.error(f"Erro ao invocar a cadeia do chatbot: {e}")
        return "Desculpe, não consegui gerar uma resposta no momento. Por favor, tente novamente."

    # --- FIM DO CÓDIGO DE chatbot_logic.py ---
    