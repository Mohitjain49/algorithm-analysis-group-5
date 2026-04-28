import game_py from "@scripts/python/game.py?raw";
import algorithms_py from "@scripts/python/algorithms.py?raw";
import session_py from "@scripts/python/session.py?raw";
import bridge_py from "@scripts/python/bridge.py?raw";
import { loadPyodide } from 'pyodide';

export const useAppStore = defineStore('app-store', () => {
    /** @type {Ref<Array<0 | 1 | 2 | 3 | 4>>} The array of tiles and their state. */
    const tiles = ref([0, 0, 0, 0, 0, 0, 0, 0, 0]);
    const gameStatus = ref(0);
    const gameState = ref(null);

    /** @type {Ref<import("pyodide").PyodideAPI>} This is the pyodide object.  */
    const pyodide = ref(null);
    const pyodideReady = ref(false);

    /** This function loads all the python scripts into the app. */
    async function loadPython() {
        pyodide.value = await loadPyodide();
        const files = [
            { name: "game.py", code: game_py },
            { name: "algorithms.py", code: algorithms_py },
            { name: "session.py", code: session_py },
            { name: "bridge.py", code: bridge_py },
        ];
        
        for(const file of files) { pyodide.value.FS.writeFile(file.name, file.code); }
        pyodide.value.runPython("from bridge import game_controller");
        
        pyodideReady.value = true;
        gameState.value = JSON.parse(pyodide.value.runPython(`game_controller.get_state()`));
    }

    /**
     * This function sets what status the game is on.
     * @param {Number} status The new game status.
     */
    function setGameStatus(status = 0) {
        const oldStatus = gameStatus.value;
        gameStatus.value = status;
        if(oldStatus != 0 && status == 0) { restartGame(); }
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
        if(gameStatus.value != 1 || !pyodideReady.value) { return; }
        const result = pyodide.value.runPython(`game_controller.fulfill_input(${index})`);

        gameState.value = JSON.parse(result);
        if(import.meta.env.DEV) { console.log(gameState.value) }

        if(!gameState.value.history) { return; }
        for(let i = 0; i < gameState.value.history.length; i++) {
            const obj = gameState.value.history[i];
            setTile(obj.cell_index, obj.player === "X" ? 1 : 3);
        }

        if(gameState.value.board.winner != null) {
            setGameStatus((gameState.value.board.winner === "X") ? 3 : 4);
            const winningTiles = getWinner(gameState.value.board.cells);

            for(let j = 0; j < winningTiles.length; j++) {
                const tileNum = winningTiles[j]
                setTile(tileNum, tiles.value[tileNum] + 1)
            }
            if(import.meta.env.DEV) { console.log(winningTiles); }
        } else if(gameState.value.history.length == 9) {
            setGameStatus(2);
        }
    }


    /** This function restarts the game. */
    function restartGame() {
        if(!pyodideReady.value) { return; }
        pyodide.value.runPython(`game_controller.restart()`);
        tiles.value = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    }

    /**
     * Determines the winner of a Tic-Tac-Toe game.
     * @param {Array} board - An array of 9 elements.
     */
    function getWinner(board) {
        const WINNING_LINES = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8], // Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8], // Cols
            [0, 4, 8], [2, 4, 6]             // Diagonals
        ];

        for (const [a, b, c] of WINNING_LINES) {
            // Check if the first cell is not empty and matches the other two
            if (board[a] && board[a] === board[b] && board[a] === board[c]) {
                return [a, b, c];
            }
        }
        return [];
    }

    return { gameStatus, tiles, pyodideReady,
        loadPython, setGameStatus, setTile, onTileClick, restartGame
    }
});