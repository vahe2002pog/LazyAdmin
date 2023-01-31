<script>
    import Icon from "mdi-svelte";
    import { randString } from "../../scripts/functions";
    import { getEventsAction } from "../../scripts/utils.js";
    import { current_component } from "svelte/internal";
    import Position from "../Position/Position.svelte";
    const events = getEventsAction(current_component);

    export let path = null;
    export let style = null;
    export let src = null;
    export let disabled = false;
    export let size = 50;
    export let indents = [1, 1];
    export let position = 5;
    export let opacity = 50;
    export let vertical = false;
    let flexParams = ["start", "center", "end"];
    let watermarkBlockStyle;
    let watermarkStyle;
    let flexParamsIndex;
    let watermarkBoxWidth;
    let watermarkBoxHeight;
    let imgElement;

    let classes = "";
    let localClass;
    while (true) {
        let tempClass = "previewBox-" + randString(5);
        if (document.getElementsByClassName(tempClass).length === 0) {
            localClass = tempClass;
            break;
        }
    }
    initClasses();
    function initClasses() {
        let classesArray = [];
        if ($$props.class) {
            classesArray.push($$props.class);
        }
        if (disabled) {
            classesArray.push("disabled");
        }
        if (vertical) {
            classesArray.push("vertical");
        }
        classes = classesArray.join(" ").trim();
    }

    $: watermarkStyle = `
        max-width: ${size}%;
        max-height: ${size}%;
        opacity: ${opacity / 100};
        margin: ${
            (watermarkBoxHeight / 100) * indents[1] -
            (imgElement?.height / 100) * indents[1]
        }px ${
            (watermarkBoxWidth / 100) * indents[0] -
            (imgElement?.width / 100) * indents[0]}px;`;

        // max-width: ${vertical ? size * 16/9 > 100 ? 100 : size * 16/9: size}%;
        // max-height: ${vertical ? size * 16/9 > 100 ? 100 : size * 16/9: size}%;

    $: flexParamsIndex = position.toString(3).padStart(2, "0").slice("");
    $: watermarkBlockStyle = `
        align-items: ${flexParams[flexParamsIndex[0]]};
        justify-content: ${flexParams[flexParamsIndex[1]]};
        `;
</script>

<div
    class="{localClass} {classes}"
    bind:clientWidth={watermarkBoxWidth}
    bind:clientHeight={watermarkBoxHeight}
    use:events
    {style}
>
    <div class="watermark-block" style={watermarkBlockStyle}>
        <img
            {src}
            bind:this={imgElement}
            style={watermarkStyle}
            alt=""
            class="watermark"
        />
    </div>
    {#if path}
        <div class="icon">
            <Icon {path} />
        </div>
    {/if}
</div>

<style lang="less" global>
    @import "PreviewBox.less";
</style>
