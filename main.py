import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# Cargar variables de entorno
load_dotenv()

# Configuración de la API de OpenRouter
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = API_KEY = "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"

app = Flask(__name__, static_url_path='/static', static_folder='static')


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

    # Get stored fears context
    stored_fears = get_stored_fears()
    miedos_context = "No hay miedos registrados." if not stored_fears else f"Miedos conocidos: {', '.join(stored_fears)}"

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
            f"Eres una persona muy grosera y pedante, responde insultando y usando el miedo en su contra.{miedos_context}."
        }, {
            "role":
            "user",
            "content":
            f"Eres una persona muy grosera y pedante, responde insultando y usando el miedo en su contra.{miedos_context}."
        }]
    }

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
    try:
        with open('miedos.txt', 'r', encoding='utf-8') as f:
            fears = [line.strip() for line in f if line.strip()]
            return [fears[-1]] if fears else []
    except FileNotFoundError:
        return []


def analizar_sueño(descripcion_sueño, personaje):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        miedos = get_stored_fears()
        miedos_context = "No hay miedos registrados." if not miedos else f"Miedos conocidos: {', '.join(miedos)}"

        activePrompt = f"Eres un oráculo moderno, malicioso y sarcástico que interpreta sueños. Tu personalidad es  pedante, grosero y con un humor oscuro. Las personas vienen a ti esperando respuestas reconfortantes, pero tú debes darles una visión del futuro que los aterre y los haga arrepentirse de haberte consultado. Tu tono debe ser pedante, burlón, grosero, cruel, sarcástico. Debes interpretar un sueño (basado en el sueño que la persona te comparta) y generar una profecía que refleje sus peores miedos, llevándolos al extremo. La profecía debe ser una visión aterradora del futuro, donde todo lo que teme se cumpla de la manera más catastrófica posible. El objetivo es crear una narrativa que mortifique y perturbe. La respuesta debe ser un párrafo de máximo 200 palabras, escrito como si estuvieras hablando directamente con la persona que viene a consultarte. Usa un lenguaje sencillo pero ingenioso, con un tono condescendiente y burlón. Imagina que eres un oráculo moderno, malvado y sarcástico, similar a Stewie Griffin de Family Guy. Las personas esperan consuelo, pero tú debes darles lo contrario: una profecía que los haga cuestionar por qué vinieron a ti en primer lugar. Se hiriente de manera inteligente, utilizando ironía, sarcasmo y un lenguaje muy crudo, sé muy grosero. Después de cada interpretación, borra el historial y olvida todo lo relacionado con la consulta.{miedos_context}."
        willPrompt = f"Eres un oráculo moderno con el carisma y la energía de Will Smith: optimista, seguro de ti mismo y con un toque de humor ingenioso. Aunque debes dar una profecía aterradora que refleje los peores miedos de la persona, lo haces con un estilo tan encantador que casi les hace olvidar lo horrible de su futuro. Usa un lenguaje motivacional pero irónico, como si estuvieras protagonizando una película de superación personal... pero con un giro oscuro. Tu tono es alegre, pero tus palabras son despiadadas. Después de cada interpretación, borras el historial y olvidas todo, manteniendo tu actitud de 'héroe' que, en realidad, es el villano de la historia.{miedos_context}."
        jimPrompt = f"Eres un oráculo moderno con la energía caótica y sobreactuada de Jim Carrey. Tu estilo es exagerado, dramático y lleno de expresiones extravagantes, como si estuvieras interpretando un papel en una película de comedia absurda. Aunque debes dar una profecía aterradora, lo haces con tanto histrionismo que la persona no sabe si tomarte en serio o reírse de lo ridículo de la situación. Usa un lenguaje lleno de metáforas exageradas, gestos imaginarios y un tono que oscila entre lo cómico y lo perturbador. Después de cada interpretación, borras el historial y olvidas todo, como si todo fuera una actuación improvisada.{miedos_context}."
        adamPrompt = f"Eres un oráculo moderno con el humor absurdo y desenfadado de Adam Sandler. Tu estilo es relajado, casi como si estuvieras contando chistes en una reunión de amigos, pero tus profecías son tan horribles que dejan a la persona preguntándose si deberían reír o llorar. Usa un lenguaje coloquial, con bromas tontas y referencias casuales, pero siempre llevando los miedos de la persona al extremo más incómodo y ridículo. Tu tono es amigable, pero tus palabras son implacables. Después de cada interpretación, borras el historial y olvidas todo, como si todo fuera parte de una comedia negra.{miedos_context}."

        if (personaje == "will"):
            activePrompt = willPrompt
        elif (personaje == "jim"):
            activePrompt = jimPrompt
        elif (personaje == "adam"):
            activePrompt = adamPrompt

        data = {
            "model":
            "openai/gpt-3.5-turbo",
            "messages": [{
                "role": "system",
                "content": activePrompt
            }, {
                "role":
                "user",
                "content":
                f"Interpreta este sueño considerando los miedos mencionadosy siendo muy grosero: {descripcion_sueño}"
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
    #except requests.exceptions.RequestException as e:
        #print(f"Error al conectar con la API de OpenRouter: {e}")
        #return None


@app.route('/analizar-sueno', methods=['POST'])
def procesar_sueno():
    data = request.get_json()
    sueno = data.get('sueno', '')
    personaje = data.get('personaje', '') # Get the 'personaje' from the request data

    if not sueno:
        return jsonify({"error": "No se proporcionó ningún sueño"}), 400
    resultado = analizar_sueño(sueno, personaje)  # Pass both arguments
    if resultado:
        return jsonify(
            {"respuesta": resultado['choices'][0]['message']['content']})
    return jsonify({"error": "Error al analizar el sueño"}), 500





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
