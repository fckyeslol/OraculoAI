async function enviarMiedos(miedos) {
  try {
      const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json'
          },
          body: JSON.stringify({ miedos: miedos })
      });

      if (!response.ok) {
          throw new Error('Error al enviar los miedos: ' + response.statusText);
      }

      const data = await response.json();
      console.log('Respuesta de la API:', data);
  } catch (error) {
      console.error('Se produjo un error:', error);
  }
}

// Ejemplo de uso
const miedos = ['miedo a la oscuridad', 'miedo a las alturas']; // Sustituye con tus datos
enviarMiedos(miedos);