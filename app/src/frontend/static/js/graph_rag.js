import { sendApiRequest } from "./modules/api.js";
import { 
    toggleContext,
    showAnswer,
    hideAnswer,
    fillAnswerOutput,
    fillQueryOutput,
    clearInput
} from "./modules/rag.js";
import { showLoader, hideLoader } from "./modules/loader.js";

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
        document.getElementById("graphDbShortOutput").textContent = `${graphDbInfoString.slice(0, 200)} ...`;
        document.getElementById("graphDbFullOutput").textContent = graphDbInfoString;
    }
    
}

function fillTokenUsageOutput(tokenUsage) {
    document.getElementById("tokenUsageOutput").textContent = tokenUsage;
}

document.getElementById("toggleButton").addEventListener("click", () => {
    toggleContext("Show graph context", "Hide graph context");
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
    hideAnswer();
    
    const query = document.getElementById("userInput").value;
    if (query.length === 0) return;

    showLoader("Processing", "Generating answer");
    const response = await sendApiRequest("/api/v1/graph/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: {"query": query}
    });

    console.log(response);

    fillAnswerOutput(response["answer"]);
    fillQueryOutput(response["user_query"]);
    fillCypherQueryOutput(response["cypher_query"]);
    fillGraphDbInfoOutput(response["graph_db_info"]);
    fillTokenUsageOutput(response["token_usage"]);
    showAnswer();
    clearInput();
    hideLoader();
})
