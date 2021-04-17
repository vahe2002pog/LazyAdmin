<script>
    import { randString } from "../../scripts/functions";
    import { getEventsAction } from "../../scripts/utils.js";
    import { current_component } from "svelte/internal";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();
    const events = getEventsAction(current_component);

    export let checked;
    export let right = false;
    export let style = null;
    export let disabled = false;

    let localClass;
    while (true) {
        let tempClass = "checkbox-" + randString(5);
        if (document.getElementsByClassName(tempClass).length === 0) {
            localClass = tempClass;
            break;
        }
    }

    function toggle() {
        checked = !checked;
        dispatch("change", { checked, class: localClass });
    }
</script>

<style lang="less" global>
    @import "CheckBox.less";
</style>

<div
    class="{localClass} {$$props.class ? $$props.class : ''}{checked ? ' checked' : ''}{right ? ' right' : ''}{disabled ? ' disabled' : ''}"
    use:events
    {style}
    on:click={toggle}>
    <div class="box">
        <span class="check">
            &#10004;
        </span>
    </div>
    <div class="text">
        <slot />
    </div>
</div>
