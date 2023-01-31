<script>
    import Icon from "mdi-svelte";
    import { randString } from "../../scripts/functions";
    import { getEventsAction } from "../../scripts/utils.js";
    import { current_component } from "svelte/internal";
    const events = getEventsAction(current_component);

    export let path = null;
    export let right = false;
    export let size = "normal";
    export let rounded = false;
    export let style = null;
    export let disabled = false;

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
    let slot = false;
    let classes = "";
    let localClass;
    while (true) {
        let tempClass = "button-" + randString(5);
        if (document.getElementsByClassName(tempClass).length === 0) {
            localClass = tempClass;
            break;
        }
    }
    initClasses();
    function initClasses() {
        let classesArray = [];
        if ($$props.$$slots) {
            slot = true;
            if (right) {
                classesArray.push("right");
            }
        }
        if ($$props.class) {
            classesArray.push($$props.class);
        }
        if (rounded) {
            classesArray.push("rounded");
        }
        if (disabled) {
            classesArray.push("disabled");
        }
        classesArray.push(size);
        classes = classesArray.join(" ").trim();
    }
</script>

<style lang="less" global>
    @import "Button.less";
</style>

<div class="{localClass} {classes}" use:events {style}>
    {#if path}
        <Icon size={iconSizes[size]} {path} />
    {/if}

    {#if slot}
        <div class="content">
            <slot />
        </div>
    {/if}
</div>
