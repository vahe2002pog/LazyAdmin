<script>
    import SelectGroup from "../Components/SelectGroup/SelectGroup.svelte";
    import { getUser, getGroups } from "../store";

    let user;
    let groups = [];

    getUser().then((response) => {
        user = {
            profileUrl: `https://vk.com/id${response.id}`,
            name: `${response.first_name} ${response.last_name}`,
            avatar: response.photo_100,
        };
    });

    getGroups().then((response) => {
        for (let i = 0; i < response.length; i++) {
            groups.push({
                groupURL: `https://vk.com/${response[i].screen_name}`,
                name: response[i].name,
                imageURL: response[i].photo_50,
            });
        }
        groups = [...groups];
    });
</script>

<style lang="less" global>
    @import "../styles/main_page.less";
</style>

<div id="content">
    <div class="header">
        <h1>Ленивый Админ</h1>
        <div style="flex-grow: 1;" />
        <SelectGroup
            class="selectGroup"
            header="Выберите сообщество"
            items={groups} />
        <div class="user">
            <a href={user?.profileUrl} target="_blank" class="user-name">
                {user?.name}
            </a>
            <div class="user-avatar">
                <a href={user?.profileUrl} target="_blank">
                    <img src={user?.avatar} alt={user?.name} />
                </a>
            </div>
        </div>
    </div>
    <div />
</div>
