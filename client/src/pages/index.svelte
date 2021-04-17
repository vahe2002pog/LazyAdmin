<script>
    import SelectGroup from "../Components/SelectGroup/SelectGroup.svelte";
    let user = {
        profileUrl: "#",
        name: "Slav Cheems",
        avatar: "https://picsum.photos/200?2",
    };
    let items = [
        {
            imageURL: "https://picsum.photos/200",
            name: "Group1",
            groupURL: "https://music.youtube.com/",
        },
        {
            imageURL: "https://picsum.photos/200?1",
            name: "Group2",
            groupURL: "https://www.reddit.com/",
        },
    ];
</script>

<style lang="less" global>
    @import "../styles/main_page.less";
</style>

<div id="content">
    <div class="header">
        <h1>Ленивый Админ</h1>
        <div style="flex-grow: 1;" />
        <SelectGroup class="selectGroup" header="Выберите сообщество" {items} />
        <div class="user">
            <a href={user.profileUrl} target="_blank" class="user-name">
                {user.name}
            </a>
            <div class="user-avatar">
                <a href={user.profileUrl} target="_blank">
                    <img src={user.avatar} alt={user.name} />
                </a>
            </div>
        </div>
    </div>
    <div>
        
    </div>
</div>
