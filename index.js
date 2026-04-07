import fs from "fs"
import path from "path"
import { fileURLToPath } from "url"
import { spawn } from "child_process"
import chessmen from "./js/chess-info.js"

// go to the chess.config.json
const configPath = path.join(process.cwd(), "chess.config.json")

// read the chess.config.json
// const config = JSON.parse(fs.readFileSync(configPath, "utf-8"))
// export let board = config.matrix

// function getBoard() {
//     return config.matrix
// }

let hasBeenCalled = false

class MatrixOperation {
    constructor(matrix) {
        this.#checkDimention(matrix)
        this.#checkMatrix(matrix)
        this.#updateDimention(matrix)
    }

    // check matrix is valid 2D array
    #checkDimention(matrix) {
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

        // 4. Check number of columns m
        const m = matrix[0].length

        if (m <= 1) {
            throw new Error("Matrix must have more than 1 column (m > 1)")
        }

        // 5. Ensure all rows have equal columns
        for (const row of matrix) {
            if (row.length !== m) {
                throw new Error("All rows must have the same number of columns")
            }
        }

        return true
    }

    // check numbers inside the matrix
    #checkMatrix(matrix) {
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

    // update the config.json for data
    #updateDimention(matrix) {
        const [bot, player] = chessmen(matrix)
        const data = {
            "row":matrix.length,
            "col":matrix[0].length,
            "matrix":matrix,
            "bot":bot,
            "player":player
        }

        // write the .env file
        fs.writeFileSync(configPath, JSON.stringify(data))
    }
}

export function StartBoard(matrix, playerColor) {
    if (hasBeenCalled)
        throw new Error("The board has been initiated before, StartBoard() should not be called more than 1 time")

    hasBeenCalled = true

    new MatrixOperation(structuredClone(matrix))

    startPrediction()

    if (playerColor === "b" || playerColor === "B") {

    } else if (playerColor === "w" || playerColor === "W") {

    } else {
        throw new Error(`${playerColor} is invalid\nValid playerSide:\n\tfor black -> \'B\' or \'b\'\n\tfor white -> \'W\' or \'w\'`)
    }
}

export function showMoves(row, col) {
    if (row < 0 || row >= config.row || col < 0 || col >= config.col) {
        throw new Error("Check the postion i.e. row and column - it is not given in the given matrix")
    } else {
        if (config.matrix[row][col] === 0) {
            return null
        } else {
            let n = (config.row >= config.col) ? config.row:config.col
            return new Promise((resolve, reject) => {
                // makes the python chessman.py file path
                const py = spawn("python3", [path.join(path.dirname(fileURLToPath(import.meta.url)), "python", "show-move.py"), row.toString(), col.toString()])

                let dataString = ""

                // to handle print result
                py.stdout.on("data", (data) => {
                    dataString += data.toString()
                })

                // handle when close
                py.on("close", () => {
                    resolve(JSON.parse(dataString.trim()).map(item => [Math.floor(item[1]/(n*n))%n, Math.floor(item[1]/(n*n*n))]))
                })
            })
        }
    }
}

export async function changeMoves(old_row, old_col, new_row, new_col, changeChessman = -1) {
    const list = await showMoves(old_row, old_col)

    // throws error when the chessman is 0 or donot have any moves
    if (list.length == 0) {
        throw new Error(`row = ${old_row} and col = ${old_col}:\nThis chessman donot have any moves`)
    }

    // check the chessman have valid moves
    if (list.some(([row, col]) => row === new_row && col === new_col)) {
        let matrix = structuredClone(config.matrix)

        // check change chessman validation
        if (changeChessman === -1 && (matrix[old_row][old_col] === 1 || matrix[old_row][old_col] === 7) && (new_row == config.row-1 || new_row == 0)) {
            throw new Error(`changeChessman is not given`)
        }

        // change the bot placement
        if (matrix[old_row][old_col] <= 6) {
            let bot = structuredClone(config.bot)
            let index = bot.findIndex(([[row, col], owner]) => row === old_row && col === old_col && owner === matrix[old_row][old_col])

            // check the change chessman validation
            if (changeChessman > 5 || changeChessman < 2 && (matrix[old_row][old_col] === 1) && (new_row == config.row-1)) {
                throw new Error(`changeChessman: ${changeChessman} is invalid for bot`)
            }

            // check the move will change or not if change then update the bot list in chess.config.json
            if (matrix[old_row][old_col] === 1 && new_row === config.row - 1) {
                bot[index] = [[new_row, new_col], changeChessman]
            } else {
                bot[index] = [[new_row, new_col], matrix[old_row][old_col]]
            }
            config.bot = bot
        } else if (matrix[old_row][old_col] >= 7) {
            let player = structuredClone(config.player)
            let index = player.findIndex(([[row, col], owner]) => row === old_row && col === old_col && owner === matrix[old_row][old_col])

            // check the change chessman validation
            if (changeChessman > 11 || changeChessman < 8 && (matrix[old_row][old_col] === 7) && (new_row == 0)) {
                throw new Error(`changeChessman: ${changeChessman} is invalid for player`)
            }

            // check the move will change or not if change then update the player list in chess.config.json
            if (matrix[old_row][old_col] === 7 && new_row === 0) {
                player[index] = [[new_row, new_col], changeChessman]
            } else {
                player[index] = [[new_row, new_col], matrix[old_row][old_col]]
            }
            config.player = player
        }

        // if any chessman kills the opponent's chessman then delete the killed chessman from the opponent's list in chess.config.json
        if ((matrix[new_row][new_col] <= 6) && (matrix[new_row][new_col] !== 0)) {
            let bot = structuredClone(config.bot)
            let index = bot.findIndex(([[row, col], owner]) => row === new_row && col === new_col && owner === matrix[new_row][new_col])
            bot.splice(index, 1)
            config.bot = bot
        } else if ((matrix[new_row][new_col] >= 7) && (matrix[new_row][new_col] !== 0)) {
            let player = structuredClone(config.player)
            let index = player.findIndex(([[row, col], owner]) => row === new_row && col === new_col && owner === matrix[new_row][new_col])
            player.splice(index, 1)
            config.player = player
        }

        if (matrix[old_row][old_col] === 1 && new_row === config.row - 1) {
            matrix[new_row][new_col] = changeChessman
            matrix[old_row][old_col] = 0
            config.matrix = matrix
        } else if (matrix[old_row][old_col] === 7 && new_row === 0) {
            matrix[new_row][new_col] = changeChessman
            matrix[old_row][old_col] = 0
            config.matrix = matrix
        } else {
            matrix[new_row][new_col] = matrix[old_row][old_col]
            matrix[old_row][old_col] = 0
            config.matrix = matrix
        }

        // rewrite the file
        fs.writeFileSync(configPath, JSON.stringify(config))
    } else {
        throw new Error(`row = ${new_row}\tcol = ${new_col}:\nThis chessman is not valid placement for this chessman`)
    }
}

function startPrediction() {

}

