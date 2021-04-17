<script>
    import { checkAuth } from "../../store";
    import Button from "../../Components/Button/Button.svelte";
    import { mdiVk } from "@mdi/js";

    let isAuth = true;

    checkAuth().then((response) => {
        isAuth = response?.auth;
        if (isAuth) {
            window.location.pathname = "/";
        }
    });

    function login() {
        window.location.pathname = "/api/login";
    }
</script>

<style lang="less" global>
    #content {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
        & .text{
            text-align: center;
        }
    }
</style>

{#if !isAuth}
    <div id="content">
        <div class="text">
            <h1>Добро пожаловать!</h1>
            <h3>Необходимо авторизоваться через Вконтакте.</h3>
        </div>
        <Button size="large" right path={mdiVk} on:click={login} >Авторизация</Button>
    </div>
{/if}
