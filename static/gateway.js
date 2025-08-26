const puter = new Puter({ debug:true });
const synth = window.speechSynthesis;

// ---- Voice Selector ----
function populateVoiceSelect(){
    let voices = synth.getVoices();
    if(!voices.length){ setTimeout(populateVoiceSelect,100); return; }
    voices = voices.filter(v => v.lang.startsWith('en'));
    const select = document.getElementById('voiceSelect');
    select.innerHTML = '';
    voices.forEach(v => {
        const opt = document.createElement('option');
        opt.value = v.name;
        opt.textContent = `${v.name} (${v.lang})`;
        select.appendChild(opt);
    });
    select.value = voices[0]?.name;
}
if(speechSynthesis.onvoiceschanged!==undefined){ 
    speechSynthesis.onvoiceschanged = populateVoiceSelect; 
} else { 
    populateVoiceSelect(); 
}

// ---- TTS ----
function playTTS(text){
    if(synth.speaking) synth.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.voice = synth.getVoices().find(v => v.name === document.getElementById('voiceSelect').value);
    synth.speak(utter);
}

// ---- Multi-AI Chat ----
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatBox = document.getElementById('chatBox');

sendBtn.addEventListener('click', askAI);
chatInput.addEventListener('keypress', e => { if(e.key === 'Enter') askAI(); });

async function askAI(){
    const question = chatInput.value.trim();
    if(!question) return;
    chatBox.innerHTML += `<p><strong>You:</strong> ${question}</p>`;
    chatInput.value = '';

    const aiModels = ['gpt-5','claude','grok','gemini'];

    for(const model of aiModels){
        try{
            const res = await puter.ai.chat(question, { model });
            const text = res.text || res;
            chatBox.innerHTML += `<p><strong>${model}:</strong> ${text}</p>`;
            chatBox.scrollTop = chatBox.scrollHeight;
            playTTS(text);
        } catch(e){
            chatBox.innerHTML += `<p><strong>${model} Error:</strong> ${e.message}</p>`;
        }
    }
}

// ---- DALL-E Image ----
const dalleInput = document.getElementById('dalleInput');
const generateBtn = document.getElementById('generateBtn');
const dalleBox = document.getElementById('dalleBox');

generateBtn.addEventListener('click', async () => {
    const prompt = dalleInput.value.trim();
    if(!prompt) return;
    const img = await puter.ai.txt2img(prompt);
    dalleBox.appendChild(img);
});
