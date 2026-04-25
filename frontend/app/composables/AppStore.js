export const useAppStore = defineStore('app-store', () => {
    const gameStatus = ref(0);

    /**
     * This function sets what status the game is on.
     * @param {Number} status The new game status.
     */
    function setGameStatus(status = 0) {
        gameStatus.value = status;
    }

    return { gameStatus, setGameStatus }
});