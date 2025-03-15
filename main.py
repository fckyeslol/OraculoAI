import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template

# Cargar variables de entorno
load_dotenv()

# Configuración de la API de OpenRouter
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")  

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Función para analizar los sueños
def analizar_sueño(descripcion_sueño):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",  
        "messages": [
            {"role": "system", "content": "Eres un oráculo moderno que interpreta sueños."},
            {"role": "user", "content": f"Interpreta este sueño: {descripcion_sueño}"}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status() 
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de OpenRouter: {e}")
        return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)  # Esto permite que el servidor sea accesible