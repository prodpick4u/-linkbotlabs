const puter = new Puter({ debug: true });
const synth = window.speechSynthesis;

// ---- Voice Selector ----
function populateVoiceSelect(){
    let voices = synth.getVoices();
    if(!voices.length){ setTimeout(populateVoiceSelect,100); return; }
    voices = voices.filter(v=>v.lang.startsWith('en'));
    const select = document.querySelector('#voiceSelect');
    select.innerHTML = '';
    voices.forEach(v=>{
        const opt = document.createElement('option');
        opt.value = v.name; opt.textContent = v.name + ' (' + v.lang + ')';
        select.appendChild(opt);
    });
    select.value = voices[0]?.name;
}
if(speechSynthesis.onvoiceschanged!==undefined){ speechSynthesis.onvoiceschanged=populateVoiceSelect; } 
else { populateVoiceSelect(); }

// ---- TTS ----
function playTTS(text){
    if(synth.speaking) synth.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.voice = synth.getVoices().find(v=>v.name === document.querySelector('#voiceSelect').value);
    synth.speak(utter);
}

// ---- Multi-AI Chat ----
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');

const aiBoxes = {
    'gpt-5': document.getElementById('gpt5Box'),
    'claude': document.getElementById('claudeBox'),
    'grok': document.getElementById('grokBox'),
    'gemini': document.getElementById('geminiBox'),
    'dalle': document.getElementById('dalleBox')
};

if(sendBtn){
    sendBtn.addEventListener('click', askAI);
    chatInput.addEventListener('keypress', e=>{ if(e.key==='Enter') askAI(); });
}

async function askAI(){
    const question = chatInput.value.trim();
    if(!question) return;

    chatInput.value='';

    for(const model of ['gpt-5','claude','grok','gemini']){
        try{
            const response = await puter.call(model, `Answer clearly: "${question}"`);
            aiBoxes[model].innerHTML += `<p>${response.text}</p>`;
            aiBoxes[model].scrollTop = aiBoxes[model].scrollHeight;
            playTTS(response.text);
        } catch(e){ console.warn(model + " failed", e); }
    }

    // DALL-E box
    try{
        const imgEl = await puter.ai.txt2img(question);
        aiBoxes['dalle'].appendChild(imgEl);
        aiBoxes['dalle'].scrollTop = aiBoxes['dalle'].scrollHeight;
    } catch(e){ console.warn("DALL-E failed", e); }
}

// ---- Affiliate Registration ----
const saveAffiliateBtn = document.getElementById('saveAffiliateBtn');
if(saveAffiliateBtn){
    saveAffiliateBtn.addEventListener('click', ()=>{
        const tag = document.getElementById('affiliateID').value.trim();
        if(tag){
            localStorage.setItem('affiliateTag', tag);
            document.getElementById('affiliateOutput').innerText = `✅ Affiliate ID "${tag}" saved!`;
        }
    });
}

// ---- Generate Products ----
async function generateProducts(category="Trending"){
    const container = document.getElementById('productContainer');
    if(!container) return;
    container.innerHTML = "";
    const affiliateTag = localStorage.getItem('affiliateTag') || "";
    try{
        const response = await puter.ai.chat(
            `Generate 5 trending Amazon products for ${category} category, JSON format [{name, link}]`,
            { model: "gpt-5" }
        );
        let products = [];
        try{ products = JSON.parse(response.text); } 
        catch{ products = Array.from({length:5},(_,i)=>({name:`${category} Product ${i+1}`, link:"#"})); }

        for(const p of products){
            const card = document.createElement('div');
            card.className = 'product-card';
            const title = document.createElement('h4'); title.innerText = p.name; card.appendChild(title);
            const btn = document.createElement('a'); 
            btn.href = p.link + (p.link.includes('?')?'&':'?') + 'tag=' + affiliateTag; 
            btn.innerText = "Buy Now"; 
            btn.className = "btn"; 
            card.appendChild(btn);
            container.appendChild(card);
        }
    } catch(err){ console.warn("Product generation failed", err); }
}

// Call product generation on load
generateProducts();
