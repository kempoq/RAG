import { sendApiRequest } from "./modules/api.js"

function showAnswer() {
    document.getElementById("answerArea").classList.remove("hidden");
}

function hideAnswer() {
    document.getElementById("answerArea").classList.add("hidden");
}

function fillAnswerOutput(answer) {
    document.getElementById("answerOutput").innerHTML = marked.parse(answer);
    renderMathInElement(document.getElementById("answerOutput"), {
        delimiters: [
            {left: "$$", right: "$$", display: true},
            {left: "$", right: "$", display: false}
        ],
        throwOnError: false
    });
}

function fillQueryOutput(query) {
    document.getElementById("queryOutput").textContent = query;

}

function fillRelevantInfoOutput(relevantInfo) {
    const relevantInfoContainer = document.getElementById("relevantInfoOutput");

    relevantInfo.forEach(ri => {
        const riString = document.createElement("p");
        riString.classList.add("text-sm", "text-slate-700", "leading-relaxed", "mt-2");
        riString.textContent = ri;
        relevantInfoContainer.appendChild(riString);
    })
}

function clearInput() {
    document.getElementById("userInput").value = "";
}

document.getElementById("toggleButton").addEventListener("click", () => {
    const block = document.getElementById("augmented-query");
    const label = document.getElementById("toggle-label");
    const icon = document.getElementById("toggle-icon");
    
    if (block.classList.contains("hidden")) {
        block.classList.remove("hidden");
        label.textContent = "Hide augmented query";
        icon.classList.remove("fa-chevron-down");
        icon.classList.add("fa-chevron-up");
    } else {
        block.classList.add("hidden");
        label.textContent = "Show augmented query";
        icon.classList.remove("fa-chevron-up");
        icon.classList.add("fa-chevron-down");
    }
})

document.getElementById("sendButton").addEventListener("click", async () => {
    hideAnswer();

    const query = document.getElementById("userInput").value;
    if (query.length === 0) return;

    const response = await sendApiRequest("/api/v1/vector/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: {"query": query}
    });

    fillAnswerOutput(response["answer"]);
    fillQueryOutput(response["query"]);
    fillRelevantInfoOutput(response["relevant_info"]);
    showAnswer();
    clearInput();
})