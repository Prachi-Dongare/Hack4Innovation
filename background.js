chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {

    if (message.type === "NEW_MESSAGE") {

        console.log("Background received:", message.text);

        chrome.runtime.sendMessage({
            type: "FOR_POPUP",
            text: message.text
        });

    }

});