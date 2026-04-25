<style scoped>
@import "~/assets/appbar.css";
</style>

<template>
<nav id="tictactoe-app-bar">
    <div class="app-bar-section">
        <button class="tictactoe-app-option" @click="appStore.setGameStatus((appStore.gameStatus == 0) ? 1 : 0)" :title="playButtonTitle">
            <FontAwesomeIcon :icon="((appStore.gameStatus == 0) ? 'fa-play' : 'fa-stop')" />
        </button>
    </div>

    <div class="app-bar-section">
        <button class="tictactoe-app-option orange" @click="reloadApp()" title="Reload App">
            <FontAwesomeIcon icon="fa-rotate-right" :spin="reloadButtonClicked" />
        </button>
        <a class="tictactoe-app-option white" :href="PROJECT_GITHUB_LINK" target="tictactoe-project-github" title="Project GitHub">
            <FontAwesomeIcon icon="fa-brands fa-github" />
        </a>
    </div>
</nav>
</template>

<script setup>
const appStore = useAppStore();
const reloadButtonClicked = ref(false);
const playButtonTitle = computed(() => { return ((appStore.gameStatus == 0) ? "Play A Game!" : "Stop Playing.") });

/** This function reloads the web application. */
function reloadApp() {
    if(reloadButtonClicked.value) { return; }
    reloadButtonClicked.value = true;
    reloadNuxtApp({ force: true });
}
</script>