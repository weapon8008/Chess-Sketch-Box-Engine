import sys
import json
from chessman import PlayerChessman, BotChessman

def _checkMove(prow, pcol, board):
    ROWLEN = board["row"]
    COLLEN = board["col"]
    matrix = board["matrix"]
    PLAYER = board["player"]
    BOT = board["bot"]
    
    if matrix[prow][pcol] <= 12 and matrix[prow][pcol] > 6:
        return list(PlayerChessman(matrix, [prow, pcol], BOT, ROWLEN, COLLEN))
    elif matrix[prow][pcol] <= 6 and matrix[prow][pcol] > 0:
        return list(BotChessman(matrix, [prow, pcol], PLAYER, ROWLEN, COLLEN))
    else:
        return [None]
    

if __name__ == "__main__":
    # Receive two arguments from JS
    input_data = sys.stdin.read()
    data = json.loads(input_data)
    row = data["row"]
    col = data["col"]
    boardData = data["boardData"]

    result = _checkMove(row, col, boardData)

    # Send the result back to JavaScript
    print(json.dumps(list(result)))
    # print(boardData["matrix"])
