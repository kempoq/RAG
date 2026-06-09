import { sendApiRequest } from "./modules/api.js";

let selectedFiles = [];

function renderEmbeddedFiles(filesList, filesInfo) {
    for (const fileInfo of filesInfo) {
        const parentDiv = document.createElement("div");
        const iconContainer = document.createElement("div");
        const icon = document.createElement("i");
        const fileInfoContainer = document.createElement("div");
        const filename = document.createElement("p");

        parentDiv.classList.add(
            "px-6", "py-4", "flex", "items-center", "gap-4", "hover:bg-slate-50", "transition-colors"
        );
        iconContainer.classList.add(
            "w-10", "h-10", "rounded-lg", "bg-red-100", "flex", "items-center", "justify-center", "shrink-0"
        );
        icon.classList.add("fa-solid", "fa-file-lines", "text-red-600");
        filename.classList.add("text-sm", "font-medium", "text-slate-900");

        filename.textContent = fileInfo;

        fileInfoContainer.appendChild(filename);
        iconContainer.appendChild(icon);
        parentDiv.appendChild(iconContainer);
        parentDiv.appendChild(fileInfoContainer);
        filesList.appendChild(parentDiv);
    }
}

function fillFilesList(filesInfo) {
    const filesList = document.getElementById("documentsList");
    filesList.removeChild(filesList.lastElementChild);

    renderEmbeddedFiles(filesList, filesInfo["files"]);
}

function fillStorageInfo(storageInfo) {
    document.getElementById("totalDocumentsValue").textContent = storageInfo["total_docs"];
    document.getElementById("embeddingModelName").textContent = storageInfo["embedding_model"];
}

function initUploadArea() {
    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const selectedFilesContainer = document.getElementById("selected-files");
    const uploadAction = document.getElementById("upload-action");

    function removeFile(index) {
        selectedFiles.splice(index, 1);
        renderSelectedFiles();
    }

    function formatSize(bytes) {
        if (bytes < 1024) return `${bytes} B`;
        if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
        return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
    }

    function renderSelectedFile(fileInfo, index) {
        const parentDiv = document.createElement("div");
        const iconContainer = document.createElement("div");
        const icon = document.createElement("i");
        const fileInfoContainer = document.createElement("div");
        const filenameString = document.createElement("p");
        const fileSizeString = document.createElement("p");
        const button = document.createElement("button")
        const buttonIcon = document.createElement("i");

        parentDiv.classList.add(
            "flex", "items-center", "gap-3", "bg-slate-50", "rounded-lg", "border", "border-slate-200", "px-4", "py-3"
        );
        iconContainer.classList.add(
            "w-8", "h-8", "rounded-lg", "bg-slate-100", "flex", "items-center", "justify-center", "shrink-0"
        );
        icon.classList.add("fa-solid", "fa-file-lines", "text-slate-600", "text-sm");
        fileInfoContainer.classList.add("flex-1", "min-w-0");
        filenameString.classList.add("text-sm", "font-medium", "text-slate-900", "truncate")
        fileSizeString.classList.add("text-xs", "text-slate-500");
        button.classList.add("text-slate-400", "hover:text-red-600", "transition-colors");
        buttonIcon.classList.add("fa-solid", "fa-xmark");

        filenameString.textContent = fileInfo.name;
        fileSizeString.textContent = formatSize(fileInfo.size);

        button.addEventListener("click", () => removeFile(index));

        iconContainer.appendChild(icon);
        fileInfoContainer.appendChild(filenameString);
        fileInfoContainer.appendChild(fileSizeString);
        button.appendChild(buttonIcon);
        parentDiv.appendChild(iconContainer);
        parentDiv.appendChild(fileInfoContainer);
        parentDiv.appendChild(button);
        selectedFilesContainer.appendChild(parentDiv);
    }

    function renderSelectedFiles() {
        if (selectedFiles.length === 0) {
            selectedFilesContainer.classList.add("hidden");
            uploadAction.classList.add("hidden");
            selectedFilesContainer.innerHTML = "";
            return;
        }

        selectedFilesContainer.classList.remove("hidden");
        uploadAction.classList.remove("hidden");
        selectedFilesContainer.innerHTML = "";

        selectedFiles.forEach((file, index) => {
            renderSelectedFile(file, index);
        });
    }

    function handleFiles(fileList) {
        if (selectedFiles.length == 5) return;

        Array.from(fileList).forEach(file => {
            const ext = file.name.split(".").pop().toLowerCase();
            if (ext !== "txt") return;

            if (selectedFiles.some(f => f.name === file.name && f.size === file.size)) return;
            
            selectedFiles.push(file);
        });
        renderSelectedFiles();
    }

    dropZone.addEventListener("click", () => fileInput.click());
    fileInput.addEventListener("change", (e) => {
        handleFiles(e.target.files);
        fileInput.value = "";
    });
    dropZone.addEventListener("dragover", (e) => {
        e.preventDefault();
        dropZone.classList.add("border-indigo-400", "bg-indigo-50/30");
    });
    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("border-indigo-400", "bg-indigo-50/30");
    });
    dropZone.addEventListener("drop", (e) => {
        e.preventDefault();
        dropZone.classList.remove("border-indigo-400", "bg-indigo-50/30");
        handleFiles(e.dataTransfer.files);
    });
}


document.addEventListener("DOMContentLoaded", async () => {
    const filesInfo = await sendApiRequest("/api/v1/vector/storage/docs", { method: "GET" });
    const storageInfo = await sendApiRequest("/api/v1/vector/storage/info", { method: "GET" });

    fillFilesList(filesInfo);
    fillStorageInfo(storageInfo);
    initUploadArea();
});

document.getElementById("uploadButton").addEventListener("click", () => {
    console.log(selectedFiles)
})
