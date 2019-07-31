#!/usr/bin/python3

import itertools
from copy import deepcopy

## どこも抜け落ちていない方陣
R_org = [
    [[0, 1], [-1, -1], [4, 5], [6, 7], [-1, -1], [-1, -1], [2, 3]],
    [[5, 7], [0, 2], [-1, -1], [-1, -1], [-1, -1], [1, 3], [4, 6]],
    [[-1, -1], [5, 6], [0, 3], [1, 2], [-1, -1], [4, 7], [-1, -1]],
    [[-1, -1], [3, 7], [-1, -1], [0, 4], [2, 6], [-1, -1], [1, 5]],
    [[3, 6], [1, 4], [2, 7], [-1, -1], [0, 5], [-1, -1], [-1, -1]],
    [[2, 4], [-1, -1], [-1, -1], [3, 5], [1, 7], [0, 6], [-1, -1]],
    [[-1, -1], [-1, -1], [1, 6], [-1, -1], [3, 4], [2, 5], [0, 7]],
]

## 抜け落ちあり
R_org = [
    [[-2, -2], [-2, -2], [-2, -2], [-1, -1], [-2, -2], [-1, -1], [-1, -1]],
    [[-1, -1], [0, 2], [-2, -2], [-2, -2], [-1, -1], [-2, -2], [-1, -1]],
    [[-1, -1], [-1, -1], [0, 3], [7, 1], [4, 6], [-1, -1], [-2, -2]],
    [[-2, -2], [-1, -1], [-1, -1], [0, 4], [1, 2], [-2, -2], [-1, -1]],
    [[-1, -1], [-2, -2], [-1, -1], [-1, -1], [-2, -2], [2, 3], [-2, -2]],
    [[-2, -2], [-1, -1], [1, 5], [-1, -1], [-1, -1], [0, 6], [-2, -2]],
    [[-2, -2], [-2, -2], [-1, -1], [-2, -2], [-1, -1], [-1, -1], [-2, -2]],
]


def show(R):
    print('=' * 35)
    print()
    for row in R:
        for s in row:
            if s[0] == -1 and s[1] == -1:
                print(' --- ', end='')
            elif s[0] == -2 and s[1] == -2:
                print(' *** ', end='')
            else:
                print(' {},{} '.format(s[0], s[1]), end='')
        print('', end='\n\n')
    print('=' * 35)


def comb(L, N):
    return [C for C in itertools.combinations(L, N)]


R_list = []
def resolver(R):
    ### 2種類の方陣ができたらcritical setではない。
    if 1 < len(R_list):
        return
    ### 空の場所の座標リスト
    emp_list = [(i, j) for i in range(len(R)) for j in range(len(R)) if R[i][j] == [-2, -2]]
    if not emp_list:
        pairs = [tuple(R[i][j]) for i in range(len(R)) for j in range(len(R)) if tuple(R[i][j]) != (-1, -1) and tuple(R[i][j]) != (-2, -2)]
        if len(pairs) == len(set(pairs)) and R not in R_list:
            print('completed')
            R_list.append(deepcopy(R))
            show(R)
            print('-'*60)
        return

    ### 埋めることのできる場所が少ないものから試すことで高速化。少ない物順にソート。
    available_num_list = []
    for el in emp_list:
        x, y = el
        in_row = [R[x][i] for i in range(len(R)) if R[x][i] != [-2, -2] and R[x][i] != [-1, -1]]
        row = [i for i in range(len(R)+1) if i not in [b for a in in_row for b in a]] ## 列で入りうる数字
        in_col = [R[i][y] for i in range(len(R)) if R[i][y] != [-2, -2] and R[i][y] != [-1, -1]]
        col = [i for i in range(len(R)+1) if i not in [b for a in in_col for b in a]] ## 行で入りうる数字
        available_num = [i for i in row if i in col]
        available_num_list.append(available_num)
#    print(available_num_list)
    len_list = []
    for anl in available_num_list:
        len_list.append(len(anl))
#    print(len_list)
    order_list = []
    for _ in len_list:
        index = len_list.index(min(len_list))
        order_list.append(index)
        len_list[index] = 100
#    print(order_list)
    emp_list = [emp_list[i] for i in order_list]
#    print(emp_list)

    ### すべての空の場所対してに入れることができる値を調べる
    for el in emp_list:
        x, y = el
        in_row = [R[x][i] for i in range(len(R)) if R[x][i] != [-2, -2] and R[x][i] != [-1, -1]]
        row = [i for i in range(len(R)+1) if i not in [b for a in in_row for b in a]] ## 列で入りうる数字
        in_col = [R[i][y] for i in range(len(R)) if R[i][y] != [-2, -2] and R[i][y] != [-1, -1]]
        col = [i for i in range(len(R)+1) if i not in [b for a in in_col for b in a]] ## 行で入りうる数字
        available_num = [i for i in row if i in col]
        available_comb = comb(available_num, 2)

#        if available_comb or True:
#            print('empty_position : {}'.format(emp_list))
#            print('current_position : {}'.format(el))
#            print('available_row : {}'.format(row))
#            print('available_col : {}'.format(col))
#            print('available_num : {}'.format(available_num))
#            print('available_comb : {}'.format(available_comb))
#            show(R)
#            print('-'*60)

        for c in available_comb:
            R[x][y] = c
            if check_integrity(R, el):
#                print("checked")
#                print('-'*60)
                resolver(deepcopy(R))


def check_integrity(R, pos):
    x, y = pos
    in_row = [R[x][i] for i in range(len(R)) if R[x][i] != [-2, -2] and R[x][i] != [-1, -1]]
    row = [n for ir in in_row for n in ir]
    in_col = [R[i][y] for i in range(len(R)) if R[i][y] != [-2, -2] and R[i][y] != [-1, -1]]
    col = [n for ic in in_col for n in ic]
    if len(row) == len(set(row)) and len(col) == len(set(col)):
        return True
    return False

resolver(deepcopy(R_org))
if len(R_list) == 1:
    print('critical set')
else:
    print('NOT critical set')
