<style scoped>
@import "~/assets/homepage.css";
</style>

<template>
<ParticlesBackground :particlesOptions="GREEN_BACKGROUND" />
<AppBar />

<main class="tictactoe-ui">
    <div class="tictactoe-box-background">
        <div v-if="(appStore.gameStatus != 0)" class="result-tab">
            <div style="width: 22px"></div>
            <span> {{ ((appStore.gameStatus == 1) ? 'Your Turn!' : resultBox) }} </span>
            <button @click="appStore.setGameStatus(0)" title="Reset Board."> <FontAwesomeIcon icon="fa-rotate-left" /> </button>
        </div>

        <div class="tictactoe-box">
            <div v-for="(tile, index) in appStore.tiles"
                :class="['tictactoe-tile', ((tile == 2 || tile == 4) ? 'highlight' : '')]"
                @click="appStore.onTileClick(index)">

                <FontAwesomeIcon v-if="(tile == 1 || tile == 2)" icon="fa-xmark" />
                <FontAwesomeIcon v-if="(tile == 3 || tile == 4)" icon="fa-o" />
            </div>
        </div>
    </div>
</main>

<div v-if="!appStore.pyodideReady" class="webpage-cover center-flex-display">
    <div class="loading-spinner"></div>
</div>
</template>

<script setup>
const appStore = useAppStore();
const resultBox = computed(() => {
    const status = appStore.gameStatus;
    return ((status == 2) ? 'Draw.' : (((status == 3) ? 'Player' : 'Minimax AI') + ' Wins!'));
});

useHead(getMeta());
onMounted(async () => { await appStore.loadPython(); });
</script>