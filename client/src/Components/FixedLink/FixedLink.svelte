<script>
    import { randString } from "../../scripts/functions";
    import { getEventsAction } from "../../scripts/utils.js";
    import { current_component } from "svelte/internal";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();
    const events = getEventsAction(current_component);

    export let style = null;
    export let disabled = false;
    export let fixedLink = "";
    export let placeholder = "";
    export let value = "";
    let localClass;


    while (true) {
        let tempClass = "link-" + randString(5);
        if (document.getElementsByClassName(tempClass).length === 0) {
            localClass = tempClass;
            break;
        }
    }
</script>

<style lang="less" global>
    @import "FixedLink.less";
</style>

<div
    {style}
    class="{$$props.class ? $$props.class : ''} {localClass}{disabled ? ' disabled' : ''}">
    <div class="fixed-field">
        {fixedLink}
    </div>
    <input
        class="input"
        type="text"
        bind:value
        {placeholder}
        use:events/>
</div>
