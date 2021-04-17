<script>
    import { randString } from "../../scripts/functions";
    import { getEventsAction } from "../../scripts/utils.js";
    import { current_component } from "svelte/internal";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();
    const events = getEventsAction(current_component);

    export let active;
    export let style = null;
    export let disabled = false;

    let localClass;
    while (true) {
        let tempClass = "switch-" + randString(5);
        if (document.getElementsByClassName(tempClass).length === 0) {
            localClass = tempClass;
            break;
        }
    }

    function toggle(){
        active = !active;
        dispatch('change', {active, "class": localClass});
    }

</script>

<style lang="less" global>
    @import "Switch.less";
</style>
<div {style} class="{localClass} {$$props.class ? $$props.class : ''}{active ? " active": ""}{disabled ? ' disabled' : ''}" use:events on:click={toggle}>
    <div class="track">
        <div class="thumb"></div>
    </div>
</div>
