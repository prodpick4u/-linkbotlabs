const synth = window.speechSynthesis;
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');

const aiBoxes = {
    'gpt-5': document.getElementById('gpt5Box'),
    'claude': document.getElementById('claudeBox'),
    'grok': document.getElementById('grokBox'),
    'gemini': document.getElementById('geminiBox'),
    'dalle': document.getElementById('dalleBox')
};

const models = {
    'gpt-5': 'gpt-5',
    'claude': 'claude-sonnet-4',
    'grok': 'grok-beta',
    'gemini': 'gemini-2.0-flash'
};

// ---- Voice Selector ----
function populateVoiceSelect(){
    let voices = synth.getVoices();
    if(!voices.length){ setTimeout(populateVoiceSelect,100); return; }
    voices = voices.filter(v=>v.lang.startsWith('en'));
    voices.forEach(v=>{
        const opt = document.createElement('option');
        opt.value = v.name;
        opt.textContent = v.name + ' (' + v.lang + ')';
        document.body.appendChild(opt);
    });
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
    synth.speak(utter);
}

// ---- Multi-AI Chat ----
async function askAI(question){
    if(!question) return;
    for(const key in models){
        const model = models[key];
        try{
            const box = aiBoxes[key];
            const p = document.createElement("p");
            box.appendChild(p);

            const stream = await puter.ai.chat(`Answer clearly: "${question}"`, { model, stream: true });
            let fullText = "";
            for await (const part of stream){
                if(part?.text){
                    fullText += part.text;
                    p.innerHTML = fullText.replace(/\n/g,"<br>");
                    box.scrollTop = box.scrollHeight;
                }
            }
            playTTS(fullText);
        } catch(e){ console.warn(key + " failed", e); }
    }
}

// ---- DALL·E 3 Images ----
async function generateImages(prompt){
    const box = aiBoxes['dalle'];
    box.innerHTML = '';
    for(let i=0;i<3;i++){
        try{
            const img = await puter.ai.txt2img(prompt);
            box.appendChild(img);
        } catch(e){ console.warn("DALL-E failed", e); }
    }
}

// ---- Event Listeners ----
sendBtn.addEventListener('click', ()=>{ askAI(chatInput.value); chatInput.value=''; });
chatInput.addEventListener('keypress', e=>{ if(e.key==='Enter'){ askAI(chatInput.value); chatInput.value=''; }});

document.getElementById('generateImgBtn').addEventListener('click', ()=>{
    generateImages(document.getElementById('dalleInput').value);
});

// ---- Affiliate ID ----
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

// ---- Products Section ----
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

// Load products on page load
generateProducts();
