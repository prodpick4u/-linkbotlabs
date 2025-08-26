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

const aiBoxes = {
    'claude': document.getElementById('claudeBox'),
    'dalle': document.getElementById('dalleBox'),
    'gemini': document.getElementById('geminiBox'),
    'gpt-5': document.getElementById('gpt5Box'),
    'grok': document.getElementById('grokBox')
};

const models = {
    'claude': 'claude-3.5-sonnet',
    'gemini': 'gemini-2.0-flash',
    'gpt-5': 'gpt-5-nano',
    'grok': 'grok-beta'
};

// ---- Voice Selector ----
function populateVoiceSelect() {
    let voices = synth.getVoices();
    if (!voices.length) { setTimeout(populateVoiceSelect, 100); return; }
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

// ---- Multi-AI Chat with Prompt ----
async function askAI(prompt) {
    if (!prompt) {
        Object.values(aiBoxes).forEach(box => {
            const p = document.createElement('p');
            p.innerHTML = 'Error: Please enter a question.';
            p.className = 'error';
            box.appendChild(p);
            box.scrollTop = box.scrollHeight;
        });
        return;
    }
    if (!window.puter || !window.puter.ai) {
        Object.values(aiBoxes).forEach(box => {
            const p = document.createElement('p');
            p.innerHTML = 'Error: Puter.js failed to load. Check network or script URL.';
            p.className = 'error';
            box.appendChild(p);
            box.scrollTop = box.scrollHeight;
        });
        return;
    }
    sendBtn.disabled = true;
    sendBtn.classList.add('loading');
    const modelKeys = Object.keys(models).sort();
    for (const key of modelKeys) {
        const model = models[key];
        const box = aiBoxes[key];
        box.setAttribute('aria-busy', 'true');
        const p = document.createElement('p');
        p.className = 'response';
        box.appendChild(p);
        try {
            const stream = await puter.ai.chat(prompt, { model, stream: true });
            let fullText = '';
            for await (const part of stream) {
                if (part?.text) {
                    fullText += part.text;
                    p.innerHTML = fullText.replace(/\n/g, '<br>');
                    box.scrollTop = box.scrollHeight;
                    playTTS(part.text);
                }
            }
            if (!fullText) {
                p.innerHTML = `Error: No response from ${key}.`;
                p.className = 'error';
            }
        } catch (e) {
            console.warn(`${key} failed`, e);
            p.innerHTML = `Error: ${key} failed to respond - ${e.message}`;
            p.className = 'error';
        }
        box.setAttribute('aria-busy', 'false');
        box.scrollTop = box.scrollHeight;
    }
    sendBtn.disabled = false;
    sendBtn.classList.remove('loading');
}

// ---- Multi-AI Chat with Messages ----
async function askWithMessages(messages) {
    if (!messages) {
        Object.values(aiBoxes).forEach(box => {
            const p = document.createElement('p');
            p.innerHTML = 'Error: Please enter valid message history (JSON).';
            p.className = 'error';
            box.appendChild(p);
            box.scrollTop = box.scrollHeight;
        });
        return;
    }
    if (!window.puter || !window.puter.ai) {
        Object.values(aiBoxes).forEach(box => {
            const p = document.createElement('p');
            p.innerHTML = 'Error: Puter.js failed to load. Check network or script URL.';
            p.className = 'error';
            box.appendChild(p);
            box.scrollTop = box.scrollHeight;
        });
        return;
    }
    sendMessagesBtn.disabled = true;
    sendMessagesBtn.classList.add('loading');
    const modelKeys = Object.keys(models).sort();
    for (const key of modelKeys) {
        const model = models[key];
        const box = aiBoxes[key];
        box.setAttribute('aria-busy', 'true');
        const p = document.createElement('p');
        p.className = 'response';
        box.appendChild(p);
        try {
            const stream = await puter.ai.chat(messages, false, { model, stream: true });
            let fullText = '';
            for await (const part of stream) {
                if (part?.text) {
                    fullText += part.text;
                    p.innerHTML = fullText.replace(/\n/g, '<br>');
                    box.scrollTop = box.scrollHeight;
                    playTTS(part.text);
                }
            }
            if (!fullText) {
                p.innerHTML = `Error: No response from ${key}.`;
                p.className = 'error';
            }
        } catch (e) {
            console.warn(`${key} failed`, e);
            p.innerHTML = `Error: ${key} failed to respond - ${e.message}`;
            p.className = 'error';
        }
        box.setAttribute('aria-busy', 'false');
        box.scrollTop = box.scrollHeight;
    }
    sendMessagesBtn.disabled = false;
    sendMessagesBtn.classList.remove('loading');
}

// ---- Image Analysis (GPT-4 Vision) ----
async function analyzeImage(prompt, imageURL) {
    if (!prompt || !imageURL) {
        Object.values(aiBoxes).forEach(box => {
            const p = document.createElement('p');
            p.innerHTML = 'Error: Please enter both a question and an image URL.';
            p.className = 'error';
            box.appendChild(p);
            box.scrollTop = box.scrollHeight;
        });
        return;
    }
    if (!window.puter || !window.puter.ai) {
        Object.values(aiBoxes).forEach(box => {
            const p = document.createElement('p');
            p.innerHTML = 'Error: Puter.js failed to load. Check network or script URL.';
            p.className = 'error';
            box.appendChild(p);
            box.scrollTop = box.scrollHeight;
        });
        return;
    }
    analyzeImgBtn.disabled = true;
    analyzeImgBtn.classList.add('loading');
    const modelKeys = Object.keys(models).sort();
    for (const key of modelKeys) {
        const model = models[key];
        const box = aiBoxes[key];
        box.setAttribute('aria-busy', 'true');
        const p = document.createElement('p');
        p.className = 'response';
        box.appendChild(p);
        try {
            const stream = await puter.ai.chat(prompt, imageURL, false, { model, stream: true });
            let fullText = '';
            for await (const part of stream) {
                if (part?.text) {
                    fullText += part.text;
                    p.innerHTML = fullText.replace(/\n/g, '<br>');
                    box.scrollTop = box.scrollHeight;
                    playTTS(part.text);
                }
            }
            if (!fullText) {
                p.innerHTML = `Error: No response from ${key} for image analysis.`;
                p.className = 'error';
            }
        } catch (e) {
            console.warn(`${key} image analysis failed`, e);
            p.innerHTML = `Error: ${key} failed to analyze image - ${e.message}`;
            p.className = 'error';
        }
        box.setAttribute('aria-busy', 'false');
        box.scrollTop = box.scrollHeight;
    }
    analyzeImgBtn.disabled = false;
    analyzeImgBtn.classList.remove('loading');
}

// ---- DALL·E 3 Images ----
async function generateImages(prompt) {
    if (!prompt) {
        const p = document.createElement('p');
        p.innerHTML = 'Error: Please enter an image prompt.';
        p.className = 'error';
        aiBoxes['dalle'].appendChild(p);
        aiBoxes['dalle'].scrollTop = aiBoxes['dalle'].scrollHeight;
        return;
    }
    if (!window.puter || !window.puter.ai) {
        const p = document.createElement('p');
        p.innerHTML = 'Error: Puter.js failed to load. Check network or script URL.';
        p.className = 'error';
        aiBoxes['dalle'].appendChild(p);
        aiBoxes['dalle'].scrollTop = aiBoxes['dalle'].scrollHeight;
        return;
    }
    generateImgBtn.disabled = true;
    generateImgBtn.classList.add('loading');
    const box = aiBoxes['dalle'];
    box.setAttribute('aria-busy', 'true');
    box.innerHTML = '<h3>DALL·E</h3><span class="loading">Processing...</span>';
    try {
        const img = await puter.ai.txt2img(prompt);
        box.appendChild(img);
    } catch (e) {
        console.warn('DALL-E failed', e);
        const p = document.createElement('p');
        p.innerHTML = `Error: Failed to generate image - ${e.message}`;
        p.className = 'error';
        box.appendChild(p);
    }
    box.setAttribute('aria-busy', 'false');
    box.scrollTop = box.scrollHeight;
    generateImgBtn.disabled = false;
    generateImgBtn.classList.remove('loading');
}

// ---- Event Listeners ----
sendBtn.addEventListener('click', () => {
    askAI(chatInput.value);
    chatInput.value = '';
});
chatInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        askAI(chatInput.value);
        chatInput.value = '';
    }
});

sendMessagesBtn.addEventListener('click', () => {
    try {
        const messages = JSON.parse(messagesInput.value);
        askWithMessages(messages);
        messagesInput.value = '';
    } catch (e) {
        Object.values(aiBoxes).forEach(box => {
            const p = document.createElement('p');
            p.innerHTML = 'Error: Invalid JSON format for messages.';
            p.className = 'error';
            box.appendChild(p);
            box.scrollTop = box.scrollHeight;
        });
    }
});
messagesInput.addEventListener('keypress', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
        try {
            const messages = JSON.parse(messagesInput.value);
            askWithMessages(messages);
            messagesInput.value = '';
        } catch (e) {
            Object.values(aiBoxes).forEach(box => {
                const p = document.createElement('p');
                p.innerHTML = 'Error: Invalid JSON format for messages.';
                p.className = 'error';
                box.appendChild(p);
                box.scrollTop = box.scrollHeight;
            });
        }
    }
});

analyzeImgBtn.addEventListener('click', () => {
    analyzeImage(chatInput.value, imageInput.value);
    chatInput.value = '';
    imageInput.value = '';
});
imageInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        analyzeImage(chatInput.value, imageInput.value);
        chatInput.value = '';
        imageInput.value = '';
    }
});

generateImgBtn.addEventListener('click', () => {
    generateImages(dalleInput.value);
    dalleInput.value = '';
});
dalleInput.addEventListener('keypress', e => {
    if (e.key === 'Enter') {
        generateImages(dalleInput.value);
        dalleInput.value = '';
    }
});
