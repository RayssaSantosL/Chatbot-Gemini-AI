# main.py
    from fastapi import FastAPI, Request, Response
    from twilio.twiml.messaging_response import MessagingResponse
    from dotenv import load_dotenv
    import os
    import logging
    from chatbot_logic import get_chatbot_response # Importa a função do chatbot

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
        # O Twilio envia os dados como um formulário x-www-form-urlencoded
        form_data = await request.form()
        incoming_msg = form_data.get('Body')
        sender_id = form_data.get('From') # Número do remetente (ex: whatsapp:+5511999999999)

        logging.info(f"Mensagem recebida de {sender_id}: {incoming_msg}")

        # Inicializa a resposta do Twilio
        resp = MessagingResponse()

        if not incoming_msg:
            logging.warning("Mensagem vazia recebida.")
            resp.message("Desculpe, não recebi nenhuma mensagem. Poderia tentar novamente?")
            return Response(content=str(resp), media_type="application/xml")

        try:
            # Chama a função do chatbot para obter a resposta
            bot_response = get_chatbot_response(incoming_msg)
            logging.info(f"Resposta gerada pelo bot: {bot_response}")
            resp.message(bot_response)
        except Exception as e:
            logging.error(f"Erro ao processar mensagem: {e}")
            resp.message("Desculpe, ocorreu um erro ao processar sua solicitação. Por favor, tente novamente mais tarde.")

        # Retorna a resposta no formato TwiML (XML)
        return Response(content=str(resp), media_type="application/xml")

    # Exemplo de como rodar o aplicativo localmente (para testes)
    # if __name__ == "__main__":
    #     import uvicorn
    #     uvicorn.run(app, host="0.0.0.0", port=8000)
    