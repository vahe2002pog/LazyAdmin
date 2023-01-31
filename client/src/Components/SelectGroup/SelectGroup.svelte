<script>
    import Icon from "mdi-svelte";
    import { clickOutside } from "../../scripts/clickOutside.js";
    import { mdiChevronDown } from "@mdi/js";
    import { randString } from "../../scripts/functions";
    import { getEventsAction } from "../../scripts/utils.js";
    import { current_component } from "svelte/internal";
    import { createEventDispatcher } from "svelte";

    const dispatch = createEventDispatcher();
    const events = getEventsAction(current_component);

    export let header = "";
    export let items = [];
    export let style = null;
    export let disabled = false;

    let chosenItem = undefined;
    let opened = false;
    let selectWidth;
    let localClass;

    while (true) {
        let tempClass = "select-" + randString(5);
        if (document.getElementsByClassName(tempClass).length === 0) {
            localClass = tempClass;
            break;
        }
    }

    function selectArrowClick(e, close = false) {
        if (close) {
            opened = true;
        } else {
            opened = !opened;
        }
        let options = document.querySelector(`.${localClass} .options`);
        if (opened) {
            dispatch('statchange',{"state": "opened", "class": localClass});
            options.style.height = "min-content";
            let height = options.offsetHeight + "px";
            options.style.height = "0px";
            setTimeout(() => {
                options.style.height = height;
            }, 0);
        } else {
            options.style.height = "0px";
            dispatch('statchange',{"state": "opened", "class": localClass});
        }
    }

    function optionClick(item) {
        chosenItem = item;
        selectArrowClick((close = true));
        dispatch('change',{item, "class": localClass});
    }

    setTimeout(() => {
        selectWidth =
            document.getElementsByClassName(localClass)[0]?.offsetWidth +
            20 +
            "px";
    }, 1);
</script>

<style lang="less" global>
    @import "SelectGroup.less";
</style>

<div>
    <div  class="select-container{disabled ? ' disabled' : ''}" style="width: {selectWidth}; {style}">
        <div
            class="{localClass} {$$props.class ? $$props.class : ''}"
            use:clickOutside
            on:click_outside={opened ? (e) => selectArrowClick((e, true)) : () => {}}>
            <div class="header">
                <div class="header-text">
                    {#if chosenItem}
                        <a href={chosenItem.groupURL} target="_blank">
                            {chosenItem.name}
                        </a>
                    {:else}
                        <div>{header}</div>
                    {/if}
                </div>
                <div
                    class={(opened ? 'rotate ' : '') + 'icon pointer'}
                    on:click={selectArrowClick}>
                    <Icon path={mdiChevronDown} />
                </div>
            </div>
            <div class="options">
                {#each items as item}
                    <hr size="5" class="none-rounded" />
                    <div
                        class="item pointer"
                        on:click={() => optionClick(item)}>
                        <img src={item.imageURL} alt="" />
                        <div class="item-text">{item.name}</div>
                    </div>
                {/each}
            </div>
        </div>
    </div>
</div>
