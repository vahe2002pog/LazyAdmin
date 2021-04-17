/**
 * @params {array} files List of file items
 * @return FileList
 */
export function FileListItems(files) {
    let data = new ClipboardEvent("").clipboardData || new DataTransfer()
    for (var i = 0, len = files.length; i < len; i++) {
        data.items.add(files[i]);
    }
    return data.files
}