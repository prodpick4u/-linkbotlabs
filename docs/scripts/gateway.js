const synth = window.speechSynthesis;
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const voiceSelect = document.getElementById('voiceSelect');

const aiBoxes = {
    'claude': document.getElementById('claudeBox'),
    'dalle': document.getElementById('dalleBox'),
    'gemini': document.getElementById('geminiBox'),
    'gpt-5': document.getElementById('gpt5Box'),
    'grok': document.getElementById('grokBox')
};

const models = {
    'claude': 'claude-sonnet-4',
    'gemini': 'gemini-2.0-flash',
    'gpt-5': 'gpt-5',
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

// ---- Multi-AI Chat with Streaming ----
async function askAI(question) {
    if (!question) return;
    sendBtn.disabled = true;
    sendBtn.classList.add('loading');
    const modelKeys = Object.keys(models).sort();
    for (const key of modelKeys) {
        const model = models[key];
        const box = aiBoxes[key];
        box.setAttribute('aria-busy', 'true');
        const p = document.createElement('p');
        box.appendChild(p);
        try {
            const stream = await puter.ai.chat(`Answer clearly: "${question}"`, { model, stream: true });
            let fullText = '';
            for await (const part of stream) {
                if (part?.text) {
                    fullText += part.text;
                    p.innerHTML = fullText.replace(/\n/g, '<br>');
                    box.scrollTop = box.scrollHeight;
                    playTTS(part.text); // Speak each chunk
                }
            }
        } catch (e) {
            console.warn(`${key} failed`, e);
            p.innerHTML = `Error: ${key} failed to respond.`;
        }
        box.setAttribute('aria-busy', 'false');
    }
    sendBtn.disabled = false;
    sendBtn.classList.remove('loading');
}

// ---- DALL·E 3 Images ----
async function generateImages(prompt) {
    const box = aiBoxes['dalle'];
    box.setAttribute('aria-busy', 'true');
    box.innerHTML = '<h3>DALL·E</h3>';
    for (let i = 0; i < 3; i++) {
        try {
            const img = await puter.ai.txt2img(prompt);
            box.appendChild(img);
        } catch (e) {
            console.warn('DALL-E failed', e);
            const p = document.createElement('p');
            p.innerHTML = 'Error: Failed to generate image.';
            box.appendChild(p);
        }
    }
    box.setAttribute('aria-busy', 'false');
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

document.getElementById('generateImgBtn').addEventListener('click', () => {
    generateImages(document.getElementById('dalleInput').value);
});
