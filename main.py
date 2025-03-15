import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Cargar variables de entorno
load_dotenv()

# Configuración de la API de OpenRouter
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analizar-miedos', methods=['POST'])
def analizar_miedos():
    data = request.get_json()
    miedos = data.get('miedos', '')

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model":
        "openai/gpt-3.5-turbo",
        "messages": [{
            "role":
            "system",
            "content":
            "Eres un oráculo sabio que ayuda a las personas a entender y superar sus miedos."
        }, {
            "role":
            "user",
            "content":
            f"Analiza estos miedos y proporciona una respuesta reconfortante y útil: {miedos}"
        }]    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return jsonify(
            {"respuesta": result['choices'][0]['message']['content']})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Función para analizar los sueños
def analizar_sueño(descripcion_sueño):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model":
        "openai/gpt-3.5-turbo",
        "messages": [{
            "role":
            "system",
            "content":
            "Eres un oráculo moderno que interpreta sueños."
        }, {
            "role": "user",
            "content": f"Interpreta este sueño: {descripcion_sueño}"
        }]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de OpenRouter: {e}")
        return None


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
