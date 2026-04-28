import game_py from "@scripts/python/game.py?raw";
import algorithms_py from "@scripts/python/algorithms.py?raw";
import session_py from "@scripts/python/session.py?raw";
import bridge_py from "@scripts/python/bridge.py?raw";
import { loadPyodide } from 'pyodide';

export const useAppStore = defineStore('app-store', () => {
    /** @type {Ref<Array<0 | 1 | 2 | 3 | 4>>} The array of tiles and their state. */
    const tiles = ref([0, 0, 0, 0, 0, 0, 0, 0, 0]);
    const nodesVisited = ref([{ num: 0, turn: -1 }]);

    const gameStatus = ref(0);
    const gameState = ref(null);

    /** @type {Ref<"minimax" | "alpha-beta">} The algorithm to use. */
    const tttAlgorithm = ref("minimax");
    const settingsOpen = ref(false);

    /** @type {Ref<import("pyodide").PyodideAPI>} This is the pyodide object.  */
    const pyodide = ref(null);
    const pyodideReady = ref(false);

    /**
     * This function sets what status the game is on.
     * @param {Number} status The new game status.
     */
    function setGameStatus(status = 0) {
        const oldStatus = gameStatus.value;
        gameStatus.value = status;
        if((oldStatus != 0 && status == 0) || (oldStatus == 0 && status == 1)) { restartGame(); }
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
     * This function sets what algorithm for the ai to use.
     * @param {"minimax" | "alpha-beta"} str the algorithm's name.
     */
    function setTictactoeAlgorithm(str = "minimax") {
        if(gameStatus.value == 0) { tttAlgorithm.value = str; }
    }

    /**
     * This function sets what algorithm for the ai to use.
     * @param {"toggle" | Boolean} status The new status of the settings menu.
     */
    function setSettings(status = "toggle") {
        status = ((gameStatus.value == 0) ? status : false);
        settingsOpen.value = ((status === "toggle") ? !settingsOpen.value : status);
    }

    /** This function returns if the algorithm is the minimax one or not. */
    function checkMinimax() { return (tttAlgorithm.value === "minimax"); }

    /**
     * -----------------------------------------------------------------------------------
     * These functions are for loading the python code with the algorithms and game logic.
     * -----------------------------------------------------------------------------------
     */

    /** This function loads all the python scripts into the app. */
    async function loadPython() {
        pyodide.value = await loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v0.29.3/full/" });
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
        nodesVisited.value = [];
    }

    /**
     * This function runs when a tile is clicked on.
     * @param {0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8} index The tile clicked on.
     */
    function onTileClick(index) {
        if(gameStatus.value != 1 || !pyodideReady.value) { return; }
        const fulfillInputFunc = (checkMinimax() ? `game_controller.fulfill_input(${index})` : `game_controller.fulfill_alpha_input(${index})`)
        const result = pyodide.value.runPython(fulfillInputFunc);

        gameState.value = JSON.parse(result);
        if(import.meta.env.DEV) { console.log(gameState.value); }

        if(!gameState.value.history) { return; }
        const historyLength = gameState.value.history.length;

        for(let i = 0; i < historyLength; i++) {
            const obj = gameState.value.history[i];
            setTile(obj.cell_index, obj.player === "X" ? 1 : 3);

            if(obj.player === "O" && (-1 == nodesVisited.value.findIndex(item => item.turn == obj.move_number))) {
                nodesVisited.value.push({ num: obj.stats.nodes_visited, turn: obj.move_number });
            }
        }

        if(gameState.value.board.winner != null) {
            setGameStatus((gameState.value.board.winner === "X") ? 3 : 4);
            const winningTiles = getWinner(gameState.value.board.cells);

            for(let j = 0; j < winningTiles.length; j++) {
                const tileNum = winningTiles[j]
                setTile(tileNum, tiles.value[tileNum] + 1);
            }

            console.log(nodesVisited.value);
            if(import.meta.env.DEV) { console.log(winningTiles); }
        } else if(historyLength == 9) {
            setGameStatus(2);
            console.log(nodesVisited.value);
        }
    }


    /** This function restarts the game. */
    function restartGame() {
        if(!pyodideReady.value) { return; }
        pyodide.value.runPython(`game_controller.restart()`);
        pyodide.value.runPython(`game_controller.alpha_restart()`);

        tiles.value = [0, 0, 0, 0, 0, 0, 0, 0, 0];
        nodesVisited.value = [];
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

    return { gameStatus, tiles, pyodideReady, tttAlgorithm, settingsOpen,
        setGameStatus, setTile, setTictactoeAlgorithm, setSettings,
        loadPython, onTileClick, restartGame
    }
});