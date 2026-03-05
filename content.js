console.log("Scam Protector content script loaded!");

// Function to scan messages
function scanMessages() {
    const messages = document.querySelectorAll("div.copyable-text");

    messages.forEach((msg) => {
        const textSpan = msg.querySelector("span");
        if (textSpan) {
            const text = textSpan.innerText;
            if (text) {
                console.log("Detected Message:", text);
            }
        }
    });
}

// Run every 4 seconds
setInterval(scanMessages, 4000);