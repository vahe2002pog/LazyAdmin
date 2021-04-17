<script>
    import { checkAuth } from "../store";

    let isAuth = false;

    if (window.location.pathname !== "/login") {
        checkAuth().then((response) => {
            isAuth = response?.auth;
            if (!isAuth) {
                window.location.pathname = "/login";
            }
        });
    }

</script>

<style>
    #site-body{
        width: 100%;
        height: 100%;
    }
</style>

<div id="site-body">
    <slot />
</div>
