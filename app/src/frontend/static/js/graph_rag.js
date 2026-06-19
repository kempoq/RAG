import { sendApiRequest } from "./modules/api.js";
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
} from "./modules/rag.js";
import { showLoader, hideLoader } from "./modules/loader.js";

const showMessageText = "Show graph context";
const hideMessageText = "Hide graph context";

function openCommunityModal() {
    document.getElementById("communityModal").classList.remove("hidden");
    document.body.style.overflow = "hidden";
}

function closeCommunityModal() {
    document.getElementById("communityModal").classList.add("hidden");
    document.body.style.overflow = "";
}

function fillCypherQueryOutput(cypherQuery) {
    document.getElementById("cypherQueryOutput").textContent = cypherQuery;
}

function fillGraphDbInfoOutput(graphDbInfo) {
    const graphDbInfoString = JSON.stringify(graphDbInfo, null, 4);

    if (graphDbInfoString.length <= 200) {
        document.getElementById("expandButton").classList.add("hidden");
        document.getElementById("graphDbShortOutput").textContent = graphDbInfoString;
    } else {
        document.getElementById("expandButton").classList.remove("hidden");
        document.getElementById("graphDbShortOutput").textContent = `${graphDbInfoString.slice(0, 200)} ...`;
        document.getElementById("graphDbFullOutput").textContent = graphDbInfoString;
    }
    
}

function clearOutputs() {
    document.getElementById("noRagAnswerOutput").innerHTML = "";
    document.getElementById("answerOutput").innerHTML = "";

    document.getElementById("graphDbShortOutput").textContent = "";
    document.getElementById("graphDbFullOutput").textContent = "";
    document.getElementById("cypherQueryOutput").textContent = "";
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

document.getElementById("expandButton").addEventListener("click", () => {
    openCommunityModal();
});

document.getElementById("modalCloseButton").addEventListener("click", () => {
    closeCommunityModal();
});

document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
        closeCommunityModal();
    }
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
    const response = await sendApiRequest("/api/v1/graph/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Accept-Encoding": "gzip"
        },
        body: {"query": query, "temperature": temperature, "docs_count": docsCount}
    });
    const tokenUsage = response["token_usage"];

    fillAnswerOutput(response["answer"], "answerOutput");
    fillQueryOutput(response["user_query"]);
    fillRelevantInfoOutput(response["vector_db_info"]);
    fillCypherQueryOutput(response["cypher_query"]);
    fillGraphDbInfoOutput(response["graph_db_info"]);

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
})
