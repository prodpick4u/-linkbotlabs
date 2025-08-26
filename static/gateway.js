// Password Handling
const correctPassword = "supersecret";
const overlay = document.getElementById('passwordOverlay');
const input = document.getElementById('dashboardPassword');
const btn = document.getElementById('submitPassword');
const dashboard = document.getElementById('dashboardContent');

btn.addEventListener('click', () => {
    if(input.value === correctPassword){
        overlay.style.display='none';
        dashboard.style.display='block';
        initPuterAI(); // initialize AI after unlock
    } else {
        document.getElementById('pwError').style.display='block';
        input.value='';
    }
});
input.addEventListener('keypress', e=>{ if(e.key==='Enter') btn.click(); });

// Tabs switching
const tabs = document.querySelectorAll('.tab');
tabs.forEach(tab=>{
    tab.addEventListener('click', ()=>{
        document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c=>c.classList.remove('active'));
        tab.classList.add('active');
        document.getElementById(tab.dataset.tab).classList.add('active');
    });
});

// --- Initialize Puter AI ---
function initPuterAI() {
    const puter = new Puter({ debug:true });

    // --- Chat / Q&A ---
    const qaInput = document.getElementById('qaInput');
    const qaBtn = document.getElementById('qaBtn');
    const qaBox = document.getElementById('qaBox');
    const modelSelect = document.getElementById('modelSelect');
    const clearChatBtn = document.getElementById('clearChatBtn');

    qaBtn.addEventListener('click', askQuestion);
    qaInput.addEventListener('keypress', e=>{ if(e.key==='Enter') askQuestion(); });
    clearChatBtn.addEventListener('click', ()=>{ qaBox.innerHTML=''; });

    async function askQuestion() {
        const question = qaInput.value.trim();
        if(!question) return;

        qaBox.innerHTML += `<p><strong>You:</strong> ${question}</p>`;
        qaInput.value='';

        const span = document.createElement('p');
        span.innerHTML = `<strong>AI:</strong> <span class="streaming">...</span>`;
        qaBox.appendChild(span);
        qaBox.scrollTop = qaBox.scrollHeight;

        try {
            const selectedModel = modelSelect.value || 'gpt-5';
            const stream = await puter.ai.chat(question, { model: selectedModel, stream:true });
            const streamingSpan = span.querySelector('.streaming');
            streamingSpan.textContent = '';
            for await (const chunk of stream) {
                streamingSpan.textContent += chunk.text || chunk;
                qaBox.scrollTop = qaBox.scrollHeight;
            }
        } catch(e) {
            span.innerHTML = `<strong>AI Error:</strong> ${e.message}`;
        }
    }

    // --- DALL-E ---
    const dalleInput = document.getElementById('dalleInput');
    const generateBtn = document.getElementById('generateBtn');
    const dalleBox = document.getElementById('dalleBox');

    generateBtn.addEventListener('click', async () => {
        const prompt = dalleInput.value.trim();
        if(!prompt) return;
        dalleBox.innerHTML = '<p>Generating image...</p>';
        try {
            const img = await puter.ai.txt2img(prompt);
            dalleBox.innerHTML='';
            dalleBox.appendChild(img);
        } catch(e){
            dalleBox.innerHTML = `<p style="color:red;">Error: ${e.message}</p>`;
        }
    });

    // --- Video generation handled by Flask / POST request ---
}
