import pandas as pd
import sys
import copy

def replace_0_to_inf(graph_df):
    """
    Функция заменяет нули в матрице смежности на значение "бесконечность" (max элемент + 1000)
    """
    max_el = graph_df.max().max()
    inf_value = max_el + 1000
    graph_df_inf = graph_df.replace(0, inf_value)
    return graph_df_inf, inf_value


def dejkstra_alg(graph_matrix_df: list,
                     start_node: int,
                     end_node: int):
    """
    Алгоритм Дейкстры для поиска кратчайшего пути между двумя вершинами
    """
    # Преобразование списка в DataFrame
    graph_matrix_df = pd.DataFrame(graph_matrix_df)

    # Замена нулей на бесконечность
    graph_matrix_df_inf, max_el = replace_0_to_inf(graph_matrix_df)

    # Инициализируем списки и переменные
    pp = [start_node]  # Постоянные пометки (посещенные вершины)
    c_vp = [max_el] * len(graph_matrix_df)  # Временные пометки (минимальное расстояние до каждой вершины)
    c_vp[start_node - 1] = 0  # Расстояние до стартовой вершины равно 0
    predecessor = [None] * len(graph_matrix_df)  # Предшественники для каждой вершины
    df_lst = [c_vp.copy()]  # Для хранения промежуточных результатов

    def pp_search(c_vp, pp):
        """
        Функция для поиска следующей вершины с минимальной временной меткой
        """
        min_weight = max_el
        min_index = -1
        for i in range(len(c_vp)):
            if (i + 1) not in pp and c_vp[i] < min_weight:
                min_weight = c_vp[i]
                min_index = i
        return min_weight, min_index + 1  # Возвращаем вес и номер вершины

    while True:
        # Обновляем временные метки и сохраняем предшественников
        for i in range(len(c_vp)):
            if (i + 1) not in pp:
                temp_weight = c_vp[pp[-1] - 1] + graph_matrix_df_inf.iloc[pp[-1] - 1, i]
                if c_vp[i] > temp_weight:
                    c_vp[i] = temp_weight
                    predecessor[i] = pp[-1]

        # Исключаем посещенные вершины
        for i in pp:
            c_vp[i - 1] = max_el

        # Сохраняем текущие временные метки
        df_lst.append(c_vp.copy())

        # Ищем следующую вершину для посещения
        min_weight, next_node = pp_search(c_vp, pp)
        if next_node == -1:
            break  # Все доступные вершины посещены

        pp.append(next_node)

        if next_node == end_node:
            break  # Достигли конечной вершины

    # Формируем DataFrame из списка временных меток
    df = pd.DataFrame(df_lst).transpose()

    # Добавляем дополнительные столбцы, если необходимо
    while len(df.columns) < len(df):
        df[len(df.columns)] = [max_el] * len(df)

    # Общий вес кратчайшего пути до конечной вершины
    weight_total = c_vp[end_node - 1]

    # Результаты работы алгоритма
    dejkstra_dict = {
        'title': 'Алгоритм Дейкстры',
        'pp': pp,
        'weight_total': weight_total,
        'df': df,
        'max_el': max_el,
        'start': start_node,
        'end': end_node,
        'predecessor': predecessor,
        'graph_matrix_df': graph_matrix_df  # Исходная матрица смежности
    }

    return dejkstra_dict
