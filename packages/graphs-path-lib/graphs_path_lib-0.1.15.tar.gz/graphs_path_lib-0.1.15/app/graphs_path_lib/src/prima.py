import pandas as pd
import sys


def prima_alg(matrix: list):
    INF = sys.maxsize
    mst_list = []  # список (вес, начальная вершина,конечная вершина)
    matrix = pd.DataFrame(matrix)
    N = len(matrix.columns)
    selected_node = [0] * N
    no_edge = 0
    selected_node[0] = True

    while (no_edge < N - 1):
        minimum = INF
        a = 0
        b = 0
        for m in range(N):
            if selected_node[m]:
                for n in range(N):
                    if ((not selected_node[n]) and matrix.iloc[m, n]):
                        # not in selected and there is an edge
                        if minimum > matrix.iloc[m, n]:
                            minimum = matrix.iloc[m, n]
                            a = m
                            b = n
        # print(str(a) + "-" + str(b) + ":" + str(Matr[a][b]))
        mst_list.append([matrix.iloc[a, b], a + 1, b + 1])
        selected_node[b] = True
        no_edge += 1

    prima_dict = {'title': 'Алгоритм Прима', 'value': mst_list}

    return prima_dict
