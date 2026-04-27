export const useAppStore = defineStore('app-store', () => {
    /** @type {Ref<Array<0 | 1 | 2 | 3 | 4>>} The array of tiles and their state. */
    const tiles = ref([0, 0, 0, 0, 0, 0, 0, 0, 0]);
    const gameStatus = ref(0);
    const playerTurn = ref(-1);

    /**
     * This function sets what status the game is on.
     * @param {Number} status The new game status.
     */
    function setGameStatus(status = 0) {
        gameStatus.value = status;
    }

    /**
     * This function sets a specific tile to a specific state.
     * @param {0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8} index The tile to set.
     * @param {0 | 1 | 2 | 3 | 4} num The status to set as a number.
     */
    function setTile(index, num = 0) {
        if((index < 0 || index > 8) || (num < 0 || num > 4)) { return; }
        tiles.value[index] = num;
    }

    /**
     * This function runs when a tile is clicked on.
     * @param {0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8} index The tile clicked on.
     */
    function onTileClick(index) {
        setTile(index, (tiles.value[index] == 2 ? 4 : 2));
    }

    return { gameStatus, tiles, playerTurn, setGameStatus, setTile, onTileClick }
});