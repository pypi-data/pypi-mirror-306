import copy
import pandas as pd
import sys


def replace_inf(matrix_out: list):
    # Определяем значение для бесконечности - I
    I = 999
    # Заменяем на I значения 0, когда дуги не существует
    # matrix_df = matrix_out.replace([0], I)
    matrix_df = [[elem if elem != 0 else I for elem in row] for row in matrix_out]

    # Заменяем на 0 значения по главной диагонали

    for i in range(len(matrix_out)):
        for j in range(len(matrix_out[i])):
            if i == j:
                matrix_df[i][j] = 0

    return matrix_df

# Нахождение кратчайших путей между всеми парами вершин
def floyd_alg(matrix_0: list):
    matrix_0 = replace_inf(matrix_0)  # применение сервисной функции
    # Количество вершин в графе`
    n = len(matrix_0)
    # Определяем список маршрутов
    route_list = [[[0] for col in range(n)] for row in range(n)]
    # Преобразуем датафрейм в список
    # matrix_list = matrix_0.values.tolist()
    matrix_list = copy.deepcopy(matrix_0)
    # Определяем матрицу весов
    D = [[0 for col in range(n)] for row in range(n)]
    # Определяем l_0
    l_1 = [0]
    # Определяем матрицу дуг
    D_route = [[l_1 for col in range(n)] for row in range(n)]
    # Последовательное улучшение стоимости маршрута для каждой пары вершин
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if i != j:
                    # Определяем временную переменную для сравнения
                    temp_sum_1 = matrix_list[i][k] + matrix_list[k][j]
                    # Определяем временную переменную из матрицы весов
                    temp_2 = matrix_list[i][j]
                    # Определяем минимум из временных переменных
                    d_el = min(temp_sum_1, temp_2)
                    # Определяем индексы вершин в маршрут
                    # print(temp_sum_1, matrix_list[i][k], matrix_list[k][j],  temp_2)
                    # Определяем временный список, копируя элемент ij матрицы дуг
                    tt = copy.copy(D_route[i][j])
                    if temp_sum_1 < temp_2:
                        # route_list[i][j] = [i+1,k+1,k+1,j+1]
                        # Добавляем вершину i во временный список
                        tt.append(i + 1)
                        # Добавляем вершину k во временный список
                        tt.append(k + 1)
                        # Добавляем вершину k во временный список
                        tt.append(k + 1)
                        # Добавляем вершину j во временный список
                        tt.append(j + 1)
                        # Добавляем дуги ik, kj в матрицу дуг
                        D_route[i][j] = tt
                    else:
                        # Добавляем вершину i во временный список
                        tt.append(i + 1)
                        # Добавляем вершину j во временный список
                        tt.append(j + 1)
                        # Добавляем дугу ij в матрицу дуг
                        D_route[i][j] = tt
                    # Переназначаем стоимость маршрута в матрице весов D
                    D[i][j] = d_el
        matrix_list = D

        # print('D',k+1, D)
        # print(matrix_list)
        # print('route',k+1,route_list)

    floyd_dict = {'title': 'Алгоритм Флойда', 'D': D, 'D_route': D_route}

    return floyd_dict

