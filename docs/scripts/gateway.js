<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Multi-AI Chat (Streaming)</title>
<script src="https://js.puter.com/v2/"></script>
<style>
    body { font-family: Arial, sans-serif; background:#111; color:#eee; }
    #chatInput { width:80%; padding:8px; }
    #sendBtn { padding:8px; }
    .ai-box { border:1px solid #444; padding:10px; margin:10px 0; height:150px; overflow-y:auto; background:#222; }
    .product-card { border:1px solid #444; padding:10px; margin:10px; background:#222; border-radius:6px; }
    .btn { display:inline-block; padding:6px 12px; background:#007bff; color:#fff; text-decoration:none; border-radius:4px; }
</style>
</head>
<body>

<h2>Multi-AI Chat (Streaming)</h2>

<!-- Chat input -->
<input type="text" id="chatInput" placeholder="Ask something..." />
<button id="sendBtn">Send</button>
<br><br>

<!-- Voice selector -->
<select id="voiceSelect"></select>

<!-- AI Response Boxes -->
<div id="gpt5Box" class="ai-box"><strong>GPT-5:</strong></div>
<div id="claudeBox" class="ai-box"><strong>Claude:</strong></div>
<div id="grokBox" class="ai-box"><strong>Grok:</strong></div>
<div id="geminiBox" class="ai-box"><strong>Gemini:</strong></div>
<div id="dalleBox" class="ai-box"><strong>DALL·E:</strong></div>

<!-- Affiliate Section -->
<h3>Affiliate</h3>
<input type="text" id="affiliateID" placeholder="Enter Affiliate ID">
<button id="saveAffiliateBtn">Save</button>
<p id="affiliateOutput"></p>

<!-- Products -->
<h3>Products</h3>
<div id="productContainer"></div>

<script>
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
        opt.value = v.name; 
        opt.textContent = v.name + ' (' + v.lang + ')';
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

// Correct model IDs
const models = {
    'gpt-5': 'gpt-5',
    'claude': 'claude-sonnet-4',
    'grok': 'grok-beta',
    'gemini': 'gemini-2.0-flash'
};

if(sendBtn){
    sendBtn.addEventListener('click', askAI);
    chatInput.addEventListener('keypress', e=>{ if(e.key==='Enter') askAI(); });
}

async function askAI(){
    const question = chatInput.value.trim();
    if(!question) return;
    chatInput.value='';

    // Text models with streaming
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

            // Play full response via TTS
            playTTS(fullText);

        } catch(e){ console.warn(model + " failed", e); }
    }

    // DALL·E image
    try{
        const imgEl = await puter.ai.txt2img(question);
        if(aiBoxes['dalle']){
            aiBoxes['dalle'].appendChild(imgEl);
            aiBoxes['dalle'].scrollTop = aiBoxes['dalle'].scrollHeight;
        }
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
</script>
</body>
</html>
