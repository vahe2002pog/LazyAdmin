export function isValid(accept, type) {
    accept = accept.split(",");
    for (let i = 0; i < accept.length; i++) {
        accept[i] = accept[i].trim();
    }
    if (accept.includes(type)) {
        return true;
    }
    let fileType = type.split("/")[0];
    let fileExtension = type.split("/")[1];
    if (accept.includes(fileType + "/*")) {
        return true;
    }
    if (accept.includes("." + fileExtension)) {
        return true;
    }
    return false;
}