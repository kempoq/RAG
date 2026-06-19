import { sendApiRequest } from "./modules/api.js"
import {
    toggleContext,
    showAnswer,
    hideOutputs,
    fillAnswerOutput,
    fillQueryOutput,
    fillRelevantInfoOutput,
    fillTokenUsageOutput,
    mergeTokenUsage,
    getInputs,
    clearInputs,
    autoResizeUserInput
} from "./modules/rag.js"
import { showLoader, hideLoader } from "./modules/loader.js";

const showMessageText = "Show augmented query";
const hideMessageText = "Hide augmented query";

function clearOutputs() {
    document.getElementById("noRagAnswerOutput").innerHTML = "";
    document.getElementById("answerOutput").innerHTML = "";

    document.getElementById("queryOutput").textContent = "";
    document.getElementById("tokenUsageOutput").textContent = "";

    // Deleting retrieved context
    Array.from(document.getElementById("relevantInfoOutput").children).slice(1).forEach((child) => {
        child.remove();
    });
}

document.getElementById("userInput").addEventListener("input", (e) => {
    autoResizeUserInput(e.target);
})

document.getElementById("toggleButton").addEventListener("click", () => {
    toggleContext(showMessageText, hideMessageText);
});

document.getElementById("sendButton").addEventListener("click", async () => {
    hideOutputs(showMessageText);
    clearOutputs();

    const [ query, addNoRagRequest, temperature, docsCount ] = getInputs();

    if (query.length === 0) {
        alert("Input something");
        return;
    }

    showLoader("Processing", "Generating answer");
    const response = await sendApiRequest("/api/v1/vector/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip"
        },
        body: {"query": query, "temperature": temperature, "docs_count": docsCount}
    });
    const tokenUsage = response["token_usage"];

    fillAnswerOutput(response["answer"], "answerOutput");
    fillQueryOutput(response["query"]);
    fillRelevantInfoOutput(response["relevant_info"]);

    if (addNoRagRequest) {
        const noRagResponse = await sendApiRequest("/api/v1/no-rag/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept-Encoding": "gzip"
            },
            body: {"query": query, "temperature": temperature}
        })
        fillAnswerOutput(noRagResponse["answer"], "noRagAnswerOutput");
        mergeTokenUsage(tokenUsage, noRagResponse["token_usage"]);
    }

    fillTokenUsageOutput(tokenUsage);

    showAnswer(addNoRagRequest);
    clearInputs();
    hideLoader();
});