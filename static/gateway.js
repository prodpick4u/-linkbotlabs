// --- Initialize Puter and all AI interactions ---
function initPuterAI() {
    const puter = new Puter({ debug: true });

    // --- Chat / Q&A ---
    const qaInput = document.getElementById('qaInput');
    const qaBtn = document.getElementById('qaBtn');
    const qaBox = document.getElementById('qaBox');
    const modelSelect = document.getElementById('modelSelect');

    qaBtn.addEventListener('click', askQuestion);
    qaInput.addEventListener('keypress', e => { if(e.key==='Enter') askQuestion(); });

    async function askQuestion() {
        const question = qaInput.value.trim();
        if (!question) return;

        const selectedModel = modelSelect.value || 'gpt-5';

        qaBox.innerHTML += `<p><strong>You:</strong> ${question}</p>`;
        qaInput.value='';

        const span = document.createElement('p');
        span.innerHTML = `<strong>AI:</strong> <span class="streaming">...</span>`;
        qaBox.appendChild(span);
        qaBox.scrollTop = qaBox.scrollHeight;

        try {
            let stream;
            try {
                // Attempt streaming first
                stream = await puter.ai.chat(question, { model: selectedModel, stream:true });
                const streamingSpan = span.querySelector('.streaming');
                streamingSpan.textContent = '';
                for await (const chunk of stream) {
                    streamingSpan.textContent += chunk.text || chunk;
                    qaBox.scrollTop = qaBox.scrollHeight;
                }
            } catch(err) {
                // Fallback to non-streaming mode
                const response = await puter.ai.chat(question, { model: selectedModel });
                span.querySelector('.streaming').textContent = response.text || response;
            }
        } catch(e) {
            span.innerHTML = `<strong>AI Error:</strong> ${e.message}<br>Try selecting another model.`;
        }
    }

    // --- DALL-E Image Generation ---
    const dalleInput = document.getElementById('dalleInput');
    const generateBtn = document.getElementById('generateBtn');
    const dalleBox = document.getElementById('dalleBox');

    generateBtn.addEventListener('click', async () => {
        const prompt = dalleInput.value.trim();
        if(!prompt) return;

        dalleBox.innerHTML = '<p>Generating image...</p>';

        try {
            const img = await puter.ai.txt2img(prompt); // You can also specify model here if needed
            dalleBox.innerHTML = '';
            dalleBox.appendChild(img);
        } catch(e) {
            dalleBox.innerHTML = `<p style="color:red;">Error: ${e.message}</p>`;
        }
    });
}
