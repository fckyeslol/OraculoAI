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
            "Eres un oráculo malo, te gusta que la gente sufra con sus miedos."
        }, {
            "role":
            "user",
            "content":
            f"Analiza estos miedos y proporciona una respuesta que le de mucho miedo y tristeza: {miedos}"
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
        "model": "openai/gpt-3.5-turbo",
        "messages": [{
            "role": "system",
            "content": "Eres un oráculo moderno, grosero y sarcástico que interpreta sueños dando respuestas de 15 lineas." #modificar la IA
        }, {
            "role": "user",
            "content": f"Interpreta este sueño: {descripcion_sueño}"
        }]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        
        # Guardar el sueño y su interpretación
        from datetime import datetime
        import json
        import os
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dreams/dream_{timestamp}.json"
        
        dream_data = {
            "fecha": datetime.now().isoformat(),
            "sueño": descripcion_sueño,
            "interpretacion": result['choices'][0]['message']['content']
        }
        
        os.makedirs('dreams', exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dream_data, f, ensure_ascii=False, indent=2)
            
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API de OpenRouter: {e}")
        return None

@app.route('/analizar-sueno', methods=['POST'])
def procesar_sueno():
    data = request.get_json()
    sueno = data.get('sueno', '')
    
    if not sueno:
        return jsonify({"error": "No se proporcionó ningún sueño"}), 400
        
    resultado = analizar_sueño(sueno)
    if resultado:
        return jsonify({
            "respuesta": resultado['choices'][0]['message']['content']
        })
    return jsonify({"error": "Error al analizar el sueño"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
