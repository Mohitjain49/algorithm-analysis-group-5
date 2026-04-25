<style scoped>
@import "~/assets/homepage.css";
</style>

<template>
<ParticlesBackground :particlesOptions="GREEN_BACKGROUND" />
<AppBar />

<main class="tictactoe-ui">
    <div class="tictactoe-box-background">
        <div class="tictactoe-box">
            <div class="item"></div>
            <div class="item"></div>
            <div class="item"></div>
            <div class="item"></div>
            <div class="item"></div>
            <div class="item"></div>
            <div class="item"></div>
            <div class="item"></div>
            <div class="item"></div>
        </div>
    </div>
</main>
</template>

<script setup>
useHead(getMeta());
</script>