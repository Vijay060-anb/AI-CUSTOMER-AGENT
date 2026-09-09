// =========================================================
// SUPPORTAI CLIENT
// =========================================================

const messageInput =
    document.getElementById("messageInput");

const sendButton =
    document.getElementById("sendButton");

const chatMessages =
    document.getElementById("chatMessages");

const customerNameInput =
    document.getElementById("customerName");

const orderIdInput =
    document.getElementById("orderId");


// =========================================================
// CONVERSATION ID
// =========================================================

function createConversationId() {

    const randomPart =
        Math.random()
            .toString(36)
            .substring(2, 10);

    return `CONV-${randomPart.toUpperCase()}`;
}


function getConversationId() {

    let conversationId =
        sessionStorage.getItem(
            "supportai_conversation_id"
        );


    if (!conversationId) {

        conversationId =
            createConversationId();

        sessionStorage.setItem(
            "supportai_conversation_id",
            conversationId
        );
    }


    return conversationId;
}


const conversationId =
    getConversationId();


// =========================================================
// DISPLAY MESSAGE
// =========================================================

function addMessage(
    message,
    type
) {

    const wrapper =
        document.createElement("div");

    wrapper.className =
        type === "user"
            ? "message user-message"
            : "message agent-message";


    const avatar =
        document.createElement("div");

    avatar.className =
        "avatar";

    avatar.textContent =
        type === "user"
            ? "YOU"
            : "AI";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    const name =
        document.createElement("div");

    name.className =
        "message-name";

    name.textContent =
        type === "user"
            ? "You"
            : "SupportAI";


    const bubble =
        document.createElement("div");

    bubble.className =
        "bubble";

    bubble.textContent =
        message;


    content.appendChild(
        name
    );

    content.appendChild(
        bubble
    );

    wrapper.appendChild(
        avatar
    );

    wrapper.appendChild(
        content
    );

    chatMessages.appendChild(
        wrapper
    );


    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// =========================================================
// TYPING MESSAGE
// =========================================================

function addTypingMessage() {

    const wrapper =
        document.createElement("div");

    wrapper.id =
        "typingMessage";

    wrapper.className =
        "message agent-message";


    const avatar =
        document.createElement("div");

    avatar.className =
        "avatar";

    avatar.textContent =
        "AI";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    const name =
        document.createElement("div");

    name.className =
        "message-name";

    name.textContent =
        "SupportAI";


    const bubble =
        document.createElement("div");

    bubble.className =
        "bubble";

    bubble.textContent =
        "Thinking...";


    content.appendChild(
        name
    );

    content.appendChild(
        bubble
    );

    wrapper.appendChild(
        avatar
    );

    wrapper.appendChild(
        content
    );

    chatMessages.appendChild(
        wrapper
    );


    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}


// =========================================================
// REMOVE TYPING MESSAGE
// =========================================================

function removeTypingMessage() {

    const typingMessage =
        document.getElementById(
            "typingMessage"
        );


    if (typingMessage) {

        typingMessage.remove();
    }
}


// =========================================================
// SEND MESSAGE
// =========================================================

async function sendMessage() {

    const message =
        messageInput.value.trim();


    if (!message) {

        return;
    }


    const customerName =
        customerNameInput.value.trim();


    const orderId =
        orderIdInput.value.trim();


    // -----------------------------------------------------
    // Show user message
    // -----------------------------------------------------

    addMessage(
        message,
        "user"
    );


    messageInput.value =
        "";


    sendButton.disabled =
        true;


    addTypingMessage();


    try {

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify(
                        {
                            message:
                                message,

                            conversation_id:
                                conversationId,

                            order_id:
                                orderId,

                            customer_name:
                                customerName
                        }
                    )
                }
            );


        if (!response.ok) {

            throw new Error(
                `Server error: ${response.status}`
            );
        }


        const data =
            await response.json();


        removeTypingMessage();


        // -------------------------------------------------
        // Display response
        // -------------------------------------------------

        addMessage(
            data.response ||
            "I couldn't process your request.",
            "agent"
        );


        // -------------------------------------------------
        // Log conversation ID for debugging
        // -------------------------------------------------

        console.log(
            "SupportAI conversation:",
            data.conversation_id
        );


    } catch (error) {

        removeTypingMessage();


        addMessage(
            "Sorry, something went wrong while processing your request.",
            "agent"
        );


        console.error(
            "SupportAI error:",
            error
        );


    } finally {

        sendButton.disabled =
            false;

        messageInput.focus();
    }
}


// =========================================================
// QUICK MESSAGE
// =========================================================

function sendQuickMessage(
    message
) {

    messageInput.value =
        message;

    sendMessage();
}


// =========================================================
// ENTER KEY
// =========================================================

messageInput.addEventListener(
    "keydown",
    function (event) {

        if (event.key === "Enter") {

            event.preventDefault();

            sendMessage();
        }
    }
);


// =========================================================
// INITIAL FOCUS
// =========================================================
