import pandas as pd
import copy
import openpyxl
from app.graphs_path_lib import (
    prima_alg, kruskal_alg, floyd_alg, dejkstra_alg
)


def load_cost_matrix(path_input: str):
    """
    Загрузка матрицы смежности ориентированного графа
    """

    try:
        # Загрузка файла XLS в датафрейм
        data_frame = pd.read_excel(path_input, header=None)

        # Проверка формата матрицы
        if not data_frame.applymap(lambda x: isinstance(x, (int, float))).values.all():
            raise ValueError('Ошибка: Матрица должна содержать только числа')

        # Преобразование датафрейма в список списков
        matrix_out = data_frame.values.tolist()

        # Проверка квадратности матрицы
        n = len(matrix_out)
        if any(len(row) != n for row in matrix_out):
            raise ValueError('Ошибка: Матрица должна быть квадратной')

        return matrix_out
    except ValueError as e:
        print(e)
        return None


def trass(mst_dict):
    """
    Трассировка маршрута в графе
    """
    start_node = mst_dict['start']
    end_node = mst_dict['end']
    predecessor = mst_dict['predecessor']
    graph_matrix_df = mst_dict['graph_matrix_df']
    weight_total = mst_dict['weight_total']

    # Инициализируем маршрут с конечной вершиной
    route_res = [end_node]
    current_node = end_node - 1  # Индексация с нуля

    # Восстанавливаем путь, следуя по предшественникам
    while predecessor[current_node] is not None:
        route_res.append(predecessor[current_node])
        current_node = predecessor[current_node] - 1  # Переходим к предшественнику

    # Проверяем, что достигли начальной вершины
    if route_res[-1] != start_node:
        print("Путь не найден")
        return None, None, None, None

    # Разворачиваем маршрут, чтобы получить путь от начальной вершины к конечной
    route_res.reverse()

    # Вычисляем веса ребер на пути
    weight_list = []
    for i in range(len(route_res) - 1):
        u = route_res[i] - 1  # Индексация с нуля
        v = route_res[i + 1] - 1
        weight = graph_matrix_df.iloc[u, v]
        weight_list.append(weight)

    # Вычисляем суммарный вес пути
    len_sum = sum(weight_list)

    # Формируем список шагов для отображения
    table_viz_lst = []
    cumulative_weight = 0
    for i in range(len(weight_list)):
        cumulative_weight += weight_list[i]
        step_info = f"{cumulative_weight - weight_list[i]} + {weight_list[i]} = {cumulative_weight}"
        table_viz_lst.append([step_info])

    return route_res, weight_list, len_sum, table_viz_lst


file_path = 'matrix_directed.xlsx'

matrix = load_cost_matrix(file_path)
print('matrix:')
for item in matrix:
    print(item)

start_node = 1
end_node = 4

# prima_res = prima_alg(matrix)
# print(f'\nАлгоритм Прима:')
# print(prima_res)
#
# kruskal_res = kruskal_alg(matrix)
# print(f'\nАлгоритм Краскала:')
# print(kruskal_res)
#
# floyd_res = floyd_alg(matrix)
# print(f'\nАлгоритм Флойда:')
# print(floyd_res)

dejkstra_res = dejkstra_alg(matrix, start_node, end_node)
print(f'\nАлгоритм Дейкстры:')
print(dejkstra_res)

route_res, weight_list, len_sum, table_viz_lst = trass(dejkstra_res)
print('route_res')
print(route_res)
print('weight_list')
print(weight_list)
print('len_sum')
print(len_sum)
print('table_viz_lst')
print(table_viz_lst)


def alg_viz(mst_dict: dict):
    """
    Этапы работы алгоритма
    """
    # Загружаем исходную таблицу
    df_temp = pd.DataFrame(mst_dict['df']) #if isinstance(df, dict) else copy.deepcopy(df)
    # df_temp = copy.deepcopy(df)

    n = len(df_temp)
    # Формируем списки новых наименований строк и столбцов таблицы
    Index_table, columns_table = [], []
    for i in range(n):
        Index_table.append(str(i + 1))
        columns_table.append("Шаг " + str(i + 1))
    # Переименовываем столбцы и индексы датафрейма
    df_temp.columns = columns_table

    df_temp.index = Index_table

    return {
            'title': f'Шаги алгоритма',
            'index': df_temp.index.to_list(),
            'value': df_temp.to_dict('list'),
        }

def trass_viz(trass_lst: list,
              route_len: int or float):
    """
    Визуализация процесса трассировки
    """
    n = len(trass_lst)

    # Составим таблицу для отображения пользователю
    column_list = ['Параметр']

    index_list = []
    for i in range(n):
        index_list.append('Шаг ' + str(i))
    index_list.append('Длина кратчайшего пути')

    to_df = copy.deepcopy(trass_lst)
    to_df.append([str(route_len)])
    print(to_df)

    df = pd.DataFrame(to_df,
                      index=index_list,
                      columns=column_list)

    return {
            'title': f'Таблица - Итерации трассировки',
            'index': df.index.to_list(),
            'value': df.to_dict('list'),
        }


alg_res = alg_viz(dejkstra_res)
print('alg_res:')
print(alg_res)

trass_viz = trass_viz(table_viz_lst, len_sum)
print('trass_viz:')
print(trass_viz)
