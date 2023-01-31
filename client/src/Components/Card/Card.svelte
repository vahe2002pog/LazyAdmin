<script>
    import { randString } from "../../scripts/functions";
    import { getEventsAction } from "../../scripts/utils.js";
    import { current_component } from "svelte/internal";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();
    const events = getEventsAction(current_component);

    export let style = null;
    export let src;
    export let disabled = false;

    let localClass;
    while (true) {
        let tempClass = "card-" + randString(5);
        if (document.getElementsByClassName(tempClass).length === 0) {
            localClass = tempClass;
            break;
        }
    }

</script>

<style lang="less" global>
    @import "Card.less";
</style>

<div
    class="{localClass} {$$props.class ? $$props.class : ''}{disabled ? ' disabled' : ''}"
    use:events
    {style}>
    <div class="image-container">
        <img {src} alt="">
    </div>
    <hr size="5" >
    <div class="text">
        <slot/>
    </div>
</div>
