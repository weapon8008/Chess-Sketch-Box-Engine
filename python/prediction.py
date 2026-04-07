import sys
import json
import copy
from pathlib import Path
from chessman import PlayerChessman, BotChessman, canMove

# go to the config.json
config_path = Path(__file__).resolve().parents[1] / "chess.config.json"

# read the row-length and column-length from config.json
with open(config_path, "r", encoding="utf-8") as file:
    data = json.load(file)
    matrix = data.get("matrix", [])
    n = data.get("row", 0) if data.get("row", 0)>=data.get("col", 0) else data.get("col", 0)
    PLAYER = data.get("player", 0)
    BOT = data.get("bot", 0)
    normal = 7*len(PLAYER) if len(PLAYER) >= len(BOT) else 7*len(PLAYER)

decision_tree = []
move_count = []

def _get_the_postion(target_index):
    # [old_row, old_col, new_row, new_col]
    return [target_index%n, int(target_index/n)%n, int(target_index/(n*n))%n, int(target_index/(n*n*n))]

class Prediction:
    __step = 0
    def __init__(self, first_move, second_move):
        # True if first move is BOT or not
        self.__bot_boolen = True if first_move[0][1] <= 6 else False
        self.__player_dict = None
        self.__bot_dict = None
        if first_move[0][1] <= 6:
            self.__bot_dict = {tuple(pos): value for pos, value in first_move}
            self.__player_dict = {tuple(pos): value for pos, value in second_move}
        else:
            self.__bot_dict = {tuple(pos): value for pos, value in second_move}
            self.__player_dict = {tuple(pos): value for pos, value in first_move}
        self.__startPrediction()
    
    def __change_to_list(self, list):
        return [[[row, col], value] for (row, col), value in list.items()]
    
    # updates the points of the moves
    def __points(self, old, new):
        if old == 0 and new == 0:
            return 0
        elif old == 0 and (new > 0 and new <= 6):
            return normal - new
        elif old == 0 and (new >= 7 and new <= 12):
            return normal + (new - 6)
        elif old != 0 and new <= 6:
            return old - new
        elif old != 0 and new >= 7:
            return old + (new - 6)
        
    # update the matrix of the chessboard in the forwarding manner as attacks, temp-matrix, temp_bot, temp_player
    def __update_matrix_in_forward(self, current_move_list, next_move_list, start, temp_matrix, temp_bot, temp_player, chessmen_attack):
        temp_matrix = copy.deepcopy(temp_matrix)
        temp_bot = copy.deepcopy(temp_bot)
        temp_player = copy.deepcopy(temp_player)
        chessmen_attack = copy.deepcopy(chessmen_attack)
        temp_start = start
        next_matrix = copy.deepcopy(temp_matrix)
        next_bot = copy.deepcopy(temp_bot)
        next_player = copy.deepcopy(temp_player)
        # update the backward, this for next_move_list
        if temp_start > 0 and next_move_list != None and (current_move_list[temp_start-1] != next_move_list[temp_start-1] or (temp_start > 1 and current_move_list[temp_start-1] == next_move_list[temp_start-1] and current_move_list[temp_start-2] != next_move_list[temp_start-2])):
            for i in range(temp_start-1, -1, -1):
                next_matrix[current_move_list[i]%n][int(current_move_list[i]/n)%n] = next_matrix[int(current_move_list[i]/(n*n))%n][int(current_move_list[i]/(n*n*n))]
                next_matrix[int(current_move_list[i]/(n*n))%n][int(current_move_list[i]/(n*n*n))] = chessmen_attack.pop()
                if next_matrix[current_move_list[i]%n][int(current_move_list[i]/n)%n] <= 6:
                    next_bot[(current_move_list[i]%n, int(current_move_list[i]/n)%n)] = next_bot.pop((int(current_move_list[i]/(n*n))%n, int(current_move_list[i]/(n*n*n))))
                    if next_matrix[int(current_move_list[i]/(n*n))%n][int(current_move_list[i]/(n*n*n))] != 0:
                        next_player[(int(current_move_list[i]/(n*n))%n, int(current_move_list[i]/(n*n*n)))] = next_matrix[int(current_move_list[i]/(n*n))%n][int(current_move_list[i]/(n*n*n))]
                elif next_matrix[current_move_list[i]%n][int(current_move_list[i]/n)%n] >= 7:
                    next_player[(current_move_list[i]%n, int(current_move_list[i]/n)%n)] = next_player.pop((int(current_move_list[i]/(n*n))%n, int(current_move_list[i]/(n*n*n))))
                    if next_matrix[int(current_move_list[i]/(n*n))%n][int(current_move_list[i]/(n*n*n))] != 0:
                        next_bot[(int(current_move_list[i]/(n*n))%n, int(current_move_list[i]/(n*n*n)))] = next_matrix[int(current_move_list[i]/(n*n))%n][int(current_move_list[i]/(n*n*n))]
                temp_start = i
                if i > 0 and current_move_list[i-1] == next_move_list[i-1]:
                    break
        # this is for the current_move_list
        for i in range(start, len(current_move_list)):
            attack = temp_matrix[int(current_move_list[i]/(n*n))%n][int(current_move_list[i]/(n*n*n))]
            # update the dict of temp_bot and temp_player
            if temp_matrix[current_move_list[i]%n][int(current_move_list[i]/n)%n] <= 6:
                temp_bot[(int(current_move_list[i]/(n*n))%n, int(current_move_list[i]/(n*n*n)))] = temp_bot.pop((current_move_list[i]%n, int(current_move_list[i]/n)%n))
                if temp_matrix[int(current_move_list[i]/(n*n))%n][int(current_move_list[i]/(n*n*n))] != 0:
                    temp_player.pop((int(current_move_list[i]/(n*n))%n, int(current_move_list[i]/(n*n*n))))
            elif temp_matrix[current_move_list[i]%n][int(current_move_list[i]/n)%n] >= 7:
                temp_player[(int(current_move_list[i]/(n*n))%n, int(current_move_list[i]/(n*n*n)))] = temp_player.pop((current_move_list[i]%n, int(current_move_list[i]/n)%n))
                if temp_matrix[int(current_move_list[i]/(n*n))%n][int(current_move_list[i]/(n*n*n))] != 0:
                    temp_bot.pop((int(current_move_list[i]/(n*n))%n, int(current_move_list[i]/(n*n*n))))
            # update the board temp_matrix
            temp_matrix[int(current_move_list[i]/(n*n))%n][int(current_move_list[i]/(n*n*n))] = temp_matrix[current_move_list[i]%n][int(current_move_list[i]/n)%n]
            temp_matrix[current_move_list[i]%n][int(current_move_list[i]/n)%n] = 0
            # check the next move indexes
            if next_move_list != None and current_move_list[i] == next_move_list[i]:
                # update the chessman attacks
                chessmen_attack.append(attack)
                temp_start = i+1
                next_matrix = copy.deepcopy(temp_matrix)
                next_bot = copy.deepcopy(temp_bot)
                next_player = copy.deepcopy(temp_player)
        if next_move_list != None:
            return temp_matrix, temp_bot, temp_player, next_matrix, next_bot, next_player, chessmen_attack, temp_start
        else:
            return temp_matrix, temp_bot, temp_player
        
    # update the next steps moves of each matrix one by one with points
    def __update_moves(self, old_list, new_move):
        if old_list[0] == 0 and new_move[2] == 0:
            return [0, old_list[1] + [new_move[1]]]
        elif old_list[0] == 0 and (new_move[2] > 0 and new_move[2] <= 6):
            return [normal - new_move[2], old_list[1] + [new_move[1]]]
        elif old_list[0] == 0 and (new_move[2] >= 7 and new_move[2] <= 12):
            return [normal + (new_move[2] - 6), old_list[1] + [new_move[1]]]
        elif old_list[0] != 0 and new_move[2] <= 6:
            return [old_list[0] - new_move[2], old_list[1] + [new_move[1]]]
        elif old_list[0] != 0 and new_move[2] >= 7:
            return [old_list[0] + (new_move[2] - 6), old_list[1] + [new_move[1]]]
    
    # start the prediction of the board
    def __startPrediction(self):
        global decision_tree
        global move_count
        while self.__step < 4:
            if self.__step == 0:
                decision_tree = self.__prediction_first_move()
                self.__step+=1
            elif self.__step % 2 == 1:
                decision_tree = self.__predict_next_move(not self.__bot_boolen)
                self.__step+=1
            elif self.__step % 2 == 0:
                decision_tree = self.__predict_next_move(self.__bot_boolen)
                self.__step+=1
            print(decision_tree)
            print()

    
    # predict the first move of the chess board game
    def __prediction_first_move(self):
        player = self.__change_to_list(self.__bot_dict if self.__bot_boolen else self.__player_dict)
        opponent = self.__change_to_list(self.__player_dict if self.__bot_boolen else self.__bot_dict)
        list1 = []
        for i in player:
            row, col = i[0]
            if canMove(matrix, [row, col]):
                if self.__bot_boolen:
                    list1.extend(list(map(lambda x: [self.__points(0, x[2]), [x[1]]], BotChessman(matrix, [row, col], opponent))))
                else:
                    list1.extend(list(map(lambda x: [self.__points(0, x[2]), [x[1]]], PlayerChessman(matrix, [row, col], opponent))))
        return list1
    
    # predict hte next moves of the chessboard in a recursive manner
    def __predict_next_move(self, bot_bool):
        global decision_tree
        global move_count
        start = 0
        list1 = []
        update_matrix = matrix
        update_bot = self.__bot_dict
        update_player = self.__player_dict
        update_attacks = []
        for index in range(len(decision_tree)):
            temp_list = []
            if index != len(decision_tree)-1:
                temp_matrix, temp_bot, temp_player, next_matrix, next_bot, next_player, temp_attacks, temp_start = self.__update_matrix_in_forward(decision_tree[index][1], decision_tree[index+1][1], start, update_matrix, update_bot, update_player, update_attacks)
                update_matrix = next_matrix
                update_bot = next_bot
                update_player = next_player
                update_attacks = temp_attacks
                start = temp_start
            else:
                temp_matrix, temp_bot, temp_player = self.__update_matrix_in_forward(decision_tree[index][1], None, start, update_matrix, update_bot, update_player, update_attacks)
            if bot_bool:
                change_player = self.__change_to_list(temp_player)
                for row, col in temp_bot.keys():
                    if canMove(temp_matrix, [row, col]):
                        temp_list.extend(list(map(lambda x: self.__update_moves(decision_tree[index], x), BotChessman(temp_matrix, [row, col], change_player))))
            else:
                change_bot = self.__change_to_list(temp_bot)
                for row, col in temp_player.keys():
                    if canMove(temp_matrix, [row, col]):
                        temp_list.extend(list(map(lambda x: self.__update_moves(decision_tree[index], x), PlayerChessman(temp_matrix, [row, col], change_bot))))
            list1.extend(temp_list)
                
                
        return list1


def start_Black_Bot_Prediction():
    print("bot")
    Prediction(BOT, PLAYER)
    print("\n\nplayer")
    Prediction(PLAYER, BOT)

if __name__ == "__main__":
    # print("Bot")
    print(normal)
    start_Black_Bot_Prediction()
    # decision_tree = _prediction_first_move(BOT, PLAYER)
    # print(decision_tree)
    # _prediction_next_move(PLAYER, BOT)
    # print(list(map(lambda x: _get_the_postion(x[1][0]), decision_tree)))
    # print(list(map(lambda x: _get_the_postion(x[1]), prediction_first_move(matrix, BOT, PLAYER))))
    # prediction_first_move(matrix, BOT, PLAYER)
    # print("\n")
    # print("Player")
    # print(_prediction_first_move(PLAYER, BOT))
    # print(list(map(lambda x: _get_the_postion(x[1][0]), _prediction_first_move(PLAYER, BOT))))
    # predictionFirstBot(matrix, PLAYER)