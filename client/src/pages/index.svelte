<script>
    import Icon from "mdi-svelte";
    import SelectGroup from "../Components/SelectGroup/SelectGroup.svelte";
    import CheckBox from "../Components/CheckBox/CheckBox.svelte";
    import RangeSlider from "../Components/RangeSlider/RangeSlider.svelte";
    import Position from "../Components/Position/Position.svelte";
    import Switch from "../Components/Switch/Switch.svelte";
    import FileInput from "../Components/File/File.svelte";
    import FixedLink from "../Components/FixedLink/FixedLink.svelte";
    import PreviewBox from "../Components/PreviewBox/PreviewBox.svelte";
    import Card from "../Components/Card/Card.svelte";
    import { getUser, getGroups, request, getFile } from "../store";
    import { mdiVideo } from "@mdi/js";

    let user;
    let groups = [];
    let active = true;
    let position = 4;
    let size = 50;
    let indents = [0, 0];
    let opacity = 50;
    let watermark = "";
    let videoList = [];

    (function init() {
        getWatermark();
    })();

    function switchChange(e) {
        let wmParams = document.querySelector(".watermark-params");
        if (e.detail.active) {
            wmParams.style.height = "max-content";
            let height = wmParams.offsetHeight + "px";
            wmParams.style.height = "0px";
            setTimeout(() => {
                wmParams.style.height = height;
            }, 0);
        } else {
            wmParams.style.height = "0px";
        }
    }

    function getWatermark() {
        getFile("/user/watermark").then((blub) => {
            if (blub) {
                let reader = new FileReader();
                reader.onload = (e) => {
                    watermark = e.target.result;
                };
                reader.readAsDataURL(blub);
            }
        });
    }

    function getPreview(video) {
        getFile("/user/video/preview/" + video.preview).then((blub) => {
            if (blub) {
                let reader = new FileReader();
                reader.onload = (e) => {
                    video.preview = e.target.result;
                    videoList = videoList.concat([video]);
                };
                reader.readAsDataURL(blub);
            }
        });
    }

    function uploadWatermark(e) {
        let image = e?.detail?.files;
        const formData = new FormData();
        formData.append("file", image[0]);
        request("/user/watermark", "POST", formData, null, null).then(
            (response) => {
                getWatermark();
            }
        );
    }

    function uploadVideos(e) {
        let videos = e?.detail?.files;
        for (let i = 0; i < videos.length; i++) {
            const formData = new FormData();
            formData.append("file", videos[i]);
            request("/user/video", "POST", formData, null, null).then(
                (response) => {
                    getPreview(response);
                }
            );
        }
    }

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

<div class="site">
    <div class="header">
        <h1>Ленивый Админ</h1>
        <div style="flex-grow: 1;" />
        <SelectGroup
            class="selectGroup"
            header="Выберите сообщество"
            items={groups}
        />
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
    <div class="site-body">
        <div class="content">
            <FileInput
                size="large"
                multiple
                buttonTitle="Выберите файл(ы)"
                accept="video/*"
                fieldTitle="или <br>  перетащите их сюда.<br>"
                style="margin: 0;"
                on:change={uploadVideos}
            >
                {#each videoList as video}
                    <Card src={video.preview}>
                        <div
                            style="overflow: hidden;
                        text-overflow: ellipsis;
                        display: -webkit-box;
                        -webkit-line-clamp: 2;
                                line-clamp: 2; 
                        -webkit-box-orient: vertical;"
                            title={video.name}
                        >
                            {video.name}
                        </div>
                        {video.duration}
                    </Card>
                {/each}
            </FileInput>
        </div>
        <div class="menu">
            <div class="text-center" style="margin: 5px 0;">
                Параметры видеозаписей
            </div>
            <div class="stretch">
                <input type="text" placeholder="Название видеозаписей" />
                <textarea
                    cols="30"
                    rows="5"
                    placeholder="Описание видеозаписей"
                />
                <div class="checkboxes">
                    <CheckBox>Зацикливать воспроизведение</CheckBox>
                    <CheckBox>Отключить комментарии</CheckBox>
                    <CheckBox>Приватный доступ</CheckBox>
                </div>
                <FixedLink
                    fixedLink="https://vk.com/"
                    placeholder="Ссылка в видео"
                />
            </div>
            <hr size="8px" />
            <div class="switch-text">
                <div style="margin: 0 20px;">Добавить вотермарку</div>
                <Switch on:change={switchChange} />
            </div>
            <div class="watermark-params">
                <FileInput mini accept="image/*" on:change={uploadWatermark} />
                <div class="controls">
                    <div class="position">
                        <div>Расположение</div>
                        <Position bind:position />
                    </div>
                    <div class="sliders">
                        <div>Размер - {size}</div>
                        <RangeSlider
                            thumb
                            bind:value={size}
                            controls
                            min="0"
                            max="100"
                            step="0.1"
                        />
                        <div>Отступы - ({indents[0]}; {indents[1]})</div>
                        <RangeSlider
                            thumb
                            bind:value={indents[0]}
                            controls
                            min="0"
                            max="50"
                            step="0.1"
                        />
                        <RangeSlider
                            thumb
                            bind:value={indents[1]}
                            controls
                            min="0"
                            max="50"
                            step="0.1"
                        />
                    </div>
                </div>
                <div class="text-center">Прозрачность - {opacity}%</div>
                <RangeSlider
                    thumb
                    bind:value={opacity}
                    controls
                    min="0"
                    max="100"
                    step="1"
                />
                <div class="text-center">Предпросмотр</div>
                <div class="preview-boxes">
                    <PreviewBox
                        path={mdiVideo}
                        {size}
                        {indents}
                        {opacity}
                        {position}
                        src={watermark}
                        vertical
                        style="width:100%"
                    />
                    <PreviewBox
                        path={mdiVideo}
                        {size}
                        {indents}
                        {opacity}
                        {position}
                        src={watermark}
                        style="width:100%"
                    />
                </div>
            </div>
        </div>
    </div>
</div>

<style lang="less" global>
    @import "../styles/main_page.less";
</style>
