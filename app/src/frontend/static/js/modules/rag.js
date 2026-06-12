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

export function showAnswer() {
    document.getElementById("answerArea").classList.remove("hidden");
}

export function hideAnswer() {
    document.getElementById("answerArea").classList.add("hidden");
}

export function fillAnswerOutput(answer) {
    document.getElementById("answerOutput").innerHTML = marked.parse(answer);
    renderMathInElement(document.getElementById("answerOutput"), {
        delimiters: [
            {left: "$$", right: "$$", display: true},
            {left: "$", right: "$", display: false}
        ],
        throwOnError: false
    });
}

export function fillQueryOutput(query) {
    document.getElementById("queryOutput").textContent = query;
}

export function clearInput() {
    document.getElementById("userInput").value = "";
}