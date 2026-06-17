import { sendApiRequest } from "./modules/api.js"
import {
    toggleContext,
    showAnswer,
    hideAnswer,
    fillAnswerOutput,
    fillQueryOutput,
    fillRelevantInfoOutput,
    clearInput
} from "./modules/rag.js"
import { showLoader, hideLoader } from "./modules/loader.js";

document.getElementById("toggleButton").addEventListener("click", () => {
    toggleContext("Show augmented query", "Hide augmented query");
})

document.getElementById("sendButton").addEventListener("click", async () => {
    hideAnswer();

    const query = document.getElementById("userInput").value;
    if (query.length === 0) return;

    showLoader("Processing", "Generating answer");
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
    hideLoader();
})