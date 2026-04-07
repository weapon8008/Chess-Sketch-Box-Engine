
        #     chessmen_attack.append(temp_matrix[int(indexes[i]/(n*n))%n][int(indexes[i]/(n*n*n))])
        #     if temp_matrix[indexes[i]%n][int(indexes[i]/n)%n] <= 6:
        #         temp_bot[(int(indexes[i]/(n*n))%n, int(indexes[i]/(n*n*n)))] = temp_bot.pop((indexes[i]%n, int(indexes[i]/n)%n))
        #         if temp_matrix[int(indexes[i]/(n*n))%n][int(indexes[i]/(n*n*n))] != 0:
        #             temp_player.pop((int(indexes[i]/(n*n))%n, int(indexes[i]/(n*n*n))))
        #     elif temp_matrix[indexes[i]%n][int(indexes[i]/n)%n] >= 7:
        #         temp_player[(int(indexes[i]/(n*n))%n, int(indexes[i]/(n*n*n)))] = temp_player.pop((indexes[i]%n, int(indexes[i]/n)%n))
        #         if temp_matrix[int(indexes[i]/(n*n))%n][int(indexes[i]/(n*n*n))] != 0:
        #             temp_bot.pop((int(indexes[i]/(n*n))%n, int(indexes[i]/(n*n*n))))
        #     temp_matrix[int(indexes[i]/(n*n))%n][int(indexes[i]/(n*n*n))] = temp_matrix[indexes[i]%n][int(indexes[i]/n)%n]
        #     temp_matrix[indexes[i]%n][int(indexes[i]/n)%n]