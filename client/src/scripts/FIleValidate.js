export function isValid(accept, type) {
    accept = accept.split(",").map(item => {return item.trim();});
    if (accept.includes("*.*") || accept.includes(".*") || accept.includes("*/*")) {
        return true;
    }
    if (accept.includes(type)) {
        return true;
    }
    let fileType;
    let fileExtension;
    [fileType, fileExtension] = type.split("/");
    if (accept.includes(fileType + "/*")) {
        return true;
    }
    if (accept.includes("." + fileExtension)) {
        return true;
    }
    return false;
}