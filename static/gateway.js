const puter = new Puter({ debug:true });

// --- Multi-AI Chat ---
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');
const chatBox = document.getElementById('chatBox');

const aiModels = ['gpt-5','gpt-4','claude','gemini']; // Puter.js free AI models

sendBtn.addEventListener('click', askAI);
chatInput.addEventListener('keypress', e => { if(e.key==='Enter') askAI(); });

async function askAI(){
    const question = chatInput.value.trim();
    if(!question) return;

    chatBox.innerHTML += `<p><strong>You:</strong> ${question}</p>`;
    chatInput.value = '';

    for(const model of aiModels){
        const modelBox = document.createElement('p');
        modelBox.innerHTML = `<strong>${model}:</strong> <span class="streaming">...</span>`;
        chatBox.appendChild(modelBox);
        chatBox.scrollTop = chatBox.scrollHeight;

        try{
            // Stream AI response character by character
            const stream = await puter.ai.chat(question, { model, stream: true });

            const span = modelBox.querySelector('.streaming');
            span.textContent = '';

            for await (const chunk of stream) {
                span.textContent += chunk.text || chunk;
                chatBox.scrollTop = chatBox.scrollHeight;
            }

        } catch(e){
            modelBox.innerHTML = `<strong>${model} Error:</strong> ${e.message}`;
        }
    }
}

// --- DALL-E Image ---
const dalleInput = document.getElementById('dalleInput');
const generateBtn = document.getElementById('generateBtn');
const dalleBox = document.getElementById('dalleBox');

generateBtn.addEventListener('click', async () => {
    const prompt = dalleInput.value.trim();
    if(!prompt) return;

    dalleBox.innerHTML = '<p>Generating image...</p>';

    try {
        const img = await puter.ai.txt2img(prompt);
        dalleBox.innerHTML = '';
        dalleBox.appendChild(img);
    } catch(e) {
        dalleBox.innerHTML = `<p style="color:red;">Error: ${e.message}</p>`;
    }
});
