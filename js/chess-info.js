export default function chessmen(matrix) {
    let bot = []
    let player = []
    for (let i = 0; i < matrix.length; i++) {
        for (let j = 0; j < matrix[0].length; j++) {
            if (matrix[i][j] > 0 && matrix[i][j] <= 6)
                bot.push([[i, j], matrix[i][j]])
            else if (matrix[i][j] >= 7 && matrix[i][j] < 13)
                player.push([[i, j], matrix[i][j]])
        }
    }    
    return [bot, player]
}
