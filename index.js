import { chessmen, kingPos } from "./js/chess-info.js"
import { PlayerChessman, BotChessman, canMove } from "./js/chessman.js"

class MatrixOperation {
    /**
     * **Get the board data**
     * --------------------
     * 
     * The board data is divided as:
     * ```
     * boardData = {
            "rowlen": matrix.length,
            "collen": matrix[0].length,
            "matrix": matrix,
            "bot": bot,
            "player": player
        }
     * ``` 
     * 
     * ---
     * 
     * **Chessboard Data** (above)
     * ----------
     * - `rowlen` is the metrix's row length
     * - `collen` is the metrix's column length
     * - `metrix` is the metrix
     * - `bot` is the BOT chessmen `[value, [pos_row, pos_col]]`
     * - `player` is the PLAYER chessmen `[value, [pos_row, pos_col]]`
     */
    boardData = undefined

    // check matrix is valid 2D array
    _checkDimention(matrix) {
        // 1. Must be an array
        if (!Array.isArray(matrix)) {
            throw new Error("Matrix must be an array")
        }

        // 2. Must not be 1D (should be array of arrays)
        if (matrix.length <= 1) {
            throw new Error("Matrix must have more than 1 row (n > 1)")
        }

        // 3. Must not be 3D array or mixed
        for (const row of matrix) {
            if (!Array.isArray(row)) {
                throw new Error("Matrix must be 2D (array of arrays). Not a 1D or invalid format")
            }

            // Check row is NOT an array of arrays (to avoid 3D)
            for (const cell of row) {
                if (Array.isArray(cell)) {
                    throw new Error("Matrix must NOT be more than 2D (3D array found)")
                }
            }
        }

        if (matrix[0].length <= 1) {
            throw new Error("Matrix must have more than 1 column (m > 1)")
        }

        // 4. Ensure all rows have equal columns
        for (const row of matrix) {
            if (row.length !== matrix[0].length) {
                throw new Error("All rows must have the same number of columns")
            }
        }

        return true
    }

    // check numbers inside the matrix
    _checkMatrix(matrix) {
        const allowedNumbers = new Set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

        function checkArray(arr) {
            for (const item of arr) {
                if (Array.isArray(item)) {
                    // Recursively check nested arrays
                    checkArray(item)
                } else {
                    if (typeof item !== "number" || !allowedNumbers.has(item)) {
                        throw new Error(
                            "Given matrix contains number out of the pre-set\n" +
                            "\tThe pre-set: {0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}\n" +
                            "Set, the matrix which should not contain any number out of the pre-set"
                        )
                    }
                }
            }
            return true
        }

        return checkArray(matrix)
    }

    // initiate the chess board data
    _initiateBoardData(matrix) {
        const [bot, player] = chessmen(matrix)
        this.boardData = {
            "rowlen": matrix.length,
            "collen": matrix[0].length,
            "matrix": matrix,
            "bot": bot,
            "player": player
        }
    }
}

export default class Board extends MatrixOperation {
    /**
    * **Start your custom chess board**
    * ---------------------------------
    * 
    * **Here**: The matrix is a **n × m** matrix  
    * - **n** (columns) > 1  
    * - **m** (rows) > 1 
    * 
    * ---
    *
    * @param {number[][]} matrix
    * ```
    * [
    *   [A00, A01, ..., A0n],
    *   [A10, A11, ..., A1n],
    *   [..., ..., ..., ...],
    *   [Am0, Am1, ..., Amn]
    * ]
    * ```
    *
    * **Number in the matrix values**:
    * 
    * - **0** - Empty box or no chessman
    * ```Bot```
    * - **1** - Bot Pawn
    * - **2** - Bot Knight
    * - **3** - Bot Bishop
    * - **4** - Bot Rook
    * - **5** - Bot Queen
    * - **6** - Bot King
    * ```Player```
    * - **7** - Player Pawn
    * - **8** - Player Knight
    * - **9** - Player Bishop
    * - **10** - Player Rook
    * - **11** - Player Queen
    * - **12** - Player King
    *  
    * ---
    * 
    * **Steps it follows**
    * --------------
    * - Check matrix is valid 2D array
    * - Check numbers inside the matrix ```[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]```
    * - Initiate the chess ```boardData```
    * 
    * ---
    * 
    * **How to use ?**
    * --------------
    * - **Step1**: create object(obj) = new Board(```matrix```, ```playerColor```)
    * - **Step2**: Then use its variables and methods - `obj`.```boardData```, `obj`.```showMoves(row, col)``` and `obj`.```playeMoves(old_row, old_col, new_row, new_col, changeChessman)```
    */
    constructor(matrix) {
        super()

        this._checkDimention(matrix)
        this._checkMatrix(matrix)
        this._initiateBoardData(matrix)

        let pos = kingPos(this.boardData.bot, this.boardData.player)
        this.#botKing = pos[0]
        this.#playerKing = pos[1]

        startPrediction()
    }

    #botKing
    #playerKing

    /**
     * **Show the moves possible**
     * -------------------------
     * - Calculate the number of moves possible by the desired **chessman** of the current chessboard.
     * - The chessman is ```matrix[row][col]```
     * 
     * @param {number} row
     * This is the chessman ```row``` postion
     * 
     * -
     * @param {number} col
     * This is the chessman ```col``` postion
     * 
     * -
     * 
     * --- 
     * 
     * These are the number of moves the desired chessman can move.
     * @returns {number[][]} 
     * ```
     * [[new_row_1, new_col_1], [new_row2, new_col_2], ..., [new_row_n, new_col_n]]
     * ```
     * If there is no move possible it will return
     * ```
     * [null]
     * ```  
    */
    showMoves(row, col) {
        if (!canMove(this.boardData.matrix, [row, col], this.boardData.rowlen, this.boardData.collen)) {
            return []
        } else {
            if (this.boardData.matrix[row][col] <= 12 && this.boardData.matrix[row][col] > 6) {
                return [...new PlayerChessman(this.boardData.matrix, [row, col], this.boardData.bot, this.boardData.rowlen, this.boardData.collen)]
            } else if (this.boardData.matrix[row][col] <= 6 && this.boardData.matrix[row][col] > 0) {
                return [...new BotChessman(this.boardData.matrix, [row, col], this.boardData.player, this.boardData.rowlen, this.boardData.collen)]
            }
        }
    }

    /**
     * **Play the chessman move**
     * -------------------------
     * - Check whether the desired **chessman** can move in the current chessboard.
     * - Move the **chessman** to new position ```matrix[new_row_1][new_col_1]```
     * - Change the chessman value, if it is `1` or `7`(pawn); which reaches to its opponent's extreme place.   
     * 
     * @param {number} old_row
     * This is the chessman ```old_row``` postion
     * 
     * -
     * @param {number} old_col
     * This is the chessman ```old_col``` postion
     * 
     * -
     * @param {number} new_row
     * This is the chessman ```new_row``` postion
     * 
     * -
     * @param {number} new_col
     * This is the chessman ```new_col``` postion
     * 
     * -
     * @param {number} changeChessman
     * If it needs to changeChessman then only give the chessman value
     * ```
     * default changeChessman = -1
     * 
     * if (matrix[new_row][new_col] == 1 and new_row == rowlen - 1) 
     *      changeChessman = 5 or 4 or 3 or 2
     * else if (matrix[new_row][new_col] == 7 and new_row == 0) 
     *      changeChessman = 11 or 10 or 9 or 8
     * ```
    */
    playMove(old_row, old_col, new_row, new_col, changeChessman = -1) {
        const list = this.showMoves(old_row, old_col)

        // throws error when the chessman is 0 or donot have any moves
        if (list.length === 0) {
            return
        }
        // check the chessman have valid moves
        if (list.some(([row, col]) => row === new_row && col === new_col)) {
            let matrix = this.boardData.matrix

            // check change chessman validation
            if (changeChessman === -1 && (matrix[old_row][old_col] === 1 || matrix[old_row][old_col] === 7) && (new_row === this.boardData.row - 1 || new_row === 0)) {
                throw new Error(`changingChessman is not given`)
            }

            // change the bot placement
            if (matrix[old_row][old_col] <= 6) {
                let bot = this.boardData.bot
                let index = bot.findIndex(([[row, col], owner]) => row === old_row && col === old_col && owner === matrix[old_row][old_col])

                // check the change chessman validation
                if ((changeChessman > 5 || changeChessman < 2) && (matrix[old_row][old_col] === 1) && (new_row == this.boardData.row - 1)) {
                    throw new Error(`changeChessman: ${changeChessman} is invalid for bot`)
                }

                // check the move will change or not if change then update the bot list in chess.this.json
                if (matrix[old_row][old_col] === 1 && new_row === this.boardData.row - 1) {
                    bot[index] = [[new_row, new_col], changeChessman]
                } else {
                    bot[index] = [[new_row, new_col], matrix[old_row][old_col]]
                }
            } else if (matrix[old_row][old_col] >= 7) {
                let player = this.boardData.player
                let index = player.findIndex(([[row, col], owner]) => row === old_row && col === old_col && owner === matrix[old_row][old_col])

                // check the change chessman validation
                if ((changeChessman > 11 || changeChessman < 8) && (matrix[old_row][old_col] === 7) && (new_row == 0)) {
                    throw new Error(`changeChessman: ${changeChessman} is invalid for player`)
                }

                // check the move will change or not if change then update the player list in chess.this.json
                if (matrix[old_row][old_col] === 7 && new_row === 0) {
                    player[index] = [[new_row, new_col], changeChessman]
                } else {
                    player[index] = [[new_row, new_col], matrix[old_row][old_col]]
                }
            }

            // if any chessman kills the opponent's chessman then delete the killed chessman from the opponent's list in chess.this.json
            if ((matrix[new_row][new_col] <= 6) && (matrix[new_row][new_col] !== 0)) {
                let bot = this.boardData.bot
                let index = bot.findIndex(([[row, col], owner]) => row === new_row && col === new_col && owner === matrix[new_row][new_col])
                bot.splice(index, 1)
            } else if ((matrix[new_row][new_col] >= 7) && (matrix[new_row][new_col] !== 0)) {
                let player = this.boardData.player
                let index = player.findIndex(([[row, col], owner]) => row === new_row && col === new_col && owner === matrix[new_row][new_col])
                player.splice(index, 1)
            }

            if (matrix[old_row][old_col] === 1 && new_row === this.boardData.row - 1) {
                matrix[new_row][new_col] = changeChessman
                matrix[old_row][old_col] = 0
            } else if (matrix[old_row][old_col] === 7 && new_row === 0) {
                matrix[new_row][new_col] = changeChessman
                matrix[old_row][old_col] = 0
            } else {
                matrix[new_row][new_col] = matrix[old_row][old_col]
                matrix[old_row][old_col] = 0
            }
        }
    }

    /**
     * **Look after the check**
     * --------------------
     * 
     * This checks that the king of either side is having any check or not.
     * 
     * @returns {boolean[]} 
     * ```
     * [bot, player]
     * ```
     * 
     */
    check() {
        let bot, player
        for (let i = 0; i < this.boardData.bot.length; i++) {
            const list = this.showMoves(this.boardData.bot[i][0][0], this.boardData.bot[i][0][1])
            if (list.some(([r, c]) => r === this.#playerKing[0] && c === this.#playerKing[1])){
                player = true
                break
            }
        }
        for (let i = 0; i < this.boardData.player.length; i++) {
            const list = this.showMoves(this.boardData.player[i][0][0], this.boardData.player[i][0][1])
            if (list.some(([r, c]) => r === this.#botKing[0] && c === this.#botKing[1])){
                bot = true
                break
            }
        }
        return [bot, player]
    }
}

function startPrediction() {

}

