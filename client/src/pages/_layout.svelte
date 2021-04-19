<script>
    import { checkAuth, getCookie } from "../store";

    let isAuth = false;
    let showContent = false;

    checkAuth().then((response) => {
        isAuth = response?.auth;
        if (isAuth) {
            if (window.location.pathname === "/login") {
                window.location.pathname = "/";
            }
            else{
                showContent = true;
            }
        } else {
            if(getCookie('token')){
                window.location.pathname = "/api/login";
            }
            else{
                if (window.location.pathname !== "/login") {
                    window.location.pathname = "/login";
                }
                else{
                    showContent = true;
                }
            }
        }
    });
</script>

<style>
    #site-body {
        width: 100%;
        height: 100%;
    }
</style>

<div id="site-body">
    {#if showContent}
        <slot />
    {/if}
</div>
