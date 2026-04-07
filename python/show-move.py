import sys
import json
from pathlib import Path
from chessman import PlayerChessman, BotChessman

def _checkMove(prow, pcol):
    # go to the config.json
    config_path = Path(__file__).resolve().parents[1] / "chess.config.json"

    # read the row-length and column-length from config.json
    with open(config_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        matrix = data.get("matrix", [])
        PLAYER = data.get("player", 0)
        BOT = data.get("bot", 0)
    
    if matrix[prow][pcol] <= 12 and matrix[prow][pcol] > 6:
        return list(PlayerChessman(matrix, [prow, pcol], BOT))
    elif matrix[prow][pcol] <= 6 and matrix[prow][pcol] > 0:
        return list(BotChessman(matrix, [prow, pcol], PLAYER))
    else:
        return [None]
    

if __name__ == "__main__":
    # Receive two arguments from JS
    row = int(sys.argv[1])
    col = int(sys.argv[2])

    result = _checkMove(row, col)

    # Send the result back to JavaScript
    print(json.dumps(list(result)))
