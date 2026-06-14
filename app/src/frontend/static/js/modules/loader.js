export function showLoader(title, message) {
    document.getElementById("loaderTitle").textContent = title;
    document.getElementById("loaderMessage").textContent = message;
    document.getElementById("loaderPopup").classList.remove("hidden");
    document.body.style.overflow = "hidden";
}

export function hideLoader() {
    document.getElementById("loaderPopup").classList.add("hidden");
    document.body.style.overflow = "";
}