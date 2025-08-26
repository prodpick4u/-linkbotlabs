const synth = window.speechSynthesis;
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const messagesInput = document.getElementById('messagesInput');
const sendMessagesBtn = document.getElementById('sendMessagesBtn');
const imageInput = document.getElementById('imageInput');
const analyzeImgBtn = document.getElementById('analyzeImgBtn');
const dalleInput = document.getElementById('dalleInput');
const generateImgBtn = document.getElementById('generateImgBtn');
const voiceSelect = document.getElementById('voiceSelect');
const modelSelect = document.getElementById('modelSelect');
const errorBox = document.getElementById('errorBox');
const responseBox = document.getElementById('responseBox');
const dalleBox = document.getElementById('dalleBox');

// ---- Error Display Function ----
function displayError(message) {
    errorBox.innerHTML += `<p>${message}</p>`;
    errorBox.classList.add('active');
    errorBox.scrollTop = errorBox.scrollHeight;
    console.error(message);
}

// ---- Voice Selector ----
function populateVoiceSelect() {
    let voices = synth.getVoices();
    if (!voices.length) {
        setTimeout(populateVoiceSelect, 100);
        return;
    }
    voices = voices.filter(v => v.lang.startsWith('en')).sort((a, b) => a.name.localeCompare(b.name));
    voiceSelect.innerHTML = '<option value="">Select Voice</option>';
    voices.forEach(v => {
        const opt = document.createElement('option');
        opt.value = v.name;
        opt.textContent = `${v.name} (${v.lang})`;
        voiceSelect.appendChild(opt);
    });
}
if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = populateVoiceSelect;
} else {
    populateVoiceSelect();
}

// ---- TTS with Queue ----
let ttsQueue = [];
let isSpeaking = false;

function playTTS(text) {
    if (!text) return;
    ttsQueue.push(text);
    processTTSQueue();
}

function processTTSQueue() {
    if (isSpeaking || !ttsQueue.length) return;
    isSpeaking = true;
    const text = ttsQueue.shift();
    const utter = new SpeechSynthesisUtterance(text);
    const selectedVoice = voiceSelect.value;
    if (selectedVoice) {
        const voice = synth.getVoices().find(v => v.name === selectedVoice);
        if (voice) utter.voice = voice;
    }
    utter.onend = () => {
        isSpeaking = false;
        processTTSQueue();
    };
    synth.speak(utter);
}

// ---- Text Generation (Example 1 & 4) ----
async function askAI(prompt) {
    if (!prompt) {
        displayError('Please enter a question.');
        const p = document.createElement('p');
        p.innerHTML = 'Error: Please enter a question.';
        p.className = 'error';
        responseBox.appendChild(p);
        responseBox.scrollTop = responseBox.scrollHeight;
        return;
    }
    if (!window.puter || !window.puter.ai) {
        displayError('Puter.js failed to load. Check network or script URL: https://js.puter.com/v2/');
        const p = document.createElement('p');
        p.innerHTML = 'Error: Puter.js failed to load.';
        p.className = 'error';
        responseBox.appendChild(p);
        responseBox.scrollTop = responseBox.scrollHeight;
        return;
    }
    sendBtn.disabled = true;
    sendBtn.classList.add('loading');
    responseBox.setAttribute('aria-busy', 'true');
    const p = document.createElement('p');
    p.className = 'response';
    responseBox.appendChild(p);
    try {
        const model = modelSelect.value || 'gpt-5-nano';
        const stream = await puter.ai.chat(prompt, { model, stream: true });
        let fullText = '';
        for await (const part of stream) {
            if (part?.text) {
                fullText += part.text;
                p.innerHTML = fullText.replace(/\n/g, '<br>');
                responseBox.scrollTop = responseBox.scrollHeight;
                playTTS(part.text);
            }
        }
        if (!fullText) {
            p.innerHTML = `Error: No response from ${model}.`;
            p.className = 'error';
            displayError(`No response from ${model}.`);
        }
    } catch (e) {
        displayError(`Text generation failed: ${e.message}`);
        p.innerHTML = `Error: Failed to respond - ${e.message}`;
        p.className = 'error';
    }
    responseBox.setAttribute('aria-busy', 'false');
    responseBox.scrollTop = responseBox.scrollHeight;
    sendBtn.disabled = false;
    sendBtn.classList.remove('loading');
}

// ---- Message History (Example 4 with messages) ----
async function askWithMessages(messages) {
    if (!messages || !Array.isArray(messages)) {
        displayError('Invalid message history. Please enter valid JSON array.');
        const p = document.createElement('p');
        p.innerHTML = 'Error: Invalid JSON format for messages.';
        p.className = 'error';
        responseBox.appendChild(p);
        responseBox.scrollTop = responseBox.scrollHeight;
        return;
    }
    if (!window.puter || !window.puter.ai) {
        displayError('Puter.js failed to load. Check network or script URL: https://js.puter.com/v2/');
        const p = document.createElement('p');
        p.innerHTML = 'Error: Puter.js failed to load.';
        p.className = 'error';
        responseBox.appendChild(p);
        responseBox.scrollTop = responseBox.scrollHeight;
        return;
    }
    sendMessagesBtn.disabled = true;
    sendMessagesBtn.classList.add('loading');
    responseBox.setAttribute('aria-busy', 'true');
    const p = document.createElement('p');
    p.className = 'response';
    responseBox.appendChild(p);
    try {
        const model = modelSelect.value || 'gpt-5-nano';
        const stream = await puter.ai.chat(messages, false, { model, stream: true });
        let fullText = '';
        for await (const part of stream) {
            if (part?.text) {
                fullText += part.text;
                p.innerHTML = fullText.replace(/\n/g, '<br>');
                responseBox.scrollTop = responseBox.scrollHeight;
                playTTS(part.text);
            }
        }
        if (!fullText) {
            p.innerHTML = `Error: No response from ${model}.`;
            p.className = 'error';
            displayError(`No response from ${model}.`);
        }
    } catch (e) {
        displayError(`Message history failed: ${e.message}`);
        p.innerHTML = `Error: Failed to respond - ${e.message}`;
        p.className = 'error';
    }
    responseBox.setAttribute('aria-busy', 'false');
    responseBox.scrollTop = responseBox.scrollHeight;
    sendMessagesBtn.disabled = false;
    sendMessagesBtn.classList.remove('loading');
}

// ---- Image Analysis (Example 3) ----
async function analyzeImage(prompt, imageURL) {
    if (!prompt || !imageURL) {
        displayError('Please enter both a question and an image URL.');
        const p = document.createElement('p');
        p.innerHTML = 'Error: Please enter both a question and an image URL.';
        p.className = 'error';
        responseBox.appendChild(p);
        responseBox.scrollTop = responseBox.scrollHeight;
        return;
    }
    if (!window.puter || !window.puter.ai) {
        displayError('Puter.js failed to load. Check network or script URL: https://js.puter.com/v2/');
        const p = document.createElement('p');
        p.innerHTML = 'Error: Puter.js failed to load.';
        p.className = 'error';
        responseBox.appendChild(p);
        responseBox.scrollTop = responseBox.scrollHeight;
        return;
    }
    analyzeImgBtn.disabled = true;
    analyzeImgBtn.classList.add('loading');
    responseBox.setAttribute('aria-busy', 'true');
    const p = document.createElement('p');
    p.className = 'response';
    responseBox.appendChild(p);
    try {
        const model = modelSelect.value || 'gpt-5-nano';
        const stream = await puter.ai.chat(prompt, imageURL, false, { model, stream: true });
        let fullText = '';
        for await (const part of stream) {
            if (part?.text) {
                fullText += part.text;
                p.innerHTML = fullText.replace(/\n/g, '<br>');
                responseBox.scrollTop = responseBox.scrollHeight;
                playTTS(part.text);
            }
        }
        if (!fullText) {
            p.innerHTML = `Error: No response from ${model} for image analysis.`;
            p.className = 'error';
            displayError(`No response from ${model} for image analysis.`);
        }
    } catch (e) {
        displayError(`Image analysis failed: ${e.message}`);
        p.innerHTML = `Error: Failed to analyze image - ${e.message}`;
        p.className = 'error';
    }
    responseBox.setAttribute('aria-busy', 'false');
    responseBox.scrollTop = responseBox.scrollHeight;
    analyzeImgBtn.disabled = false;
    analyzeImgBtn.classList.remove('loading');
}

// ---- Image Generation (Example 2) ----
async function generateImages(prompt) {
    if (!prompt) {
        displayError('Please enter an image prompt.');
        const p = document.createElement('p');
        p.innerHTML = 'Error: Please enter an image prompt.';
        p.className = 'error';
        dalleBox.appendChild(p);
        dalleBox.scrollTop = dalleBox.scrollHeight;
        return;
    }
    if (!window.puter || !window.puter.ai) {
        displayError('Puter.js failed to load. Check network or script URL: https://js.puter.com/v2/');
        const p = document.createElement('p');
        p.innerHTML = 'Error: Puter.js failed to load.';
        p.className = 'error';
        dalleBox.appendChild(p);
        dalleBox.scrollTop = dalleBox.scrollHeight;
        return;
    }
    generateImgBtn.disabled = true;
    generateImgBtn.classList.add('loading');
    dalleBox.setAttribute('aria-busy', 'true');
    dalleBox.innerHTML = '<h3>DALL·E</h3><span class="loading">Processing...</span>';
    try {
        const img = await puter.ai.txt2img(prompt);
        dalleBox.appendChild(img);
    } catch (e) {
        displayError(`DALL-E failed: ${e.message}`);
        const p = document.createElement('p');
        p.innerHTML = `Error: Failed to generate image - ${e.message}`;
        p.className = 'error';
        dalleBox.appendChild(p);
    }
    dalleBox.setAttribute('aria-busy', 'false');
    dalleBox.scrollTop = dalleBox.scrollHeight;
    generateImgBtn.disabled = false;
    generateImgBtn.classList.remove('loading');
}

// ---- Event Listeners ----
sendBtn.addEventListener('click', () => {
    errorBox.innerHTML = '';
    errorBox.classList.remove('active');
    askAI(chatInput.value);
    chatInput.value = '';
});
chatInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        errorBox.innerHTML = '';
        errorBox.classList.remove('active');
        askAI(chatInput.value);
        chatInput.value = '';
    }
});

sendMessagesBtn.addEventListener('click', () => {
    errorBox.innerHTML = '';
    errorBox.classList.remove('active');
    try {
        const messages = JSON.parse(messagesInput.value);
        askWithMessages(messages);
        messagesInput.value = '';
    } catch (e) {
        displayError('Invalid JSON format for messages.');
        const p = document.createElement('p');
        p.innerHTML = 'Error: Invalid JSON format for messages.';
        p.className = 'error';
        responseBox.appendChild(p);
        responseBox.scrollTop = responseBox.scrollHeight;
    }
});
messagesInput.addEventListener('keypress', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
        errorBox.innerHTML = '';
        errorBox.classList.remove('active');
        try {
            const messages = JSON.parse(messagesInput.value);
            askWithMessages(messages);
            messagesInput.value = '';
        } catch (e) {
            displayError('Invalid JSON format for messages.');
            const p = document.createElement('p');
            p.innerHTML = 'Error: Invalid JSON format for messages.';
            p.className = 'error';
            responseBox.appendChild(p);
            responseBox.scrollTop = responseBox.scrollHeight;
        }
    }
});

analyzeImgBtn.addEventListener('click', () => {
    errorBox.innerHTML = '';
    errorBox.classList.remove('active');
    analyzeImage(chatInput.value, imageInput.value);
    chatInput.value = '';
    imageInput.value = '';
});
imageInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        errorBox.innerHTML = '';
        errorBox.classList.remove('active');
        analyzeImage(chatInput.value, imageInput.value);
        chatInput.value = '';
        imageInput.value = '';
    }
});

generateImgBtn.addEventListener('click', () => {
    errorBox.innerHTML = '';
    errorBox.classList.remove('active');
    generateImages(dalleInput.value);
    dalleInput.value = '';
});
dalleInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        errorBox.innerHTML = '';
        errorBox.classList.remove('active');
        generateImages(dalleInput.value);
        dalleInput.value = '';
    }
});

// ---- Initial Check for Puter.js ----
if (!window.puter || !window.puter.ai) {
    displayError('Puter.js failed to load on page load. Check network or script URL: https://js.puter.com/v2/');
}
