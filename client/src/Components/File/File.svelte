<script>
    import Icon from "mdi-svelte";
    import { randString } from "../../scripts/functions";
    import { FileListItems } from "../../scripts/FileListItems";
    import { isValid } from "../../scripts/FileValidate";
    import { getEventsAction } from "../../scripts/utils.js";
    import { current_component } from "svelte/internal";
    import { createEventDispatcher } from "svelte";
    import Button from "../Button/Button.svelte";
    // import { mdiTrayArrowDown } from "@mdi/js";

    const dispatch = createEventDispatcher();
    const events = getEventsAction(current_component);

    export let buttonTitle = "Открыть";
    export let fieldTitle = "Файл не выбран";
    export let multiple = false;
    export let style = null;
    export let files = null;
    export let accept = "*.*";
    export let size = "normal";
    export let mini = false;
    export let disabled = false;
    let title = "Файл не выбран";
    let canDrop = false;
    let localClass;
    let counter = 0;
    let mdiTrayArrowDown =
        "M2 12H4V17H20V12H22V17C22 18.11 21.11 19 20 19H4C2.9 19 2 18.11 2 17V12M12 15L17.55 9.54L16.13 8.13L13 11.25V2H11V11.25L7.88 8.13L6.46 9.55L12 15Z";
    let iconSizes = {
        "x-large": "32px",
        large: "28px",
        normal: "24px",
        small: "20px",
        "x-small": "14px",
    };
    if (Object.keys(iconSizes).indexOf(size) === -1) {
        size = "normal";
    }
    while (true) {
        let tempClass = "file-" + randString(5);
        if (document.getElementsByClassName(tempClass).length === 0) {
            localClass = tempClass;
            break;
        }
    }

    function getFiles(items) {
        let tempFiles = [];
        for (let i = 0; i < items.length; i++) {
            let item = items[i];
            if (item.kind === "file") {
                if (isValid(accept, item.type)) {
                    tempFiles.push(item.getAsFile());
                    if (!multiple) {
                        break;
                    }
                }
            }
        }
        return tempFiles;
    }

    function dropHandler(e) {
        e.preventDefault();
        let items = Object.values(e?.dataTransfer?.items);
        let tempFiles = new FileListItems(getFiles(items));
        if (tempFiles != []) {
            files = new FileListItems(tempFiles);
        }
        changeEvent();
        canDrop = false;
        setTitle();
    }

    function dragLeaveHandler(e) {
        canDrop = false;
    }

    function dragOverHandler(e) {
        e.preventDefault();
        let items = Object.values(e?.dataTransfer?.items);
        if (getFiles(items).length > 0) {
            e.dataTransfer.dropEffect = "move";
            canDrop = true;
        } else {
            e.dataTransfer.dropEffect = "none";
            canDrop = false;
            e.stopPropagation();
        }
    }

    function fileInputChange(e) {
        e.stopPropagation();
        let tempFiles = [];
        Array.from(e.target.files).forEach((file) => {
            if (isValid(accept, file.type)) {
                tempFiles.push(file);
            }
        });
        if (tempFiles != []) {
            files = new FileListItems(tempFiles);
        }
        changeEvent();
        setTitle();
    }

    function setTitle() {
        if (multiple) {
            fieldTitle = "Выбрано файлов: " + files.length;
        } else {
            fieldTitle = files[0].name;
        }
        setNames();
    }

    function setNames() {
        title = "";
        for (let i = 0; i < files.length; i++) {
            title += files[i].name + "\n";
        }
    }

    function changeEvent() {
        dispatch("change", { files, class: localClass });
    }
</script>

<div
    {style}
    class="{$$props.class ? $$props.class : ''} {localClass}{mini
        ? ' mini'
        : ' big'}{canDrop ? ' drop' : ''}{disabled ? ' disabled' : ''}"
    use:events
>
    <input
        id={localClass}
        {multiple}
        type="file"
        {accept}
        on:change={fileInputChange}
    />
    <div class="dropZone"
        on:dragover={dragOverHandler}
        on:drop={dropHandler}
        on:dragenter={dragOverHandler}
        on:dragleave={dragLeaveHandler}>
    </div>
    <div class="field" {title}>
        
        <div class="slot">
            <slot/>
        </div>
        
        <label for={localClass} style="z-index: 1;" class="label">
            <Button
                {size}
                style={mini
                    ? "border-top-left-radius: 36px; border-bottom-left-radius: 36px; margin: 0;"
                    : ""}
            >
                {buttonTitle}
            </Button>
        </label>
        <div class="field-title">
            {#if !mini}
                <br />
            {/if}
            <div class="text {size}">{@html fieldTitle}</div>
            {#if !mini}
                <br />
            {/if}
            {#if !mini}
                <Icon size={iconSizes[size]} path={mdiTrayArrowDown} />
            {/if}
        </div>
        {#if !mini}
            <div class="icon">
                <Icon size={iconSizes[size]} path={mdiTrayArrowDown} />
            </div>
        {/if}
    </div>
</div>

<style lang="less" global>
    @import "File.less";
</style>
