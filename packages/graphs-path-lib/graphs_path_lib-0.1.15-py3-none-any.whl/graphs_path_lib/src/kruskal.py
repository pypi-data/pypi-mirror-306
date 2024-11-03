import pandas as pd


def list_from_matrix(matrix: list):
  matrix = pd.DataFrame(matrix)
  n = len(matrix.columns)
  gr_list = []
  for i in range(n):
    for j in range(i, n):
      if matrix.iloc[i, j] != 0:
        gr_list.append([matrix.iloc[i, j], i+1, j+1])
  return gr_list

def kruskal_alg(matrix: list):
    Spisok = list_from_matrix(matrix)
    Rs = sorted(Spisok, key=lambda x: x[0])
    U = set()   # список соединенных вершин
    D = {}      # словарь списка изолированных групп вершин
    mst_list = []      # список остова

    for r in Rs:
        if r[1] not in U or r[2] not in U:  # проверка для исключения циклов в остове
            if r[1] not in U and r[2] not in U: # если обе вершины не соединены, то
                D[r[1]] = [r[1], r[2]]          # формируем в словаре ключ с номерами вершин
                D[r[2]] = D[r[1]]               # и связываем их с одним и тем же списком вершин
            else:                           # иначе
                if not D.get(r[1]):             # если в словаре нет первой вершины, то
                    D[r[2]].append(r[1])        # добавляем в список первую вершину
                    D[r[1]] = D[r[2]]           # и добавляем ключ с номером первой вершины
                else:
                    D[r[1]].append(r[2])        # иначе, все то же самое делаем со второй вершиной
                    D[r[2]] = D[r[1]]

            mst_list.append(r)             # добавляем ребро в остов
            U.add(r[1])             # добавляем вершины в множество U
            U.add(r[2])

    for r in Rs:   # проходим по ребрам второй раз и объединяем разрозненные группы вершин
        if r[2] not in D[r[1]]:     # если вершины принадлежат разным группам, то объединяем
            mst_list.append(r)             # добавляем ребро в остов
            gr1 = D[r[1]]
            D[r[1]] += D[r[2]]      # объединем списки двух групп вершин
            D[r[2]] += gr1

    kruskal_dict = {'title': 'Алгоритм Краскала', 'value': mst_list}

    return kruskal_dict
