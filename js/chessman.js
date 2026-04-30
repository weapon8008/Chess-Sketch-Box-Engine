let ROWLEN = 0
let COLLEN = 0

export function canMove(matrix, pos, ROWLEN, COLLEN) {
    const [row, col] = pos

    const inBounds = (r, c) =>
        r >= 0 && r < ROWLEN && c >= 0 && c < COLLEN

    const val = matrix[row][col]

    if (val === 1) {
        if (inBounds(row + 1, col - 1) && matrix[row + 1][col - 1] > 6) return true
        if (inBounds(row + 1, col + 1) && matrix[row + 1][col + 1] > 6) return true
        if (inBounds(row + 1, col) && matrix[row + 1][col] === 0) return true
        return false
    }

    else if (val === 2) {
        const moves = [
            [row - 2, col + 1], [row - 1, col + 2],
            [row + 1, col + 2], [row + 2, col + 1],
            [row + 2, col - 1], [row + 1, col - 2],
            [row - 1, col - 2], [row - 2, col - 1]
        ]

        return moves.some(([r, c]) =>
            inBounds(r, c) && (matrix[r][c] > 6 || matrix[r][c] === 0)
        )
    }

    else if (val === 3) {
        const moves = [
            [row - 1, col + 1], [row + 1, col + 1],
            [row + 1, col - 1], [row - 1, col - 1]
        ]

        return moves.some(([r, c]) =>
            inBounds(r, c) && (matrix[r][c] > 6 || matrix[r][c] === 0)
        )
    }

    else if (val === 4) {
        const moves = [
            [row - 1, col], [row, col + 1],
            [row + 1, col], [row, col - 1]
        ]

        return moves.some(([r, c]) =>
            inBounds(r, c) && (matrix[r][c] > 6 || matrix[r][c] === 0)
        )
    }

    else if (val === 5 || val === 6) {
        const moves = [
            [row - 1, col], [row - 1, col + 1], [row, col + 1],
            [row + 1, col + 1], [row + 1, col], [row + 1, col - 1],
            [row, col - 1], [row - 1, col - 1]
        ]

        return moves.some(([r, c]) =>
            inBounds(r, c) && (matrix[r][c] > 6 || matrix[r][c] === 0)
        )
    }

    else if (val === 7) {
        if (inBounds(row - 1, col - 1) && matrix[row - 1][col - 1] <= 6 && matrix[row - 1][col - 1] !== 0) return true
        if (inBounds(row - 1, col + 1) && matrix[row - 1][col + 1] <= 6 && matrix[row - 1][col + 1] !== 0) return true
        if (inBounds(row - 1, col) && matrix[row - 1][col] === 0) return true
        return false
    }

    else if (val === 8) {
        const moves = [
            [row - 2, col + 1], [row - 1, col + 2],
            [row + 1, col + 2], [row + 2, col + 1],
            [row + 2, col - 1], [row + 1, col - 2],
            [row - 1, col - 2], [row - 2, col - 1]
        ]

        return moves.some(([r, c]) =>
            inBounds(r, c) && matrix[r][c] <= 6
        )
    }

    else if (val === 9) {
        const moves = [
            [row - 1, col + 1], [row + 1, col + 1],
            [row + 1, col - 1], [row - 1, col - 1]
        ]

        return moves.some(([r, c]) =>
            inBounds(r, c) && matrix[r][c] <= 6
        )
    }

    else if (val === 10) {
        const moves = [
            [row - 1, col], [row, col + 1],
            [row + 1, col], [row, col - 1]
        ]

        return moves.some(([r, c]) =>
            inBounds(r, c) && matrix[r][c] <= 6
        )
    }

    else if (val === 11 || val === 12) {
        const moves = [
            [row - 1, col], [row - 1, col + 1], [row, col + 1],
            [row + 1, col + 1], [row + 1, col], [row + 1, col - 1],
            [row, col - 1], [row - 1, col - 1]
        ]

        return moves.some(([r, c]) =>
            inBounds(r, c) && matrix[r][c] <= 6
        )
    }

    return false
}

export class PlayerChessman {
    constructor(matrix, pos, bot, rowlen, collen) {
        this.matrix = matrix.map(row => [...row])
        this.pos = pos
        this.bot = bot
        ROWLEN = rowlen
        COLLEN = collen
    }

    [Symbol.iterator]() {
        const [row, col] = this.pos
        const piece = this.matrix[row][col]

        if (piece === 7) {
            return this.#pawn(row, col)[Symbol.iterator]()
        } else if (piece === 8) {
            return this.#knight(row, col)[Symbol.iterator]()
        } else if (piece === 9) {
            return this.#bishop(row, col)[Symbol.iterator]()
        } else if (piece === 10) {
            return this.#rook(row, col)[Symbol.iterator]()
        } else if (piece === 11) {
            return this.#queen(row, col)[Symbol.iterator]()
        } else if (piece === 12) {
            return this.#king(row, col)[Symbol.iterator]()
        }
        return [][Symbol.iterator]()
    }

    #filterEnemy(arg) {
        const [enemy, row, col] = arg
        if (this.matrix[enemy[0]][enemy[1]] === 1) {
            if (enemy[0] === row - 2 && enemy[1] === col - 2) {
                return [1]
            } else if (enemy[0] === row - 2 && enemy[1] === col - 1) {
                return [2]
            } else if (enemy[0] === row - 2 && enemy[1] === col) {
                return [1, 3]
            } else if (enemy[0] === row - 2 && enemy[1] === col + 1) {
                return [2]
            } else if (enemy[0] === row - 2 && enemy[1] === col + 2) {
                return [3]
            } else if (enemy[0] === row - 1 && enemy[1] === col - 2) {
                return [4]
            } else if (enemy[0] === row - 1 && enemy[1] === col) {
                return [4, 5]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 2) {
                return [5]
            } else if (enemy[0] === row && enemy[1] === col - 2) {
                return [6]
            } else if (enemy[0] === row && enemy[1] === col - 1) {
                return [7]
            } else if (enemy[0] === row && enemy[1] === col + 1) {
                return [7]
            } else if (enemy[0] === row && enemy[1] === col + 2) {
                return [8]
            }
        } else if (this.matrix[enemy[0]][enemy[1]] === 2) {
            if (enemy[0] === row - 3 && enemy[1] === col - 2) {
                return [1]
            } else if (enemy[0] === row - 3 && enemy[1] === col - 1) {
                return [2]
            } else if (enemy[0] === row - 3 && enemy[1] === col) {
                return [1, 3]
            } else if (enemy[0] === row - 3 && enemy[1] === col + 1) {
                return [2]
            } else if (enemy[0] === row - 3 && enemy[1] === col + 2) {
                return [3]
            } else if (enemy[0] === row - 2 && enemy[1] === col - 3) {
                return [1]
            } else if (enemy[0] === row - 2 && enemy[1] === col - 2) {
                return [2, 4]
            } else if (enemy[0] === row - 2 && enemy[1] === col - 1) {
                return [3]
            } else if (enemy[0] === row - 2 && enemy[1] === col) {
                return [4, 5]
            } else if (enemy[0] === row - 2 && enemy[1] === col + 1) {
                return [1]
            } else if (enemy[0] === row - 2 && enemy[1] === col + 2) {
                return [2, 5]
            } else if (enemy[0] === row - 2 && enemy[1] === col + 3) {
                return [3]
            } else if (enemy[0] === row - 1 && enemy[1] === col - 3) {
                return [4]
            } else if (enemy[0] === row - 1 && enemy[1] === col - 2) {
                return [6]
            } else if (enemy[0] === row - 1 && enemy[1] === col - 1) {
                return [5, 7]
            } else if (enemy[0] === row - 1 && enemy[1] === col) {
                return [6, 8]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 1) {
                return [4, 7]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 2) {
                return [8]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 3) {
                return [5]
            } else if (enemy[0] === row && enemy[1] === col - 3) {
                return [1, 6]
            } else if (enemy[0] === row && enemy[1] === col - 2) {
                return [2, 7]
            } else if (enemy[0] === row && enemy[1] === col - 1) {
                return [3, 8]
            } else if (enemy[0] === row && enemy[1] === col + 1) {
                return [1, 6]
            } else if (enemy[0] === row && enemy[1] === col + 2) {
                return [2, 7]
            } else if (enemy[0] === row && enemy[1] === col + 3) {
                return [3, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 3) {
                return [4]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 2) {
                return [1]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 1) {
                return [2, 5]
            } else if (enemy[0] === row + 1 && enemy[1] === col) {
                return [1, 3]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 1) {
                return [2, 4]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 2) {
                return [3]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 3) {
                return [5]
            } else if (enemy[0] === row + 2 && enemy[1] === col - 3) {
                return [6]
            } else if (enemy[0] === row + 2 && enemy[1] === col - 2) {
                return [4, 7]
            } else if (enemy[0] === row + 2 && enemy[1] === col - 1) {
                return [8]
            } else if (enemy[0] === row + 2 && enemy[1] === col) {
                return [4, 5]
            } else if (enemy[0] === row + 2 && enemy[1] === col + 1) {
                return [6]
            } else if (enemy[0] === row + 2 && enemy[1] === col + 2) {
                return [5, 7]
            } else if (enemy[0] === row + 2 && enemy[1] === col + 3) {
                return [8]
            } else if (enemy[0] === row - 3 && enemy[1] === col - 2) {
                return [6]
            } else if (enemy[0] === row - 3 && enemy[1] === col - 1) {
                return [7]
            } else if (enemy[0] === row - 3 && enemy[1] === col) {
                return [6, 8]
            } else if (enemy[0] === row - 3 && enemy[1] === col + 1) {
                return [7]
            } else if (enemy[0] === row - 3 && enemy[1] === col + 2) {
                return [8]
            }
        } else if (this.matrix[enemy[0]][enemy[1]] === 3) {
            if (enemy[0] === row + 2 && enemy[1] === col) {
                return [6, 8]
            } else if (
                (enemy[0] === row + 1 && enemy[1] === col) ||
                (enemy[0] === row - 1 && enemy[1] === col)
            ) {
                return [4, 5]
            } else if (enemy[0] === row - 2 && enemy[1] === col) {
                return [1, 3]
            } else if (enemy[0] === row && enemy[1] === col + 2) {
                return [3, 8]
            } else if (
                (enemy[0] === row && enemy[1] === col + 1) ||
                (enemy[0] === row && enemy[1] === col - 1)
            ) {
                return [2, 7]
            } else if (enemy[0] === row && enemy[1] === col - 2) {
                return [1, 6]
            } else {
                if (
                    enemy[0] !== row - 1 &&
                    enemy[1] !== col - 1 &&
                    Math.abs(enemy[0] - (row - 1)) === Math.abs(enemy[1] - (col - 1))
                ) {
                    if (
                        enemy[0] !== row + 1 &&
                        enemy[1] !== col + 1 &&
                        Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - (col + 1))
                    ) {
                        if (enemy[0] < row - 1 && enemy[1] < col - 1) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] + x] !== 0) return null
                            }
                            if (this.matrix[row - 1][col - 1] !== 0) return [1]
                        } else if (enemy[0] > row + 1 && enemy[1] > col + 1) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] - x] !== 0) return null
                            }
                            if (this.matrix[row + 1][col + 1] !== 0) return [8]
                        }
                        return [1, 8]
                    } else {
                        if (enemy[0] < row - 1 && enemy[1] > col - 1) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] - x] !== 0) return null
                            }
                        } else if (enemy[0] > row - 1 && enemy[1] < col - 1) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] + x] !== 0) return null
                            }
                        }
                        return [1]
                    }
                } else if (
                    enemy[0] !== row - 1 &&
                    enemy[1] !== col &&
                    Math.abs(enemy[0] - (row - 1)) === Math.abs(enemy[1] - col)
                ) {
                    if (
                        enemy[0] !== row &&
                        enemy[1] !== col + 1 &&
                        Math.abs(enemy[0] - row) === Math.abs(enemy[1] - (col + 1))
                    ) {
                        if (enemy[0] < row - 1 && enemy[1] < col) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] + x] !== 0) return null
                            }
                            if (this.matrix[row - 1][col] !== 0) return [2]

                        } else if (enemy[0] > row && enemy[1] > col + 1) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] - x] !== 0) return null
                            }
                            if (this.matrix[row][col + 1] !== 0) return [5]
                        }
                        return [2, 5]
                    } else if (
                        enemy[0] !== row &&
                        enemy[1] !== col - 1 &&
                        Math.abs(enemy[0] - row) === Math.abs(enemy[1] - (col - 1))
                    ) {
                        if (enemy[0] < row - 1 && enemy[1] > col) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] - x] !== 0) return null
                            }
                            if (this.matrix[row - 1][col] !== 0) return [2]

                        } else if (enemy[0] > row && enemy[1] < col - 1) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] + x] !== 0) return null
                            }
                            if (this.matrix[row][col - 1] !== 0) return [4]
                        }
                        return [2, 4]
                    }
                }
            }
        } else if (this.matrix[enemy[0]][enemy[1]] === 4) {
            if (enemy[0] === row - 1 && enemy[1] === col - 1) {
                if (this.matrix[row][col - 1] !== 0 && this.matrix[row - 1][col] !== 0) {
                    return [2, 4]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 4, 6]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [2, 3, 4]
                } else {
                    return [2, 3, 4, 6]
                }
            } else if (enemy[0] === row - 1 && enemy[1] === col) {
                return [1, 3, 7]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 1) {
                if (this.matrix[row][col + 1] !== 0 && this.matrix[row - 1][col] !== 0) {
                    return [2, 5]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 5, 8]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [1, 2, 5]
                } else {
                    return [1, 2, 5, 8]
                }
            } else if (enemy[0] === row && enemy[1] === col - 1) {
                return [1, 5, 6]
            } else if (enemy[0] === row && enemy[1] === col + 1) {
                return [3, 4, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 1) {
                if (this.matrix[row][col - 1] !== 0 && this.matrix[row + 1][col] !== 0) {
                    return [4, 7]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [1, 4, 7]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [4, 7, 8]
                } else {
                    return [1, 4, 7, 8]
                }
            } else if (enemy[0] === row + 1 && enemy[1] === col) {
                return [2, 6, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 1) {
                if (this.matrix[row][col + 1] !== 0 && this.matrix[row + 1][col] !== 0) {
                    return [5, 7]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [3, 5, 7]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [5, 6, 7]
                } else {
                    return [3, 5, 6, 7]
                }
            } else {
                if (enemy[0] === row - 1) {
                    if (enemy[1] < col - 1) {
                        for (let x = enemy[1] + 1; x < col - 1; x++) {
                            if (this.matrix[row - 1][x] !== 0) return null
                        }
                        if (this.matrix[row - 1][col - 1] !== 0) return [1]
                        else if (this.matrix[row - 1][col] !== 0) return [1, 2]
                    } else if (enemy[1] > col + 1) {
                        for (let x = col + 2; x < enemy[1]; x++) {
                            if (this.matrix[row - 1][x] !== 0) return null
                        }
                        if (this.matrix[row - 1][col + 1] !== 0) return [3]
                        else if (this.matrix[row - 1][col] !== 0) return [2, 3]
                    }
                    return [1, 2, 3]
                } else if (enemy[0] === row) {
                    if (enemy[1] < col - 1) {
                        for (let x = enemy[1] + 1; x < col - 1; x++) {
                            if (this.matrix[row][x] !== 0) return null
                        }
                        if (this.matrix[row][col - 1] !== 0) return [4]
                    } else if (enemy[1] > col + 1) {
                        for (let x = col + 2; x < enemy[1]; x++) {
                            if (this.matrix[row][x] !== 0) return null
                        }
                        if (this.matrix[row][col + 1] !== 0) return [5]
                    }
                    return [4, 5]
                } else if (enemy[0] === row + 1) {
                    if (enemy[1] < col - 1) {
                        for (let x = enemy[1] + 1; x < col - 1; x++) {
                            if (this.matrix[row + 1][x] !== 0) return null
                        }
                        if (this.matrix[row + 1][col - 1] !== 0) return [6]
                        else if (this.matrix[row + 1][col] !== 0) return [6, 7]
                    } else if (enemy[1] > col + 1) {
                        for (let x = col + 2; x < enemy[1]; x++) {
                            if (this.matrix[row + 1][x] !== 0) return null
                        }
                        if (this.matrix[row + 1][col + 1] !== 0) return [8]
                        else if (this.matrix[row + 1][col] !== 0) return [7, 8]
                    }
                    return [6, 7, 8]
                } else if (enemy[1] === col - 1) {
                    if (enemy[0] < row - 1) {
                        for (let x = enemy[0] + 1; x < row - 1; x++) {
                            if (this.matrix[x][col - 1] !== 0) return null
                        }
                        if (this.matrix[row - 1][col - 1] !== 0) return [1]
                        else if (this.matrix[row][col - 1] !== 0) return [1, 4]

                    } else if (enemy[0] > row + 1) {
                        for (let x = row + 2; x < enemy[0]; x++) {
                            if (this.matrix[x][col - 1] !== 0) return null
                        }
                        if (this.matrix[row + 1][col - 1] !== 0) return [6]
                        else if (this.matrix[row][col - 1] !== 0) return [4, 6]
                    }
                    return [1, 4, 6]
                } else if (enemy[1] === col) {
                    if (enemy[0] < row - 1) {
                        for (let x = enemy[0] + 1; x < row - 1; x++) {
                            if (this.matrix[x][col] !== 0) return null
                        }
                        if (this.matrix[row - 1][col] !== 0) return [2]
                    } else if (enemy[0] > row + 1) {
                        for (let x = row + 2; x < enemy[0]; x++) {
                            if (this.matrix[x][col] !== 0) return null
                        }
                        if (this.matrix[row + 1][col] !== 0) return [7]
                    }
                    return [2, 7]
                } else if (enemy[1] === col + 1) {
                    if (enemy[0] < row - 1) {
                        for (let x = enemy[0] + 1; x < row - 1; x++) {
                            if (this.matrix[x][col + 1] !== 0) return null
                        }
                        if (this.matrix[row - 1][col + 1] !== 0) return [3]
                        else if (this.matrix[row][col + 1] !== 0) return [3, 5]
                    } else if (enemy[0] > row + 1) {
                        for (let x = row + 2; x < enemy[0]; x++) {
                            if (this.matrix[x][col + 1] !== 0) return null
                        }
                        if (this.matrix[row + 1][col + 1] !== 0) return [8]
                        else if (this.matrix[row][col + 1] !== 0) return [5, 8]
                    }
                    return [3, 5, 8]
                }
            }
        } else if (this.matrix[enemy[0]][enemy[1]] === 5) {
            if (enemy[0] === row - 1 && enemy[1] === col - 1) {
                if (this.matrix[row - 1][col] !== 0 && this.matrix[row][col - 1] !== 0) {
                    return [2, 4, 8]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 4, 6, 8]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [2, 3, 4, 8]
                } else {
                    return [2, 3, 4, 6, 8]
                }
            } else if (enemy[0] === row - 1 && enemy[1] === col) {
                return [1, 3, 4, 5, 7]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 1) {
                if (this.matrix[row - 1][col] !== 0 && this.matrix[row][col + 1] !== 0) {
                    return [2, 5, 6]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 5, 6, 8]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [1, 2, 5, 6]
                } else {
                    return [1, 2, 5, 6, 8]
                }
            } else if (enemy[0] === row && enemy[1] === col - 1) {
                return [1, 2, 5, 6, 7]
            } else if (enemy[0] === row && enemy[1] === col + 1) {
                return [2, 3, 4, 7, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 1) {
                if (this.matrix[row + 1][col] !== 0 && this.matrix[row][col - 1] !== 0) {
                    return [3, 4, 7]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [1, 3, 4, 7]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [3, 4, 7, 8]
                } else {
                    return [1, 3, 4, 7, 8]
                }
            } else if (enemy[0] === row + 1 && enemy[1] === col) {
                return [2, 4, 5, 6, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 1) {
                if (this.matrix[row + 1][col] !== 0 && this.matrix[row][col + 1] !== 0) {
                    return [1, 5, 7]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [1, 3, 5, 7]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [1, 5, 6, 7]
                } else {
                    return [1, 3, 5, 6, 7]
                }
            } else if (enemy[0] === row - 2 && enemy[1] === col - 1) {
                if (this.matrix[row - 1][col - 1] !== 0 && this.matrix[row - 1][col] !== 0) {
                    return [1, 2]
                } else if (this.matrix[row][col - 1] !== 0 && this.matrix[row - 1][col] !== 0) {
                    return [1, 2, 4]
                } else if (this.matrix[row - 1][col - 1] !== 0) {
                    return [1, 2, 5]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [1, 2, 4, 6]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [1, 2, 4, 5]
                } else {
                    return [1, 2, 4, 5, 6]
                }
            } else if (enemy[0] === row - 2 && enemy[1] === col) {
                if (this.matrix[row - 1][col] !== 0) {
                    return [1, 2, 3]
                } else {
                    return [1, 2, 3, 7]
                }
            } else if (enemy[0] === row - 2 && enemy[1] === col + 1) {
                if (this.matrix[row - 1][col + 1] !== 0 && this.matrix[row - 1][col] !== 0) {
                    return [2, 3]
                } else if (this.matrix[row][col + 1] !== 0 && this.matrix[row - 1][col] !== 0) {
                    return [2, 3, 5]
                } else if (this.matrix[row - 1][col + 1] !== 0) {
                    return [2, 3, 4]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 3, 5, 8]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [2, 3, 4, 5]
                } else {
                    return [2, 3, 4, 5, 8]
                }
            } else if (enemy[0] === row - 1 && enemy[1] === col - 2) {
                if (this.matrix[row - 1][col - 1] !== 0 && this.matrix[row][col - 1] !== 0) {
                    return [1, 4]
                } else if (this.matrix[row - 1][col] !== 0 && this.matrix[row][col - 1] !== 0) {
                    return [1, 2, 4]
                } else if (this.matrix[row - 1][col - 1] !== 0) {
                    return [1, 4, 7]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [1, 2, 4, 7]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [1, 2, 3, 4]
                } else {
                    return [1, 2, 3, 4, 7]
                }
            } else if (enemy[0] === row && enemy[1] === col - 2) {
                if (this.matrix[row][col - 1] !== 0) {
                    return [1, 4, 6]
                } else {
                    return [1, 4, 5, 6]
                }
            } else if (enemy[0] === row + 1 && enemy[1] === col - 2) {
                if (this.matrix[row + 1][col - 1] !== 0 && this.matrix[row][col - 1] !== 0) {
                    return [4, 6]
                } else if (this.matrix[row + 1][col] !== 0 && this.matrix[row][col - 1] !== 0) {
                    return [4, 6, 7]
                } else if (this.matrix[row + 1][col - 1] !== 0) {
                    return [2, 4, 6]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [2, 4, 6, 7]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [4, 6, 7, 8]
                } else {
                    return [2, 4, 6, 7, 8]
                }
            } else if (enemy[0] === row + 2 && enemy[1] === col - 1) {
                if (this.matrix[row + 1][col - 1] !== 0 && this.matrix[row + 1][col] !== 0) {
                    return [6, 7]
                } else if (this.matrix[row][col - 1] !== 0 && this.matrix[row + 1][col] !== 0) {
                    return [4, 6, 7]
                } else if (this.matrix[row + 1][col - 1] !== 0) {
                    return [5, 6, 7]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [1, 4, 6, 7]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [4, 5, 6, 7]
                } else {
                    return [1, 4, 5, 6, 7]
                }
            } else if (enemy[0] === row + 2 && enemy[1] === col) {
                if (this.matrix[row + 1][col] !== 0) {
                    return [6, 7, 8]
                } else {
                    return [2, 6, 7, 8]
                }
            } else if (enemy[0] === row + 2 && enemy[1] === col + 1) {
                if (this.matrix[row + 1][col + 1] !== 0 && this.matrix[row + 1][col] !== 0) {
                    return [7, 8]
                } else if (this.matrix[row][col + 1] !== 0 && this.matrix[row + 1][col] !== 0) {
                    return [5, 7, 8]
                } else if (this.matrix[row + 1][col + 1] !== 0) {
                    return [4, 7, 8]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [3, 5, 7, 8]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [4, 5, 7, 8]
                } else {
                    return [3, 4, 5, 7, 8]
                }
            } else if (enemy[0] === row - 1 && enemy[1] === col + 2) {
                if (this.matrix[row - 1][col + 1] !== 0 && this.matrix[row][col + 1] !== 0) {
                    return [3, 5]
                } else if (this.matrix[row - 1][col] !== 0 && this.matrix[row][col + 1] !== 0) {
                    return [2, 3, 5]
                } else if (this.matrix[row - 1][col + 1] !== 0) {
                    return [3, 5, 7]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 3, 5, 7]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [1, 2, 3, 5]
                } else {
                    return [1, 2, 3, 5, 7]
                }
            } else if (enemy[0] === row && enemy[1] === col + 2) {
                if (this.matrix[row][col + 1] !== 0) {
                    return [3, 5, 8]
                } else {
                    return [3, 4, 5, 8]
                }
            } else if (enemy[0] === row + 1 && enemy[1] === col + 2) {
                if (this.matrix[row + 1][col + 1] !== 0 && this.matrix[row][col + 1] !== 0) {
                    return [5, 8]
                } else if (this.matrix[row + 1][col] !== 0 && this.matrix[row][col + 1] !== 0) {
                    return [5, 7, 8]
                } else if (this.matrix[row + 1][col + 1] !== 0) {
                    return [2, 5, 8]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [2, 5, 7, 8]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [5, 6, 7, 8]
                } else {
                    return [2, 5, 6, 7, 8]
                }
            } else if (enemy[0] === row - 3 && enemy[1] === col - 1) {
                if (this.matrix[row - 2][col - 1] !== 0 && this.matrix[row - 2][col] !== 0) {
                    return null
                } else if (this.matrix[row - 2][col - 1] !== 0) {
                    return [3]
                } else if (this.matrix[row - 2][col] !== 0) {
                    return [1]
                } else if (this.matrix[row - 1][col - 1] !== 0) {
                    return [1, 3]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [1, 4, 3]
                } else {
                    return [1, 3, 4, 6]
                }
            } else if (enemy[0] === row - 3 && enemy[1] === col) {
                if (this.matrix[row - 2][col] !== 0) {
                    return null
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2]
                } else {
                    return [2, 7]
                }
            } else if (enemy[0] === row - 3 && enemy[1] === col + 1) {
                if (this.matrix[row - 2][col + 1] !== 0 && this.matrix[row - 2][col] !== 0) {
                    return null
                } else if (this.matrix[row - 2][col + 1] !== 0) {
                    return [1]
                } else if (this.matrix[row - 2][col] !== 0) {
                    return [3]
                } else if (this.matrix[row - 1][col + 1] !== 0) {
                    return [1, 3]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [1, 3, 5]
                } else {
                    return [1, 3, 5, 8]
                }
            } else if (enemy[0] === row - 1 && enemy[1] === col - 3) {
                if (this.matrix[row - 1][col - 2] !== 0 && this.matrix[row][col - 2] !== 0) {
                    return null
                } else if (this.matrix[row - 1][col - 2] !== 0) {
                    return [6]
                } else if (this.matrix[row][col - 2] !== 0) {
                    return [1]
                } else if (this.matrix[row - 1][col - 1] !== 0) {
                    return [1, 6]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [1, 2, 6]
                } else {
                    return [1, 2, 3, 6]
                }
            } else if (enemy[0] === row && enemy[1] === col - 3) {
                if (this.matrix[row][col - 2] !== 0) {
                    return null
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [4]
                } else {
                    return [4, 5]
                }
            } else if (enemy[0] === row + 1 && enemy[1] === col - 3) {
                if (this.matrix[row + 1][col - 2] !== 0 && this.matrix[row][col - 2] !== 0) {
                    return null
                } else if (this.matrix[row + 1][col - 2] !== 0) {
                    return [1]
                } else if (this.matrix[row][col - 2] !== 0) {
                    return [6]
                } else if (this.matrix[row + 1][col - 1] !== 0) {
                    return [1, 6]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [1, 6, 7]
                } else {
                    return [1, 3, 4, 6]
                }
            } else if (enemy[0] === row + 3 && enemy[1] === col - 1) {
                if (this.matrix[row + 2][col - 1] !== 0 && this.matrix[row + 2][col] !== 0) {
                    return null
                } else if (this.matrix[row + 2][col - 1] !== 0) {
                    return [8]
                } else if (this.matrix[row + 2][col] !== 0) {
                    return [6]
                } else if (this.matrix[row + 1][col - 1] !== 0) {
                    return [6, 8]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [4, 6, 8]
                } else {
                    return [1, 4, 6, 8]
                }
            } else if (enemy[0] === row + 3 && enemy[1] === col) {
                if (this.matrix[row + 2][col] !== 0) {
                    return null
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [7]
                } else {
                    return [2, 7]
                }
            } else if (enemy[0] === row + 3 && enemy[1] === col + 1) {
                if (this.matrix[row + 2][col + 1] !== 0 && this.matrix[row + 2][col] !== 0) {
                    return null
                } else if (this.matrix[row + 2][col + 1] !== 0) {
                    return [6]
                } else if (this.matrix[row + 2][col] !== 0) {
                    return [8]
                } else if (this.matrix[row + 1][col + 1] !== 0) {
                    return [6, 8]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [5, 6, 8]
                } else {
                    return [3, 5, 6, 8]
                }
            } else if (enemy[0] === row - 1 && enemy[1] === col + 3) {
                if (this.matrix[row - 1][col + 2] !== 0 && this.matrix[row][col + 2] !== 0) {
                    return null
                } else if (this.matrix[row - 1][col + 2] !== 0) {
                    return [8]
                } else if (this.matrix[row + 2][col] !== 0) {
                    return [3]
                } else if (this.matrix[row - 1][col + 1] !== 0) {
                    return [3, 8]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 3, 8]
                } else {
                    return [1, 2, 3, 8]
                }
            } else if (enemy[0] === row && enemy[1] === col + 3) {
                if (this.matrix[row][col + 2] !== 0) {
                    return null
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [5]
                } else {
                    return [4, 5]
                }
            } else if (enemy[0] === row + 1 && enemy[1] === col + 3) {
                if (this.matrix[row + 1][col + 2] !== 0 && this.matrix[row][col + 2] !== 0) {
                    return null
                } else if (this.matrix[row + 1][col + 2] !== 0) {
                    return [3]
                } else if (this.matrix[row + 2][col] !== 0) {
                    return [8]
                } else if (this.matrix[row + 1][col + 1] !== 0) {
                    return [3, 8]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [3, 7, 8]
                } else {
                    return [3, 6, 7, 8]
                }
            } else if (
                (
                    ((enemy[0] >= 0 && enemy[0] < row - 3) || (enemy[0] > row + 3 && enemy[0] < ROWLEN)) &&
                    (enemy[1] >= col - 1 && enemy[1] <= col + 1)
                ) ||
                (
                    ((enemy[1] >= 0 && enemy[1] < col - 3) || (enemy[1] > col + 3 && enemy[1] < COLLEN)) &&
                    (enemy[0] >= row - 1 && enemy[0] <= row + 1)
                )
            ) {
                if (enemy[0] === row - 1) {
                    if (enemy[1] < col - 1) {
                        for (let x = enemy[1] + 1; x < col - 1; x++) {
                            if (this.matrix[row - 1][x] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row - 1][col - 1] !== 0) {
                            return [1]
                        } else if (this.matrix[row - 1][col] !== 0) {
                            return [1, 2]
                        }
                    } else if (enemy[1] > col + 1) {
                        for (let x = col + 2; x < enemy[1]; x++) {
                            if (this.matrix[row - 1][x] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row - 1][col + 1] !== 0) {
                            return [3]
                        } else if (this.matrix[row - 1][col] !== 0) {
                            return [2, 3]
                        }
                    }
                    return [1, 2, 3]
                } else if (enemy[0] === row) {
                    if (enemy[1] < col - 1) {
                        for (let x = enemy[1] + 1; x < col - 1; x++) {
                            if (this.matrix[row][x] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row][col - 1] !== 0) {
                            return [4]
                        }
                    } else if (enemy[1] > col + 1) {
                        for (let x = col + 2; x < enemy[1]; x++) {
                            if (this.matrix[row][x] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row][col + 1] !== 0) {
                            return [5]
                        }
                    }
                    return [4, 5]
                } else if (enemy[0] === row + 1) {
                    if (enemy[1] < col - 1) {
                        for (let x = enemy[1] + 1; x < col - 1; x++) {
                            if (this.matrix[row + 1][x] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row + 1][col - 1] !== 0) {
                            return [6]
                        } else if (this.matrix[row + 1][col] !== 0) {
                            return [6, 7]
                        }
                    } else if (enemy[1] > col + 1) {
                        for (let x = col + 2; x < enemy[1]; x++) {
                            if (this.matrix[row + 1][x] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row + 1][col + 1] !== 0) {
                            return [8]
                        } else if (this.matrix[row + 1][col] !== 0) {
                            return [7, 8]
                        }
                    }
                    return [6, 7, 8]
                } else if (enemy[1] === col - 1) {
                    if (enemy[0] < row - 1) {
                        for (let x = enemy[0] + 1; x < row - 1; x++) {
                            if (this.matrix[x][col - 1] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row - 1][col - 1] !== 0) {
                            return [1]
                        } else if (this.matrix[row][col - 1] !== 0) {
                            return [1, 4]
                        }
                    } else if (enemy[0] > row + 1) {
                        for (let x = row + 2; x < enemy[0]; x++) {
                            if (this.matrix[x][col - 1] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row + 1][col - 1] !== 0) {
                            return [6]
                        } else if (this.matrix[row][col - 1] !== 0) {
                            return [4, 6]
                        }
                    }
                    return [1, 4, 6]
                } else if (enemy[1] === col) {
                    if (enemy[0] < row - 1) {
                        for (let x = enemy[0] + 1; x < row - 1; x++) {
                            if (this.matrix[x][col] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row - 1][col] !== 0) {
                            return [2]
                        }
                    } else if (enemy[0] > row + 1) {
                        for (let x = row + 2; x < enemy[0]; x++) {
                            if (this.matrix[x][col] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row + 1][col] !== 0) {
                            return [7]
                        }
                    }
                    return [2, 7]
                } else if (enemy[1] === col + 1) {
                    if (enemy[0] < row - 1) {
                        for (let x = enemy[0] + 1; x < row - 1; x++) {
                            if (this.matrix[x][col + 1] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row - 1][col + 1] !== 0) {
                            return [3]
                        } else if (this.matrix[row][col + 1] !== 0) {
                            return [3, 5]
                        }
                    } else if (enemy[0] > row + 1) {
                        for (let x = row + 2; x < enemy[0]; x++) {
                            if (this.matrix[x][col + 1] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row + 1][col + 1] !== 0) {
                            return [8]
                        } else if (this.matrix[row][col + 1] !== 0) {
                            return [5, 8]
                        }
                    }
                    return [3, 5, 8]
                }
            } else {
                if (
                    enemy[0] !== (row - 1) &&
                    enemy[1] !== (col - 1) &&
                    Math.abs(enemy[0] - (row - 1)) === Math.abs(enemy[1] - (col - 1))
                ) {
                    if (
                        enemy[0] !== (row + 1) &&
                        enemy[1] !== (col + 1) &&
                        Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - (col + 1))
                    ) {
                        if (enemy[0] < (row - 1) && enemy[1] < (col - 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row - 1][col - 1] !== 0) {
                                return [1]
                            }
                        } else if (enemy[0] > (row + 1) && enemy[1] > (col + 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row + 1][col + 1] !== 0) {
                                return [8]
                            }
                        }
                        return [1, 8]
                    } else {
                        if (enemy[0] < (row - 1) && enemy[1] > (col - 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                        } else if (enemy[0] > (row - 1) && enemy[1] < (col - 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                        }
                        return [1]
                    }
                } else if (
                    enemy[0] !== (row - 1) &&
                    enemy[1] !== col &&
                    Math.abs(enemy[0] - (row - 1)) === Math.abs(enemy[1] - col)
                ) {
                    if (
                        enemy[0] !== row &&
                        enemy[1] !== (col + 1) &&
                        Math.abs(enemy[0] - row) === Math.abs(enemy[1] - (col + 1))
                    ) {
                        if (enemy[0] < (row - 1) && enemy[1] < col) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row - 1][col] !== 0) {
                                return [2]
                            }
                        } else if (enemy[0] > row && enemy[1] > (col + 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row][col + 1] !== 0) {
                                return [5]
                            }
                        }
                        return [2, 5]
                    } else if (
                        enemy[0] !== row &&
                        enemy[1] !== (col - 1) &&
                        Math.abs(enemy[0] - row) === Math.abs(enemy[1] - (col - 1))
                    ) {
                        if (enemy[0] < (row - 1) && enemy[1] > col) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row - 1][col] !== 0) {
                                return [2]
                            }
                        } else if (enemy[0] > row && enemy[1] < (col - 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row][col - 1] !== 0) {
                                return [4]
                            }
                        }
                        return [2, 4]
                    }
                } else if (
                    enemy[0] !== (row - 1) &&
                    enemy[1] !== (col + 1) &&
                    Math.abs(enemy[0] - (row - 1)) === Math.abs(enemy[1] - (col + 1))
                ) {
                    if (
                        enemy[0] !== (row + 1) &&
                        enemy[1] !== (col - 1) &&
                        Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - (col - 1))
                    ) {
                        if (enemy[0] < (row - 1) && enemy[1] > (col + 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row - 1][col + 1] !== 0) {
                                return [3]
                            }
                        } else if (enemy[0] > (row + 1) && enemy[1] < (col - 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row + 1][col - 1] !== 0) {
                                return [6]
                            }
                        }
                        return [3, 6]
                    } else {
                        if (enemy[0] < (row - 1) && enemy[1] < (col + 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                        } else if (enemy[0] > (row - 1) && enemy[1] > (col + 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                        }
                        return [3]
                    }
                } else if (
                    enemy[0] !== row &&
                    enemy[1] !== (col - 1) &&
                    Math.abs(enemy[0] - row) === Math.abs(enemy[1] - (col - 1))
                ) {
                    if (
                        enemy[0] !== (row + 1) &&
                        enemy[1] !== col &&
                        Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - col)
                    ) {
                        if (enemy[0] < row && enemy[1] < (col - 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row - 1][col] !== 0) {
                                return [4]
                            }
                        } else if (enemy[0] > (row + 1) && enemy[1] > col) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row + 1][col] !== 0) {
                                return [7]
                            }
                        }

                        return [4, 7]
                    }
                } else if (
                    enemy[0] !== row &&
                    enemy[1] !== (col + 1) &&
                    Math.abs(enemy[0] - row) === Math.abs(enemy[1] - (col + 1))
                ) {
                    if (
                        enemy[0] !== (row + 1) &&
                        enemy[1] !== col &&
                        Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - col)
                    ) {
                        if (enemy[0] < row && enemy[1] > (col + 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row][col + 1] !== 0) {
                                return [5]
                            }
                        } else if (enemy[0] > (row + 1) && enemy[1] < col) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row + 1][col] !== 0) {
                                return [7]
                            }
                        }
                        return [5, 7]
                    }
                } else if (
                    enemy[0] !== (row + 1) &&
                    enemy[1] !== (col - 1) &&
                    Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - (col - 1))
                ) {
                    if (enemy[0] < (row + 1) && enemy[1] < (col - 1)) {
                        for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                            if (this.matrix[enemy[0] + x][enemy[1] + x] !== 0) {
                                return null
                            }
                        }
                    } else if (enemy[0] > (row + 1) && enemy[1] > (col - 1)) {
                        for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                            if (this.matrix[enemy[0] - x][enemy[1] - x] !== 0) {
                                return null
                            }
                        }
                    }
                    return [6]
                } else if (
                    enemy[0] !== (row + 1) &&
                    enemy[1] !== (col + 1) &&
                    Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - (col + 1))
                ) {
                    if (enemy[0] < (row + 1) && enemy[1] > (col + 1)) {
                        for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                            if (this.matrix[enemy[0] + x][enemy[1] - x] !== 0) {
                                return null
                            }
                        }
                    } else if (enemy[0] > (row + 1) && enemy[1] < (col + 1)) {
                        for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                            if (this.matrix[enemy[0] - x][enemy[1] + x] !== 0) {
                                return null
                            }
                        }
                    }
                    return [8]
                }
            }
        } else if (this.matrix[enemy[0]][enemy[1]] === 6) {
            if (enemy[0] === row - 2 && enemy[1] === col - 2) {
                return [1]
            } else if (enemy[0] === row - 2 && enemy[1] === col - 1) {
                return [1, 2]
            } else if (enemy[0] === row - 2 && enemy[1] === col) {
                return [1, 2, 3]
            } else if (enemy[0] === row - 2 && enemy[1] === col + 1) {
                return [2, 3]
            } else if (enemy[0] === row - 2 && enemy[1] === col + 2) {
                return [3]
            } else if (enemy[0] === row - 1 && enemy[1] === col - 2) {
                return [1, 4]
            } else if (enemy[0] === row - 1 && enemy[1] === col - 1) {
                return [2, 4]
            } else if (enemy[0] === row - 1 && enemy[1] === col) {
                return [1, 3, 4, 5]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 1) {
                return [2, 5]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 2) {
                return [3, 5]
            } else if (enemy[0] === row && enemy[1] === col - 2) {
                return [1, 4, 6]
            } else if (enemy[0] === row && enemy[1] === col - 1) {
                return [1, 2, 6, 7]
            } else if (enemy[0] === row && enemy[1] === col + 1) {
                return [2, 3, 7, 8]
            } else if (enemy[0] === row && enemy[1] === col + 2) {
                return [3, 5, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 2) {
                return [4, 6]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 1) {
                return [4, 7]
            } else if (enemy[0] === row + 1 && enemy[1] === col) {
                return [4, 5, 6, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 1) {
                return [5, 7]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 2) {
                return [5, 8]
            } else if (enemy[0] === row + 2 && enemy[1] === col - 2) {
                return [6]
            } else if (enemy[0] === row + 2 && enemy[1] === col - 1) {
                return [6, 7]
            } else if (enemy[0] === row + 2 && enemy[1] === col) {
                return [6, 7, 8]
            } else if (enemy[0] === row + 2 && enemy[1] === col + 1) {
                return [7, 8]
            } else if (enemy[0] === row + 2 && enemy[1] === col + 2) {
                return [8]
            }
        }
    }

    #slide(row, col, dr, dc) {
        let moves = []
        let r = row + dr
        let c = col + dc
        while (r >= 0 && r < ROWLEN && c >= 0 && c < COLLEN) {
            if (this.matrix[r][c] === 0) {
                moves.push([r, c])
            } else if (this.matrix[r][c] <= 6) {
                moves.push([r, c])
                break
            } else {
                break
            }
            r += dr
            c += dc
        }
        return moves
    }

    #pawn(row, col) {
        let list1 = []
        if (row > 0) {
            if (row === ROWLEN - 2) {
                if (this.matrix[row - 1][col] === 0 && this.matrix[row - 2][col] === 0) {
                    list1 = [
                        [row - 1, col],
                        [row - 2, col]
                    ]
                } else if (this.matrix[row - 1][col] === 0) {
                    list1 = [
                        [row - 1, col]
                    ]
                }
            } else {
                if (this.matrix[row - 1][col] === 0) {
                    list1 = [
                        [row - 1, col]
                    ]
                }
            }
            if (col - 1 >= 0) {
                if (this.matrix[row - 1][col - 1] !== 0 && this.matrix[row - 1][col - 1] <= 6) {
                    list1.push([row - 1, col - 1])
                }
            }
            if (col + 1 < COLLEN) {
                if (this.matrix[row - 1][col + 1] !== 0 && this.matrix[row - 1][col + 1] <= 6) {
                    list1.push([row - 1, col + 1])
                }
            }
        }

        return list1
    }
    #knight(row, col) {
        let list1 = []
        const moves = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]
        for (const [dr, dc] of moves) {
            const r = row + dr
            const c = col + dc

            if (r >= 0 && r < ROWLEN && c >= 0 && c < COLLEN && this.matrix[r][c] < 7) {
                list1.push([r, c])
            }
        }

        return list1
    }
    #bishop(row, col) {
        const directions = [[-1, +1], [+1, +1], [+1, -1], [-1, -1]]
        let moves = []
        for (const [dr, dc] of directions)
            moves = moves.concat(this.#slide(row, col, dr, dc))
        return moves
    }
    #rook(row, col) {
        const directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        let moves = []
        for (const [dr, dc] of directions) {
            moves = moves.concat(this.#slide(row, col, dr, dc))
        }
        return moves
    }
    #queen(row, col) {
        const directions = [[-1, 0], [0, 1], [1, 0], [0, -1], [-1, 1], [1, 1], [1, -1], [-1, -1]]
        let moves = []
        for (const [dr, dc] of directions) {
            moves = moves.concat(this.#slide(row, col, dr, dc))
        }
        return moves
    }
    #king(row, col) {
        let list1 = []
        const s = new Set()
        this.bot.forEach(e => {
            const res = this.#filterEnemy([e[0], row, col])
            if (res) {
                res.forEach(v => s.add(v))
            }
        })
        const directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        for (let i = 0; i < 8; i++) {
            const [dr, dc] = directions[i]
            const r = row + dr
            const c = col + dc
            if (
                r >= 0 && r < ROWLEN &&
                c >= 0 && c < COLLEN &&
                this.matrix[r][c] < 7 &&
                !s.has(i + 1)
            ) {
                list1.push([r, c])
            }
        }
        return list1
    }
}

export class BotChessman {
    constructor(matrix, pos, player, rowlen, collen) {
        this.matrix = matrix.map(row => [...row])
        this.pos = pos
        this.player = player
        ROWLEN = rowlen
        COLLEN = collen
    }

    [Symbol.iterator]() {
        const [row, col] = this.pos
        const piece = this.matrix[row][col]

        if (piece === 1) {
            return this.#pawn(row, col)[Symbol.iterator]()
        } else if (piece === 2) {
            return this.#knight(row, col)[Symbol.iterator]()
        } else if (piece === 3) {
            return this.#bishop(row, col)[Symbol.iterator]()
        } else if (piece === 4) {
            return this.#rook(row, col)[Symbol.iterator]()
        } else if (piece === 5) {
            return this.#queen(row, col)[Symbol.iterator]()
        } else if (piece === 6) {
            return this.#king(row, col)[Symbol.iterator]()
        }
        return [][Symbol.iterator]()
    }

    #filterEnemy(arg) {
        const [enemy, row, col] = arg
        if (this.matrix[enemy[0]][enemy[1]] === 7) {
            if (enemy[0] === row && enemy[1] === col - 2) {
                return [1]
            } else if (enemy[0] === row && enemy[1] === col - 1) {
                return [2]
            } else if (enemy[0] === row && enemy[1] === col + 1) {
                return [2]
            } else if (enemy[0] === row && enemy[1] === col + 2) {
                return [3]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 2) {
                return [4]
            } else if (enemy[0] === row + 1 && enemy[1] === col) {
                return [4, 5]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 2) {
                return [5]
            } else if (enemy[0] === row + 2 && enemy[1] === col - 2) {
                return [6]
            } else if (enemy[0] === row + 2 && enemy[1] === col - 1) {
                return [7]
            } else if (enemy[0] === row + 2 && enemy[1] === col) {
                return [6, 8]
            } else if (enemy[0] === row + 2 && enemy[1] === col + 1) {
                return [7]
            } else if (enemy[0] === row + 2 && enemy[1] === col + 2) {
                return [8]
            }
        } else if (this.matrix[enemy[0]][enemy[1]] === 8) {
            if (enemy[0] === row - 3 && enemy[1] === col - 2) {
                return [1]
            } else if (enemy[0] === row - 3 && enemy[1] === col - 1) {
                return [2]
            } else if (enemy[0] === row - 3 && enemy[1] === col) {
                return [1, 3]
            } else if (enemy[0] === row - 3 && enemy[1] === col + 1) {
                return [2]
            } else if (enemy[0] === row - 3 && enemy[1] === col + 2) {
                return [3]
            } else if (enemy[0] === row - 2 && enemy[1] === col - 3) {
                return [1]
            } else if (enemy[0] === row - 2 && enemy[1] === col - 2) {
                return [2, 4]
            } else if (enemy[0] === row - 2 && enemy[1] === col - 1) {
                return [3]
            } else if (enemy[0] === row - 2 && enemy[1] === col) {
                return [4, 5]
            } else if (enemy[0] === row - 2 && enemy[1] === col + 1) {
                return [1]
            } else if (enemy[0] === row - 2 && enemy[1] === col + 2) {
                return [2, 5]
            } else if (enemy[0] === row - 2 && enemy[1] === col + 3) {
                return [3]
            } else if (enemy[0] === row - 1 && enemy[1] === col - 3) {
                return [4]
            } else if (enemy[0] === row - 1 && enemy[1] === col - 2) {
                return [6]
            } else if (enemy[0] === row - 1 && enemy[1] === col - 1) {
                return [5, 7]
            } else if (enemy[0] === row - 1 && enemy[1] === col) {
                return [6, 8]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 1) {
                return [4, 7]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 2) {
                return [8]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 3) {
                return [5]
            } else if (enemy[0] === row && enemy[1] === col - 3) {
                return [1, 6]
            } else if (enemy[0] === row && enemy[1] === col - 2) {
                return [2, 7]
            } else if (enemy[0] === row && enemy[1] === col - 1) {
                return [3, 8]
            } else if (enemy[0] === row && enemy[1] === col + 1) {
                return [1, 6]
            } else if (enemy[0] === row && enemy[1] === col + 2) {
                return [2, 7]
            } else if (enemy[0] === row && enemy[1] === col + 3) {
                return [3, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 3) {
                return [4]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 2) {
                return [1]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 1) {
                return [2, 5]
            } else if (enemy[0] === row + 1 && enemy[1] === col) {
                return [1, 3]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 1) {
                return [2, 4]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 2) {
                return [3]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 3) {
                return [5]
            } else if (enemy[0] === row + 2 && enemy[1] === col - 3) {
                return [6]
            } else if (enemy[0] === row + 2 && enemy[1] === col - 2) {
                return [4, 7]
            } else if (enemy[0] === row + 2 && enemy[1] === col - 1) {
                return [8]
            } else if (enemy[0] === row + 2 && enemy[1] === col) {
                return [4, 5]
            } else if (enemy[0] === row + 2 && enemy[1] === col + 1) {
                return [6]
            } else if (enemy[0] === row + 2 && enemy[1] === col + 2) {
                return [5, 7]
            } else if (enemy[0] === row + 2 && enemy[1] === col + 3) {
                return [8]
            } else if (enemy[0] === row - 3 && enemy[1] === col - 2) {
                return [6]
            } else if (enemy[0] === row - 3 && enemy[1] === col - 1) {
                return [7]
            } else if (enemy[0] === row - 3 && enemy[1] === col) {
                return [6, 8]
            } else if (enemy[0] === row - 3 && enemy[1] === col + 1) {
                return [7]
            } else if (enemy[0] === row - 3 && enemy[1] === col + 2) {
                return [8]
            }
        } else if (this.matrix[enemy[0]][enemy[1]] === 9) {
            if (enemy[0] === row + 2 && enemy[1] === col) {
                return [6, 8]
            } else if (
                (enemy[0] === row + 1 && enemy[1] === col) ||
                (enemy[0] === row - 1 && enemy[1] === col)
            ) {
                return [4, 5]
            } else if (enemy[0] === row - 2 && enemy[1] === col) {
                return [1, 3]
            } else if (enemy[0] === row && enemy[1] === col + 2) {
                return [3, 8]
            } else if (
                (enemy[0] === row && enemy[1] === col + 1) ||
                (enemy[0] === row && enemy[1] === col - 1)
            ) {
                return [2, 7]
            } else if (enemy[0] === row && enemy[1] === col - 2) {
                return [1, 6]
            } else {
                if (
                    enemy[0] !== row - 1 &&
                    enemy[1] !== col - 1 &&
                    Math.abs(enemy[0] - (row - 1)) === Math.abs(enemy[1] - (col - 1))
                ) {
                    if (
                        enemy[0] !== row + 1 &&
                        enemy[1] !== col + 1 &&
                        Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - (col + 1))
                    ) {
                        if (enemy[0] < row - 1 && enemy[1] < col - 1) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] + x] !== 0) return null
                            }
                            if (this.matrix[row - 1][col - 1] !== 0) return [1]
                        } else if (enemy[0] > row + 1 && enemy[1] > col + 1) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] - x] !== 0) return null
                            }
                            if (this.matrix[row + 1][col + 1] !== 0) return [8]
                        }
                        return [1, 8]
                    } else {
                        if (enemy[0] < row - 1 && enemy[1] > col - 1) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] - x] !== 0) return null
                            }
                        } else if (enemy[0] > row - 1 && enemy[1] < col - 1) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] + x] !== 0) return null
                            }
                        }
                        return [1]
                    }
                }
            }
        } else if (this.matrix[enemy[0]][enemy[1]] === 10) {
            if (enemy[0] === row - 1 && enemy[1] === col - 1) {
                if (this.matrix[row][col - 1] !== 0 && this.matrix[row - 1][col] !== 0) {
                    return [2, 4]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 4, 6]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [2, 3, 4]
                } else {
                    return [2, 3, 4, 6]
                }
            } else if (enemy[0] === row - 1 && enemy[1] === col) {
                return [1, 3, 7]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 1) {
                if (this.matrix[row][col + 1] !== 0 && this.matrix[row - 1][col] !== 0) {
                    return [2, 5]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 5, 8]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [1, 2, 5]
                } else {
                    return [1, 2, 5, 8]
                }
            } else if (enemy[0] === row && enemy[1] === col - 1) {
                return [1, 5, 6]
            } else if (enemy[0] === row && enemy[1] === col + 1) {
                return [3, 4, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 1) {
                if (this.matrix[row][col - 1] !== 0 && this.matrix[row + 1][col] !== 0) {
                    return [4, 7]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [1, 4, 7]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [4, 7, 8]
                } else {
                    return [1, 4, 7, 8]
                }
            } else if (enemy[0] === row + 1 && enemy[1] === col) {
                return [2, 6, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 1) {
                if (this.matrix[row][col + 1] !== 0 && this.matrix[row + 1][col] !== 0) {
                    return [5, 7]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [3, 5, 7]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [5, 6, 7]
                } else {
                    return [3, 5, 6, 7]
                }
            } else {
                if (enemy[0] === row - 1) {
                    if (enemy[1] < col - 1) {
                        for (let x = enemy[1] + 1; x < col - 1; x++) {
                            if (this.matrix[row - 1][x] !== 0) return null
                        }
                        if (this.matrix[row - 1][col - 1] !== 0) return [1]
                        else if (this.matrix[row - 1][col] !== 0) return [1, 2]
                    } else if (enemy[1] > col + 1) {
                        for (let x = col + 2; x < enemy[1]; x++) {
                            if (this.matrix[row - 1][x] !== 0) return null
                        }
                        if (this.matrix[row - 1][col + 1] !== 0) return [3]
                        else if (this.matrix[row - 1][col] !== 0) return [2, 3]
                    }
                    return [1, 2, 3]
                } else if (enemy[0] === row) {
                    if (enemy[1] < col - 1) {
                        for (let x = enemy[1] + 1; x < col - 1; x++) {
                            if (this.matrix[row][x] !== 0) return null
                        }
                        if (this.matrix[row][col - 1] !== 0) return [4]
                    } else if (enemy[1] > col + 1) {
                        for (let x = col + 2; x < enemy[1]; x++) {
                            if (this.matrix[row][x] !== 0) return null
                        }
                        if (this.matrix[row][col + 1] !== 0) return [5]
                    }
                    return [4, 5]
                } else if (enemy[0] === row + 1) {
                    if (enemy[1] < col - 1) {
                        for (let x = enemy[1] + 1; x < col - 1; x++) {
                            if (this.matrix[row + 1][x] !== 0) return null
                        }
                        if (this.matrix[row + 1][col - 1] !== 0) return [6]
                        else if (this.matrix[row + 1][col] !== 0) return [6, 7]
                    } else if (enemy[1] > col + 1) {
                        for (let x = col + 2; x < enemy[1]; x++) {
                            if (this.matrix[row + 1][x] !== 0) return null
                        }
                        if (this.matrix[row + 1][col + 1] !== 0) return [8]
                        else if (this.matrix[row + 1][col] !== 0) return [7, 8]
                    }
                    return [6, 7, 8]
                } else if (enemy[1] === col - 1) {
                    if (enemy[0] < row - 1) {
                        for (let x = enemy[0] + 1; x < row - 1; x++) {
                            if (this.matrix[x][col - 1] !== 0) return null
                        }
                        if (this.matrix[row - 1][col - 1] !== 0) return [1]
                        else if (this.matrix[row][col - 1] !== 0) return [1, 4]
                    } else if (enemy[0] > row + 1) {
                        for (let x = row + 2; x < enemy[0]; x++) {
                            if (this.matrix[x][col - 1] !== 0) return null
                        }
                        if (this.matrix[row + 1][col - 1] !== 0) return [6]
                        else if (this.matrix[row][col - 1] !== 0) return [4, 6]
                    }
                    return [1, 4, 6]
                } else if (enemy[1] === col) {
                    if (enemy[0] < row - 1) {
                        for (let x = enemy[0] + 1; x < row - 1; x++) {
                            if (this.matrix[x][col] !== 0) return null
                        }
                        if (this.matrix[row - 1][col] !== 0) return [2]
                    } else if (enemy[0] > row + 1) {
                        for (let x = row + 2; x < enemy[0]; x++) {
                            if (this.matrix[x][col] !== 0) return null
                        }
                        if (this.matrix[row + 1][col] !== 0) return [7]
                    }
                    return [2, 7]
                } else if (enemy[1] === col + 1) {
                    if (enemy[0] < row - 1) {
                        for (let x = enemy[0] + 1; x < row - 1; x++) {
                            if (this.matrix[x][col + 1] !== 0) return null
                        }
                        if (this.matrix[row - 1][col + 1] !== 0) return [3]
                        else if (this.matrix[row][col + 1] !== 0) return [3, 5]
                    } else if (enemy[0] > row + 1) {
                        for (let x = row + 2; x < enemy[0]; x++) {
                            if (this.matrix[x][col + 1] !== 0) return null
                        }
                        if (this.matrix[row + 1][col + 1] !== 0) return [8]
                        else if (this.matrix[row][col + 1] !== 0) return [5, 8]
                    }
                    return [3, 5, 8]
                }

            }
        } else if (this.matrix[enemy[0]][enemy[1]] === 11) {
            if (enemy[0] === row - 1 && enemy[1] === col - 1) {
                if (this.matrix[row - 1][col] !== 0 && this.matrix[row][col - 1] !== 0) {
                    return [2, 4, 8]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 4, 6, 8]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [2, 3, 4, 8]
                } else {
                    return [2, 3, 4, 6, 8]
                }
            } else if (enemy[0] === row - 1 && enemy[1] === col) {
                return [1, 3, 4, 5, 7]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 1) {
                if (this.matrix[row - 1][col] !== 0 && this.matrix[row][col + 1] !== 0) {
                    return [2, 5, 6]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 5, 6, 8]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [1, 2, 5, 6]
                } else {
                    return [1, 2, 5, 6, 8]
                }
            } else if (enemy[0] === row && enemy[1] === col - 1) {
                return [1, 2, 5, 6, 7]
            } else if (enemy[0] === row && enemy[1] === col + 1) {
                return [2, 3, 4, 7, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 1) {
                if (this.matrix[row + 1][col] !== 0 && this.matrix[row][col - 1] !== 0) {
                    return [3, 4, 7]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [1, 3, 4, 7]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [3, 4, 7, 8]
                } else {
                    return [1, 3, 4, 7, 8]
                }
            } else if (enemy[0] === row + 1 && enemy[1] === col) {
                return [2, 4, 5, 6, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 1) {
                if (this.matrix[row + 1][col] !== 0 && this.matrix[row][col + 1] !== 0) {
                    return [1, 5, 7]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [1, 3, 5, 7]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [1, 5, 6, 7]
                } else {
                    return [1, 3, 5, 6, 7]
                }
            } else if (enemy[0] === row - 2 && enemy[1] === col - 1) {
                if (this.matrix[row - 1][col - 1] !== 0 && this.matrix[row - 1][col] !== 0) {
                    return [1, 2]
                } else if (this.matrix[row][col - 1] !== 0 && this.matrix[row - 1][col] !== 0) {
                    return [1, 2, 4]
                } else if (this.matrix[row - 1][col - 1] !== 0) {
                    return [1, 2, 5]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [1, 2, 4, 6]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [1, 2, 4, 5]
                } else {
                    return [1, 2, 4, 5, 6]
                }
            } else if (enemy[0] === row - 2 && enemy[1] === col) {
                if (this.matrix[row - 1][col] !== 0) {
                    return [1, 2, 3]
                } else {
                    return [1, 2, 3, 7]
                }
            } else if (enemy[0] === row - 2 && enemy[1] === col + 1) {
                if (this.matrix[row - 1][col + 1] !== 0 && this.matrix[row - 1][col] !== 0) {
                    return [2, 3]
                } else if (this.matrix[row][col + 1] !== 0 && this.matrix[row - 1][col] !== 0) {
                    return [2, 3, 5]
                } else if (this.matrix[row - 1][col + 1] !== 0) {
                    return [2, 3, 4]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 3, 5, 8]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [2, 3, 4, 5]
                } else {
                    return [2, 3, 4, 5, 8]
                }
            } else if (enemy[0] === row - 1 && enemy[1] === col - 2) {
                if (this.matrix[row - 1][col - 1] !== 0 && this.matrix[row][col - 1] !== 0) {
                    return [1, 4]
                } else if (this.matrix[row - 1][col] !== 0 && this.matrix[row][col - 1] !== 0) {
                    return [1, 2, 4]
                } else if (this.matrix[row - 1][col - 1] !== 0) {
                    return [1, 4, 7]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [1, 2, 4, 7]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [1, 2, 3, 4]
                } else {
                    return [1, 2, 3, 4, 7]
                }
            } else if (enemy[0] === row && enemy[1] === col - 2) {
                if (this.matrix[row][col - 1] !== 0) {
                    return [1, 4, 6]
                } else {
                    return [1, 4, 5, 6]
                }
            } else if (enemy[0] === row + 1 && enemy[1] === col - 2) {
                if (this.matrix[row + 1][col - 1] !== 0 && this.matrix[row][col - 1] !== 0) {
                    return [4, 6]
                } else if (this.matrix[row + 1][col] !== 0 && this.matrix[row][col - 1] !== 0) {
                    return [4, 6, 7]
                } else if (this.matrix[row + 1][col - 1] !== 0) {
                    return [2, 4, 6]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [2, 4, 6, 7]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [4, 6, 7, 8]
                } else {
                    return [2, 4, 6, 7, 8]
                }
            } else if (enemy[0] === row + 2 && enemy[1] === col - 1) {
                if (this.matrix[row + 1][col - 1] !== 0 && this.matrix[row + 1][col] !== 0) {
                    return [6, 7]
                } else if (this.matrix[row][col - 1] !== 0 && this.matrix[row + 1][col] !== 0) {
                    return [4, 6, 7]
                } else if (this.matrix[row + 1][col - 1] !== 0) {
                    return [5, 6, 7]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [1, 4, 6, 7]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [4, 5, 6, 7]
                } else {
                    return [1, 4, 5, 6, 7]
                }
            } else if (enemy[0] === row + 2 && enemy[1] === col) {
                if (this.matrix[row + 1][col] !== 0) {
                    return [6, 7, 8]
                } else {
                    return [2, 6, 7, 8]
                }
            } else if (enemy[0] === row + 2 && enemy[1] === col + 1) {
                if (this.matrix[row + 1][col + 1] !== 0 && this.matrix[row + 1][col] !== 0) {
                    return [7, 8]
                } else if (this.matrix[row][col + 1] !== 0 && this.matrix[row + 1][col] !== 0) {
                    return [5, 7, 8]
                } else if (this.matrix[row + 1][col + 1] !== 0) {
                    return [4, 7, 8]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [3, 5, 7, 8]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [4, 5, 7, 8]
                } else {
                    return [3, 4, 5, 7, 8]
                }
            } else if (enemy[0] === row - 1 && enemy[1] === col + 2) {
                if (this.matrix[row - 1][col + 1] !== 0 && this.matrix[row][col + 1] !== 0) {
                    return [3, 5]
                } else if (this.matrix[row - 1][col] !== 0 && this.matrix[row][col + 1] !== 0) {
                    return [2, 3, 5]
                } else if (this.matrix[row - 1][col + 1] !== 0) {
                    return [3, 5, 7]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 3, 5, 7]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [1, 2, 3, 5]
                } else {
                    return [1, 2, 3, 5, 7]
                }
            } else if (enemy[0] === row && enemy[1] === col + 2) {
                if (this.matrix[row][col + 1] !== 0) {
                    return [3, 5, 8]
                } else {
                    return [3, 4, 5, 8]
                }
            } else if (enemy[0] === row + 1 && enemy[1] === col + 2) {
                if (this.matrix[row + 1][col + 1] !== 0 && this.matrix[row][col + 1] !== 0) {
                    return [5, 8]
                } else if (this.matrix[row + 1][col] !== 0 && this.matrix[row][col + 1] !== 0) {
                    return [5, 7, 8]
                } else if (this.matrix[row + 1][col + 1] !== 0) {
                    return [2, 5, 8]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [2, 5, 7, 8]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [5, 6, 7, 8]
                } else {
                    return [2, 5, 6, 7, 8]
                }
            } else if (enemy[0] === row - 3 && enemy[1] === col - 1) {
                if (this.matrix[row - 2][col - 1] !== 0 && this.matrix[row - 2][col] !== 0) {
                    return null
                } else if (this.matrix[row - 2][col - 1] !== 0) {
                    return [3]
                } else if (this.matrix[row - 2][col] !== 0) {
                    return [1]
                } else if (this.matrix[row - 1][col - 1] !== 0) {
                    return [1, 3]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [1, 4, 3]
                } else {
                    return [1, 3, 4, 6]
                }
            } else if (enemy[0] === row - 3 && enemy[1] === col) {
                if (this.matrix[row - 2][col] !== 0) {
                    return null
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2]
                } else {
                    return [2, 7]
                }
            } else if (enemy[0] === row - 3 && enemy[1] === col + 1) {
                if (this.matrix[row - 2][col + 1] !== 0 && this.matrix[row - 2][col] !== 0) {
                    return null
                } else if (this.matrix[row - 2][col + 1] !== 0) {
                    return [1]
                } else if (this.matrix[row - 2][col] !== 0) {
                    return [3]
                } else if (this.matrix[row - 1][col + 1] !== 0) {
                    return [1, 3]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [1, 3, 5]
                } else {
                    return [1, 3, 5, 8]
                }
            } else if (enemy[0] === row - 1 && enemy[1] === col - 3) {
                if (this.matrix[row - 1][col - 2] !== 0 && this.matrix[row][col - 2] !== 0) {
                    return null
                } else if (this.matrix[row - 1][col - 2] !== 0) {
                    return [6]
                } else if (this.matrix[row][col - 2] !== 0) {
                    return [1]
                } else if (this.matrix[row - 1][col - 1] !== 0) {
                    return [1, 6]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [1, 2, 6]
                } else {
                    return [1, 2, 3, 6]
                }
            } else if (enemy[0] === row && enemy[1] === col - 3) {
                if (this.matrix[row][col - 2] !== 0) {
                    return null
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [4]
                } else {
                    return [4, 5]
                }
            } else if (enemy[0] === row + 1 && enemy[1] === col - 3) {
                if (this.matrix[row + 1][col - 2] !== 0 && this.matrix[row][col - 2] !== 0) {
                    return null
                } else if (this.matrix[row + 1][col - 2] !== 0) {
                    return [1]
                } else if (this.matrix[row][col - 2] !== 0) {
                    return [6]
                } else if (this.matrix[row + 1][col - 1] !== 0) {
                    return [1, 6]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [1, 6, 7]
                } else {
                    return [1, 3, 4, 6]
                }
            } else if (enemy[0] === row + 3 && enemy[1] === col - 1) {
                if (this.matrix[row + 2][col - 1] !== 0 && this.matrix[row + 2][col] !== 0) {
                    return null
                } else if (this.matrix[row + 2][col - 1] !== 0) {
                    return [8]
                } else if (this.matrix[row + 2][col] !== 0) {
                    return [6]
                } else if (this.matrix[row + 1][col - 1] !== 0) {
                    return [6, 8]
                } else if (this.matrix[row][col - 1] !== 0) {
                    return [4, 6, 8]
                } else {
                    return [1, 4, 6, 8]
                }
            } else if (enemy[0] === row + 3 && enemy[1] === col) {
                if (this.matrix[row + 2][col] !== 0) {
                    return null
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [7]
                } else {
                    return [2, 7]
                }
            } else if (enemy[0] === row + 3 && enemy[1] === col + 1) {
                if (this.matrix[row + 2][col + 1] !== 0 && this.matrix[row + 2][col] !== 0) {
                    return null
                } else if (this.matrix[row + 2][col + 1] !== 0) {
                    return [6]
                } else if (this.matrix[row + 2][col] !== 0) {
                    return [8]
                } else if (this.matrix[row + 1][col + 1] !== 0) {
                    return [6, 8]
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [5, 6, 8]
                } else {
                    return [3, 5, 6, 8]
                }
            } else if (enemy[0] === row - 1 && enemy[1] === col + 3) {
                if (this.matrix[row - 1][col + 2] !== 0 && this.matrix[row][col + 2] !== 0) {
                    return null
                } else if (this.matrix[row - 1][col + 2] !== 0) {
                    return [8]
                } else if (this.matrix[row + 2][col] !== 0) {
                    return [3]
                } else if (this.matrix[row - 1][col + 1] !== 0) {
                    return [3, 8]
                } else if (this.matrix[row - 1][col] !== 0) {
                    return [2, 3, 8]
                } else {
                    return [1, 2, 3, 8]
                }
            } else if (enemy[0] === row && enemy[1] === col + 3) {
                if (this.matrix[row][col + 2] !== 0) {
                    return null
                } else if (this.matrix[row][col + 1] !== 0) {
                    return [5]
                } else {
                    return [4, 5]
                }
            } else if (enemy[0] === row + 1 && enemy[1] === col + 3) {
                if (this.matrix[row + 1][col + 2] !== 0 && this.matrix[row][col + 2] !== 0) {
                    return null
                } else if (this.matrix[row + 1][col + 2] !== 0) {
                    return [3]
                } else if (this.matrix[row + 2][col] !== 0) {
                    return [8]
                } else if (this.matrix[row + 1][col + 1] !== 0) {
                    return [3, 8]
                } else if (this.matrix[row + 1][col] !== 0) {
                    return [3, 7, 8]
                } else {
                    return [3, 6, 7, 8]
                }
            } else if (
                (
                    ((enemy[0] >= 0 && enemy[0] < row - 3) || (enemy[0] > row + 3 && enemy[0] < ROWLEN)) &&
                    (enemy[1] >= col - 1 && enemy[1] <= col + 1)
                ) ||
                (
                    ((enemy[1] >= 0 && enemy[1] < col - 3) || (enemy[1] > col + 3 && enemy[1] < COLLEN)) &&
                    (enemy[0] >= row - 1 && enemy[0] <= row + 1)
                )
            ) {
                if (enemy[0] === row - 1) {
                    if (enemy[1] < col - 1) {
                        for (let x = enemy[1] + 1; x < col - 1; x++) {
                            if (this.matrix[row - 1][x] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row - 1][col - 1] !== 0) {
                            return [1]
                        } else if (this.matrix[row - 1][col] !== 0) {
                            return [1, 2]
                        }
                    } else if (enemy[1] > col + 1) {
                        for (let x = col + 2; x < enemy[1]; x++) {
                            if (this.matrix[row - 1][x] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row - 1][col + 1] !== 0) {
                            return [3]
                        } else if (this.matrix[row - 1][col] !== 0) {
                            return [2, 3]
                        }
                    }
                    return [1, 2, 3]
                } else if (enemy[0] === row) {
                    if (enemy[1] < col - 1) {
                        for (let x = enemy[1] + 1; x < col - 1; x++) {
                            if (this.matrix[row][x] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row][col - 1] !== 0) {
                            return [4]
                        }
                    } else if (enemy[1] > col + 1) {
                        for (let x = col + 2; x < enemy[1]; x++) {
                            if (this.matrix[row][x] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row][col + 1] !== 0) {
                            return [5]
                        }
                    }
                    return [4, 5]
                } else if (enemy[0] === row + 1) {
                    if (enemy[1] < col - 1) {
                        for (let x = enemy[1] + 1; x < col - 1; x++) {
                            if (this.matrix[row + 1][x] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row + 1][col - 1] !== 0) {
                            return [6]
                        } else if (this.matrix[row + 1][col] !== 0) {
                            return [6, 7]
                        }
                    } else if (enemy[1] > col + 1) {
                        for (let x = col + 2; x < enemy[1]; x++) {
                            if (this.matrix[row + 1][x] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row + 1][col + 1] !== 0) {
                            return [8]
                        } else if (this.matrix[row + 1][col] !== 0) {
                            return [7, 8]
                        }
                    }
                    return [6, 7, 8]
                } else if (enemy[1] === col - 1) {
                    if (enemy[0] < row - 1) {
                        for (let x = enemy[0] + 1; x < row - 1; x++) {
                            if (this.matrix[x][col - 1] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row - 1][col - 1] !== 0) {
                            return [1]
                        } else if (this.matrix[row][col - 1] !== 0) {
                            return [1, 4]
                        }
                    } else if (enemy[0] > row + 1) {
                        for (let x = row + 2; x < enemy[0]; x++) {
                            if (this.matrix[x][col - 1] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row + 1][col - 1] !== 0) {
                            return [6]
                        } else if (this.matrix[row][col - 1] !== 0) {
                            return [4, 6]
                        }
                    }
                    return [1, 4, 6]
                } else if (enemy[1] === col) {
                    if (enemy[0] < row - 1) {
                        for (let x = enemy[0] + 1; x < row - 1; x++) {
                            if (this.matrix[x][col] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row - 1][col] !== 0) {
                            return [2]
                        }
                    } else if (enemy[0] > row + 1) {
                        for (let x = row + 2; x < enemy[0]; x++) {
                            if (this.matrix[x][col] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row + 1][col] !== 0) {
                            return [7]
                        }
                    }
                    return [2, 7]
                } else if (enemy[1] === col + 1) {
                    if (enemy[0] < row - 1) {
                        for (let x = enemy[0] + 1; x < row - 1; x++) {
                            if (this.matrix[x][col + 1] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row - 1][col + 1] !== 0) {
                            return [3]
                        } else if (this.matrix[row][col + 1] !== 0) {
                            return [3, 5]
                        }
                    } else if (enemy[0] > row + 1) {
                        for (let x = row + 2; x < enemy[0]; x++) {
                            if (this.matrix[x][col + 1] !== 0) {
                                return null
                            }
                        }
                        if (this.matrix[row + 1][col + 1] !== 0) {
                            return [8]
                        } else if (this.matrix[row][col + 1] !== 0) {
                            return [5, 8]
                        }
                    }
                    return [3, 5, 8]
                }
            } else {
                if (
                    enemy[0] !== (row - 1) &&
                    enemy[1] !== (col - 1) &&
                    Math.abs(enemy[0] - (row - 1)) === Math.abs(enemy[1] - (col - 1))
                ) {
                    if (
                        enemy[0] !== (row + 1) &&
                        enemy[1] !== (col + 1) &&
                        Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - (col + 1))
                    ) {
                        if (enemy[0] < (row - 1) && enemy[1] < (col - 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row - 1][col - 1] !== 0) {
                                return [1]
                            }
                        } else if (enemy[0] > (row + 1) && enemy[1] > (col + 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row + 1][col + 1] !== 0) {
                                return [8]
                            }
                        }
                        return [1, 8]
                    } else {
                        if (enemy[0] < (row - 1) && enemy[1] > (col - 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                        } else if (enemy[0] > (row - 1) && enemy[1] < (col - 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                        }
                        return [1]
                    }
                } else if (
                    enemy[0] !== (row - 1) &&
                    enemy[1] !== col &&
                    Math.abs(enemy[0] - (row - 1)) === Math.abs(enemy[1] - col)
                ) {
                    if (
                        enemy[0] !== row &&
                        enemy[1] !== (col + 1) &&
                        Math.abs(enemy[0] - row) === Math.abs(enemy[1] - (col + 1))
                    ) {
                        if (enemy[0] < (row - 1) && enemy[1] < col) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row - 1][col] !== 0) {
                                return [2]
                            }
                        } else if (enemy[0] > row && enemy[1] > (col + 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row][col + 1] !== 0) {
                                return [5]
                            }
                        }
                        return [2, 5]
                    } else if (
                        enemy[0] !== row &&
                        enemy[1] !== (col - 1) &&
                        Math.abs(enemy[0] - row) === Math.abs(enemy[1] - (col - 1))
                    ) {
                        if (enemy[0] < (row - 1) && enemy[1] > col) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row - 1][col] !== 0) {
                                return [2]
                            }
                        } else if (enemy[0] > row && enemy[1] < (col - 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row][col - 1] !== 0) {
                                return [4]
                            }
                        }
                        return [2, 4]
                    }
                } else if (
                    enemy[0] !== (row - 1) &&
                    enemy[1] !== (col + 1) &&
                    Math.abs(enemy[0] - (row - 1)) === Math.abs(enemy[1] - (col + 1))
                ) {
                    if (
                        enemy[0] !== (row + 1) &&
                        enemy[1] !== (col - 1) &&
                        Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - (col - 1))
                    ) {
                        if (enemy[0] < (row - 1) && enemy[1] > (col + 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row - 1][col + 1] !== 0) {
                                return [3]
                            }
                        } else if (enemy[0] > (row + 1) && enemy[1] < (col - 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row + 1][col - 1] !== 0) {
                                return [6]
                            }
                        }
                        return [3, 6]
                    } else {
                        if (enemy[0] < (row - 1) && enemy[1] < (col + 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                        } else if (enemy[0] > (row - 1) && enemy[1] > (col + 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - (row - 1)); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                        }
                        return [3]
                    }
                } else if (
                    enemy[0] !== row &&
                    enemy[1] !== (col - 1) &&
                    Math.abs(enemy[0] - row) === Math.abs(enemy[1] - (col - 1))
                ) {
                    if (
                        enemy[0] !== (row + 1) &&
                        enemy[1] !== col &&
                        Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - col)
                    ) {
                        if (enemy[0] < row && enemy[1] < (col - 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row - 1][col] !== 0) {
                                return [4]
                            }
                        } else if (enemy[0] > (row + 1) && enemy[1] > col) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row + 1][col] !== 0) {
                                return [7]
                            }
                        }

                        return [4, 7]
                    }
                } else if (
                    enemy[0] !== row &&
                    enemy[1] !== (col + 1) &&
                    Math.abs(enemy[0] - row) === Math.abs(enemy[1] - (col + 1))
                ) {
                    if (
                        enemy[0] !== (row + 1) &&
                        enemy[1] !== col &&
                        Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - col)
                    ) {
                        if (enemy[0] < row && enemy[1] > (col + 1)) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] + x][enemy[1] - x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row][col + 1] !== 0) {
                                return [5]
                            }
                        } else if (enemy[0] > (row + 1) && enemy[1] < col) {
                            for (let x = 1; x < Math.abs(enemy[0] - row); x++) {
                                if (this.matrix[enemy[0] - x][enemy[1] + x] !== 0) {
                                    return null
                                }
                            }
                            if (this.matrix[row + 1][col] !== 0) {
                                return [7]
                            }
                        }
                        return [5, 7]
                    }
                } else if (
                    enemy[0] !== (row + 1) &&
                    enemy[1] !== (col - 1) &&
                    Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - (col - 1))
                ) {
                    if (enemy[0] < (row + 1) && enemy[1] < (col - 1)) {
                        for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                            if (this.matrix[enemy[0] + x][enemy[1] + x] !== 0) {
                                return null
                            }
                        }
                    } else if (enemy[0] > (row + 1) && enemy[1] > (col - 1)) {
                        for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                            if (this.matrix[enemy[0] - x][enemy[1] - x] !== 0) {
                                return null
                            }
                        }
                    }
                    return [6]
                } else if (
                    enemy[0] !== (row + 1) &&
                    enemy[1] !== (col + 1) &&
                    Math.abs(enemy[0] - (row + 1)) === Math.abs(enemy[1] - (col + 1))
                ) {
                    if (enemy[0] < (row + 1) && enemy[1] > (col + 1)) {
                        for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                            if (this.matrix[enemy[0] + x][enemy[1] - x] !== 0) {
                                return null
                            }
                        }
                    } else if (enemy[0] > (row + 1) && enemy[1] < (col + 1)) {
                        for (let x = 1; x < Math.abs(enemy[0] - (row + 1)); x++) {
                            if (this.matrix[enemy[0] - x][enemy[1] + x] !== 0) {
                                return null
                            }
                        }
                    }
                    return [8]
                }
            }
        } else if (this.matrix[enemy[0]][enemy[1]] === 12) {
            if (enemy[0] === row - 2 && enemy[1] === col - 2) {
                return [1]
            } else if (enemy[0] === row - 2 && enemy[1] === col - 1) {
                return [1, 2]
            } else if (enemy[0] === row - 2 && enemy[1] === col) {
                return [1, 2, 3]
            } else if (enemy[0] === row - 2 && enemy[1] === col + 1) {
                return [2, 3]
            } else if (enemy[0] === row - 2 && enemy[1] === col + 2) {
                return [3]
            } else if (enemy[0] === row - 1 && enemy[1] === col - 2) {
                return [1, 4]
            } else if (enemy[0] === row - 1 && enemy[1] === col - 1) {
                return [2, 4]
            } else if (enemy[0] === row - 1 && enemy[1] === col) {
                return [1, 3, 4, 5]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 1) {
                return [2, 5]
            } else if (enemy[0] === row - 1 && enemy[1] === col + 2) {
                return [3, 5]
            } else if (enemy[0] === row && enemy[1] === col - 2) {
                return [1, 4, 6]
            } else if (enemy[0] === row && enemy[1] === col - 1) {
                return [1, 2, 6, 7]
            } else if (enemy[0] === row && enemy[1] === col + 1) {
                return [2, 3, 7, 8]
            } else if (enemy[0] === row && enemy[1] === col + 2) {
                return [3, 5, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 2) {
                return [4, 6]
            } else if (enemy[0] === row + 1 && enemy[1] === col - 1) {
                return [4, 7]
            } else if (enemy[0] === row + 1 && enemy[1] === col) {
                return [4, 5, 6, 8]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 1) {
                return [5, 7]
            } else if (enemy[0] === row + 1 && enemy[1] === col + 2) {
                return [5, 8]
            } else if (enemy[0] === row + 2 && enemy[1] === col - 2) {
                return [6]
            } else if (enemy[0] === row + 2 && enemy[1] === col - 1) {
                return [6, 7]
            } else if (enemy[0] === row + 2 && enemy[1] === col) {
                return [6, 7, 8]
            } else if (enemy[0] === row + 2 && enemy[1] === col + 1) {
                return [7, 8]
            } else if (enemy[0] === row + 2 && enemy[1] === col + 2) {
                return [8]
            }
        }
    }

    #slide(row, col, dr, dc) {
        let moves = []
        let r = row + dr
        let c = col + dc
        while (r >= 0 && r < ROWLEN && c >= 0 && c < COLLEN) {
            if (this.matrix[r][c] === 0) {
                moves.push([r, c])
            } else if (this.matrix[r][c] >= 7) {
                moves.push([r, c])
                break
            } else {
                break
            }
            r += dr
            c += dc
        }
        return moves
    }

    #pawn(row, col) {
        let list1 = []
        if (row < ROWLEN - 1) {
            if (row === 1) {
                if (
                    this.matrix[row + 1][col] === 0 &&
                    this.matrix[row + 2][col] === 0
                ) {
                    list1.push(
                        [row + 1, col],
                        [row + 2, col]
                    )
                } else if (this.matrix[row + 1][col] === 0) {
                    list1.push([row + 1, col])
                }
            } else {
                if (this.matrix[row + 1][col] === 0) {
                    list1.push([row + 1, col])
                }
            }
            if (col - 1 >= 0) {
                if (
                    this.matrix[row + 1][col - 1] !== 0 &&
                    this.matrix[row + 1][col - 1] > 6
                ) {
                    list1.push([row + 1, col - 1])
                }
            }
            if (col + 1 < COLLEN) {
                if (
                    this.matrix[row + 1][col + 1] !== 0 &&
                    this.matrix[row + 1][col + 1] > 6
                ) {
                    list1.push([row + 1, col + 1])
                }
            }
        }
        return list1
    }
    #knight(row, col) {
        let list1 = []
        const moves = [[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]]
        for (let [dr, dc] of moves) {
            const r = row + dr
            const c = col + dc
            if (
                r >= 0 && r < ROWLEN &&
                c >= 0 && c < COLLEN &&
                (this.matrix[r][c] === 0 || this.matrix[r][c] > 6)
            ) {
                list1.push([r, c])
            }
        }
        return list1
    }
    #bishop(row, col) {
        const directions = [[-1, +1], [+1, +1], [+1, -1], [-1, -1]]
        let moves = []
        for (const [dr, dc] of directions)
            moves = moves.concat(this.#slide(row, col, dr, dc))
        return moves
    }
    #rook(row, col) {
        const directions = [[-1, 0], [0, 1], [1, 0], [0, -1]]
        let moves = []
        for (const [dr, dc] of directions) {
            moves = moves.concat(this.#slide(row, col, dr, dc))
        }
        return moves
    }
    #queen(row, col) {
        const directions = [[-1, 0], [0, 1], [1, 0], [0, -1], [-1, 1], [1, 1], [1, -1], [-1, -1]]
        let moves = []
        for (const [dr, dc] of directions) {
            moves = moves.concat(this.#slide(row, col, dr, dc))
        }
        return moves
    }
    #king(row, col) {
        let list1 = []
        const s = new Set()
        this.player.forEach(e => {
            const res = this.#filterEnemy([e[0], row, col])
            if (res) {
                res.forEach(v => s.add(v))
            }
        })
        const directions = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        for (let i = 0; i < 8; i++) {
            const [dr, dc] = directions[i]
            const r = row + dr
            const c = col + dc
            if (
                r >= 0 && r < ROWLEN &&
                c >= 0 && c < COLLEN &&
                (this.matrix[r][c] >= 7 || this.matrix[r][c] === 0) &&
                !s.has(i + 1)
            ) {
                list1.push([r, c])
            }
        }
        return list1
    }
}