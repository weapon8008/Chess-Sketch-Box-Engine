import fs from "fs"
import path from "path"
import { fileURLToPath } from "url"
import { spawn } from "child_process"
import chessmen from "./js/chess-info.js"


class MatrixOperation {
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
            "row": matrix.length,
            "col": matrix[0].length,
            "matrix": matrix,
            "bot": bot,
            "player": player
        }
    }
}

export default class Board extends MatrixOperation {
    constructor(matrix, playerColor) {
        super()

        this._checkDimention(matrix)
        this._checkMatrix(matrix)
        this._initiateBoardData(matrix)

        startPrediction()

        if (playerColor === "b" || playerColor === "B") {

        } else if (playerColor === "w" || playerColor === "W") {

        } else {
            throw new Error(`${playerColor} is invalid\nValid playerSide:\n\tfor black -> \'B\' or \'b\'\n\tfor white -> \'W\' or \'w\'`)
        }
    }

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
        if (row < 0 || row >= this.boardData.row || col < 0 || col >= this.boardData.col) {
            throw new Error("Invalid position")
        }

        if (this.boardData.matrix[row][col] === 0) {
            return null
        }

        let n = Math.max(this.boardData.row, this.boardData.col)

        return new Promise((resolve, reject) => {
            const py = spawn("python3", [
                path.join(
                    path.dirname(fileURLToPath(import.meta.url)),
                    "python",
                    "show-move.py"
                )
            ])

            let dataString = ""
            let errorString = ""

            py.stdin.write(JSON.stringify({
                row,
                col,
                boardData: this.boardData
            }))

            py.stdin.end()

            py.stdout.on("data", (data) => {
                dataString += data.toString()
            })

            py.stderr.on("data", (err) => {
                errorString += err.toString()
            })

            py.on("close", (code) => {
                if (code !== 0) {
                    return reject(errorString || "Python process failed")
                }

                try {
                    const parsed = JSON.parse(dataString.trim())

                    const result = parsed.map(item => [
                        Math.floor(item[1] / (n * n)) % n,
                        Math.floor(item[1] / (n * n * n))
                    ])

                    resolve(result)
                } catch (err) {
                    reject("Invalid JSON from Python")
                }
            })
        })
    }

    async playMove(old_row, old_col, new_row, new_col, changeChessman = -1) {
        const list = await this.showMoves(old_row, old_col)

        // throws error when the chessman is 0 or donot have any moves
        if (list.length == 0) {
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
        } else {
            throw new Error(`row = ${new_row}\tcol = ${new_col}:\nThis chessman is not valid placement for this chessman`)
        }
    }
}

function startPrediction() {

}

