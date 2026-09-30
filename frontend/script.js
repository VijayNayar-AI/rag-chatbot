const questionInput = document.getElementById("question");
const sendButton = document.getElementById("sendButton");
const chatMessages = document.getElementById("chatMessages");


async function sendMessage() {

    const question = questionInput.value.trim();


    // Empty question check
    if (!question) {
        return;
    }


    // Remove welcome message
    const welcomeMessage =
        document.querySelector(".welcome-message");

    if (welcomeMessage) {
        welcomeMessage.remove();
    }


    // Add user message
    addMessage(question, "user");


    // Clear input
    questionInput.value = "";


    // Disable button while processing
    sendButton.disabled = true;
    sendButton.innerText = "Thinking...";


    // Add temporary bot message
    const thinkingMessage =
        addMessage("Thinking...", "bot");


    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail || "API request failed"
            );

        }


        // Replace Thinking... with actual answer
        thinkingMessage.innerText = data.answer;


    }
    catch (error) {

        console.error("Chat error:", error);

        thinkingMessage.innerText =
            "Sorry, something went wrong.";

    }


    // Enable button again
    sendButton.disabled = false;
    sendButton.innerText = "Send";


    // Scroll to latest message
    chatMessages.scrollTop =
        chatMessages.scrollHeight;

}


/*
    Create a chat message
*/
function addMessage(text, sender) {

    const messageContainer =
        document.createElement("div");


    if (sender === "user") {

        messageContainer.className =
            "user-message";

    }
    else {

        messageContainer.className =
            "bot-message";

    }


    const message =
        document.createElement("div");


    message.className = "message";

    message.innerText = text;


    messageContainer.appendChild(message);

    chatMessages.appendChild(messageContainer);


    // Scroll to bottom
    chatMessages.scrollTop =
        chatMessages.scrollHeight;


    return message;

}


/*
    Send message when button is clicked
*/
sendButton.addEventListener(
    "click",
    sendMessage
);


/*
    Send message when Enter is pressed
*/
questionInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);