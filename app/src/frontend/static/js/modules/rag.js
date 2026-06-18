export function toggleContext(showMessage, hideMessage) {
    const block = document.getElementById("context");
    const label = document.getElementById("toggleLabel");
    const icon = document.getElementById("toggleIcon");
    
    if (block.classList.contains("hidden")) {
        block.classList.remove("hidden");
        label.textContent = hideMessage;
        icon.classList.remove("fa-chevron-down");
        icon.classList.add("fa-chevron-up");
    } else {
        block.classList.add("hidden");
        label.textContent = showMessage;
        icon.classList.remove("fa-chevron-up");
        icon.classList.add("fa-chevron-down");
    }
}

export function autoResizeUserInput(textArea) {
    textArea.style.height = "auto";
    textArea.style.height = Math.min(textArea.scrollHeight, 200) + "px";
}

export function showAnswer(addNoRagRequest) {
    if (addNoRagRequest) {
        document.getElementById("answersContainer").classList.remove("lg:grid-cols-1");
        document.getElementById("answersContainer").classList.add("lg:grid-cols-2");
        document.getElementById("noRagAnswerContainer").classList.remove("hidden");
    } else {
        document.getElementById("answersContainer").classList.remove("lg:grid-cols-2");
        document.getElementById("answersContainer").classList.add("lg:grid-cols-1");
        document.getElementById("noRagAnswerContainer").classList.add("hidden");
    }
    document.getElementById("answerArea").classList.remove("hidden");
}

export function hideOutputs(showMessage) {
    document.getElementById("answerArea").classList.add("hidden");

    const block = document.getElementById("context");
    const label = document.getElementById("toggleLabel");
    const icon = document.getElementById("toggleIcon");

    if (!block.classList.contains("hidden")) {
        block.classList.add("hidden");
        label.textContent = showMessage;
        icon.classList.remove("fa-chevron-up");
        icon.classList.add("fa-chevron-down");
    }
}

export function fillAnswerOutput(answer, elementClass) {
    document.getElementById(elementClass).innerHTML = marked.parse(answer);
    renderMathInElement(document.getElementById(elementClass), {
        delimiters: [
            {left: "$$", right: "$$", display: true},
            {left: "$", right: "$", display: false}
        ],
        throwOnError: false
    });
}

export function fillRelevantInfoOutput(relevantInfo) {
    const relevantInfoContainer = document.getElementById("relevantInfoOutput");

    relevantInfo.forEach(ri => {
        const riString = document.createElement("p");
        riString.classList.add("text-sm", "text-slate-700", "leading-relaxed", "mt-2");
        riString.textContent = ri;
        relevantInfoContainer.appendChild(riString);
    })
}

export function fillQueryOutput(query) {
    document.getElementById("queryOutput").textContent = query;
}

export function mergeTokenUsage(tu1, tu2) {
    // tu1 changes
    Object.keys(tu1).forEach((modelName) => {
        if (Object.hasOwn(tu2, modelName)) {
            if (tu2[modelName] == -1) return;
            tu1[modelName] += tu2[modelName];
        }
    });
}

export function fillTokenUsageOutput(tokenUsage) {
    const usageContainer = document.getElementById("tokenUsageOutput")

    Object.keys(tokenUsage).forEach((modelName) => {
        const usageInfo = document.createElement("p");
        usageInfo.classList.add("text-sm", "text-slate-700", "leading-relaxed");
        usageInfo.innerHTML = `<b>${modelName}</b>: ${tokenUsage[modelName]}`;
        usageContainer.appendChild(usageInfo);
    });
}

export function clearInputs() {
    document.getElementById("userInput").value = "";
    document.getElementById("noRagCheckbox").checked = false;
    document.getElementById("temperatureInput").value = 0;
}