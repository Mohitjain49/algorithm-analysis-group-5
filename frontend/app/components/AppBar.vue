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

        <button v-if="(appStore.gameStatus == 0)" class="tictactoe-app-option" @click="appStore.setSettings(true)" title="Settings Menu" pulse-loop>
            <FontAwesomeIcon icon="fa-gear" />
        </button>
        <div v-if="(appStore.gameStatus > 1)" class="tictactoe-app-option" title="Use (Ctrl + Shift + I) to see the nodes visited." pulse-loop>
            <FontAwesomeIcon icon="fa-circle-nodes" />
        </div>
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
<div v-if="appStore.settingsOpen" class="webpage-cover tictactoe-settingsCover">
    <div id="settings" class="tictactoe-versionBox animate__animated animate__bounceIn">
        <div class="radio-input">
            <input type="radio" value="minimax" v-model="appStore.tttAlgorithm" />
            <label for="minimax"> Minimax Algorithm </label>
        </div>
        <div class="radio-input">
            <input type="radio" value="alpha-beta" v-model="appStore.tttAlgorithm" />
            <label for="alpha-beta"> Alpha-Beta Pruning </label>
        </div>

        <button class="tictactoe-versionBox-closeBtn" @click="appStore.setSettings(false)" title="Hide App Version">
            <FontAwesomeIcon icon="fa-xmark" />
        </button>
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
const showVersionPopup = computed(() => { return (router.currentRoute.value.hash === "#version"); });

/** This function reloads the web application. */
function reloadApp() {
    if(reloadButtonClicked.value) { return; }
    reloadButtonClicked.value = true;
    reloadNuxtApp({ force: true });
}
</script>