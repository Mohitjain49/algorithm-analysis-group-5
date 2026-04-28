<style scoped>
@import "~/assets/appbar.css";
</style>

<template>
<nav id="tictactoe-app-bar" ref="tictactoe-app-bar">
    <div class="app-bar-section">
        <button v-if="(appStore.gameStatus == 0)" class="tictactoe-app-option" @click="appStore.setGameStatus(1)" title="Play A Game!" pulse-loop>
            <FontAwesomeIcon icon="fa-play" />
        </button>
        <button v-if="(appStore.gameStatus != 0)" class="tictactoe-app-option orange-light" @click="appStore.setGameStatus(0)" title="Reset Board." pulse-loop>
            <FontAwesomeIcon icon="fa-rotate-left" />
        </button>
        <button class="tictactoe-app-option orange" @click="reloadApp()" title="Reload App" pulse-loop>
            <FontAwesomeIcon icon="fa-rotate-right" :spin="reloadButtonClicked" />
        </button>
    </div>

    <div class="app-bar-section">
        <RouterLink class="tictactoe-app-option orange" to="/#version" title="See App Version" pulse-loop>
            <FontAwesomeIcon icon="fa-brands fa-git-alt" />
        </RouterLink>
        <a class="tictactoe-app-option white" :href="PROJECT_GITHUB_LINK" target="tictactoe-project-github" title="Project GitHub" pulse-loop>
            <FontAwesomeIcon icon="fa-brands fa-github" />
        </a>
    </div>
</nav>

<div v-if="showVersionPopup" class="webpage-cover tictactoe-versionCover">
    <div id="version" class="tictactoe-versionBox animate__animated animate__bounceIn">
        <h2 class="tictactoe-versionBox-text version"> {{ APP_VERSION }} </h2>
        <h2 class="tictactoe-versionBox-text"> {{ APP_RELEASE.date }} </h2>
        <h2 class="tictactoe-versionBox-text small"> {{ APP_RELEASE.time }} </h2>

        <RouterLink to="/" class="tictactoe-versionBox-closeBtn" title="Hide App Version">
            <FontAwesomeIcon icon="fa-xmark" />
        </RouterLink>
    </div>
</div>
</template>

<script setup>
const appStore = useAppStore();
const router = useRouter();
const { num: APP_VERSION, release: APP_RELEASE } = useAppVersion();

const appBarRef = useTemplateRef('tictactoe-app-bar');
usePulseLoopAnimation(appBarRef);

const reloadButtonClicked = ref(false);
const playButtonTitle = computed(() => { return ((appStore.gameStatus == 0) ? "Play A Game!" : "Stop Playing.") });
const showVersionPopup = computed(() => { return (router.currentRoute.value.hash === "#version"); });

/** This function reloads the web application. */
function reloadApp() {
    if(reloadButtonClicked.value) { return; }
    reloadButtonClicked.value = true;
    reloadNuxtApp({ force: true });
}
</script>