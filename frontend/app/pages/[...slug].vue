<template></template>

<script setup>
const router = useRouter();
useHead(getMeta("404 Page | Tic-Tac-Toe | Algorithm Analysis Group 5 | CS 4306", "/404"));

// This redirects the user to the homepage.
onBeforeMount(() => {
    const routePath = router.currentRoute.value.path;
    if(routePath === "/version" || routePath.startsWith("/version/")) {
        router.replace("/#version");
    } else if(routePath === "/v" || routePath.startsWith("/v/")) {
        router.replace("/#version");
    } else {
        router.replace("/");
    }
});
</script>