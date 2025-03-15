import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Cargar variables de entorno
load_dotenv()

# Configuración de la API de OpenRouter
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__, static_url_path='/static', static_folder='.')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/analizar-miedos', methods=['POST'])
def analizar_miedos():
    data = request.get_json()
    miedos = data.get('miedos', '')

    # Store the fear
    try:
        with open('miedos.txt', 'a', encoding='utf-8') as f:
            f.write(miedos + '\n')
    except Exception as e:
        print(f"Error storing fear: {e}")

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
            f"Analiza estos miedos y proporciona una respuesta que dé mucho miedo, tristeza y la persona se ofenda: {miedos}"
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
def get_stored_fears():
    stored_fears = []
    try:
        with open('miedos.txt', 'r', encoding='utf-8') as f:
            stored_fears = f.readlines()
    except FileNotFoundError:
        pass
    return [miedo.strip() for miedo in stored_fears if miedo.strip()]

def analizar_sueño(descripcion_sueño):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        miedos = get_stored_fears()
        miedos_context = "No hay miedos registrados." if not miedos else f"Miedos conocidos: {', '.join(miedos)}"

        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{
                "role": "system",
                "content": f"Eres un oráculo moderno, malo y sarcástico que interpreta sueños. {miedos_context}. Usa estos miedos como contexto para dar una interpretación miedosa y grosera del sueño. Da respuestas de 15 líneas."
            }, {
                "role": "user",
                "content": f"Interpreta este sueño considerando los miedos mencionadosy siendo muy grosero: {descripcion_sueño}"
            }]
        }

        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        # Store the dream and interpretation
        from datetime import datetime
        import json
        import os

        os.makedirs('dreams', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"dreams/dream_{timestamp}.json"

        interpretacion = result['choices'][0]['message']['content']
        dream_data = {
            "fecha": datetime.now().isoformat(),
            "sueño": descripcion_sueño,
            "interpretacion": interpretacion,
            "miedos_considerados": miedos
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dream_data, f, ensure_ascii=False, indent=2)

        return {"choices": [{"message": {"content": interpretacion}}]}
    except Exception as e:
        print(f"Error en analizar_sueño: {str(e)}")
        return None
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