export function chessmen(matrix) {
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

export function kingPos(bot, player) {
    for (let i = 0; i < bot.length; i++) {
        if (bot[i][1] === 6) {
            bot = bot[i][0]
        }
    }
    for (let i = 0; i < player.length; i++) {
        if (player[i][1] === 12) {
            player = player[i][0]
        }
    }
    return [bot, player]
}