const puter = new Puter({ debug:true });

const dalleInput = document.getElementById('dalleInput');
const generateBtn = document.getElementById('generateBtn');
const dalleBox = document.getElementById('dalleBox');

generateBtn.addEventListener('click', async () => {
    const prompt = dalleInput.value.trim();
    if(!prompt) return;

    // Clear previous images
    dalleBox.innerHTML = '<p>Generating...</p>';

    try {
        const img = await puter.ai.txt2img(prompt);
        dalleBox.innerHTML = '';
        dalleBox.appendChild(img);
    } catch(e) {
        dalleBox.innerHTML = `<p style="color:red;">Error: ${e.message}</p>`;
    }
});
