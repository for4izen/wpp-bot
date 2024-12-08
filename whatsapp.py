from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# URL da sua API personalizada para envio de mensagens
WHATSAPP_API_URL = "/message/sendList/teste"
HEADERS = {
    "apikey": "dddddd5",
    "Content-Type": "application/json"
}


def send_whatsapp_message(number, message_text):
    """
    Função para enviar mensagens no WhatsApp automaticamente.
    """
    payload = {
        "number": number,
        "title": "Resposta Automática",
        "description": "Mensagem enviada automaticamente",
        "buttonText": "Clique Aqui",
        "footerText": "Resposta do seu bot",
        "sections": [
            {
                "title": "Resposta do Bot",
                "rows": [
                    {
                        "title": "Obter mais informações",
                        "description": "Clique aqui para saber mais",
                        "rowId": "more_info"
                    }
                ]
            }
        ],
        "delay": 100,
        "quoted": {
            "key": {
                "remoteJid": f"{number}@s.whatsapp.com",
                "fromMe": False,
                "id": "12345678",
                "participant": f"{number}@s.whatsapp.com"
            },
            "message": {"conversation": message_text}
        }
    }

    try:
        # Enviar mensagem para o WhatsApp
        response = requests.post(WHATSAPP_API_URL, json=payload, headers=HEADERS)
        if response.status_code == 200:
            print(f"Mensagem enviada com sucesso para {number}")
        else:
            print(f"Erro ao enviar mensagem: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")


@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Ponto de entrada para processar mensagens recebidas.
    Captura as mensagens enviadas pelo usuário e responde com base nelas.
    """
    try:
        # Captura os dados da mensagem recebida
        data = request.json
        print(f"Mensagem recebida: {data}")

        # Validar dados da mensagem recebida
        if 'number' in data and 'text' in data:
            user_number = data['number']  # Número do usuário que enviou a mensagem
            user_message = data['text']  # Conteúdo da mensagem enviada pelo usuário

            # Lógica de resposta com base no conteúdo da mensagem
            if "olá" in user_message.lower():
                response_text = "Olá! Como posso ajudar você hoje?"
            elif "ajuda" in user_message.lower():
                response_text = "Claro! Informe como posso ajudar com sua solicitação."
            elif "pedido" in user_message.lower():
                response_text = "Seu pedido está sendo processado. Aguarde um momento!"
            else:
                response_text = "Desculpe, não entendi sua mensagem. Por favor, tente novamente."

            # Enviar resposta automática ao usuário
            send_whatsapp_message(user_number, response_text)

            # Retornar sucesso ao servidor
            return jsonify({"status": "Mensagem processada com sucesso"}), 200

        # Caso os dados esperados não sejam encontrados
        return jsonify({"status": "Dados inválidos"}), 400
    except Exception as e:
        print(f"Erro no processamento da mensagem: {e}")
        return jsonify({"status": "Erro interno do servidor"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
