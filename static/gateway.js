// static/gateway.js

// === Multi-AI Chat Handler ===
document.getElementById("sendBtn").addEventListener("click", async () => {
    const input = document.getElementById("chatInput").value;
    if (!input) return;

    const chatBox = document.getElementById("chatBox");
    chatBox.innerHTML += `<div><strong>You:</strong> ${input}</div>`;

    // Choose which model to test (switch this as you like)
    const model = "gpt-5-nano"; 
    // Examples: "x-ai/grok-4", "google/gemini-2.5-pro-exp-03-25:free", "claude-sonnet-4"

    try {
        const response = await puter.ai.chat(input, { model, stream: true });

        // Add AI response progressively
        const aiDiv = document.createElement("div");
        aiDiv.innerHTML = `<strong>${model}:</strong> <span></span>`;
        chatBox.appendChild(aiDiv);
        const span = aiDiv.querySelector("span");

        for await (const part of response) {
            if (part?.text) {
                span.innerHTML += part.text;
                chatBox.scrollTop = chatBox.scrollHeight;
            }
        }
    } catch (err) {
        chatBox.innerHTML += `<div style="color:red;"><strong>Error:</strong> ${err}</div>`;
    }

    document.getElementById("chatInput").value = "";
});

// === DALL·E / Image Generation ===
document.getElementById("generateBtn").addEventListener("click", async () => {
    const prompt = document.getElementById("dalleInput").value;
    if (!prompt) return;

    const dalleBox = document.getElementById("dalleBox");
    dalleBox.innerHTML = `<div><strong>Generating:</strong> ${prompt}</div>`;

    try {
        const imgEl = await puter.ai.txt2img(prompt); 
        dalleBox.innerHTML = "";
        dalleBox.appendChild(imgEl);
    } catch (err) {
        dalleBox.innerHTML = `<div style="color:red;"><strong>Error:</strong> ${err}</div>`;
    }
});
