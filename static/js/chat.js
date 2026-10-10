const sendBtn = document.getElementById("send-btn");
const input = document.getElementById("message");
const messages = document.querySelector(".messages");

sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});

function sendMessage() {

    const text = input.value.trim();

    if (text === "") return;

    messages.innerHTML += `
        <div class="user-message">
            ${text}
        </div>
    `;

    input.value = "";

    sendBtn.disabled = true;
    input.disabled = true;

    messages.innerHTML += `
        <div class="bot-message thinking" id="thinking">
            Thinking...
        </div>
    `;

    messages.scrollTop = messages.scrollHeight;

    fetch("/ask", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            message: text
        })

    })

    .then(response => response.json())

    .then(data => {

        const thinking = document.getElementById("thinking");

        if (thinking) {
            thinking.remove();
        }

        messages.innerHTML += `
            <div class="bot-message">
                ${marked.parse(data.response)}
            </div>
        `;

        messages.scrollTop = messages.scrollHeight;

        sendBtn.disabled = false;
        input.disabled = false;
        input.focus();

    })

    .catch(error => {

        const thinking = document.getElementById("thinking");

        if (thinking) {
            thinking.remove();
        }

        messages.innerHTML += `
            <div class="bot-message">
                Sorry, something went wrong.
            </div>
        `;

        sendBtn.disabled = false;
        input.disabled = false;
        input.focus();

        console.error(error);

    });

}