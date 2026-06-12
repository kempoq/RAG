import { sendApiRequest } from "./modules/api.js"
import {
    toggleContext,
    showAnswer,
    hideAnswer,
    fillAnswerOutput,
    fillQueryOutput,
    clearInput
} from "./modules/rag.js"

function fillRelevantInfoOutput(relevantInfo) {
    const relevantInfoContainer = document.getElementById("relevantInfoOutput");

    relevantInfo.forEach(ri => {
        const riString = document.createElement("p");
        riString.classList.add("text-sm", "text-slate-700", "leading-relaxed", "mt-2");
        riString.textContent = ri;
        relevantInfoContainer.appendChild(riString);
    })
}

document.getElementById("toggleButton").addEventListener("click", () => {
    toggleContext("Show augmented query", "Hide augmented query");
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