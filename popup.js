const analyzeBtn = document.getElementById("analyzeBtn");
const recordBtn = document.getElementById("recordBtn");
const uploadBtn = document.getElementById("uploadBtn");
const audioFile = document.getElementById("audioFile");
const textInput = document.getElementById("textInput");
const resultDiv = document.getElementById("result");


// ================= TEXT ANALYSIS =================

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

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        resultDiv.innerText =
            "Risk Level: " + data.risk_level +
            "\nRisk Score: " + data.risk_score +
            "\nConfidence: " + data.confidence + "%";

    }

    catch (error) {

        resultDiv.innerText = "Backend not connected";

    }

});


// ================= VOICE RECORD =================

recordBtn.addEventListener("click", () => {

    if (!('webkitSpeechRecognition' in window)) {

        resultDiv.innerText = "Speech recognition not supported in this browser.";

        return;

    }

    const recognition = new webkitSpeechRecognition();

    recognition.lang = "en-US";

    recognition.start();

    resultDiv.innerText = "Listening... 🎤";

    recognition.onresult = function(event) {

        const transcript = event.results[0][0].transcript;

        textInput.value = transcript;

        resultDiv.innerText = "You said: " + transcript;

        analyzeBtn.click();

    };

    recognition.onerror = function() {

        resultDiv.innerText = "Microphone permission denied.";

    };

});


// ================= AUDIO UPLOAD =================

uploadBtn.addEventListener("click", () => {

    audioFile.click();

});


audioFile.addEventListener("change", async () => {

    if (audioFile.files.length === 0) return;

    const file = audioFile.files[0];

    const formData = new FormData();

    formData.append("file", file);

    resultDiv.innerText = "Processing audio...";

    try {

        const response = await fetch("http://127.0.0.1:8000/analyze-audio", {

            method: "POST",

            body: formData

        });

        const data = await response.json();

        textInput.value = data.transcript;

        resultDiv.innerText =
            "Transcript: " + data.transcript +
            "\nRisk Level: " + data.risk_level +
            "\nConfidence: " + data.confidence + "%";

    }

    catch (error) {

        resultDiv.innerText = "Audio processing failed.";

    }

});