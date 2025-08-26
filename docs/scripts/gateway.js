const synth = window.speechSynthesis;
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const dalleInput = document.getElementById('dalleInput');
const generateImgBtn = document.getElementById('generateImgBtn');
const productUrls = document.getElementById('productUrls');
const generateVideoBtn = document.getElementById('generateVideoBtn');
const voiceSelect = document.getElementById('voiceSelect');
const retryBtn = document.getElementById('retryBtn');
const errorBox = document.getElementById('errorBox');
const responseBox = document.getElementById('responseBox');
const dalleBox = document.getElementById('dalleBox');
const videoBox = document.getElementById('videoBox');

const defaultModel = 'gpt-4o-mini'; // Fallback model
const appId = 'linkbotlabs'; // Placeholder app ID

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

// ---- Text Generation (Example 1) ----
async function askAI(prompt, retry = false) {
    if (!prompt) {
        displayError('Please enter a text prompt.');
        const p = document.createElement('p');
        p.innerHTML = 'Error: Please enter a text prompt.';
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
    let model = retry ? defaultModel : 'gpt-5-nano';
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
        } else {
            // Store text in puter.kv
            await puter.kv.set(`${appId}:lastText`, fullText);
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

// ---- Image Generation (Example 2) ----
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
    try {
        const img = await puter.ai.txt2img(prompt);
        const imgUrl = img.src; // Get image URL
        dalleBox.appendChild(img);
        // Store image URL in puter.kv
        let imageUrls = await puter.kv.get(`${appId}:imageUrls`) || [];
        if (!Array.isArray(imageUrls)) imageUrls = [];
        imageUrls.push(imgUrl);
        await puter.kv.set(`${appId}:imageUrls`, imageUrls);
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

// ---- Generate Video ----
async function generateVideo() {
    if (!window.puter || !window.puter.ai) {
        displayError('Puter.js failed to load. Check network or script URL: https://js.puter.com/v2/');
        const p = document.createElement('p');
        p.innerHTML = 'Error: Puter.js failed to load.';
        p.className = 'error';
        videoBox.appendChild(p);
        videoBox.scrollTop = videoBox.scrollHeight;
        return;
    }
    generateVideoBtn.disabled = true;
    generateVideoBtn.classList.add('loading');
    videoBox.setAttribute('aria-busy', 'true');
    videoBox.innerHTML = '<h3>Generated Video</h3><span class="loading">Processing...</span>';
    try {
        // Get data from puter.kv
        const scriptText = await puter.kv.get(`${appId}:lastText`) || '';
        const dalleUrls = await puter.kv.get(`${appId}:imageUrls`) || [];
        const productUrlsList = productUrls.value.split('\n').filter(url => url.trim());

        // Prepare form data
        const formData = new FormData();
        formData.append('urls', JSON.stringify(productUrlsList));
        formData.append('dalle_urls', JSON.stringify(dalleUrls));
        formData.append('script', scriptText);

        // Send to Flask endpoint
        const response = await fetch('/generate_video', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        if (result.error) {
            throw new Error(result.error);
        }

        // Display video
        const video = document.createElement('video');
        video.src = `/download/${result.video_file}`;
        video.controls = true;
        videoBox.innerHTML = '<h3>Generated Video</h3>';
        videoBox.appendChild(video);
    } catch (e) {
        displayError(`Video generation failed: ${e.message}`);
        const p = document.createElement('p');
        p.innerHTML = `Error: Failed to generate video - ${e.message}`;
        p.className = 'error';
        videoBox.appendChild(p);
    }
    videoBox.setAttribute('aria-busy', 'false');
    videoBox.scrollTop = videoBox.scrollHeight;
    generateVideoBtn.disabled = false;
    generateVideoBtn.classList.remove('loading');
}

// ---- Retry Mechanism ----
async function retryLastAction() {
    errorBox.innerHTML = '';
    errorBox.classList.remove('active');
    const lastTextPrompt = await puter.kv.get(`${appId}:lastTextPrompt`);
    const lastImagePrompt = await puter.kv.get(`${appId}:lastImagePrompt`);
    if (lastTextPrompt) {
        chatInput.value = lastTextPrompt;
        return askAI(lastTextPrompt, true);
    } else if (lastImagePrompt) {
        dalleInput.value = lastImagePrompt;
        return generateImages(lastImagePrompt, true);
    } else {
        displayError('No previous action to retry.');
    }
}

// ---- Event Listeners ----
sendBtn.addEventListener('click', async () => {
    errorBox.innerHTML = '';
    errorBox.classList.remove('active');
    await puter.kv.set(`${appId}:lastTextPrompt`, chatInput.value);
    await puter.kv.del(`${appId}:lastImagePrompt`);
    askAI(chatInput.value);
    chatInput.value = '';
});
chatInput.addEventListener('keypress', async e => {
    if (e.key === 'Enter') {
        errorBox.innerHTML = '';
        errorBox.classList.remove('active');
        await puter.kv.set(`${appId}:lastTextPrompt`, chatInput.value);
        await puter.kv.del(`${appId}:lastImagePrompt`);
        askAI(chatInput.value);
        chatInput.value = '';
    }
});

generateImgBtn.addEventListener('click', async () => {
    errorBox.innerHTML = '';
    errorBox.classList.remove('active');
    await puter.kv.set(`${appId}:lastImagePrompt`, dalleInput.value);
    await puter.kv.del(`${appId}:lastTextPrompt`);
    generateImages(dalleInput.value);
    dalleInput.value = '';
});
dalleInput.addEventListener('keypress', async e => {
    if (e.key === 'Enter') {
        errorBox.innerHTML = '';
        errorBox.classList.remove('active');
        await puter.kv.set(`${appId}:lastImagePrompt`, dalleInput.value);
        await puter.kv.del(`${appId}:lastTextPrompt`);
        generateImages(dalleInput.value);
        dalleInput.value = '';
    }
});

generateVideoBtn.addEventListener('click', () => {
    errorBox.innerHTML = '';
    errorBox.classList.remove('active');
    generateVideo();
});

retryBtn.addEventListener('click', () => {
    retryLastAction();
});

// ---- Initial Check for Puter.js ----
if (!window.puter || !window.puter.ai) {
    displayError('Puter.js failed to load on page load. Check network or script URL: https://js.puter.com/v2/');
}
