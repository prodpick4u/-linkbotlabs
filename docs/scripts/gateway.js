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
const retryBtn = document.getElementById('retryBtn');
const errorBox = document.getElementById('errorBox');
const responseBox = document.getElementById('responseBox');
const dalleBox = document.getElementById('dalleBox');

const defaultModel = 'gpt-4o-mini'; // Fallback model

// ---- Error Display Function ----
function displayError(message) {
    errorBox.innerHTML += `<p>${new Date().toLocaleTimeString()}: ${message}</p>`;
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

// ---- Text Generation ----
async function askAI(prompt, retry = false) {
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
    let model = retry ? defaultModel : (modelSelect.value || 'gpt-5-nano');
    try {
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
        if (!fullText && !retry) {
            p.innerHTML = `Error: No response from ${model}. Retrying with ${defaultModel}.`;
            p.className = 'error';
            displayError(`No response from ${model}. Retrying with ${defaultModel}.`);
            sendBtn.disabled = false;
            sendBtn.classList.remove('loading');
            return askAI(prompt, true); // Retry with default model
        } else if (!fullText) {
            p.innerHTML = `Error: No response from ${model}.`;
            p.className = 'error';
            displayError(`No response from ${model}.`);
        }
    } catch (e) {
        if (!retry) {
            p.innerHTML = `Error: ${model} failed. Retrying with ${defaultModel}.`;
            p.className = 'error';
            displayError(`${model} failed: ${e.message}. Retrying with ${defaultModel}.`);
            sendBtn.disabled = false;
            sendBtn.classList.remove('loading');
            return askAI(prompt, true); // Retry with default model
        } else {
            displayError(`Retry with ${model} failed: ${e.message}`);
            p.innerHTML = `Error: Failed to respond - ${e.message}`;
            p.className = 'error';
        }
    }
    responseBox.setAttribute('aria-busy', 'false');
    responseBox.scrollTop = responseBox.scrollHeight;
    sendBtn.disabled = false;
    sendBtn.classList.remove('loading');
}

// ---- Message History ----
async function askWithMessages(messages, retry = false) {
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
    let model = retry ? defaultModel : (modelSelect.value || 'gpt-5-nano');
    try {
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
        if (!fullText && !retry) {
            p.innerHTML = `Error: No response from ${model}. Retrying with ${defaultModel}.`;
            p.className = 'error';
            displayError(`No response from ${model}. Retrying with ${defaultModel}.`);
            sendMessagesBtn.disabled = false;
            sendMessagesBtn.classList.remove('loading');
            return askWithMessages(messages, true); // Retry with default model
        } else if (!fullText) {
            p.innerHTML = `Error: No response from ${model}.`;
            p.className = 'error';
            displayError(`No response from ${model}.`);
        }
    } catch (e) {
        if (!retry) {
            p.innerHTML = `Error: ${model} failed. Retrying with ${defaultModel}.`;
            p.className = 'error';
            displayError(`${model} failed: ${e.message}. Retrying with ${defaultModel}.`);
            sendMessagesBtn.disabled = false;
            sendMessagesBtn.classList.remove('loading');
            return askWithMessages(messages, true); // Retry with default model
        } else {
            displayError(`Retry with ${model} failed: ${e.message}`);
            p.innerHTML = `Error: Failed to respond - ${e.message}`;
            p.className = 'error';
        }
    }
    responseBox.setAttribute('aria-busy', 'false');
    responseBox.scrollTop = responseBox.scrollHeight;
    sendMessagesBtn.disabled = false;
    sendMessagesBtn.classList.remove('loading');
}

// ---- Image Analysis ----
async function analyzeImage(prompt, imageURL, retry = false) {
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
    let model = retry ? defaultModel : (modelSelect.value || 'gpt-5-nano');
    try {
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
        if (!fullText && !retry) {
            p.innerHTML = `Error: No response from ${model} for image analysis. Retrying with ${defaultModel}.`;
            p.className = 'error';
            displayError(`No response from ${model} for image analysis. Retrying with ${defaultModel}.`);
            analyzeImgBtn.disabled = false;
            analyzeImgBtn.classList.remove('loading');
            return analyzeImage(prompt, imageURL, true); // Retry with default model
        } else if (!fullText) {
            p.innerHTML = `Error: No response from ${model}.`;
            p.className = 'error';
            displayError(`No response from ${model} for image analysis.`);
        }
    } catch (e) {
        if (!retry) {
            p.innerHTML = `Error: ${model} failed. Retrying with ${defaultModel}.`;
            p.className = 'error';
            displayError(`${model} failed: ${e.message}. Retrying with ${defaultModel}.`);
            analyzeImgBtn.disabled = false;
            analyzeImgBtn.classList.remove('loading');
            return analyzeImage(prompt, imageURL, true); // Retry with default model
        } else {
            displayError(`Retry with ${model} failed: ${e.message}`);
            p.innerHTML = `Error: Failed to analyze image - ${e.message}`;
            p.className = 'error';
        }
    }
    responseBox.setAttribute('aria-busy', 'false');
    responseBox.scrollTop = responseBox.scrollHeight;
    analyzeImgBtn.disabled = false;
    analyzeImgBtn.classList.remove('loading');
}

// ---- Image Generation ----
async function generateImages(prompt, retry = false) {
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
        if (!retry) {
            displayError(`DALL-E failed: ${e.message}. Retrying.`);
            const p = document.createElement('p');
            p.innerHTML = `Error: Failed to generate image - ${e.message}. Retrying.`;
            p.className = 'error';
            dalleBox.appendChild(p);
            generateImgBtn.disabled = false;
            generateImgBtn.classList.remove('loading');
            return generateImages(prompt, true); // Retry once
        } else {
            displayError(`Retry DALL-E failed: ${e.message}`);
            const p = document.createElement('p');
            p.innerHTML = `Error: Failed to generate image - ${e.message}`;
            p.className = 'error';
            dalleBox.appendChild(p);
        }
    }
    dalleBox.setAttribute('aria-busy', 'false');
    dalleBox.scrollTop = dalleBox.scrollHeight;
    generateImgBtn.disabled = false;
    generateImgBtn.classList.remove('loading');
}

// ---- Retry Mechanism ----
async function retryLastAction() {
    errorBox.innerHTML = '';
    errorBox.classList.remove('active');
    modelSelect.value = defaultModel; // Reset to fallback model
    const lastPrompt = localStorage.getItem('lastPrompt');
    const lastMessages = localStorage.getItem('lastMessages');
    const lastImagePrompt = localStorage.getItem('lastImagePrompt');
    const lastImageURL = localStorage.getItem('lastImageURL');
    if (lastPrompt) {
        chatInput.value = lastPrompt;
        return askAI(lastPrompt, true);
    } else if (lastMessages) {
        messagesInput.value = lastMessages;
        try {
            const messages = JSON.parse(lastMessages);
            return askWithMessages(messages, true);
        } catch (e) {
            displayError('Invalid JSON for retry.');
        }
    } else if (lastImagePrompt && lastImageURL) {
        chatInput.value = lastImagePrompt;
        imageInput.value = lastImageURL;
        return analyzeImage(lastImagePrompt, lastImageURL, true);
    } else if (lastImagePrompt) {
        dalleInput.value = lastImagePrompt;
        return generateImages(lastImagePrompt, true);
    } else {
        displayError('No previous action to retry.');
    }
}

// ---- Event Listeners ----
sendBtn.addEventListener('click', () => {
    errorBox.innerHTML = '';
    errorBox.classList.remove('active');
    localStorage.setItem('lastPrompt', chatInput.value);
    localStorage.removeItem('lastMessages');
    localStorage.removeItem('lastImagePrompt');
    localStorage.removeItem('lastImageURL');
    askAI(chatInput.value);
    chatInput.value = '';
});
chatInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        errorBox.innerHTML = '';
        errorBox.classList.remove('active');
        localStorage.setItem('lastPrompt', chatInput.value);
        localStorage.removeItem('lastMessages');
        localStorage.removeItem('lastImagePrompt');
        localStorage.removeItem('lastImageURL');
        askAI(chatInput.value);
        chatInput.value = '';
    }
});

sendMessagesBtn.addEventListener('click', () => {
    errorBox.innerHTML = '';
    errorBox.classList.remove('active');
    try {
        const messages = JSON.parse(messagesInput.value);
        localStorage.setItem('lastMessages', messagesInput.value);
        localStorage.removeItem('lastPrompt');
        localStorage.removeItem('lastImagePrompt');
        localStorage.removeItem('lastImageURL');
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
            localStorage.setItem('lastMessages', messagesInput.value);
            localStorage.removeItem('lastPrompt');
            localStorage.removeItem('lastImagePrompt');
            localStorage.removeItem('lastImageURL');
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
    localStorage.setItem('lastImagePrompt', chatInput.value);
    localStorage.setItem('lastImageURL', imageInput.value);
    localStorage.removeItem('lastPrompt');
    localStorage.removeItem('lastMessages');
    analyzeImage(chatInput.value, imageInput.value);
    chatInput.value = '';
    imageInput.value = '';
});
imageInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        errorBox.innerHTML = '';
        errorBox.classList.remove('active');
        localStorage.setItem('lastImagePrompt', chatInput.value);
        localStorage.setItem('lastImageURL', imageInput.value);
        localStorage.removeItem('lastPrompt');
        localStorage.removeItem('lastMessages');
        analyzeImage(chatInput.value, imageInput.value);
        chatInput.value = '';
        imageInput.value = '';
    }
});

generateImgBtn.addEventListener('click', () => {
    errorBox.innerHTML = '';
    errorBox.classList.remove('active');
    localStorage.setItem('lastImagePrompt', dalleInput.value);
    localStorage.removeItem('lastPrompt');
    localStorage.removeItem('lastMessages');
    localStorage.removeItem('lastImageURL');
    generateImages(dalleInput.value);
    dalleInput.value = '';
});
dalleInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        errorBox.innerHTML = '';
        errorBox.classList.remove('active');
        localStorage.setItem('lastImagePrompt', dalleInput.value);
        localStorage.removeItem('lastPrompt');
        localStorage.removeItem('lastMessages');
        localStorage.removeItem('lastImageURL');
        generateImages(dalleInput.value);
        dalleInput.value = '';
    }
});

retryBtn.addEventListener('click', () => {
    retryLastAction();
});

// ---- Initial Check for Puter.js ----
if (!window.puter || !window.puter.ai) {
    displayError('Puter.js failed to load on page load. Check network or script URL: https://js.puter.com/v2/');
}
