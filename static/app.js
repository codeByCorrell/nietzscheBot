// static/app.js

// choose DOM elements
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const nietzscheOutput = document.getElementById('nietzsche-output');

// url of fast api endpoint
const API_ENDPOINT = '/api/nietzsche-chat'; 

// sends request of user to backend
async function sendMessage() {
    const message = userInput.value.trim();
    if (message === '') return;

    // ui feedback
    nietzscheOutput.textContent = '...Nietzsche thinks...';
    // deactivate button while waiting
    sendButton.disabled = true; 

    try {
        // send request to fast api backend
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            // send user message in json format as is expected from backend site
            body: JSON.stringify({ message: message }) 
        });

        const data = await response.json();

        // process and return answer
        if (response.ok && data.response) {
            nietzscheOutput.textContent = data.response;
        } else {
            // show error if necessary
            nietzscheOutput.textContent = `ERROR: ${data.error || 'Unexpected Server Error.'}`;
        }

    } catch (error) {
        // network error
        console.error('Network Error:', error);
        nietzscheOutput.textContent = 'FAILURE: Connection to server failed';
    } finally {
        // reactivate send button 
        sendButton.disabled = false; 
    }
}

// Event Listener for click of send button
sendButton.addEventListener('click', sendMessage);

// Event Listener for hitting enter key
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});