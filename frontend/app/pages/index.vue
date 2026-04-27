<style scoped>
@import "~/assets/homepage.css";
</style>

<template>
<ParticlesBackground :particlesOptions="GREEN_BACKGROUND" />
<AppBar />

<main class="tictactoe-ui">
    <div class="tictactoe-box-background">
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
</template>

<script setup>
const appStore = useAppStore();
useHead(getMeta());
</script>