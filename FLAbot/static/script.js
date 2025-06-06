let fsaData = null;

function processImage() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    if (!file) {
        alert("Please select an image file.");
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    fetch('/process_image', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                document.getElementById('error').innerText = data.error;
            } else {
                fsaData = data.fsa_data;
                document.getElementById('chat').innerHTML = '';
                document.getElementById('error').innerText = '';

                // Speak welcome message
                const welcomeMessage = new SpeechSynthesisUtterance(
                    "Welcome to the FSA Chatbot! Ask me about the FSA or its concepts! " +
                    "Press Tab on your keyboard to start typing your question or Press S to speak."
                );
                window.speechSynthesis.speak(welcomeMessage);

                // Add visual confirmation
                const chat = document.getElementById('chat');
                chat.innerHTML += `<p><strong>System:</strong> FSA image processed successfully!</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('error').innerText = "An error occurred while processing the image.";
        });
}

function askQuestion(useVoice) {
    if (!fsaData) {
        document.getElementById('error').innerText = "Please upload and process an FSA image first.";
        return;
    }

    const questionInput = document.getElementById('question');
    const chat = document.getElementById('chat');

    // Clear any previous error
    document.getElementById('error').innerText = '';

    if (useVoice) {
        questionInput.value = "Listening...";
        questionInput.disabled = true;
    } else {
        const question = questionInput.value.trim();
        if (!question) {
            document.getElementById('error').innerText = "Please enter a question.";
            return;
        }
    }

    // Disable buttons during processing
    document.getElementById('askBtn').disabled = true;
    document.getElementById('micBtn').disabled = true;

    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            question: useVoice ? null : questionInput.value.trim(),
            fsa_data: fsaData,
            voice_input: useVoice
        })
    })
        .then(response => response.json())
        .then(data => {
            questionInput.disabled = false;
            document.getElementById('askBtn').disabled = false;
            document.getElementById('micBtn').disabled = false;

            if (data.error) {
                document.getElementById('error').innerText = data.error;
            } else {
                // Display the conversation
                if (data.question) {
                    chat.innerHTML += `<p><strong>You:</strong> ${data.question}</p>`;
                } else if (!useVoice) {
                    chat.innerHTML += `<p><strong>You:</strong> ${questionInput.value}</p>`;
                }

                chat.innerHTML += `<p><strong>Chatbot:</strong> ${data.response}</p>`;

                // Clear and unfocus the input
                questionInput.value = '';
                questionInput.blur();
                chat.scrollTop = chat.scrollHeight;

                // Speak the response once
                if (window.speechSynthesis) {
                    window.speechSynthesis.cancel(); // Cancel any pending
                    const utterance = new SpeechSynthesisUtterance(data.response);
                    window.speechSynthesis.speak(utterance);
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            questionInput.disabled = false;
            document.getElementById('askBtn').disabled = false;
            document.getElementById('micBtn').disabled = false;
            document.getElementById('error').innerText = "An error occurred while asking the question.";
            questionInput.blur();
        });
}

// Helper functions
function showError(message) {
    document.getElementById('error').innerText = message;
}

function clearError() {
    document.getElementById('error').innerText = '';
}

function setControlsDisabled(disabled) {
    document.getElementById('askBtn').disabled = disabled;
    document.getElementById('micBtn').disabled = disabled;
    document.getElementById('question').disabled = disabled;
}

function addToChat(question, response) {
    const chat = document.getElementById('chat');
    if (question) {
        chat.innerHTML += `<p><strong>You:</strong> ${question}</p>`;
    }
    chat.innerHTML += `<p><strong>Chatbot:</strong> ${response}</p>`;
    chat.scrollTop = chat.scrollHeight;

    // Speak the response
    if (window.speechSynthesis) {
        const utterance = new SpeechSynthesisUtterance(response);
        window.speechSynthesis.speak(utterance);
    }
}


document.addEventListener('keydown', function (e) {
    const questionInput = document.getElementById('question');

    // Only handle 'S' key when input isn't focused and not during voice input
    if ((e.key === 's' || e.key === 'S') &&
        document.activeElement !== questionInput &&
        !questionInput.disabled) {
        e.preventDefault();
        askQuestion(true);
    }

    // Tab key handling remains the same
    if (e.key === 'Tab' && document.activeElement !== questionInput) {
        e.preventDefault();
        questionInput.focus();
    }
});

document.getElementById('question').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        askQuestion(false);
    }
});  