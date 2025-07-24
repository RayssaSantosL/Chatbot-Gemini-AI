**🤖 Chatbot de Farmácia com IA para WhatsApp**

Este projeto implementa um chatbot inteligente para farmácias de manipulação, capaz de interagir com clientes via WhatsApp. Ele utiliza a inteligência artificial do Google Gemini para compreender e responder a perguntas, e o FastAPI para criar uma API web que se integra com o Twilio.

**✨ Funcionalidades Principais**

*Comunicação via WhatsApp:* Integrado ao Twilio para receber e enviar mensagens diretamente no WhatsApp.

*Inteligência Artificial (IA):* Utiliza o modelo Gemini do Google AI para processar a linguagem natural e gerar respostas coerentes.

*API Web Robusta:* Construído com FastAPI para uma interface HTTP performática e escalável.

*Conteinerização com Docker:* Empacotado em uma imagem Docker para facilitar a implantação e garantir a portabilidade em diferentes ambientes.

*Informações Essenciais:* Capaz de responder a perguntas sobre produtos, serviços, horários de funcionamento, como enviar receitas e outras dúvidas comuns da farmácia.

**🚀 Tecnologias Utilizadas**

Python 3.10+

*FastAPI:* Framework web para construir APIs assíncronas.

*Uvicorn:* Servidor ASGI para rodar aplicações FastAPI.

*Google Generative AI (Gemini):* A inteligência por trás das respostas do chatbot.

*LangChain:* Framework para orquestração de Large Language Models (LLMs).

*Twilio:* Plataforma para a integração com a API do WhatsApp Business.

*Docker:* Para empacotamento e execução da aplicação em contêineres.

*ngrok:* Ferramenta para expor o servidor local à internet (para desenvolvimento/testes).

*Render.com:* Plataforma de nuvem para implantação em produção.

**📦 Como Rodar Localmente**

Siga estes passos para configurar e executar o chatbot em seu ambiente de desenvolvimento.

Pré-requisitos
Antes de começar, certifique-se de ter o seguinte instalado e configurado:

Python 3.10+

Docker Desktop: Essencial para construir e rodar a imagem Docker.

Conta Twilio: Com a WhatsApp Sandbox configurada. Anote seu Account SID e Auth Token.

Chave de API do Google Generative AI (Gemini): Obtenha uma chave no Google AI Studio.

ngrok: Baixe e configure seu authtoken.

**1. Clonar o Repositório (ou Criar o Projeto)**

Se você já clonou um repositório vazio, pule este passo. Caso contrário, crie a pasta do projeto:

mkdir chatbot_farmacia

cd chatbot_farmacia

**2. Configurar Variáveis de Ambiente**

Crie um arquivo chamado .env na raiz do diretório chatbot_farmacia (no mesmo nível de main.py e Dockerfile). Este arquivo armazenará suas chaves de API de forma segura.

|# .env
GOOGLE_API_KEY="SUA_CHAVE_DE_API_DO_GOOGLE_GEMINI_AQUI"
TWILIO_ACCOUNT_SID="ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Seu Account SID do Twilio
TWILIO_AUTH_TOKEN="your_auth_token_here"             # Seu Auth Token do Twilio

Atenção: Nunca adicione o arquivo .env ao seu controle de versão (Git/GitHub). Ele já está listado no .dockerignore e deve ser adicionado ao .gitignore do seu repositório principal.

3. Gerar requirements.txt
Certifique-se de que seu ambiente virtual Python (venv) está ativado e que todas as dependências do projeto estão instaladas. Em seguida, gere o arquivo requirements.txt:

# Crie um ambiente virtual (se ainda não tiver)
python -m venv venv

# Ative seu ambiente virtual
# No Windows: .\venv\Scripts\activate
# No macOS/Linux: source venv/bin/activate

# Instale as dependências
pip install fastapi uvicorn python-dotenv twilio langchain-google-genai google-generativeai langchain-core

# Gere o requirements.txt
pip freeze > requirements.txt

4. Construir a Imagem Docker
Com o Docker Desktop rodando, navegue até o diretório chatbot_farmacia no seu terminal e construa a imagem Docker:

docker build -t chatbot-farmacia .

Este processo pode levar alguns minutos na primeira vez, pois o Docker baixará a imagem base do Python e instalará todas as dependências.

5. Rodar o Contêiner Docker Localmente
Após a construção bem-sucedida da imagem, execute o contêiner. O parâmetro -p 8000:8000 mapeia a porta 8000 do contêiner para a porta 8000 do seu computador, permitindo o acesso local.

docker run -p 8000:8000 --env-file .env chatbot-farmacia

Deixe este terminal aberto e rodando. Seu chatbot estará acessível localmente em http://localhost:8000.

6. Expor seu Localhost para o Twilio com ngrok
O Twilio precisa de uma URL pública para enviar as mensagens recebidas. Use o ngrok para criar um túnel para seu servidor local.

Abra um novo terminal (separado do Docker) e inicie o ngrok:

ngrok http 8000

O ngrok fornecerá uma URL HTTPS temporária (ex: https://SEU_SUBDOMINIO.ngrok-free.app). Copie esta URL.

7. Configurar o Webhook do Twilio Sandbox
Acesse o Console do Twilio.

Navegue até "Develop" -> "Messaging" -> "Try it out" -> "WhatsApp Sandbox".

Na seção "Sandbox Configuration", no campo "When a message comes in" (Endpoint URL), cole a URL HTTPS do ngrok que você copiou, seguida por /webhook.

Exemplo: https://SEU_SUBDOMINIO.ngrok-free.app/webhook

Certifique-se de que o Método esteja definido como POST.

Clique em "Save".

Agora, você pode enviar mensagens para o seu número da Sandbox do Twilio no WhatsApp e interagir com o chatbot!

☁️ Implantação em Produção (Render.com)
Para que seu chatbot funcione 24/7 sem a necessidade do seu computador local, você pode implantá-lo no Render.com.

Crie uma conta no Render.com e conecte-a ao seu repositório Git (GitHub, GitLab, Bitbucket).

No painel do Render, clique em "New" e selecione "Web Service".

Escolha o repositório do seu chatbot.

Configure os detalhes do serviço:

Name: chatbot-farmacia (ou o nome que preferir).

Region: Escolha uma região próxima aos seus usuários.

Branch: main (ou sua branch de deploy).

Root Directory: Se seu Dockerfile e código estiverem em um subdiretório (ex: chatbot_farmacia), especifique-o aqui.

Runtime: Selecione "Docker".

Build Command: Deixe em branco (o Render usará seu Dockerfile).

Start Command: uvicorn main:app --host 0.0.0.0 --port 8000

Plan Type: Escolha um plano (Free ou Starter para começar).

Adicione as Variáveis de Ambiente: Na seção "Environment Variables", adicione suas chaves de API:

GOOGLE_API_KEY

TWILIO_ACCOUNT_SID

TWILIO_AUTH_TOKEN

Clique em "Create Web Service". O Render construirá e implantará sua aplicação.

Após a implantação bem-sucedida, o Render fornecerá uma URL pública (ex: https://seu-chatbot.onrender.com).

Atualize o Endpoint URL no Twilio para esta nova URL do Render (ex: https://seu-chatbot.onrender.com/webhook).

⚠️ Considerações de Segurança
Variáveis de Ambiente: Nunca inclua suas chaves de API ou outras informações sensíveis diretamente no código-fonte ou no Dockerfile. Sempre use variáveis de ambiente, como demonstrado com o arquivo .env e a configuração no Render.

.gitignore: Certifique-se de que seu arquivo .gitignore na raiz do repositório inclua .env, __pycache__/, e venv/ para evitar que esses arquivos sejam versionados.

🤝 Contribuição
Contribuições são muito bem-vindas! Se você tiver sugestões, melhorias ou encontrar algum bug, sinta-se à vontade para abrir uma issue ou enviar um Pull Request.

📄 Licença
Este projeto está licenciado sob a Licença MIT.
