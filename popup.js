const analyzeBtn = document.getElementById("analyzeBtn");
const recordBtn = document.getElementById("recordBtn");
const uploadBtn = document.getElementById("uploadBtn");
const audioFile = document.getElementById("audioFile");
const textInput = document.getElementById("textInput");
const resultDiv = document.getElementById("result");

// ---------- TEXT ANALYZE ----------
analyzeBtn.addEventListener("click", async () => {
    const message = textInput.value.trim();
    if (!message) {
        resultDiv.innerText = "Please enter text first.";
        return;
    }

    resultDiv.innerText = "Analyzing...";

    try {
        const response = await fetch("http://127.0.0.1:8000/analyze-text", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await response.json();
        resultDiv.innerText = "Risk Score: " + data.risk_score;

    } catch (error) {
        resultDiv.innerText = "Backend not connected (Ignore if teammate handling)";
    }
});


// ---------- VOICE RECORD ----------
recordBtn.addEventListener("click", () => {

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        resultDiv.innerText = "Speech Recognition not supported in this browser.";
        return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.start();

    resultDiv.innerText = "Listening... 🎤";

    recognition.onresult = async function(event) {
        const transcript = event.results[0][0].transcript;
        textInput.value = transcript;
        resultDiv.innerText = "You said: " + transcript;

        // Optional backend call
        try {
            const response = await fetch("http://127.0.0.1:8000/analyze-text", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: transcript })
            });

            const data = await response.json();
            resultDiv.innerText = "Risk Score: " + data.risk_score;

        } catch (error) {
            // ignore backend if not ready
        }
    };
});


// ---------- AUDIO UPLOAD ----------
uploadBtn.addEventListener("click", () => {
    audioFile.click();
});

audioFile.addEventListener("change", () => {
    if (audioFile.files.length > 0) {
        resultDiv.innerText = "Audio file selected: " + audioFile.files[0].name;
        // Backend handling your teammate will implement
    }
});