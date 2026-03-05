console.log("🛡 Scam Shield realtime scanner active");

async function checkMessage(text) {

    if (!text || text.length < 5) return;

    try {

        const response = await fetch("http://127.0.0.1:8000/analyze-text", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: text
            })

        });

        const data = await response.json();

        if (data.risk_level === "HIGH RISK") {

            showWarning(text, data.confidence);

        }

    } catch (error) {

        console.log("Backend not reachable");

    }

}


function showWarning(message, confidence) {

    const alertBox = document.createElement("div");

    alertBox.innerText =
        "⚠ SCAM WARNING\n\nMessage: " + message +
        "\nConfidence: " + confidence + "%";

    alertBox.style.position = "fixed";
    alertBox.style.bottom = "20px";
    alertBox.style.right = "20px";
    alertBox.style.background = "#ff4d4d";
    alertBox.style.color = "white";
    alertBox.style.padding = "15px";
    alertBox.style.borderRadius = "10px";
    alertBox.style.zIndex = "9999";
    alertBox.style.fontSize = "14px";

    document.body.appendChild(alertBox);

    setTimeout(() => {
        alertBox.remove();
    }, 6000);
}


function scanMessages() {

    const messages = document.querySelectorAll("span.selectable-text");

    messages.forEach(msg => {

        const text = msg.innerText;

        checkMessage(text);

    });

}


// Run every 3 seconds
setInterval(scanMessages, 3000);