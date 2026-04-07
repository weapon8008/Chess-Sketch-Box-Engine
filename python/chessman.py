import json
import multiprocessing as mp
from pathlib import Path

# go to the config.json
config_path = Path(__file__).resolve().parents[1] / "chess.config.json"

# read the row-length and column-length from config.json
with open(config_path, "r", encoding="utf-8") as file:
    data = json.load(file)
    ROWLEN = data.get("row", 0)
    COLLEN = data.get("col", 0)

def _oneInteger(old_row, old_col, new_row, new_col):
    '''
    This convert the list of position [old_row, old_col, new_row, new_col] into one integer
    by taking, n = ROWLEN if the ROWLEN >= COLLEN else n = COLLEN
    n = old_row + old_col*(n) + new_row*(n**2) + new_col*(n**3)
    '''
    n = ROWLEN if ROWLEN >= COLLEN else COLLEN
    return old_row + old_col*(n) + new_row*(n**2) + new_col*(n**3)

# top-level worker function
def _worker(fn, args, q):
    q.put(fn(*args))

class PlayerChessman:
    # constructor
    def __init__(self, matrix, pos, bot):
        self.__matrix = [row[:] for row in matrix]
        self.__pos = pos
        self.__bot = bot
        
    # inner moves of chessman
    def _top(self, row, col):
        list1 = []
        for i in range(row - 1, -1, -1):
            if self.__matrix[i][col] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, i, col), self.__matrix[i][col]])
            elif self.__matrix[i][col] <= 6:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, i, col), self.__matrix[i][col]])
                break
            else:
                break
        return list1
    def _rightTop(self, row, col):
        list1 = []
        for i in range(1, ROWLEN):
            if self.__matrix[row - i][col + i] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row-i, col+i), self.__matrix[row - i][col + i]])
            elif self.__matrix[row - i][col + i] < 7:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row-i, col+i), self.__matrix[row - i][col + i]])
                break
            else:
                break

            if (row - i == 0 or col + i == COLLEN - 1):
                break
        
        return list1
    def _right(self, row, col):
        list1 = []
        for i in range(col + 1, COLLEN):
            if self.__matrix[row][i] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row, i), self.__matrix[row][i]])
            elif self.__matrix[row][i] <= 6:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row, i), self.__matrix[row][i]])
                break
            else:
                break
        return list1
    def _rightBottom(self, row, col):
        list1 = []
        for i in range(1, ROWLEN):
            if self.__matrix[row + i][col + i] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row+i, col+i), self.__matrix[row + i][col + i]])
            elif self.__matrix[row + i][col + i] < 7:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row+i, col+i), self.__matrix[row + i][col + i]])
                break
            else:
                break

            if (row + i == ROWLEN - 1 or col + i == COLLEN - 1):
                break
        return list1
    def _bottom(self, row, col):
        list1 = []
        for i in range(row + 1, ROWLEN):
            if self.__matrix[i][col] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, i, col), self.__matrix[i][col]])
            elif self.__matrix[i][col] <= 6:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, i, col), self.__matrix[i][col]])
                break
            else:
                break
        return list1
    def _leftBottom(self, row, col):
        list1 = []
        for i in range(1, ROWLEN):
            if self.__matrix[row + i][col - i] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row+i, col-i), self.__matrix[row + i][col - i]])
            elif self.__matrix[row + i][col - i] < 7:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row+i, col-i), self.__matrix[row + i][col - i]])
                break
            else:
                break

            if (row + i == ROWLEN - 1 or col - i == 0):
                break
        return list1
    def _left(self, row, col):
        list1 = []
        for i in range(col - 1, -1, -1):
            if self.__matrix[row][i] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row, i), self.__matrix[row][i]])
            elif self.__matrix[row][i] <= 6:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row, i), self.__matrix[row][i]])
                break
            else:
                break
        return list1
    def _leftTop(self, row, col):
        list1 = []
        for i in range(1, ROWLEN):
            if self.__matrix[row - i][col - i] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row-i, col-i), self.__matrix[row - i][col - i]])
            elif self.__matrix[row - i][col - i] < 7:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row-i, col-i), self.__matrix[row - i][col - i]])
                break
            else:
                break

            if (row - i == 0 or col - i == 0):
                break
        return list1
    
    # check where king cannot move
    def _filterEnemy(self, arg):
        enemy, row, col = arg
        if self.__matrix[enemy[0]][enemy[1]] == 1:
            if enemy[0] == row-2 and enemy[1] == col-2:
                return [1]
            elif enemy[0] == row-2 and enemy[1] == col-1:
                return [2]
            elif enemy[0] == row-2 and enemy[1] == col:
                return [1, 3]
            elif enemy[0] == row-2 and enemy[1] == col+1:
                return [2]
            elif enemy[0] == row-2 and enemy[1] == col+2:
                return [3]
            elif enemy[0] == row-1 and enemy[1] == col-2:
                return [4]
            elif enemy[0] == row-1 and enemy[1] == col:
                return [4, 5]
            elif enemy[0] == row-1 and enemy[1] == col+2:
                return [5]
            elif enemy[0] == row and enemy[1] == col-2:
                return [6]
            elif enemy[0] == row and enemy[1] == col-1:
                return [7]
            elif enemy[0] == row and enemy[1] == col+1:
                return [7]
            elif enemy[0] == row and enemy[1] == col+2:
                return [8]
        elif self.__matrix[enemy[0]][enemy[1]] == 2:
            if (enemy[0] == (row-3) and enemy[1] == (col-2)):
                return [1]
            elif (enemy[0] == (row-3) and enemy[1] == (col-1)):
                return [2]
            elif (enemy[0] == (row-3) and enemy[1] == (col)):
                return [1, 3]
            elif (enemy[0] == (row-3) and enemy[1] == (col+1)):
                return [2]
            elif (enemy[0] == (row-3) and enemy[1] == (col+2)):
                return [3]
            elif (enemy[0] == (row-2) and enemy[1] == (col-3)):
                return [1]
            elif (enemy[0] == (row-2) and enemy[1] == (col-2)):
                return [2, 4]
            elif (enemy[0] == (row-2) and enemy[1] == (col-1)):
                return [3]
            elif (enemy[0] == (row-2) and enemy[1] == (col)):
                return [4, 5]
            elif (enemy[0] == (row-2) and enemy[1] == (col+1)):
                return [1]
            elif (enemy[0] == (row-2) and enemy[1] == (col+2)):
                return [2, 5]
            elif (enemy[0] == (row-2) and enemy[1] == (col+3)):
                return [3]
            elif (enemy[0] == (row-1) and enemy[1] == (col-3)):
                return [4]
            elif (enemy[0] == (row-1) and enemy[1] == (col-2)):
                return [6]
            elif (enemy[0] == (row-1) and enemy[1] == (col-1)):
                return [5, 7]
            elif (enemy[0] == (row-1) and enemy[1] == (col)):
                return [6, 8]
            elif (enemy[0] == (row-1) and enemy[1] == (col+1)):
                return [4, 7]
            elif (enemy[0] == (row-1) and enemy[1] == (col+2)):
                return [8]
            elif (enemy[0] == (row-1) and enemy[1] == (col+3)):
                return [5]
            elif (enemy[0] == (row) and enemy[1] == (col-3)):
                return [1, 6]
            elif (enemy[0] == (row) and enemy[1] == (col-2)):
                return [2, 7]
            elif (enemy[0] == (row) and enemy[1] == (col-1)):
                return [3, 8]
            elif (enemy[0] == (row) and enemy[1] == (col+1)):
                return [1, 6]
            elif (enemy[0] == (row) and enemy[1] == (col+2)):
                return [2, 7]
            elif (enemy[0] == (row) and enemy[1] == (col+3)):
                return [3, 8]
            elif (enemy[0] == (row+1) and enemy[1] == (col-3)):
                return [4]
            elif (enemy[0] == (row+1) and enemy[1] == (col-2)):
                return [1]
            elif (enemy[0] == (row+1) and enemy[1] == (col-1)):
                return [2, 5]
            elif (enemy[0] == (row+1) and enemy[1] == (col)):
                return [1, 3]
            elif (enemy[0] == (row+1) and enemy[1] == (col+1)):
                return [2, 4]
            elif (enemy[0] == (row+1) and enemy[1] == (col+2)):
                return [3]
            elif (enemy[0] == (row+1) and enemy[1] == (col+3)):
                return [5]
            elif (enemy[0] == (row+2) and enemy[1] == (col-3)):
                return [6]
            elif (enemy[0] == (row+2) and enemy[1] == (col-2)):
                return [4, 7]
            elif (enemy[0] == (row+2) and enemy[1] == (col-1)):
                return [8]
            elif (enemy[0] == (row+2) and enemy[1] == (col)):
                return [4, 5]
            elif (enemy[0] == (row+2) and enemy[1] == (col+1)):
                return [6]
            elif (enemy[0] == (row+2) and enemy[1] == (col+2)):
                return [5, 7]
            elif (enemy[0] == (row+2) and enemy[1] == (col+3)):
                return [8]
            elif (enemy[0] == (row-3) and enemy[1] == (col-2)):
                return [6]
            elif (enemy[0] == (row-3) and enemy[1] == (col-1)):
                return [7]
            elif (enemy[0] == (row-3) and enemy[1] == (col)):
                return [6, 8]
            elif (enemy[0] == (row-3) and enemy[1] == (col+1)):
                return [7]
            elif (enemy[0] == (row-3) and enemy[1] == (col+2)):
                return [8]
        elif self.__matrix[enemy[0]][enemy[1]] == 3:
            if enemy[0] == (row+2) and enemy[1] == col:
                return [6, 8]
            elif (enemy[0] == (row+1) and enemy[1] == col) or (enemy[0] == (row-1) and enemy[1] == col):
                return [4, 5]
            elif enemy[0] == (row-2) and enemy[1] == col:
                return [1, 3]
            elif enemy[0] == row and enemy[1] == (col+2):
                return [3, 8]
            elif (enemy[0] == row and enemy[1] == (col+1)) or (enemy[0] == row and enemy[1] == (col-1)):
                return [2, 7]
            elif enemy[0] == row and enemy[1] == (col-2):
                return [1, 6]
            else:
                if enemy[0] != (row-1) and enemy[1] != (col-1) and abs(enemy[0]-(row-1)) == abs(enemy[1]-(col-1)):
                    if enemy[0] != (row+1) and enemy[1] != (col+1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col+1)):
                        if enemy[0] < (row-1) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row-1][col-1] != 0:
                                return [1]
                        elif enemy[0] > (row+1) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-(row+1))):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row+1][col+1] != 0:
                                return [8]
                        return [1, 8]
                    else:
                        if enemy[0] < (row-1) and enemy[1] > (col-1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                        elif enemy[0] > (row-1) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                        return [1]
                elif enemy[0] != (row-1) and enemy[1] != (col) and abs(enemy[0]-(row-1)) == abs(enemy[1]-(col)):
                    if enemy[0] != (row) and enemy[1] != (col+1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col+1)):
                        if enemy[0] < (row-1) and enemy[1] < (col):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row-1][col] != 0:
                                return [2]
                        elif enemy[0] > (row) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row][col+1] != 0:
                                return [5]
                        return [2, 5]
                    elif enemy[0] != (row) and enemy[1] != (col-1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col-1)):
                        if enemy[0] < (row-1) and enemy[1] > (col):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row-1][col] != 0:
                                return [2]
                        elif enemy[0] > (row) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row][col-1] != 0:
                                return [4]
                        return [2, 4]
                elif enemy[0] != (row-1) and enemy[1] != (col+1) and abs(enemy[0]-(row-1)) == abs(enemy[1]-(col+1)):
                    if enemy[0] != (row+1) and enemy[1] != (col-1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col-1)):
                        if enemy[0] < (row-1) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row-1][col+1] != 0:
                                return [3]
                        elif enemy[0] > (row+1) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-(row+1))):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row+1][col-1] != 0:
                                return [6]
                        return [3, 6]
                    else:
                        if enemy[0] < (row-1) and enemy[1] < (col+1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                        elif enemy[0] > (row-1) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                        return [3]
                elif enemy[0] != (row) and enemy[1] != (col-1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col-1)):
                    if enemy[0] != (row+1) and enemy[1] != (col) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col)):
                        if enemy[0] < (row) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row-1][col] != 0:
                                return [4]
                        elif enemy[0] > (row+1) and enemy[1] > (col):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row+1][col] != 0:
                                return [7]
                        return [4, 7]
                elif enemy[0] != (row) and enemy[1] != (col+1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col+1)):
                    if enemy[0] != (row+1) and enemy[1] != (col) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col)):
                        if enemy[0] < (row) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row][col+1] != 0:
                                return [5]
                        elif enemy[0] > (row+1) and enemy[1] < (col):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row+1][col] != 0:
                                return [7]
                        return [5, 7]
                elif enemy[0] != (row+1) and enemy[1] != (col-1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col-1)):
                    if enemy[0] < (row+1) and enemy[1] < (col-1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                return None
                    elif enemy[0] > (row+1) and enemy[1] > (col-1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                return None
                    return [6]
                elif enemy[0] != (row+1) and enemy[1] != (col+1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col+1)):
                    if enemy[0] < (row+1) and enemy[1] > (col+1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                return None
                    elif enemy[0] > (row+1) and enemy[1] < (col+1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                return None
                    return [8]
        elif self.__matrix[enemy[0]][enemy[1]] == 4:
            if enemy[0] == row-1 and enemy[1] == col-1:
                if self.__matrix[row][col-1] != 0 and self.__matrix[row-1][col] != 0:
                    return [2, 4]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 4, 6]
                elif self.__matrix[row][col-1] != 0:
                    return [2, 3, 4]
                else:
                    return [2, 3, 4, 6]
            elif enemy[0] == row-1 and enemy[1] == col:
                return [1, 3, 7]
            elif enemy[0] == row-1 and enemy[1] == col+1:
                if self.__matrix[row][col+1] != 0 and self.__matrix[row-1][col] != 0:
                    return [2, 5]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 5, 8]
                elif self.__matrix[row][col+1] != 0:
                    return [1, 2, 5]
                else:
                    return [1, 2, 5, 8]
            elif enemy[0] == row and enemy[1] == col-1:
                return [1, 5, 6]
            elif enemy[0] == row and enemy[1] == col+1:
                return [3, 4, 8]
            elif enemy[0] == row+1 and enemy[1] == col-1:
                if self.__matrix[row][col-1] != 0 and self.__matrix[row+1][col] != 0:
                    return [4, 7]
                elif self.__matrix[row+1][col] != 0:
                    return [1, 4, 7]
                elif self.__matrix[row][col-1] != 0:
                    return [4, 7, 8]
                else:
                    return [1, 4, 7, 8]
            elif enemy[0] == row+1 and enemy[1] == col:
                return [2, 6, 8]
            elif enemy[0] == row+1 and enemy[1] == col+1:
                if self.__matrix[row][col+1] != 0 and self.__matrix[row+1][col] != 0:
                    return [5, 7]
                elif self.__matrix[row+1][col] != 0:
                    return [3, 5, 7]
                elif self.__matrix[row][col+1] != 0:
                    return [5, 6, 7]
                else:
                    return [3, 5, 6, 7]
            else:
                if enemy[0] == row-1:
                    if  enemy[1] < col-1:
                        for x in range(enemy[1]+1, col-1):
                            if self.__matrix[row-1][x] != 0:
                                return None
                        if self.__matrix[row-1][col-1] != 0:
                            return [1]
                        elif self.__matrix[row-1][col] != 0:
                            return [1, 2]
                    elif enemy[1] > col+1:
                        for x in range(col+2, enemy[1]):
                            if self.__matrix[row-1][x] != 0:
                                return None
                        if self.__matrix[row-1][col+1] != 0:
                            return [3]
                        elif self.__matrix[row-1][col] != 0:
                            return [2, 3]
                    return [1, 2, 3]
                elif enemy[0] == row:
                    if  enemy[1] < col-1:
                        for x in range(enemy[1]+1, col-1):
                            if self.__matrix[row][x] != 0:
                                return None
                        if self.__matrix[row][col-1] != 0:
                            return [4]
                    elif enemy[1] > col+1:
                        for x in range(col+2, enemy[1]):
                            if self.__matrix[row][x] != 0:
                                return None
                        if self.__matrix[row][col+1] != 0:
                            return [5]
                    return [4, 5]
                elif enemy[0] == row+1:
                    if enemy[1] < col-1:
                        for x in range(enemy[1]+1, col-1):
                            if self.__matrix[row+1][x] != 0:
                                return None
                        if self.__matrix[row+1][col-1] != 0:
                            return [6]
                        elif self.__matrix[row+1][col] != 0:
                            return [6, 7]
                    elif enemy[1] > col+1:
                        for x in range(col+2, enemy[1]):
                            if self.__matrix[row+1][x] != 0:
                                return None
                        if self.__matrix[row+1][col+1] != 0:
                            return [8]
                        elif self.__matrix[row+1][col] != 0:
                            return [7, 8]
                    return [6, 7, 8]
                elif enemy[1] == col-1:
                    if enemy[0] < row-1:
                        for x in range(enemy[0]+1, row-1):
                            if self.__matrix[x][col-1] != 0:
                                return None
                        if self.__matrix[row-1][col-1] != 0:
                            return [1]
                        elif self.__matrix[row][col-1] != 0:
                            return [1, 4]
                    elif enemy[0] > row+1:
                        for x in range(row+2, enemy[0]):
                            if self.__matrix[x][col-1] != 0:
                                return None
                        if self.__matrix[row+1][col-1] != 0:
                            return [6]
                        elif self.__matrix[row][col-1] != 0:
                            return [4, 6]
                    return [1, 4, 6]
                elif enemy[1] == col:
                    if enemy[0] < row-1:
                        for x in range(enemy[0]+1, row-1):
                            if self.__matrix[x][col] != 0:
                                return None
                        if self.__matrix[row-1][col] != 0:
                            return [2]
                    elif enemy[0] > row+1:
                        for x in range(row+2, enemy[0]):
                            if self.__matrix[x][col] != 0:
                                return None
                        if self.__matrix[row+1][col] != 0:
                            return [7]
                    return [2, 7]
                elif enemy[1] == col+1:
                    if enemy[0] < row-1:
                        for x in range(enemy[0]+1, row-1):
                            if self.__matrix[x][col+1] != 0:
                                return None
                        if self.__matrix[row-1][col+1] != 0:
                            return [3]
                        elif self.__matrix[row][col+1] != 0:
                            return [3, 5]
                    elif enemy[0] > row+1:
                        for x in range(row+2, enemy[0]):
                            if self.__matrix[x][col+1] != 0:
                                return None
                        if self.__matrix[row+1][col+1] != 0:
                            return [8]
                        elif self.__matrix[row][col+1] != 0:
                            return [5, 8]
                    return [3, 5, 8]
        elif self.__matrix[enemy[0]][enemy[1]] == 5:
            if enemy[0] == row-1 and enemy[1] == col-1:
                if self.__matrix[row-1][col] != 0 and self.__matrix[row][col-1] != 0:
                    return [2, 4, 8]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 4, 6, 8]
                elif self.__matrix[row][col-1] != 0:
                    return [2, 3, 4, 8]
                else:
                    return [2, 3, 4, 6, 8]
            elif enemy[0] == row-1 and enemy[1] == col:
                return [1, 3, 4, 5, 7]
            elif enemy[0] == row-1 and enemy[1] == col+1:
                if self.__matrix[row-1][col] != 0 and self.__matrix[row][col+1] != 0:
                    return [2, 5, 6]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 5, 6, 8]
                elif self.__matrix[row][col-1] != 0:
                    return [1, 2, 5, 6]
                else:
                    return [1, 2, 5, 6, 8]
            elif enemy[0] == row and enemy[1] == col-1:
                return [1, 2, 5, 6, 7]
            elif enemy[0] == row and enemy[1] == col+1:
                return [2, 3, 4, 7, 8]
            elif enemy[0] == row+1 and enemy[1] == col-1:
                if self.__matrix[row+1][col] != 0 and self.__matrix[row][col-1] != 0:
                    return [3, 4, 7]
                elif self.__matrix[row+1][col] != 0:
                    return [1, 3, 4, 7]
                elif self.__matrix[row][col-1] != 0:
                    return [3, 4, 7, 8]
                else:
                    return [1, 3, 4, 7, 8]
            elif enemy[0] == row+1 and enemy[1] == col:
                return [2, 4, 5, 6, 8]
            elif enemy[0] == row+1 and enemy[1] == col+1:
                if self.__matrix[row+1][col] != 0 and self.__matrix[row][col+1] != 0:
                    return [1, 5, 7]
                elif self.__matrix[row+1][col] != 0:
                    return [1, 3, 5, 7]
                elif self.__matrix[row][col+1] != 0:
                    return [1, 5, 6, 7]
                else:
                    return [1, 3, 5, 6, 7]
            elif enemy[0] == row-2 and enemy[1] == col-1:
                if self.__matrix[row-1][col-1] != 0 and self.__matrix[row-1][col] != 0:
                    return [1, 2]
                elif self.__matrix[row][col-1] != 0 and self.__matrix[row-1][col] != 0:
                    return [1, 2, 4]
                elif self.__matrix[row-1][col-1] != 0:
                    return [1, 2, 5]
                elif self.__matrix[row-1][col] != 0:
                    return [1, 2, 4, 6]
                elif self.__matrix[row][col-1] != 0:
                    return [1, 2, 4, 5]
                else:
                    return [1, 2, 4, 5, 6]
            elif enemy[0] == row-2 and enemy[1] == col:
                if self.__matrix[row-1][col] != 0:
                    return [1, 2, 3]
                else:
                    return [1, 2, 3, 7]
            elif enemy[0] == row-2 and enemy[1] == col+1:
                if self.__matrix[row-1][col+1] != 0 and self.__matrix[row-1][col] != 0:
                    return [2, 3]
                elif self.__matrix[row][col+1] != 0 and self.__matrix[row-1][col] != 0:
                    return [2, 3, 5]
                elif self.__matrix[row-1][col+1] != 0:
                    return [2, 3, 4]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 3, 5, 8]
                elif self.__matrix[row][col+1] != 0:
                    return [2, 3, 4, 5]
                else:
                    return [2, 3, 4, 5, 8]
            elif enemy[0] == row-1 and enemy[1] == col-2:
                if self.__matrix[row-1][col-1] != 0 and self.__matrix[row][col-1] != 0:
                    return [1, 4]
                elif self.__matrix[row-1][col] != 0 and self.__matrix[row][col-1] != 0:
                    return [1, 2, 4]
                elif self.__matrix[row-1][col-1] != 0:
                    return [1, 4, 7]
                elif self.__matrix[row-1][col] != 0:
                    return [1, 2, 4, 7]
                elif self.__matrix[row][col-1] != 0:
                    return [1, 2, 3, 4]
                else:
                    return [1, 2, 3, 4, 7]
            elif enemy[0] == row and enemy[1] == col-2:
                if self.__matrix[row][col-1] != 0:
                    return [1, 4, 6]
                else:
                    return [1, 4, 5, 6]
            elif enemy[0] == row+1 and enemy[1] == col-2:
                if self.__matrix[row+1][col-1] != 0 and self.__matrix[row][col-1] != 0:
                    return [4, 6]
                elif self.__matrix[row+1][col] != 0 and self.__matrix[row][col-1] != 0:
                    return [4, 6, 7]
                elif self.__matrix[row+1][col-1] != 0:
                    return [2, 4, 6]
                elif self.__matrix[row+1][col] != 0:
                    return [2, 4, 6, 7]
                elif self.__matrix[row][col-1] != 0:
                    return [4, 6, 7, 8]
                else:
                    return [2, 4, 6, 7, 8]
            elif enemy[0] == row+2 and enemy[1] == col-1:
                if self.__matrix[row+1][col-1] != 0 and self.__matrix[row+1][col] != 0:
                    return [6, 7]
                elif self.__matrix[row][col-1] != 0 and self.__matrix[row+1][col] != 0:
                    return [4, 6, 7]
                elif self.__matrix[row+1][col-1] != 0:
                    return [5, 6, 7]
                elif self.__matrix[row+1][col] != 0:
                    return [1, 4, 6, 7]
                elif self.__matrix[row][col-1] != 0:
                    return [4, 5, 6, 7]
                else:
                    return [1, 4, 5, 6, 7]
            elif enemy[0] == row+2 and enemy[1] == col:
                if self.__matrix[row+1][col] != 0:
                    return [6, 7, 8]
                else:
                    return [2, 6, 7, 8]
            elif enemy[0] == row+2 and enemy[1] == col+1:
                if self.__matrix[row+1][col+1] != 0 and self.__matrix[row+1][col] != 0:
                    return [7, 8]
                elif self.__matrix[row][col+1] != 0 and self.__matrix[row+1][col] != 0:
                    return [5, 7, 8]
                elif self.__matrix[row+1][col+1] != 0:
                    return [4, 7, 8]
                elif self.__matrix[row+1][col] != 0:
                    return [3, 5, 7, 8]
                elif self.__matrix[row][col+1] != 0:
                    return [4, 5, 7, 8]
                else:
                    return [3, 4, 5, 7, 8]
            elif enemy[0] == row-1 and enemy[1] == col+2:
                if self.__matrix[row-1][col+1] != 0 and self.__matrix[row][col+1] != 0:
                    return [3, 5]
                elif self.__matrix[row-1][col] != 0 and self.__matrix[row][col+1] != 0:
                    return [2, 3, 5]
                elif self.__matrix[row-1][col+1] != 0:
                    return [3, 5, 7]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 3, 5, 7]
                elif self.__matrix[row][col+1] != 0:
                    return [1, 2, 3, 5]
                else:
                    return [1, 2, 3, 5, 7]
            elif enemy[0] == row and enemy[1] == col+2:
                if self.__matrix[row][col+1] != 0:
                    return [3, 5, 8]
                else:
                    return [3, 4, 5, 8]
            elif enemy[0] == row+1 and enemy[1] == col+2:
                if self.__matrix[row+1][col+1] != 0 and self.__matrix[row][col+1] != 0:
                    return [5, 8]
                elif self.__matrix[row+1][col] != 0 and self.__matrix[row][col+1] != 0:
                    return [5, 7, 8]
                elif self.__matrix[row+1][col+1] != 0:
                    return [2, 5, 8]
                elif self.__matrix[row+1][col] != 0:
                    return [2, 5, 7, 8]
                elif self.__matrix[row][col+1] != 0:
                    return [5, 6, 7, 8]
                else:
                    return [2, 5, 6, 7, 8]
            elif enemy[0] == row-3 and enemy[1] == col-1:
                if self.__matrix[row-2][col-1] != 0 and self.__matrix[row-2][col] != 0:
                    return None
                elif self.__matrix[row-2][col-1] != 0:
                    return [3]
                elif self.__matrix[row-2][col] != 0:
                    return [1]
                elif self.__matrix[row-1][col-1] != 0:
                    return [1, 3]
                elif self.__matrix[row][col-1] != 0:
                    return [1, 4, 3]
                else:
                    return [1, 3, 4, 6]
            elif enemy[0] == row-3 and enemy[1] == col:
                if self.__matrix[row-2][col] != 0:
                    return None
                elif self.__matrix[row-1][col] != 0:
                    return [2]
                else:
                    return [2, 7]
            elif enemy[0] == row-3 and enemy[1] == col+1:
                if self.__matrix[row-2][col+1] != 0 and self.__matrix[row-2][col] != 0:
                    return None
                elif self.__matrix[row-2][col+1] != 0:
                    return [1]
                elif self.__matrix[row-2][col] != 0:
                    return [3]
                elif self.__matrix[row-1][col+1] != 0:
                    return [1, 3]
                elif self.__matrix[row][col+1] != 0:
                    return [1, 3, 5]
                else:
                    return [1, 3, 5, 8]
            elif enemy[0] == row-1 and enemy[1] == col-3:
                if self.__matrix[row-1][col-2] != 0 and self.__matrix[row][col-2] != 0:
                    return None
                elif self.__matrix[row-1][col-2] != 0:
                    return [6]
                elif self.__matrix[row][col-2] != 0:
                    return [1]
                elif self.__matrix[row-1][col-1] != 0:
                    return [1, 6]
                elif self.__matrix[row-1][col] != 0:
                    return [1, 2, 6]
                else:
                    return [1, 2, 3, 6]
            elif enemy[0] == row and enemy[1] == col-3:
                if self.__matrix[row][col-2] != 0:
                    return None
                elif self.__matrix[row][col-1] != 0:
                    return [4]
                else:
                    return [4, 5]
            elif enemy[0] == row+1 and enemy[1] == col-3:
                if self.__matrix[row+1][col-2] != 0 and self.__matrix[row][col-2] != 0:
                    return None
                elif self.__matrix[row+1][col-2] != 0:
                    return [1]
                elif self.__matrix[row][col-2] != 0:
                    return [6]
                elif self.__matrix[row+1][col-1] != 0:
                    return [1, 6]
                elif self.__matrix[row+1][col] != 0:
                    return [1, 6, 7]
                else:
                    return [1, 3, 4, 6]
            elif enemy[0] == row+3 and enemy[1] == col-1:
                if self.__matrix[row+2][col-1] != 0 and self.__matrix[row+2][col] != 0:
                    return None
                elif self.__matrix[row+2][col-1] != 0:
                    return [8]
                elif self.__matrix[row+2][col] != 0:
                    return [6]
                elif self.__matrix[row+1][col-1] != 0:
                    return [6, 8]
                elif self.__matrix[row][col-1] != 0:
                    return [4, 6, 8]
                else:
                    return [1, 4, 6, 8]
            elif enemy[0] == row+3 and enemy[1] == col:
                if self.__matrix[row+2][col] != 0:
                    return None
                elif self.__matrix[row+1][col] != 0:
                    return [7]
                else:
                    return [2, 7]
            elif enemy[0] == row+3 and enemy[1] == col+1:
                if self.__matrix[row+2][col+1] != 0 and self.__matrix[row+2][col] != 0:
                    return None
                elif self.__matrix[row+2][col+1] != 0:
                    return [6]
                elif self.__matrix[row+2][col] != 0:
                    return [8]
                elif self.__matrix[row+1][col+1] != 0:
                    return [6, 8]
                elif self.__matrix[row][col+1] != 0:
                    return [5, 6, 8]
                else:
                    return [3, 5, 6, 8]
            elif enemy[0] == row-1 and enemy[1] == col+3:
                if self.__matrix[row-1][col+2] != 0 and self.__matrix[row][col+2] != 0:
                    return None
                elif self.__matrix[row-1][col+2] != 0:
                    return [8]
                elif self.__matrix[row+2][col] != 0:
                    return [3]
                elif self.__matrix[row-1][col+1] != 0:
                    return [3, 8]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 3, 8]
                else:
                    return [1, 2, 3, 8]
            elif enemy[0] == row and enemy[1] == col+3:
                if self.__matrix[row][col+2] != 0:
                    return None
                elif self.__matrix[row][col+1] != 0:
                    return [5]
                else:
                    return [4, 5]
            elif enemy[0] == row+1 and enemy[1] == col+3:
                if self.__matrix[row+1][col+2] != 0 and self.__matrix[row][col+2] != 0:
                    return None
                elif self.__matrix[row+1][col+2] != 0:
                    return [3]
                elif self.__matrix[row+2][col] != 0:
                    return [8]
                elif self.__matrix[row+1][col+1] != 0:
                    return [3, 8]
                elif self.__matrix[row+1][col] != 0:
                    return [3, 7, 8]
                else:
                    return [3, 6, 7, 8]
            elif (((enemy[0] >= 0 and enemy[0] < row-3) or (enemy[0] > row+3 and enemy[0] < ROWLEN)) and (enemy[1] >= col-1 and enemy[1] <= col+1)) or (((enemy[1] >= 0 and enemy[1] < col-3) or (enemy[1] > col+3 and enemy[1] < COLLEN)) and (enemy[0] >= row-1 and enemy[0] <= row+1)):
                if enemy[0] == row-1:
                    if  enemy[1] < col-1:
                        for x in range(enemy[1]+1, col-1):
                            if self.__matrix[row-1][x] != 0:
                                return None
                        if self.__matrix[row-1][col-1] != 0:
                            return [1]
                        elif self.__matrix[row-1][col] != 0:
                            return [1, 2]
                    elif enemy[1] > col+1:
                        for x in range(col+2, enemy[1]):
                            if self.__matrix[row-1][x] != 0:
                                return None
                        if self.__matrix[row-1][col+1] != 0:
                            return [3]
                        elif self.__matrix[row-1][col] != 0:
                            return [2, 3]
                    return [1, 2, 3]
                elif enemy[0] == row:
                    if  enemy[1] < col-1:
                        for x in range(enemy[1]+1, col-1):
                            if self.__matrix[row][x] != 0:
                                return None
                        if self.__matrix[row][col-1] != 0:
                            return [4]
                    elif enemy[1] > col+1:
                        for x in range(col+2, enemy[1]):
                            if self.__matrix[row][x] != 0:
                                return None
                        if self.__matrix[row][col+1] != 0:
                            return [5]
                    return [4, 5]
                elif enemy[0] == row+1:
                    if enemy[1] < col-1:
                        for x in range(enemy[1]+1, col-1):
                            if self.__matrix[row+1][x] != 0:
                                return None
                        if self.__matrix[row+1][col-1] != 0:
                            return [6]
                        elif self.__matrix[row+1][col] != 0:
                            return [6, 7]
                    elif enemy[1] > col+1:
                        for x in range(col+2, enemy[1]):
                            if self.__matrix[row+1][x] != 0:
                                return None
                        if self.__matrix[row+1][col+1] != 0:
                            return [8]
                        elif self.__matrix[row+1][col] != 0:
                            return [7, 8]
                    return [6, 7, 8]
                elif enemy[1] == col-1:
                    if enemy[0] < row-1:
                        for x in range(enemy[0]+1, row-1):
                            if self.__matrix[x][col-1] != 0:
                                return None
                        if self.__matrix[row-1][col-1] != 0:
                            return [1]
                        elif self.__matrix[row][col-1] != 0:
                            return [1, 4]
                    elif enemy[0] > row+1:
                        for x in range(row+2, enemy[0]):
                            if self.__matrix[x][col-1] != 0:
                                return None
                        if self.__matrix[row+1][col-1] != 0:
                            return [6]
                        elif self.__matrix[row][col-1] != 0:
                            return [4, 6]
                    return [1, 4, 6]
                elif enemy[1] == col:
                    if enemy[0] < row-1:
                        for x in range(enemy[0]+1, row-1):
                            if self.__matrix[x][col] != 0:
                                return None
                        if self.__matrix[row-1][col] != 0:
                            return [2]
                    elif enemy[0] > row+1:
                        for x in range(row+2, enemy[0]):
                            if self.__matrix[x][col] != 0:
                                return None
                        if self.__matrix[row+1][col] != 0:
                            return [7]
                    return [2, 7]
                elif enemy[1] == col+1:
                    if enemy[0] < row-1:
                        for x in range(enemy[0]+1, row-1):
                            if self.__matrix[x][col+1] != 0:
                                return None
                        if self.__matrix[row-1][col+1] != 0:
                            return [3]
                        elif self.__matrix[row][col+1] != 0:
                            return [3, 5]
                    elif enemy[0] > row+1:
                        for x in range(row+2, enemy[0]):
                            if self.__matrix[x][col+1] != 0:
                                return None
                        if self.__matrix[row+1][col+1] != 0:
                            return [8]
                        elif self.__matrix[row][col+1] != 0:
                            return [5, 8]
                    return [3, 5, 8]
            else:
                if enemy[0] != (row-1) and enemy[1] != (col-1) and abs(enemy[0]-(row-1)) == abs(enemy[1]-(col-1)):
                    if enemy[0] != (row+1) and enemy[1] != (col+1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col+1)):
                        if enemy[0] < (row-1) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row-1][col-1] != 0:
                                return [1]
                        elif enemy[0] > (row+1) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-(row+1))):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row+1][col+1] != 0:
                                return [8]
                        return [1, 8]
                    else:
                        if enemy[0] < (row-1) and enemy[1] > (col-1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                        elif enemy[0] > (row-1) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                        return [1]
                elif enemy[0] != (row-1) and enemy[1] != (col) and abs(enemy[0]-(row-1)) == abs(enemy[1]-(col)):
                    if enemy[0] != (row) and enemy[1] != (col+1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col+1)):
                        if enemy[0] < (row-1) and enemy[1] < (col):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row-1][col] != 0:
                                return [2]
                        elif enemy[0] > (row) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row][col+1] != 0:
                                return [5]
                        return [2, 5]
                    elif enemy[0] != (row) and enemy[1] != (col-1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col-1)):
                        if enemy[0] < (row-1) and enemy[1] > (col):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row-1][col] != 0:
                                return [2]
                        elif enemy[0] > (row) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row][col-1] != 0:
                                return [4]
                        return [2, 4]
                elif enemy[0] != (row-1) and enemy[1] != (col+1) and abs(enemy[0]-(row-1)) == abs(enemy[1]-(col+1)):
                    if enemy[0] != (row+1) and enemy[1] != (col-1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col-1)):
                        if enemy[0] < (row-1) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row-1][col+1] != 0:
                                return [3]
                        elif enemy[0] > (row+1) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-(row+1))):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row+1][col-1] != 0:
                                return [6]
                        return [3, 6]
                    else:
                        if enemy[0] < (row-1) and enemy[1] < (col+1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                        elif enemy[0] > (row-1) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                        return [3]
                elif enemy[0] != (row) and enemy[1] != (col-1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col-1)):
                    if enemy[0] != (row+1) and enemy[1] != (col) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col)):
                        if enemy[0] < (row) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row-1][col] != 0:
                                return [4]
                        elif enemy[0] > (row+1) and enemy[1] > (col):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row+1][col] != 0:
                                return [7]
                        return [4, 7]
                elif enemy[0] != (row) and enemy[1] != (col+1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col+1)):
                    if enemy[0] != (row+1) and enemy[1] != (col) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col)):
                        if enemy[0] < (row) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row][col+1] != 0:
                                return [5]
                        elif enemy[0] > (row+1) and enemy[1] < (col):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row+1][col] != 0:
                                return [7]
                        return [5, 7]
                elif enemy[0] != (row+1) and enemy[1] != (col-1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col-1)):
                    if enemy[0] < (row+1) and enemy[1] < (col-1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                return None
                    elif enemy[0] > (row+1) and enemy[1] > (col-1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                return None
                    return [6]
                elif enemy[0] != (row+1) and enemy[1] != (col+1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col+1)):
                    if enemy[0] < (row+1) and enemy[1] > (col+1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                return None
                    elif enemy[0] > (row+1) and enemy[1] < (col+1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                return None
                    return [8]
        elif self.__matrix[enemy[0]][enemy[1]] == 6:
            if enemy[0] == row-2 and enemy[1] == col-2:
                return [1]
            elif enemy[0] == row-2 and enemy[1] == col-1:
                return [1, 2]
            elif enemy[0] == row-2 and enemy[1] == col:
                return [1, 2, 3]
            elif enemy[0] == row-2 and enemy[1] == col+1:
                return [2, 3]
            elif enemy[0] == row-2 and enemy[1] == col+2:
                return [3]
            elif enemy[0] == row-1 and enemy[1] == col-2:
                return [1, 4]
            elif enemy[0] == row-1 and enemy[1] == col-1:
                return [2, 4]
            elif enemy[0] == row-1 and enemy[1] == col:
                return [1, 3, 4, 5]
            elif enemy[0] == row-1 and enemy[1] == col+1:
                return [2, 5]
            elif enemy[0] == row-1 and enemy[1] == col+2:
                return [3, 5]
            elif enemy[0] == row and enemy[1] == col-2:
                return [1, 4, 6]
            elif enemy[0] == row and enemy[1] == col-1:
                return [1, 2, 6, 7]
            elif enemy[0] == row and enemy[1] == col+1:
                return [2, 3, 7, 8]
            elif enemy[0] == row and enemy[1] == col+2:
                return [3, 5, 8]
            elif enemy[0] == row+1 and enemy[1] == col-2:
                return [4, 6]
            elif enemy[0] == row+1 and enemy[1] == col-1:
                return [4, 7]
            elif enemy[0] == row+1 and enemy[1] == col:
                return [4, 5, 6, 8]
            elif enemy[0] == row+1 and enemy[1] == col+1:
                return [5, 7]
            elif enemy[0] == row+1 and enemy[1] == col+2:
                return [5, 8]
            elif enemy[0] == row+2 and enemy[1] == col-2:
                return [6]
            elif enemy[0] == row+2 and enemy[1] == col-1:
                return [6, 7]
            elif enemy[0] == row+2 and enemy[1] == col:
                return [6, 7, 8]
            elif enemy[0] == row+2 and enemy[1] == col+1:
                return [7, 8]
            elif enemy[0] == row+2 and enemy[1] == col+2:
                return [8]
             
    # gives the result as iterable when the class is been created as an object
    def __iter__(self):
        row, col = self.__pos
        if self.__matrix[row][col] == 7:
            return iter(self._pawn(row, col))
        elif self.__matrix[row][col] == 8:
            return iter(self._knight(row, col))
        elif self.__matrix[row][col] == 9:
            return iter(self._bishop(row, col))
        elif self.__matrix[row][col] == 10:
            return iter(self._rook(row, col))
        elif self.__matrix[row][col] == 11:
            return iter(self._queen(row, col))
        elif self.__matrix[row][col] == 12:
            return iter(self._king(row, col))

    # chessmen moves
    def _pawn(self, row, col):
        list1 = []
        if row > 0:
            if row == ROWLEN - 2:
                if (self.__matrix[row - 1][col] == 0 and self.__matrix[row - 2][col] == 0):
                    list1 = [[self.__matrix[row][col], _oneInteger(row, col, row - 1, col), self.__matrix[row - 1][col]],
                             [self.__matrix[row][col], _oneInteger(row, col, row - 2, col), self.__matrix[row - 2][col]]
                             ]
                elif (self.__matrix[row - 1][col] == 0 and self.__matrix[row - 2][col] != 0):
                    list1 = [[self.__matrix[row][col], _oneInteger(row, col, row - 1, col), self.__matrix[row - 1][col]]]
            else:
                if (self.__matrix[row - 1][col] == 0):
                    list1 = [[self.__matrix[row][col], _oneInteger(row, col, row - 1, col), self.__matrix[row - 1][col]]]
            if col - 1 >= 0:
                if (self.__matrix[row - 1][col - 1] != 0 and self.__matrix[row - 1][col - 1] <= 6):
                    list1 = list1+[[self.__matrix[row][col], _oneInteger(row, col, row - 1, col - 1), self.__matrix[row - 1][col - 1]]]
            if col + 1 < COLLEN:
                if (self.__matrix[row - 1][col + 1] != 0 and self.__matrix[row - 1][col + 1] <= 6):
                    list1 = list1+[[self.__matrix[row][col], _oneInteger(row, col, row - 1, col + 1), self.__matrix[row - 1][col + 1]]]
        return list1

    def _knight(self, row, col):
        list1 = []
        if row+1 >= 0 and row+1 < ROWLEN and col+2 >= 0 and col+2 < COLLEN and self.__matrix[row+1][col+2] < 7:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+1, col+2), self.__matrix[row+1][col+2]])
        if row+2 >= 0 and row+2 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and self.__matrix[row+2][col+1] < 7:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+2, col+1), self.__matrix[row+2][col+1]])
        if row+2 >= 0 and row+2 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and self.__matrix[row+2][col-1] < 7:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+2, col-1), self.__matrix[row+2][col-1]])
        if row+1 >= 0 and row+1 < ROWLEN and col-2 >= 0 and col-2 < COLLEN and self.__matrix[row+1][col-2] < 7:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+1, col-2), self.__matrix[row+1][col-2]])
        if row-1 >= 0 and row-1 < ROWLEN and col-2 >= 0 and col-2 < COLLEN and self.__matrix[row-1][col-2] < 7:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-1, col-2), self.__matrix[row-1][col-2]])
        if row-2 >= 0 and row-2 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and self.__matrix[row-2][col-1] < 7:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-2, col-1), self.__matrix[row-2][col-1]])
        if row-2 >= 0 and row-2 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and self.__matrix[row-2][col+1] < 7:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-2, col+1), self.__matrix[row-2][col+1]])
        if row-1 >= 0 and row-1 < ROWLEN and col+2 >= 0 and col+2 < COLLEN and self.__matrix[row-1][col+2] < 7:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-1, col+2), self.__matrix[row-1][col+2]])
        return list1

    def _bishop(self, row, col):
        q = mp.Queue()
        # for multiprocessing
        rt = mp.Process(target=_worker, args=((self._rightTop, (row, col), q)))
        lt = mp.Process(target=_worker, args=((self._leftTop, (row, col), q)))
        rb = mp.Process(target=_worker, args=((self._rightBottom, (row, col), q)))
        lb = mp.Process(target=_worker, args=((self._leftBottom, (row, col), q)))
        list1 = []
        if col == 0:
            if row == 0:
                # right-bottom[row + i][col + i]
                list1 = self._rightBottom(row, col)
            elif row == ROWLEN - 1:
                # right-top[row - i][col + i]
                list1 = self._rightTop(row, col)
            else:
                # right-top[row - i][col + i]
                # right-bottom[row + i][col + i]
                processes = [rt, rb]
                
                for p in processes:
                    p.start()
                
                for p in processes:
                    p.join()
                
                for _ in processes:
                    list1.extend(q.get())
        elif col == COLLEN - 1:
            if row == 0:
                # left-bottom[row + i][col - i]
                list1 = self._leftBottom(row, col)
            elif row == ROWLEN - 1:
                # left-top[row - i][col - i]
                list1 = self._leftTop(row, col)
            else:
                # left-top[row - i][col - i]
                # left-bottom[row + i][col - i]
                processes = [lt, lb]
                
                for p in processes:
                    p.start()
                
                for p in processes:
                    p.join()
                
                for _ in processes:
                    list1.extend(q.get())
        else:
            if row == 0:
                # right-bottom[row + i][col + i]
                # left-bottom[row + i][col - i]
                processes = [rb, lb]
                
                for p in processes:
                    p.start()
                
                for p in processes:
                    p.join()
                
                for _ in processes:
                    list1.extend(q.get())
            elif row == ROWLEN - 1:
                # right-top[row - i][col + i]
                # left-top[row - i][col - i]
                processes = [rt, lt]
                
                for p in processes:
                    p.start()
                
                for p in processes:
                    p.join()
                
                for _ in processes:
                    list1.extend(q.get())
            else:
                # right-top[row - i][col + i]
                # right-bottom[row + i][col + i]
                # left-bottom[row + i][col - i]
                # left-top[row - i][col - i]
                processes = [rt, rb, lb, lt]
                
                for p in processes:
                    p.start()
                
                for p in processes:
                    p.join()
                
                for _ in processes:
                    list1.extend(q.get())

        return list1

    def _rook(self, row, col):
        q = mp.Queue()
        # for multiprocessing
        t = mp.Process(target=_worker, args=((self._top, (row, col), q)))
        r = mp.Process(target=_worker, args=((self._right, (row, col), q)))
        b = mp.Process(target=_worker, args=((self._bottom, (row, col), q)))
        l = mp.Process(target=_worker, args=((self._left, (row, col), q)))
        list1 = []
        # top[row - 1][col]
        # right[row][col + 1]
        # bottom[row + 1][col]
        # left[row][col - 1]
        processes = [t, r, b, l]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        for _ in processes:
            list1.extend(q.get())
        return list1

    def _queen(self, row, col):
        q = mp.Queue()
        # for multiprocessing
        bishop = mp.Process(target=_worker, args=((self._bishop, (row, col), q)))
        rook = mp.Process(target=_worker, args=((self._rook, (row, col), q)))
        list1 = []
        processes = [bishop, rook]
        for p in processes:
            p.start()
        for p in processes:
            p.join()
        for _ in processes:
            list1.extend(q.get())
        return list1

    def _king(self, row, col):
        list1 = []
        with mp.Pool(int(mp.cpu_count()/2)) as p:
            s = set([result for x in p.map(self._filterEnemy, [(e[0], row, col) for e in self.__bot]) if x for result in x])
        index = [i + 1 not in s for i in range(8)]
        # [row-1][col-1]=1, [row-1][col]=2, [row-1][col+1]=3, [row][col-1]=4, [row][col+1]=5, [row+1][col-1]=6, [row+1][col]=7, [row+1][col+1]=8
        if row-1 >= 0 and row-1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and self.__matrix[row-1][col-1] < 7 and index[0]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-1, col-1), self.__matrix[row-1][col-1]])
        if row-1 >= 0 and row-1 < ROWLEN and col >= 0 and col < COLLEN and self.__matrix[row-1][col] < 7 and index[1]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-1, col), self.__matrix[row-1][col]])
        if row-1 >= 0 and row-1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and self.__matrix[row-1][col+1] < 7 and index[2]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-1, col+1), self.__matrix[row-1][col+1]])
        if row >= 0 and row < ROWLEN and col-1 >= 0 and col-1 < COLLEN and self.__matrix[row][col-1] < 7 and index[3]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row, col-1), self.__matrix[row][col-1]])
        if row >= 0 and row < ROWLEN and col+1 >= 0 and col+1 < COLLEN and self.__matrix[row][col+1] < 7 and index[4]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row, col+1), self.__matrix[row][col+1]])
        if row+1 >= 0 and row+1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and self.__matrix[row+1][col-1] < 7 and index[5]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+1, col-1), self.__matrix[row+1][col-1]])
        if row+1 >= 0 and row+1 < ROWLEN and col >= 0 and col < COLLEN and self.__matrix[row+1][col] < 7 and index[6]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+1, col), self.__matrix[row+1][col]])
        if row+1 >= 0 and row+1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and self.__matrix[row+1][col+1] < 7 and index[7]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+1, col+1), self.__matrix[row+1][col+1]])
        return list1

class BotChessman:
    # constructor
    def __init__(self, matrix, pos, player):
        self.__matrix = [row[:] for row in matrix]
        self.__pos = pos
        self.__player = player
    
    # inner moves of chessman
    def _top(self, row, col):
        list1 = []
        for i in range(row - 1, -1, -1):
            if self.__matrix[i][col] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, i, col), self.__matrix[i][col]])
            elif self.__matrix[i][col] > 6:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, i, col), self.__matrix[i][col]])
                break
            else:
                break
        return list1
    def _rightTop(self, row, col):
        list1 = []
        for i in range(1, ROWLEN):
            if self.__matrix[row - i][col + i] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row-i, col+i), self.__matrix[row - i][col + i]])
            elif self.__matrix[row - i][col + i] >= 7:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row-i, col+i), self.__matrix[row - i][col + i]])
                break
            else:
                break

            if (row - i == 0 or col + i == COLLEN - 1):
                break
        return list1
    def _right(self, row, col):
        list1 = []
        for i in range(col + 1, COLLEN):
            if self.__matrix[row][i] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row, i), self.__matrix[row][i]])
            elif self.__matrix[row][i] > 6:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row, i), self.__matrix[row][i]])
                break
            else:
                break
        return list1
    def _rightBottom(self, row, col):
        list1 = []
        for i in range(1, ROWLEN):
            if self.__matrix[row + i][col + i] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row+i, col+i), self.__matrix[row + i][col + i]])
            elif self.__matrix[row + i][col + i] >= 7:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row+i, col+i), self.__matrix[row + i][col + i]])
                break
            else:
                break

            if (row + i == ROWLEN - 1 or col + i == COLLEN - 1):
                break
        return list1
    def _bottom(self, row, col):
        list1 = []
        for i in range(row + 1, ROWLEN):
            if self.__matrix[i][col] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, i, col), self.__matrix[i][col]])
            elif self.__matrix[i][col] > 6:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, i, col), self.__matrix[i][col]])
                break
            else:
                break
        return list1
    def _leftBottom(self, row, col):
        list1 = []
        for i in range(1, ROWLEN):
            if self.__matrix[row + i][col - i] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row+i, col-i), self.__matrix[row + i][col - i]])
            elif self.__matrix[row + i][col - i] >= 7:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row+i, col-i), self.__matrix[row + i][col - i]])
                break
            else:
                break

            if (row + i == ROWLEN - 1 or col - i == 0):
                break
        return list1
    def _left(self, row, col):
        list1 = []
        for i in range(col - 1, -1, -1):
            if self.__matrix[row][i] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row, i), self.__matrix[row][i]])
            elif self.__matrix[row][i] > 6:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row, i), self.__matrix[row][i]])
                break
            else:
                break

        return list1
    def _leftTop(self, row, col):
        list1 = []
        for i in range(1, ROWLEN):
            if self.__matrix[row - i][col - i] == 0:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row-i, col-i), self.__matrix[row - i][col - i]])
            elif self.__matrix[row - i][col - i] >= 7:
                list1.append([self.__matrix[row][col], _oneInteger(row, col, row-i, col-i), self.__matrix[row - i][col - i]])
                break
            else:
                break

            if (row - i == 0 or col - i == 0):
                break
        return list1
    
    # check where king cannot move
    def _filterEnemy(self, arg):
        enemy, row, col = arg
        if self.__matrix[enemy[0]][enemy[1]] == 7:
            if enemy[0] == row and enemy[1] == col-2:
                return [1]
            elif enemy[0] == row and enemy[1] == col-1:
                return [2]
            elif enemy[0] == row and enemy[1] == col+1:
                return [2]
            elif enemy[0] == row and enemy[1] == col+2:
                return [3]
            elif enemy[0] == row+1 and enemy[1] == col-2:
                return [4]
            elif enemy[0] == row+1 and enemy[1] == col:
                return [4, 5]
            elif enemy[0] == row+1 and enemy[1] == col+2:
                return [5]
            elif enemy[0] == row+2 and enemy[1] == col-2:
                return [6]
            elif enemy[0] == row+2 and enemy[1] == col-1:
                return [7]
            elif enemy[0] == row+2 and enemy[1] == col:
                return [6, 8]
            elif enemy[0] == row+2 and enemy[1] == col+1:
                return [7]
            elif enemy[0] == row+2 and enemy[1] == col+2:
                return [8]
        elif self.__matrix[enemy[0]][enemy[1]] == 8:
            if (enemy[0] == (row-3) and enemy[1] == (col-2)):
                return [1]
            elif (enemy[0] == (row-3) and enemy[1] == (col-1)):
                return [2]
            elif (enemy[0] == (row-3) and enemy[1] == (col)):
                return [1, 3]
            elif (enemy[0] == (row-3) and enemy[1] == (col+1)):
                return [2]
            elif (enemy[0] == (row-3) and enemy[1] == (col+2)):
                return [3]
            elif (enemy[0] == (row-2) and enemy[1] == (col-3)):
                return [1]
            elif (enemy[0] == (row-2) and enemy[1] == (col-2)):
                return [2, 4]
            elif (enemy[0] == (row-2) and enemy[1] == (col-1)):
                return [3]
            elif (enemy[0] == (row-2) and enemy[1] == (col)):
                return [4, 5]
            elif (enemy[0] == (row-2) and enemy[1] == (col+1)):
                return [1]
            elif (enemy[0] == (row-2) and enemy[1] == (col+2)):
                return [2, 5]
            elif (enemy[0] == (row-2) and enemy[1] == (col+3)):
                return [3]
            elif (enemy[0] == (row-1) and enemy[1] == (col-3)):
                return [4]
            elif (enemy[0] == (row-1) and enemy[1] == (col-2)):
                return [6]
            elif (enemy[0] == (row-1) and enemy[1] == (col-1)):
                return [5, 7]
            elif (enemy[0] == (row-1) and enemy[1] == (col)):
                return [6, 8]
            elif (enemy[0] == (row-1) and enemy[1] == (col+1)):
                return [4, 7]
            elif (enemy[0] == (row-1) and enemy[1] == (col+2)):
                return [8]
            elif (enemy[0] == (row-1) and enemy[1] == (col+3)):
                return [5]
            elif (enemy[0] == (row) and enemy[1] == (col-3)):
                return [1, 6]
            elif (enemy[0] == (row) and enemy[1] == (col-2)):
                return [2, 7]
            elif (enemy[0] == (row) and enemy[1] == (col-1)):
                return [3, 8]
            elif (enemy[0] == (row) and enemy[1] == (col+1)):
                return [1, 6]
            elif (enemy[0] == (row) and enemy[1] == (col+2)):
                return [2, 7]
            elif (enemy[0] == (row) and enemy[1] == (col+3)):
                return [3, 8]
            elif (enemy[0] == (row+1) and enemy[1] == (col-3)):
                return [4]
            elif (enemy[0] == (row+1) and enemy[1] == (col-2)):
                return [1]
            elif (enemy[0] == (row+1) and enemy[1] == (col-1)):
                return [2, 5]
            elif (enemy[0] == (row+1) and enemy[1] == (col)):
                return [1, 3]
            elif (enemy[0] == (row+1) and enemy[1] == (col+1)):
                return [2, 4]
            elif (enemy[0] == (row+1) and enemy[1] == (col+2)):
                return [3]
            elif (enemy[0] == (row+1) and enemy[1] == (col+3)):
                return [5]
            elif (enemy[0] == (row+2) and enemy[1] == (col-3)):
                return [6]
            elif (enemy[0] == (row+2) and enemy[1] == (col-2)):
                return [4, 7]
            elif (enemy[0] == (row+2) and enemy[1] == (col-1)):
                return [8]
            elif (enemy[0] == (row+2) and enemy[1] == (col)):
                return [4, 5]
            elif (enemy[0] == (row+2) and enemy[1] == (col+1)):
                return [6]
            elif (enemy[0] == (row+2) and enemy[1] == (col+2)):
                return [5, 7]
            elif (enemy[0] == (row+2) and enemy[1] == (col+3)):
                return [8]
            elif (enemy[0] == (row-3) and enemy[1] == (col-2)):
                return [6]
            elif (enemy[0] == (row-3) and enemy[1] == (col-1)):
                return [7]
            elif (enemy[0] == (row-3) and enemy[1] == (col)):
                return [6, 8]
            elif (enemy[0] == (row-3) and enemy[1] == (col+1)):
                return [7]
            elif (enemy[0] == (row-3) and enemy[1] == (col+2)):
                return [8]
        elif self.__matrix[enemy[0]][enemy[1]] == 9:
            if enemy[0] == (row+2) and enemy[1] == col:
                return [6, 8]
            elif (enemy[0] == (row+1) and enemy[1] == col) or (enemy[0] == (row-1) and enemy[1] == col):
                return [4, 5]
            elif enemy[0] == (row-2) and enemy[1] == col:
                return [1, 3]
            elif enemy[0] == row and enemy[1] == (col+2):
                return [3, 8]
            elif (enemy[0] == row and enemy[1] == (col+1)) or (enemy[0] == row and enemy[1] == (col-1)):
                return [2, 7]
            elif enemy[0] == row and enemy[1] == (col-2):
                return [1, 6]
            else:
                if enemy[0] != (row-1) and enemy[1] != (col-1) and abs(enemy[0]-(row-1)) == abs(enemy[1]-(col-1)):
                    if enemy[0] != (row+1) and enemy[1] != (col+1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col+1)):
                        if enemy[0] < (row-1) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row-1][col-1] != 0:
                                return [1]
                        elif enemy[0] > (row+1) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-(row+1))):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row+1][col+1] != 0:
                                return [8]
                        return [1, 8]
                    else:
                        if enemy[0] < (row-1) and enemy[1] > (col-1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                        elif enemy[0] > (row-1) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                        return [1]
                elif enemy[0] != (row-1) and enemy[1] != (col) and abs(enemy[0]-(row-1)) == abs(enemy[1]-(col)):
                    if enemy[0] != (row) and enemy[1] != (col+1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col+1)):
                        if enemy[0] < (row-1) and enemy[1] < (col):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row-1][col] != 0:
                                return [2]
                        elif enemy[0] > (row) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row][col+1] != 0:
                                return [5]
                        return [2, 5]
                    elif enemy[0] != (row) and enemy[1] != (col-1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col-1)):
                        if enemy[0] < (row-1) and enemy[1] > (col):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row-1][col] != 0:
                                return [2]
                        elif enemy[0] > (row) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row][col-1] != 0:
                                return [4]
                        return [2, 4]
                elif enemy[0] != (row-1) and enemy[1] != (col+1) and abs(enemy[0]-(row-1)) == abs(enemy[1]-(col+1)):
                    if enemy[0] != (row+1) and enemy[1] != (col-1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col-1)):
                        if enemy[0] < (row-1) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row-1][col+1] != 0:
                                return [3]
                        elif enemy[0] > (row+1) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-(row+1))):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row+1][col-1] != 0:
                                return [6]
                        return [3, 6]
                    else:
                        if enemy[0] < (row-1) and enemy[1] < (col+1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                        elif enemy[0] > (row-1) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                        return [3]
                elif enemy[0] != (row) and enemy[1] != (col-1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col-1)):
                    if enemy[0] != (row+1) and enemy[1] != (col) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col)):
                        if enemy[0] < (row) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row-1][col] != 0:
                                return [4]
                        elif enemy[0] > (row+1) and enemy[1] > (col):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row+1][col] != 0:
                                return [7]
                        return [4, 7]
                elif enemy[0] != (row) and enemy[1] != (col+1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col+1)):
                    if enemy[0] != (row+1) and enemy[1] != (col) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col)):
                        if enemy[0] < (row) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row][col+1] != 0:
                                return [5]
                        elif enemy[0] > (row+1) and enemy[1] < (col):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row+1][col] != 0:
                                return [7]
                        return [5, 7]
                elif enemy[0] != (row+1) and enemy[1] != (col-1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col-1)):
                    if enemy[0] < (row+1) and enemy[1] < (col-1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                return None
                    elif enemy[0] > (row+1) and enemy[1] > (col-1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                return None
                    return [6]
                elif enemy[0] != (row+1) and enemy[1] != (col+1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col+1)):
                    if enemy[0] < (row+1) and enemy[1] > (col+1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                return None
                    elif enemy[0] > (row+1) and enemy[1] < (col+1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                return None
                    return [8]
        elif self.__matrix[enemy[0]][enemy[1]] == 10:
            if enemy[0] == row-1 and enemy[1] == col-1:
                if self.__matrix[row][col-1] != 0 and self.__matrix[row-1][col] != 0:
                    return [2, 4]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 4, 6]
                elif self.__matrix[row][col-1] != 0:
                    return [2, 3, 4]
                else:
                    return [2, 3, 4, 6]
            elif enemy[0] == row-1 and enemy[1] == col:
                return [1, 3, 7]
            elif enemy[0] == row-1 and enemy[1] == col+1:
                if self.__matrix[row][col+1] != 0 and self.__matrix[row-1][col] != 0:
                    return [2, 5]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 5, 8]
                elif self.__matrix[row][col+1] != 0:
                    return [1, 2, 5]
                else:
                    return [1, 2, 5, 8]
            elif enemy[0] == row and enemy[1] == col-1:
                return [1, 5, 6]
            elif enemy[0] == row and enemy[1] == col+1:
                return [3, 4, 8]
            elif enemy[0] == row+1 and enemy[1] == col-1:
                if self.__matrix[row][col-1] != 0 and self.__matrix[row+1][col] != 0:
                    return [4, 7]
                elif self.__matrix[row+1][col] != 0:
                    return [1, 4, 7]
                elif self.__matrix[row][col-1] != 0:
                    return [4, 7, 8]
                else:
                    return [1, 4, 7, 8]
            elif enemy[0] == row+1 and enemy[1] == col:
                return [2, 6, 8]
            elif enemy[0] == row+1 and enemy[1] == col+1:
                if self.__matrix[row][col+1] != 0 and self.__matrix[row+1][col] != 0:
                    return [5, 7]
                elif self.__matrix[row+1][col] != 0:
                    return [3, 5, 7]
                elif self.__matrix[row][col+1] != 0:
                    return [5, 6, 7]
                else:
                    return [3, 5, 6, 7]
            else:
                if enemy[0] == row-1:
                    if  enemy[1] < col-1:
                        for x in range(enemy[1]+1, col-1):
                            if self.__matrix[row-1][x] != 0:
                                return None
                        if self.__matrix[row-1][col-1] != 0:
                            return [1]
                        elif self.__matrix[row-1][col] != 0:
                            return [1, 2]
                    elif enemy[1] > col+1:
                        for x in range(col+2, enemy[1]):
                            if self.__matrix[row-1][x] != 0:
                                return None
                        if self.__matrix[row-1][col+1] != 0:
                            return [3]
                        elif self.__matrix[row-1][col] != 0:
                            return [2, 3]
                    return [1, 2, 3]
                elif enemy[0] == row:
                    if  enemy[1] < col-1:
                        for x in range(enemy[1]+1, col-1):
                            if self.__matrix[row][x] != 0:
                                return None
                        if self.__matrix[row][col-1] != 0:
                            return [4]
                    elif enemy[1] > col+1:
                        for x in range(col+2, enemy[1]):
                            if self.__matrix[row][x] != 0:
                                return None
                        if self.__matrix[row][col+1] != 0:
                            return [5]
                    return [4, 5]
                elif enemy[0] == row+1:
                    if enemy[1] < col-1:
                        for x in range(enemy[1]+1, col-1):
                            if self.__matrix[row+1][x] != 0:
                                return None
                        if self.__matrix[row+1][col-1] != 0:
                            return [6]
                        elif self.__matrix[row+1][col] != 0:
                            return [6, 7]
                    elif enemy[1] > col+1:
                        for x in range(col+2, enemy[1]):
                            if self.__matrix[row+1][x] != 0:
                                return None
                        if self.__matrix[row+1][col+1] != 0:
                            return [8]
                        elif self.__matrix[row+1][col] != 0:
                            return [7, 8]
                    return [6, 7, 8]
                elif enemy[1] == col-1:
                    if enemy[0] < row-1:
                        for x in range(enemy[0]+1, row-1):
                            if self.__matrix[x][col-1] != 0:
                                return None
                        if self.__matrix[row-1][col-1] != 0:
                            return [1]
                        elif self.__matrix[row][col-1] != 0:
                            return [1, 4]
                    elif enemy[0] > row+1:
                        for x in range(row+2, enemy[0]):
                            if self.__matrix[x][col-1] != 0:
                                return None
                        if self.__matrix[row+1][col-1] != 0:
                            return [6]
                        elif self.__matrix[row][col-1] != 0:
                            return [4, 6]
                    return [1, 4, 6]
                elif enemy[1] == col:
                    if enemy[0] < row-1:
                        for x in range(enemy[0]+1, row-1):
                            if self.__matrix[x][col] != 0:
                                return None
                        if self.__matrix[row-1][col] != 0:
                            return [2]
                    elif enemy[0] > row+1:
                        for x in range(row+2, enemy[0]):
                            if self.__matrix[x][col] != 0:
                                return None
                        if self.__matrix[row+1][col] != 0:
                            return [7]
                    return [2, 7]
                elif enemy[1] == col+1:
                    if enemy[0] < row-1:
                        for x in range(enemy[0]+1, row-1):
                            if self.__matrix[x][col+1] != 0:
                                return None
                        if self.__matrix[row-1][col+1] != 0:
                            return [3]
                        elif self.__matrix[row][col+1] != 0:
                            return [3, 5]
                    elif enemy[0] > row+1:
                        for x in range(row+2, enemy[0]):
                            if self.__matrix[x][col+1] != 0:
                                return None
                        if self.__matrix[row+1][col+1] != 0:
                            return [8]
                        elif self.__matrix[row][col+1] != 0:
                            return [5, 8]
                    return [3, 5, 8]
        elif self.__matrix[enemy[0]][enemy[1]] == 11:
            if enemy[0] == row-1 and enemy[1] == col-1:
                if self.__matrix[row-1][col] != 0 and self.__matrix[row][col-1] != 0:
                    return [2, 4, 8]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 4, 6, 8]
                elif self.__matrix[row][col-1] != 0:
                    return [2, 3, 4, 8]
                else:
                    return [2, 3, 4, 6, 8]
            elif enemy[0] == row-1 and enemy[1] == col:
                return [1, 3, 4, 5, 7]
            elif enemy[0] == row-1 and enemy[1] == col+1:
                if self.__matrix[row-1][col] != 0 and self.__matrix[row][col+1] != 0:
                    return [2, 5, 6]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 5, 6, 8]
                elif self.__matrix[row][col-1] != 0:
                    return [1, 2, 5, 6]
                else:
                    return [1, 2, 5, 6, 8]
            elif enemy[0] == row and enemy[1] == col-1:
                return [1, 2, 5, 6, 7]
            elif enemy[0] == row and enemy[1] == col+1:
                return [2, 3, 4, 7, 8]
            elif enemy[0] == row+1 and enemy[1] == col-1:
                if self.__matrix[row+1][col] != 0 and self.__matrix[row][col-1] != 0:
                    return [3, 4, 7]
                elif self.__matrix[row+1][col] != 0:
                    return [1, 3, 4, 7]
                elif self.__matrix[row][col-1] != 0:
                    return [3, 4, 7, 8]
                else:
                    return [1, 3, 4, 7, 8]
            elif enemy[0] == row+1 and enemy[1] == col:
                return [2, 4, 5, 6, 8]
            elif enemy[0] == row+1 and enemy[1] == col+1:
                if self.__matrix[row+1][col] != 0 and self.__matrix[row][col+1] != 0:
                    return [1, 5, 7]
                elif self.__matrix[row+1][col] != 0:
                    return [1, 3, 5, 7]
                elif self.__matrix[row][col+1] != 0:
                    return [1, 5, 6, 7]
                else:
                    return [1, 3, 5, 6, 7]
            elif enemy[0] == row-2 and enemy[1] == col-1:
                if self.__matrix[row-1][col-1] != 0 and self.__matrix[row-1][col] != 0:
                    return [1, 2]
                elif self.__matrix[row][col-1] != 0 and self.__matrix[row-1][col] != 0:
                    return [1, 2, 4]
                elif self.__matrix[row-1][col-1] != 0:
                    return [1, 2, 5]
                elif self.__matrix[row-1][col] != 0:
                    return [1, 2, 4, 6]
                elif self.__matrix[row][col-1] != 0:
                    return [1, 2, 4, 5]
                else:
                    return [1, 2, 4, 5, 6]
            elif enemy[0] == row-2 and enemy[1] == col:
                if self.__matrix[row-1][col] != 0:
                    return [1, 2, 3]
                else:
                    return [1, 2, 3, 7]
            elif enemy[0] == row-2 and enemy[1] == col+1:
                if self.__matrix[row-1][col+1] != 0 and self.__matrix[row-1][col] != 0:
                    return [2, 3]
                elif self.__matrix[row][col+1] != 0 and self.__matrix[row-1][col] != 0:
                    return [2, 3, 5]
                elif self.__matrix[row-1][col+1] != 0:
                    return [2, 3, 4]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 3, 5, 8]
                elif self.__matrix[row][col+1] != 0:
                    return [2, 3, 4, 5]
                else:
                    return [2, 3, 4, 5, 8]
            elif enemy[0] == row-1 and enemy[1] == col-2:
                if self.__matrix[row-1][col-1] != 0 and self.__matrix[row][col-1] != 0:
                    return [1, 4]
                elif self.__matrix[row-1][col] != 0 and self.__matrix[row][col-1] != 0:
                    return [1, 2, 4]
                elif self.__matrix[row-1][col-1] != 0:
                    return [1, 4, 7]
                elif self.__matrix[row-1][col] != 0:
                    return [1, 2, 4, 7]
                elif self.__matrix[row][col-1] != 0:
                    return [1, 2, 3, 4]
                else:
                    return [1, 2, 3, 4, 7]
            elif enemy[0] == row and enemy[1] == col-2:
                if self.__matrix[row][col-1] != 0:
                    return [1, 4, 6]
                else:
                    return [1, 4, 5, 6]
            elif enemy[0] == row+1 and enemy[1] == col-2:
                if self.__matrix[row+1][col-1] != 0 and self.__matrix[row][col-1] != 0:
                    return [4, 6]
                elif self.__matrix[row+1][col] != 0 and self.__matrix[row][col-1] != 0:
                    return [4, 6, 7]
                elif self.__matrix[row+1][col-1] != 0:
                    return [2, 4, 6]
                elif self.__matrix[row+1][col] != 0:
                    return [2, 4, 6, 7]
                elif self.__matrix[row][col-1] != 0:
                    return [4, 6, 7, 8]
                else:
                    return [2, 4, 6, 7, 8]
            elif enemy[0] == row+2 and enemy[1] == col-1:
                if self.__matrix[row+1][col-1] != 0 and self.__matrix[row+1][col] != 0:
                    return [6, 7]
                elif self.__matrix[row][col-1] != 0 and self.__matrix[row+1][col] != 0:
                    return [4, 6, 7]
                elif self.__matrix[row+1][col-1] != 0:
                    return [5, 6, 7]
                elif self.__matrix[row+1][col] != 0:
                    return [1, 4, 6, 7]
                elif self.__matrix[row][col-1] != 0:
                    return [4, 5, 6, 7]
                else:
                    return [1, 4, 5, 6, 7]
            elif enemy[0] == row+2 and enemy[1] == col:
                if self.__matrix[row+1][col] != 0:
                    return [6, 7, 8]
                else:
                    return [2, 6, 7, 8]
            elif enemy[0] == row+2 and enemy[1] == col+1:
                if self.__matrix[row+1][col+1] != 0 and self.__matrix[row+1][col] != 0:
                    return [7, 8]
                elif self.__matrix[row][col+1] != 0 and self.__matrix[row+1][col] != 0:
                    return [5, 7, 8]
                elif self.__matrix[row+1][col+1] != 0:
                    return [4, 7, 8]
                elif self.__matrix[row+1][col] != 0:
                    return [3, 5, 7, 8]
                elif self.__matrix[row][col+1] != 0:
                    return [4, 5, 7, 8]
                else:
                    return [3, 4, 5, 7, 8]
            elif enemy[0] == row-1 and enemy[1] == col+2:
                if self.__matrix[row-1][col+1] != 0 and self.__matrix[row][col+1] != 0:
                    return [3, 5]
                elif self.__matrix[row-1][col] != 0 and self.__matrix[row][col+1] != 0:
                    return [2, 3, 5]
                elif self.__matrix[row-1][col+1] != 0:
                    return [3, 5, 7]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 3, 5, 7]
                elif self.__matrix[row][col+1] != 0:
                    return [1, 2, 3, 5]
                else:
                    return [1, 2, 3, 5, 7]
            elif enemy[0] == row and enemy[1] == col+2:
                if self.__matrix[row][col+1] != 0:
                    return [3, 5, 8]
                else:
                    return [3, 4, 5, 8]
            elif enemy[0] == row+1 and enemy[1] == col+2:
                if self.__matrix[row+1][col+1] != 0 and self.__matrix[row][col+1] != 0:
                    return [5, 8]
                elif self.__matrix[row+1][col] != 0 and self.__matrix[row][col+1] != 0:
                    return [5, 7, 8]
                elif self.__matrix[row+1][col+1] != 0:
                    return [2, 5, 8]
                elif self.__matrix[row+1][col] != 0:
                    return [2, 5, 7, 8]
                elif self.__matrix[row][col+1] != 0:
                    return [5, 6, 7, 8]
                else:
                    return [2, 5, 6, 7, 8]
            elif enemy[0] == row-3 and enemy[1] == col-1:
                if self.__matrix[row-2][col-1] != 0 and self.__matrix[row-2][col] != 0:
                    return None
                elif self.__matrix[row-2][col-1] != 0:
                    return [3]
                elif self.__matrix[row-2][col] != 0:
                    return [1]
                elif self.__matrix[row-1][col-1] != 0:
                    return [1, 3]
                elif self.__matrix[row][col-1] != 0:
                    return [1, 4, 3]
                else:
                    return [1, 3, 4, 6]
            elif enemy[0] == row-3 and enemy[1] == col:
                if self.__matrix[row-2][col] != 0:
                    return None
                elif self.__matrix[row-1][col] != 0:
                    return [2]
                else:
                    return [2, 7]
            elif enemy[0] == row-3 and enemy[1] == col+1:
                if self.__matrix[row-2][col+1] != 0 and self.__matrix[row-2][col] != 0:
                    return None
                elif self.__matrix[row-2][col+1] != 0:
                    return [1]
                elif self.__matrix[row-2][col] != 0:
                    return [3]
                elif self.__matrix[row-1][col+1] != 0:
                    return [1, 3]
                elif self.__matrix[row][col+1] != 0:
                    return [1, 3, 5]
                else:
                    return [1, 3, 5, 8]
            elif enemy[0] == row-1 and enemy[1] == col-3:
                if self.__matrix[row-1][col-2] != 0 and self.__matrix[row][col-2] != 0:
                    return None
                elif self.__matrix[row-1][col-2] != 0:
                    return [6]
                elif self.__matrix[row][col-2] != 0:
                    return [1]
                elif self.__matrix[row-1][col-1] != 0:
                    return [1, 6]
                elif self.__matrix[row-1][col] != 0:
                    return [1, 2, 6]
                else:
                    return [1, 2, 3, 6]
            elif enemy[0] == row and enemy[1] == col-3:
                if self.__matrix[row][col-2] != 0:
                    return None
                elif self.__matrix[row][col-1] != 0:
                    return [4]
                else:
                    return [4, 5]
            elif enemy[0] == row+1 and enemy[1] == col-3:
                if self.__matrix[row+1][col-2] != 0 and self.__matrix[row][col-2] != 0:
                    return None
                elif self.__matrix[row+1][col-2] != 0:
                    return [1]
                elif self.__matrix[row][col-2] != 0:
                    return [6]
                elif self.__matrix[row+1][col-1] != 0:
                    return [1, 6]
                elif self.__matrix[row+1][col] != 0:
                    return [1, 6, 7]
                else:
                    return [1, 3, 4, 6]
            elif enemy[0] == row+3 and enemy[1] == col-1:
                if self.__matrix[row+2][col-1] != 0 and self.__matrix[row+2][col] != 0:
                    return None
                elif self.__matrix[row+2][col-1] != 0:
                    return [8]
                elif self.__matrix[row+2][col] != 0:
                    return [6]
                elif self.__matrix[row+1][col-1] != 0:
                    return [6, 8]
                elif self.__matrix[row][col-1] != 0:
                    return [4, 6, 8]
                else:
                    return [1, 4, 6, 8]
            elif enemy[0] == row+3 and enemy[1] == col:
                if self.__matrix[row+2][col] != 0:
                    return None
                elif self.__matrix[row+1][col] != 0:
                    return [7]
                else:
                    return [2, 7]
            elif enemy[0] == row+3 and enemy[1] == col+1:
                if self.__matrix[row+2][col+1] != 0 and self.__matrix[row+2][col] != 0:
                    return None
                elif self.__matrix[row+2][col+1] != 0:
                    return [6]
                elif self.__matrix[row+2][col] != 0:
                    return [8]
                elif self.__matrix[row+1][col+1] != 0:
                    return [6, 8]
                elif self.__matrix[row][col+1] != 0:
                    return [5, 6, 8]
                else:
                    return [3, 5, 6, 8]
            elif enemy[0] == row-1 and enemy[1] == col+3:
                if self.__matrix[row-1][col+2] != 0 and self.__matrix[row][col+2] != 0:
                    return None
                elif self.__matrix[row-1][col+2] != 0:
                    return [8]
                elif self.__matrix[row+2][col] != 0:
                    return [3]
                elif self.__matrix[row-1][col+1] != 0:
                    return [3, 8]
                elif self.__matrix[row-1][col] != 0:
                    return [2, 3, 8]
                else:
                    return [1, 2, 3, 8]
            elif enemy[0] == row and enemy[1] == col+3:
                if self.__matrix[row][col+2] != 0:
                    return None
                elif self.__matrix[row][col+1] != 0:
                    return [5]
                else:
                    return [4, 5]
            elif enemy[0] == row+1 and enemy[1] == col+3:
                if self.__matrix[row+1][col+2] != 0 and self.__matrix[row][col+2] != 0:
                    return None
                elif self.__matrix[row+1][col+2] != 0:
                    return [3]
                elif self.__matrix[row+2][col] != 0:
                    return [8]
                elif self.__matrix[row+1][col+1] != 0:
                    return [3, 8]
                elif self.__matrix[row+1][col] != 0:
                    return [3, 7, 8]
                else:
                    return [3, 6, 7, 8]
            elif (((enemy[0] >= 0 and enemy[0] < row-3) or (enemy[0] > row+3 and enemy[0] < ROWLEN)) and (enemy[1] >= col-1 and enemy[1] <= col+1)) or (((enemy[1] >= 0 and enemy[1] < col-3) or (enemy[1] > col+3 and enemy[1] < COLLEN)) and (enemy[0] >= row-1 and enemy[0] <= row+1)):
                if enemy[0] == row-1:
                    if  enemy[1] < col-1:
                        for x in range(enemy[1]+1, col-1):
                            if self.__matrix[row-1][x] != 0:
                                return None
                        if self.__matrix[row-1][col-1] != 0:
                            return [1]
                        elif self.__matrix[row-1][col] != 0:
                            return [1, 2]
                    elif enemy[1] > col+1:
                        for x in range(col+2, enemy[1]):
                            if self.__matrix[row-1][x] != 0:
                                return None
                        if self.__matrix[row-1][col+1] != 0:
                            return [3]
                        elif self.__matrix[row-1][col] != 0:
                            return [2, 3]
                    return [1, 2, 3]
                elif enemy[0] == row:
                    if  enemy[1] < col-1:
                        for x in range(enemy[1]+1, col-1):
                            if self.__matrix[row][x] != 0:
                                return None
                        if self.__matrix[row][col-1] != 0:
                            return [4]
                    elif enemy[1] > col+1:
                        for x in range(col+2, enemy[1]):
                            if self.__matrix[row][x] != 0:
                                return None
                        if self.__matrix[row][col+1] != 0:
                            return [5]
                    return [4, 5]
                elif enemy[0] == row+1:
                    if enemy[1] < col-1:
                        for x in range(enemy[1]+1, col-1):
                            if self.__matrix[row+1][x] != 0:
                                return None
                        if self.__matrix[row+1][col-1] != 0:
                            return [6]
                        elif self.__matrix[row+1][col] != 0:
                            return [6, 7]
                    elif enemy[1] > col+1:
                        for x in range(col+2, enemy[1]):
                            if self.__matrix[row+1][x] != 0:
                                return None
                        if self.__matrix[row+1][col+1] != 0:
                            return [8]
                        elif self.__matrix[row+1][col] != 0:
                            return [7, 8]
                    return [6, 7, 8]
                elif enemy[1] == col-1:
                    if enemy[0] < row-1:
                        for x in range(enemy[0]+1, row-1):
                            if self.__matrix[x][col-1] != 0:
                                return None
                        if self.__matrix[row-1][col-1] != 0:
                            return [1]
                        elif self.__matrix[row][col-1] != 0:
                            return [1, 4]
                    elif enemy[0] > row+1:
                        for x in range(row+2, enemy[0]):
                            if self.__matrix[x][col-1] != 0:
                                return None
                        if self.__matrix[row+1][col-1] != 0:
                            return [6]
                        elif self.__matrix[row][col-1] != 0:
                            return [4, 6]
                    return [1, 4, 6]
                elif enemy[1] == col:
                    if enemy[0] < row-1:
                        for x in range(enemy[0]+1, row-1):
                            if self.__matrix[x][col] != 0:
                                return None
                        if self.__matrix[row-1][col] != 0:
                            return [2]
                    elif enemy[0] > row+1:
                        for x in range(row+2, enemy[0]):
                            if self.__matrix[x][col] != 0:
                                return None
                        if self.__matrix[row+1][col] != 0:
                            return [7]
                    return [2, 7]
                elif enemy[1] == col+1:
                    if enemy[0] < row-1:
                        for x in range(enemy[0]+1, row-1):
                            if self.__matrix[x][col+1] != 0:
                                return None
                        if self.__matrix[row-1][col+1] != 0:
                            return [3]
                        elif self.__matrix[row][col+1] != 0:
                            return [3, 5]
                    elif enemy[0] > row+1:
                        for x in range(row+2, enemy[0]):
                            if self.__matrix[x][col+1] != 0:
                                return None
                        if self.__matrix[row+1][col+1] != 0:
                            return [8]
                        elif self.__matrix[row][col+1] != 0:
                            return [5, 8]
                    return [3, 5, 8]
            else:
                if enemy[0] != (row-1) and enemy[1] != (col-1) and abs(enemy[0]-(row-1)) == abs(enemy[1]-(col-1)):
                    if enemy[0] != (row+1) and enemy[1] != (col+1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col+1)):
                        if enemy[0] < (row-1) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row-1][col-1] != 0:
                                return [1]
                        elif enemy[0] > (row+1) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-(row+1))):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row+1][col+1] != 0:
                                return [8]
                        return [1, 8]
                    else:
                        if enemy[0] < (row-1) and enemy[1] > (col-1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                        elif enemy[0] > (row-1) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                        return [1]
                elif enemy[0] != (row-1) and enemy[1] != (col) and abs(enemy[0]-(row-1)) == abs(enemy[1]-(col)):
                    if enemy[0] != (row) and enemy[1] != (col+1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col+1)):
                        if enemy[0] < (row-1) and enemy[1] < (col):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row-1][col] != 0:
                                return [2]
                        elif enemy[0] > (row) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row][col+1] != 0:
                                return [5]
                        return [2, 5]
                    elif enemy[0] != (row) and enemy[1] != (col-1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col-1)):
                        if enemy[0] < (row-1) and enemy[1] > (col):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row-1][col] != 0:
                                return [2]
                        elif enemy[0] > (row) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row][col-1] != 0:
                                return [4]
                        return [2, 4]
                elif enemy[0] != (row-1) and enemy[1] != (col+1) and abs(enemy[0]-(row-1)) == abs(enemy[1]-(col+1)):
                    if enemy[0] != (row+1) and enemy[1] != (col-1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col-1)):
                        if enemy[0] < (row-1) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row-1][col+1] != 0:
                                return [3]
                        elif enemy[0] > (row+1) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-(row+1))):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row+1][col-1] != 0:
                                return [6]
                        return [3, 6]
                    else:
                        if enemy[0] < (row-1) and enemy[1] < (col+1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                        elif enemy[0] > (row-1) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-(row-1))):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                        return [3]
                elif enemy[0] != (row) and enemy[1] != (col-1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col-1)):
                    if enemy[0] != (row+1) and enemy[1] != (col) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col)):
                        if enemy[0] < (row) and enemy[1] < (col-1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row-1][col] != 0:
                                return [4]
                        elif enemy[0] > (row+1) and enemy[1] > (col):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row+1][col] != 0:
                                return [7]
                        return [4, 7]
                elif enemy[0] != (row) and enemy[1] != (col+1) and abs(enemy[0]-(row)) == abs(enemy[1]-(col+1)):
                    if enemy[0] != (row+1) and enemy[1] != (col) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col)):
                        if enemy[0] < (row) and enemy[1] > (col+1):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                    return None
                            if self.__matrix[row][col+1] != 0:
                                return [5]
                        elif enemy[0] > (row+1) and enemy[1] < (col):
                            for x in range(1, abs(enemy[0]-row)):
                                if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                    return None
                            if self.__matrix[row+1][col] != 0:
                                return [7]
                        return [5, 7]
                elif enemy[0] != (row+1) and enemy[1] != (col-1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col-1)):
                    if enemy[0] < (row+1) and enemy[1] < (col-1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]+x][enemy[1]+x] != 0:
                                return None
                    elif enemy[0] > (row+1) and enemy[1] > (col-1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]-x][enemy[1]-x] != 0:
                                return None
                    return [6]
                elif enemy[0] != (row+1) and enemy[1] != (col+1) and abs(enemy[0]-(row+1)) == abs(enemy[1]-(col+1)):
                    if enemy[0] < (row+1) and enemy[1] > (col+1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]+x][enemy[1]-x] != 0:
                                return None
                    elif enemy[0] > (row+1) and enemy[1] < (col+1):
                        for x in range(1, abs(enemy[0]-(row+1))):
                            if self.__matrix[enemy[0]-x][enemy[1]+x] != 0:
                                return None
                    return [8]
        elif self.__matrix[enemy[0]][enemy[1]] == 12:
            if enemy[0] == row-2 and enemy[1] == col-2:
                return [1]
            elif enemy[0] == row-2 and enemy[1] == col-1:
                return [1, 2]
            elif enemy[0] == row-2 and enemy[1] == col:
                return [1, 2, 3]
            elif enemy[0] == row-2 and enemy[1] == col+1:
                return [2, 3]
            elif enemy[0] == row-2 and enemy[1] == col+2:
                return [3]
            elif enemy[0] == row-1 and enemy[1] == col-2:
                return [1, 4]
            elif enemy[0] == row-1 and enemy[1] == col-1:
                return [2, 4]
            elif enemy[0] == row-1 and enemy[1] == col:
                return [1, 3, 4, 5]
            elif enemy[0] == row-1 and enemy[1] == col+1:
                return [2, 5]
            elif enemy[0] == row-1 and enemy[1] == col+2:
                return [3, 5]
            elif enemy[0] == row and enemy[1] == col-2:
                return [1, 4, 6]
            elif enemy[0] == row and enemy[1] == col-1:
                return [1, 2, 6, 7]
            elif enemy[0] == row and enemy[1] == col+1:
                return [2, 3, 7, 8]
            elif enemy[0] == row and enemy[1] == col+2:
                return [3, 5, 8]
            elif enemy[0] == row+1 and enemy[1] == col-2:
                return [4, 6]
            elif enemy[0] == row+1 and enemy[1] == col-1:
                return [4, 7]
            elif enemy[0] == row+1 and enemy[1] == col:
                return [4, 5, 6, 8]
            elif enemy[0] == row+1 and enemy[1] == col+1:
                return [5, 7]
            elif enemy[0] == row+1 and enemy[1] == col+2:
                return [5, 8]
            elif enemy[0] == row+2 and enemy[1] == col-2:
                return [6]
            elif enemy[0] == row+2 and enemy[1] == col-1:
                return [6, 7]
            elif enemy[0] == row+2 and enemy[1] == col:
                return [6, 7, 8]
            elif enemy[0] == row+2 and enemy[1] == col+1:
                return [7, 8]
            elif enemy[0] == row+2 and enemy[1] == col+2:
                return [8]
    
    
    # gives the result as iterable when the class is been created as an object
    def __iter__(self):
        row, col = self.__pos
        if self.__matrix[row][col] == 1:
            return iter(self._pawn(row, col))
        elif self.__matrix[row][col] == 2:
            return iter(self._knight(row, col))
        elif self.__matrix[row][col] == 3:
            return iter(self._bishop(row, col))
        elif self.__matrix[row][col] == 4:
            return iter(self._rook(row, col))
        elif self.__matrix[row][col] == 5:
            return iter(self._queen(row, col))
        elif self.__matrix[row][col] == 6:
            return iter(self._king(row, col))

    # chessmen moves
    def _pawn(self, row, col):
        list1 = []
        if row < ROWLEN - 1:
            if row == 1:
                if (self.__matrix[row + 1][col] == 0 and self.__matrix[row + 2][col] == 0):
                    list1 = [[self.__matrix[row][col], _oneInteger(row, col, row+1, col), self.__matrix[row + 1][col]],
                             [self.__matrix[row][col], _oneInteger(row, col, row+2, col), self.__matrix[row + 2][col]]]
                elif (self.__matrix[row + 1][col] == 0 and self.__matrix[row + 2][col] != 0):
                    list1 = [[self.__matrix[row][col], _oneInteger(row, col, row+1, col), self.__matrix[row + 1][col]]]
            else:
                if (self.__matrix[row + 1][col] == 0):
                    list1 = [[self.__matrix[row][col], _oneInteger(row, col, row+1, col), self.__matrix[row + 1][col]]]
            if col - 1 >= 0:
                if (self.__matrix[row + 1][col - 1] != 0 and self.__matrix[row + 1][col - 1] > 6):
                    list1 = list1+[[self.__matrix[row][col], _oneInteger(row, col, row+1, col-1), self.__matrix[row + 1][col - 1]]]
            if col + 1 < COLLEN:
                if (self.__matrix[row + 1][col + 1] != 0 and self.__matrix[row + 1][col + 1] > 6):
                    list1 = list1+[[self.__matrix[row][col], _oneInteger(row, col, row+1, col+1), self.__matrix[row + 1][col + 1]]]
        return list1
    
    def _knight(self, row, col):
        list1 = []
        if row+1 >= 0 and row+1 < ROWLEN and col+2 >= 0 and col+2 < COLLEN and (self.__matrix[row+1][col+2] > 6 or self.__matrix[row+1][col+2] == 0):
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+1, col+2), self.__matrix[row+1][col+2]])
        if row+2 >= 0 and row+2 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (self.__matrix[row+2][col+1] > 6 or self.__matrix[row+2][col+1] == 0):
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+2, col+1), self.__matrix[row+2][col+1]])
        if row+2 >= 0 and row+2 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (self.__matrix[row+2][col-1] > 6 or self.__matrix[row+2][col-1] == 0):
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+2, col-1), self.__matrix[row+2][col-1]])
        if row+1 >= 0 and row+1 < ROWLEN and col-2 >= 0 and col-2 < COLLEN and (self.__matrix[row+1][col-2] > 6 or self.__matrix[row+1][col-2] == 0):
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+1, col-2), self.__matrix[row+1][col-2]])
        if row-1 >= 0 and row-1 < ROWLEN and col-2 >= 0 and col-2 < COLLEN and (self.__matrix[row-1][col-2] > 6 or self.__matrix[row-1][col-2] == 0):
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-1, col-2), self.__matrix[row-1][col-2]])
        if row-2 >= 0 and row-2 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (self.__matrix[row-2][col-1] > 6 or self.__matrix[row-2][col-1] == 0):
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-2, col-1), self.__matrix[row-2][col-1]])
        if row-2 >= 0 and row-2 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (self.__matrix[row-2][col+1] > 6 or self.__matrix[row-2][col+1] == 0):
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-2, col+1), self.__matrix[row-2][col+1]])
        if row-1 >= 0 and row-1 < ROWLEN and col+2 >= 0 and col+2 < COLLEN and (self.__matrix[row-1][col+2] > 6 or self.__matrix[row-1][col+2] == 0):
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-1, col+2), self.__matrix[row-1][col+2]])
        return list1
    
    def _bishop(self, row, col):
        q = mp.Queue()
        # for multiprocessing
        rt = mp.Process(target=_worker, args=((self._rightTop, (row, col), q)))
        lt = mp.Process(target=_worker, args=((self._leftTop, (row, col), q)))
        rb = mp.Process(target=_worker, args=((self._rightBottom, (row, col), q)))
        lb = mp.Process(target=_worker, args=((self._leftBottom, (row, col), q)))
        list1 = []
        if col == 0:
            if row == 0:
                # right-bottom[row + i][col + i]
                list1 = self._rightBottom(row, col)
            elif row == ROWLEN - 1:
                # right-top[row - i][col + i]
                list1 = self._rightTop(row, col)
            else:
                # right-top[row - i][col + i]
                # right-bottom[row + i][col + i]
                processes = [rt, rb]
                
                for p in processes:
                    p.start()
                
                for p in processes:
                    p.join()
                
                for _ in processes:
                    list1.extend(q.get())
        elif col == COLLEN - 1:
            if row == 0:
                # left-bottom[row + i][col - i]
                list1 = self._leftBottom(row, col)
            elif row == ROWLEN - 1:
                # left-top[row - i][col - i]
                list1 = self._leftTop(row, col)
            else:
                # left-top[row - i][col - i]
                # left-bottom[row + i][col - i]
                processes = [lt, lb]
                
                for p in processes:
                    p.start()
                
                for p in processes:
                    p.join()
                
                for _ in processes:
                    list1.extend(q.get())
        else:
            if row == 0:
                # right-bottom[row + i][col + i]
                # left-bottom[row + i][col - i]
                processes = [rb, lb]
                
                for p in processes:
                    p.start()
                
                for p in processes:
                    p.join()
                
                for _ in processes:
                    list1.extend(q.get())
            elif row == ROWLEN - 1:
                # right-top[row - i][col + i]
                # left-top[row - i][col - i]
                processes = [rt, lt]
                
                for p in processes:
                    p.start()
                
                for p in processes:
                    p.join()
                
                for _ in processes:
                    list1.extend(q.get())
            else:
                # right-top[row - i][col + i]
                # right-bottom[row + i][col + i]
                # left-bottom[row + i][col - i]
                # left-top[row - i][col - i]
                processes = [rt, rb, lt, lb]
                
                for p in processes:
                    p.start()
                
                for p in processes:
                    p.join()
                
                for _ in processes:
                    list1.extend(q.get())
        return list1
    
    def _rook(self, row, col):
        q = mp.Queue()
        # for multiprocessing
        t = mp.Process(target=_worker, args=((self._top, (row, col), q)))
        r = mp.Process(target=_worker, args=((self._right, (row, col), q)))
        b = mp.Process(target=_worker, args=((self._bottom, (row, col), q)))
        l = mp.Process(target=_worker, args=((self._left, (row, col), q)))
        
        list1 = []

        # top[row - 1][col]
        # right[row][col + 1]
        # bottom[row + 1][col]
        # left[row][col - 1]
        processes = [t, r, b, l]
                
        for p in processes:
            p.start()
                
        for p in processes:
            p.join()
                
        for _ in processes:
            list1.extend(q.get())
        
        return list1
        
    def _queen(self, row, col):
        q = mp.Queue()
        # for multiprocessing
        bishop = mp.Process(target=_worker, args=((self._bishop, (row, col), q)))
        rook = mp.Process(target=_worker, args=((self._rook, (row, col), q)))
        
        list1 = []
        
        processes = [bishop, rook]
        
        for p in processes:
            p.start()
            
        for p in processes:
            p.join()
        
        for _ in processes:
            list1.extend(q.get())
        
        return list1

    def _king(self, row, col):
        list1 = []
        with mp.Pool(int(mp.cpu_count()/2)) as p:
            s = set([result for x in p.map(self._filterEnemy, [(e[0], row, col) for e in self.__player]) if x for result in x])
        index = [i + 1 not in s for i in range(8)]
        # [row-1][col-1]=1, [row-1][col]=2, [row-1][col+1]=3, [row][col-1]=4, [row][col+1]=5, [row+1][col-1]=6, [row+1][col]=7, [row+1][col+1]=8
        if row-1 >= 0 and row-1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (self.__matrix[row-1][col-1] > 6 or self.__matrix[row-1][col-1] == 0) and index[0]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-1, col-1), self.__matrix[row-1][col-1]])
        if row-1 >= 0 and row-1 < ROWLEN and col >= 0 and col < COLLEN and (self.__matrix[row-1][col] > 6 or self.__matrix[row-1][col] == 0) and index[1]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-1, col), self.__matrix[row-1][col]])
        if row-1 >= 0 and row-1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (self.__matrix[row-1][col+1] > 6 or self.__matrix[row-1][col+1] == 0) and index[2]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row-1, col+1), self.__matrix[row-1][col+1]])
        if row >= 0 and row < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (self.__matrix[row][col-1] > 6 or self.__matrix[row][col-1] == 0) and index[3]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row, col-1), self.__matrix[row][col-1]])
        if row >= 0 and row < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (self.__matrix[row][col+1] > 6 or self.__matrix[row][col+1] == 0) and index[4]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row, col+1), self.__matrix[row][col+1]])
        if row+1 >= 0 and row+1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (self.__matrix[row+1][col-1] > 6 or self.__matrix[row+1][col-1] == 0) and index[5]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+1, col-1), self.__matrix[row+1][col-1]])
        if row+1 >= 0 and row+1 < ROWLEN and col >= 0 and col < COLLEN and (self.__matrix[row+1][col] > 6 or self.__matrix[row+1][col] == 0) and index[6]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+1, col), self.__matrix[row+1][col]])
        if row+1 >= 0 and row+1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (self.__matrix[row+1][col+1] > 6 or self.__matrix[row+1][col+1] == 0) and index[7]:
            list1.append([self.__matrix[row][col], _oneInteger(row, col, row+1, col+1), self.__matrix[row+1][col+1]])
        return list1

# check that the chessman can move or not
def canMove(matrix, pos):
    row, col = pos
    if matrix[row][col] == 1:
        if row+1 >= 0 and row+1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (matrix[row+1][col-1] > 6):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (matrix[row+1][col+1] > 6):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col >= 0 and col < COLLEN and (matrix[row+1][col] == 0):
            return True
        else:
            return False
    elif matrix[row][col] == 2:
        if row-2 >= 0 and row-2 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and ((matrix[row-2][col+1] > 6) or (matrix[row-2][col+1] == 0)):
            return True
        elif row-1 >= 0 and row-1 < ROWLEN and col+2 >= 0 and col+2 < COLLEN and ((matrix[row-1][col+2] > 6) or (matrix[row-1][col+2] == 0)):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col+2 >= 0 and col+2 < COLLEN and ((matrix[row+1][col+2] > 6) or (matrix[row+1][col+2] == 0)):
            return True
        elif row+2 >= 0 and row+2 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and ((matrix[row+2][col+1] > 6) or (matrix[row+2][col+1] == 0)):
            return True
        elif row+2 >= 0 and row+2 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and ((matrix[row+2][col-1] > 6) or (matrix[row+2][col-1] == 0)):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col-2 >= 0 and col-2 < COLLEN and ((matrix[row+1][col-2] > 6) or (matrix[row+1][col-2] == 0)):
            return True
        elif row-1 >= 0 and row-1 < ROWLEN and col-2 >= 0 and col-2 < COLLEN and ((matrix[row-1][col-2] > 6) or (matrix[row-1][col-2] == 0)):
            return True
        elif row-2 >= 0 and row-2 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and ((matrix[row-2][col-1] > 6) or (matrix[row-2][col-1] == 0)):
            return True
        else:
            return False
    elif matrix[row][col] == 3:
        if row-1 >= 0 and row-1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and ((matrix[row-1][col+1] > 6) or (matrix[row-1][col+1] == 0)):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and ((matrix[row+1][col+1] > 6) or (matrix[row+1][col+1] == 0)):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and ((matrix[row+1][col-1] > 6) or (matrix[row+1][col-1] == 0)):
            return True
        elif row-1 >= 0 and row-1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and ((matrix[row-1][col-1] > 6) or (matrix[row-1][col-1] == 0)):
            return True
        else:
            return False
    elif matrix[row][col] == 4:
        if row-1 >= 0 and row-1 < ROWLEN and col >= 0 and col < COLLEN and ((matrix[row-1][col] > 6) or (matrix[row-1][col] == 0)):
            return True
        elif row >= 0 and row < ROWLEN and col+1 >= 0 and col+1 < COLLEN and ((matrix[row][col+1] > 6) or (matrix[row][col+1] == 0)):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col >= 0 and col < COLLEN and ((matrix[row+1][col] > 6) or (matrix[row+1][col] == 0)):
            return True
        elif row >= 0 and row < ROWLEN and col-1 >= 0 and col-1 < COLLEN and ((matrix[row][col-1] > 6) or (matrix[row][col-1] == 0)):
            return True
        else:
            return False
    elif (matrix[row][col] == 5) or (matrix[row][col] == 6):
        if row-1 >= 0 and row-1 < ROWLEN and col >= 0 and col < COLLEN and ((matrix[row-1][col] > 6) or (matrix[row-1][col] == 0)):
            return True
        elif row-1 >= 0 and row-1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and ((matrix[row-1][col+1] > 6) or (matrix[row-1][col+1] == 0)):
            return True
        elif row >= 0 and row < ROWLEN and col+1 >= 0 and col+1 < COLLEN and ((matrix[row][col+1] > 6) or (matrix[row][col+1] == 0)):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and ((matrix[row+1][col+1] > 6) or (matrix[row+1][col+1] == 0)):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col >= 0 and col < COLLEN and ((matrix[row+1][col] > 6) or (matrix[row+1][col] == 0)):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and ((matrix[row+1][col-1] > 6) or (matrix[row+1][col-1] == 0)):
            return True
        elif row >= 0 and row < ROWLEN and col-1 >= 0 and col-1 < COLLEN and ((matrix[row][col-1] > 6) or (matrix[row][col-1] == 0)):
            return True
        elif row-1 >= 0 and row-1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and ((matrix[row-1][col-1] > 6) or (matrix[row-1][col-1] == 0)):
            return True
        else:
            return False
    elif matrix[row][col] == 7:
        if row-1 >= 0 and row-1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and ((matrix[row-1][col-1] <= 6) and (matrix[row-1][col-1] != 0)):
            return True
        elif row-1 >= 0 and row-1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and ((matrix[row-1][col-1] <= 6) and (matrix[row-1][col-1] != 0)):
            return True
        elif row-1 >= 0 and row-1 < ROWLEN and col >= 0 and col < COLLEN and (matrix[row-1][col] == 0):
            return True
        else:
            return False
    elif matrix[row][col] == 8:
        if row-2 >= 0 and row-2 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (matrix[row-2][col+1] <= 6):
            return True
        elif row-1 >= 0 and row-1 < ROWLEN and col+2 >= 0 and col+2 < COLLEN and (matrix[row-1][col+2] <= 6):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col+2 >= 0 and col+2 < COLLEN and (matrix[row+1][col+2] <= 6):
            return True
        elif row+2 >= 0 and row+2 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (matrix[row+2][col+1] <= 6):
            return True
        elif row+2 >= 0 and row+2 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (matrix[row+2][col-1] <= 6):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col-2 >= 0 and col-2 < COLLEN and (matrix[row+1][col-2] <= 6):
            return True
        elif row-1 >= 0 and row-1 < ROWLEN and col-2 >= 0 and col-2 < COLLEN and (matrix[row-1][col-2] <= 6):
            return True
        elif row-2 >= 0 and row-2 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (matrix[row-2][col-1] <= 6):
            return True
        else:
            return False
    elif matrix[row][col] == 9:
        if row-1 >= 0 and row-1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (matrix[row-1][col+1] <= 6):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (matrix[row+1][col+1] <= 6):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (matrix[row+1][col-1] <= 6):
            return True
        elif row-1 >= 0 and row-1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (matrix[row-1][col-1] <= 6):
            return True
        else:
            return False
    elif matrix[row][col] == 10:
        if row-1 >= 0 and row-1 < ROWLEN and col >= 0 and col < COLLEN and (matrix[row-1][col] <= 6):
            return True
        elif row >= 0 and row < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (matrix[row][col+1] <= 6):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col >= 0 and col < COLLEN and (matrix[row+1][col] <= 6):
            return True
        elif row >= 0 and row < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (matrix[row][col-1] <= 6):
            return True
        else:
            return False
    elif (matrix[row][col] == 11) or (matrix[row][col] == 12):
        if row-1 >= 0 and row-1 < ROWLEN and col >= 0 and col < COLLEN and (matrix[row-1][col] <= 6):
            return True
        elif row-1 >= 0 and row-1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (matrix[row-1][col+1] <= 6):
            return True
        elif row >= 0 and row < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (matrix[row][col+1] <= 6):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col+1 >= 0 and col+1 < COLLEN and (matrix[row+1][col+1] <= 6):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col >= 0 and col < COLLEN and (matrix[row+1][col] <= 6):
            return True
        elif row+1 >= 0 and row+1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (matrix[row+1][col-1] <= 6):
            return True
        elif row >= 0 and row < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (matrix[row][col-1] <= 6):
            return True
        elif row-1 >= 0 and row-1 < ROWLEN and col-1 >= 0 and col-1 < COLLEN and (matrix[row-1][col-1] <= 6):
            return True
        else:
            return False
    return False


# if __name__ == "__main__":
    # print(_oneInteger(2, 3, 4, 5))
    # print(canMove([
    #     [4, 2, 3, 5, 6],
    #     [1, 1, 1, 1, 1],
    #     [0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0],
    #     [7, 7, 7, 7, 7],
    #     [10, 8, 9, 11, 12]
    # ], [1, 0], [[]]))

    # board = PlayerChessman([
    #     [3, 5, 6],
    #     [1, 1, 1],
    #     [0, 0, 0],
    #     [0, 0, 0],
    #     [7, 7, 7],
    #     [9, 11, 12]
    # ], [4, 2], [[]])
    # print(list(board))
    
    # print(get_the_postion(7459))
    # print(get_the_postion(7234))
    # print(get_the_postion(4084))

    
    # board = PlayerChessman([
    #     [3, 0, 0, 4, 2, 12],
    #     [0, 0, 0, 5, 0, 0],
    #     [5, 0, 0, 0, 0, 4],
    #     [0, 0, 0, 12, 0, 3],
    #     [3, 0, 5, 0, 1, 0],
    #     [5, 5, 0, 3, 0, 3]
    # ], [0, 5],
    # [[[1, 3], 5]])
    # print(list(board))
    # print("[",
    #     [0, 1, 0, 0, 0, 0],"\n",
    #     [1, 4, 0, 1, 0, 0],"\n",
    #     [4, 6, 6, 0, 0, 4],"\n",
    #     [0, 0, 0, 12, 0, 0],"\n",
    #     [0, 0, 0, 6, 0, 0],"\n",
    #     [6, 0, 6, 0, 4, 0],"\n",
    # "]")
    # print(3,3)
