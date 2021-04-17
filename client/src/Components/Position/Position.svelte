<script>
    import { randString } from "../../scripts/functions";
    import { getEventsAction } from "../../scripts/utils.js";
    import { current_component } from "svelte/internal";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();
    const events = getEventsAction(current_component);

    export let position = 1;
    export let style = null;
    export let disabled = false;

    let localClass;
    while (true) {
        let tempClass = "position-" + randString(5);
        if (document.getElementsByClassName(tempClass).length === 0) {
            localClass = tempClass;
            setTimeout(() => {
                let elements = document.querySelectorAll(`.${tempClass} div`);
                elements.forEach((element, index) => {
                    element.addEventListener("click", () =>
                        itemClick(index + 1)
                    );
                });
            }, 0);
            break;
        }
    }

    function itemClick(index) {
        dispatch("change", { position: index, pastPosition: position, class: localClass });
        position = index;
    }
</script>

<style lang="less" global>
    @import "Position.less";
</style>

<div
    class="{localClass} {$$props.class ? $$props.class : ''}{disabled ? ' disabled' : ''}"
    use:events
    {style}>
    <div class="rounded-1{position === 1 ? ' pressed' : ''}" />
    <div class={position === 2 ? ' pressed' : ''} />
    <div class="rounded-2{position === 3 ? ' pressed' : ''}" />
    <div class={position === 4 ? ' pressed' : ''} />
    <div class={position === 5 ? ' pressed' : ''} />
    <div class={position === 6 ? ' pressed' : ''} />
    <div class="rounded-3{position === 7 ? ' pressed' : ''}" />
    <div class={position === 8 ? ' pressed' : ''} />
    <div class="rounded-4{position === 9 ? ' pressed' : ''}" />
</div>
