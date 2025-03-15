
async function processFears() {
    const fearsInput = document.getElementById('userFears');
    const responseDiv = document.getElementById('response');
    const fears = fearsInput.value.trim();

    if (!fears) {
        alert('Por favor, describe tus miedos primero.');
        return;
    }

    responseDiv.innerHTML = 'El oráculo está analizando tus miedos...';
    responseDiv.classList.remove('hidden');

    try {
        const response = await fetch('/analizar-miedos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ miedos: fears })
        });

        if (!response.ok) {
            throw new Error('Error en la comunicación con el oráculo');
        }

        const data = await response.json();
        responseDiv.innerHTML = `
            <h3>El oráculo responde:</h3>
            <p>${data.respuesta}</p>
        `;
    } catch (error) {
        responseDiv.innerHTML = 'El oráculo no puede responder en este momento. Inténtalo más tarde.';
        console.error('Error:', error);
    }
}

// Permitir envío con Enter en el textarea
document.getElementById('userFears')?.addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        processFears();
    }
});
