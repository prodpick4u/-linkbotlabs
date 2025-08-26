// Function to initialize Puter and all AI interactions
function initPuterAI() {
    const puter = new Puter({ debug: true });

    // --- Q&A / Search ---
    const qaInput = document.getElementById('qaInput');
    const qaBtn = document.getElementById('qaBtn');
    const qaBox = document.getElementById('qaBox');

    qaBtn.addEventListener('click', askQuestion);
    qaInput.addEventListener('keypress', e => { if(e.key === 'Enter') askQuestion(); });

    async function askQuestion() {
        const question = qaInput.value.trim();
        if (!question) return;

        qaBox.innerHTML += `<p><strong>You:</strong> ${question}</p>`;
        qaInput.value = '';

        const span = document.createElement('p');
        span.innerHTML = `<strong>AI:</strong> <span class="streaming">...</span>`;
        qaBox.appendChild(span);
        qaBox.scrollTop = qaBox.scrollHeight;

        try {
            // Change model here if you want Claude, GPT-5, or Grok
            const stream = await puter.ai.chat(question, { model: 'gpt-5', stream: true });
            const streamingSpan = span.querySelector('.streaming');
            streamingSpan.textContent = '';
            for await (const chunk of stream) {
                streamingSpan.textContent += chunk.text || chunk;
                qaBox.scrollTop = qaBox.scrollHeight;
            }
        } catch (e) {
            span.innerHTML = `<strong>AI Error:</strong> ${e.message}`;
        }
    }

    // --- DALL-E Image ---
    const dalleInput = document.getElementById('dalleInput');
    const generateBtn = document.getElementById('generateBtn');
    const dalleBox = document.getElementById('dalleBox');

    generateBtn.addEventListener('click', async () => {
        const prompt = dalleInput.value.trim();
        if (!prompt) return;

        dalleBox.innerHTML = '<p>Generating image...</p>';

        try {
            const img = await puter.ai.txt2img(prompt); // Can switch to DALL-E, Gemini, or Claude image models
            dalleBox.innerHTML = '';
            dalleBox.appendChild(img);
        } catch (e) {
            dalleBox.innerHTML = `<p style="color:red;">Error: ${e.message}</p>`;
        }
    });
}

// --- Password Overlay Handling ---
const correctPassword = "supersecret";
const overlay = document.getElementById('passwordOverlay');
const input = document.getElementById('dashboardPassword');
const btn = document.getElementById('submitPassword');
const dashboard = document.getElementById('dashboardContent');

btn.addEventListener('click', () => {
    if (input.value === correctPassword) {
        overlay.style.display = 'none';
        dashboard.style.display = 'block';
        initPuterAI(); // Initialize Puter AFTER password is correct
    } else {
        document.getElementById('pwError').style.display = 'block';
        input.value = '';
    }
});
input.addEventListener('keypress', e => { if (e.key === 'Enter') btn.click(); });
