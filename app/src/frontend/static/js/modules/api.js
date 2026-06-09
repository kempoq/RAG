function convertBodyToString(options) {
    if (typeof options["body"] !== "string")
        options["body"] = JSON.stringify(options["body"]);
}

export async function sendApiRequest(url, options) {
    if (options["headers"] && options["headers"]["Content-Type"])
        convertBodyToString(options);

    const response = await fetch(url, {...options});
    const contentType = response.headers.get("Content-Type");
    var responseContent;

    if (!contentType)
        responseContent = null;
    else if (contentType.includes("json"))
        responseContent = await response.json();
    else
        throw new Error("Not supported Content-Type header");

    if (!response.ok) {
        throw new Error(`Request to API is failed: ${response.status} - ${response.statusText}`)
    }

    return responseContent
}