import Board from "./index.js"

const board = new Board([
    [4, 2, 3, 5, 6],
    [1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [7, 7, 7, 7, 7],
    [10, 8, 9, 11, 12]
], "b")
console.log("In testing")
// console.log(board)
// console.log(await showMoves(0, 1))
// await changeMoves(0, 1, 3, 2)
// console.log(board)
import readline from "readline"
import { BotChessman } from "./js/chessman.js"

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
})

function ask(question) {
    return new Promise(resolve => rl.question(question, resolve))
}

let loop = true

while (loop) {
    let choice = await ask("Enter 1 : To get the chess board matrix\nEnter 2 : To show the moves\nEnter 3 : To play move\nEnter any other key : To exit\nChoose : ")

    switch (choice) {
        case "2":
            let row = await ask("Enter row number: ")
            let col = await ask("Enter col number: ")
            console.log(await board.showMoves(Number(row), Number(col)))
            break
        case "3":
            let old_row = await ask("Enter current row number: ")
            let old_col = await ask("Enter current col number: ")
            let new_row = await ask("Enter next row number: ")
            let new_col = await ask("Enter next col number: ")
            if ((board.boardData.matrix[Number(old_row)][Number(old_col)] === 1 && Number(new_row) === board.boardData.row - 1) || (board.boardData.matrix[Number(old_row)][Number(old_col)] === 7 && Number(new_row) === 0)) {
                let changeChessman = await ask("Enter new number for the chessman to change to: ")
                board.playMove(Number(old_row), Number(old_col), Number(new_row), Number(new_col), Number(changeChessman))
            } else {
                board.playMove(Number(old_row), Number(old_col), Number(new_row), Number(new_col))
            }
            let [botCheck, playerCheck] = await board.check()
            console.log("Play move")
            console.log(botCheck, playerCheck)
            if (botCheck) 
                console.log("Bot King Check")
            if (playerCheck)
                console.log("Player King Check")
        case "1":
            console.log(board.boardData)
            break
        default:
            console.log("Exiting...")
            loop = false
    }
}

rl.close()
