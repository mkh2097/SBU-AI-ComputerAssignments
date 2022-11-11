# start node is 'P'
# target node is 'G'

import numpy as np
from math import sqrt
from collections import deque

np.set_printoptions(linewidth=160)
matrix = np.loadtxt("C:/Users/MOHAMMAD/PycharmProjects/tweet_bot/matrix3.txt", dtype='str')
temp_matrix = matrix
matrix = np.where(matrix == 'P', 2, matrix)
matrix = np.where(matrix == 'G', 3, matrix)
matrix = matrix.astype(float)
result = np.where(matrix == 2)
start_x_pos = result[0][0]
start_y_pos = result[1][0]
result = np.where(matrix == 3)
target_x_pos = result[0][0]
target_y_pos = result[1][0]
rows, columns = matrix.shape


# calculate heuristic function
def calculate_h(dest, mode="e"):
    x = dest[0]
    y = dest[1]
    if mode == "m":  # mode := Manhattan Distance
        return abs(x - target_x_pos) + abs(y - target_y_pos)
    elif mode == "d":  # mode := Diagonal Distance
        return max(abs(x - target_x_pos), abs(y - target_y_pos))
    elif mode == "e":  # mode := Euclidean Distance
        return sqrt((x - target_x_pos) ** 2 + (y - target_y_pos) ** 2)


def a_star():
    # matrix for visited coordination (closed list alternative)
    visit_matrix = temp_matrix.copy()

    # matrix for holding each coordination's parent
    parent_matrix = temp_matrix.copy()
    parent_matrix = parent_matrix.astype(object)
    parent_matrix[start_x_pos][start_y_pos] = (-1, -1)

    # matrix for holding each coordination's distance to start node (g function)
    g_matrix = temp_matrix.copy()
    g_matrix = np.where(g_matrix == '1', -1, g_matrix)
    g_matrix = np.where(g_matrix == 'G', 0, g_matrix)
    g_matrix = np.where(g_matrix == 'P', 0, g_matrix)
    g_matrix = g_matrix.astype(float)

    # g := cost for moving from starting point to given point
    # h := distance between starting point & target point
    # f = g + h

    # calculate root's f function and add it to open list
    start_dest = (start_x_pos, start_y_pos)
    start_h = calculate_h(start_dest)
    start_g = 0
    start_f = start_h + start_g

    open_list = list()
    open_list.append((start_dest, start_f))

    find_target = False

    while len(open_list) > 0:
        if find_target:
            break

        # sort open list in decreasing order by f function value of each coordination
        open_list.sort(key=lambda x: x[1])
        open_list.reverse()

        # pop from stack (last element := lowest f value)
        value = open_list.pop()
        x_pos, y_pos = value[0]

        # mark this coordination as visited
        visit_matrix[x_pos][y_pos] = True

        adjacent = [[-1, 0], [1, 0], [0, 1], [0, -1]]

        for i in range(len(adjacent)):

            x_pos_adj = x_pos + adjacent[i][0]
            y_pos_adj = y_pos + adjacent[i][1]

            # finding adjutants
            if x_pos_adj == rows:
                x_pos_adj -= rows
            elif x_pos_adj == -1:
                x_pos_adj += rows
            if y_pos_adj == columns:
                y_pos_adj -= columns
            elif y_pos_adj == -1:
                y_pos_adj += columns

            # validate adjacency
            # visited (aka found in closed list)
            if visit_matrix[x_pos_adj][y_pos_adj] == 'T':
                continue
            # obstacle
            if visit_matrix[x_pos_adj][y_pos_adj] == '1':
                continue

            # check for duplicated coordination in open list
            adj_pos = (x_pos_adj, y_pos_adj)
            found_dup = False
            for open in open_list[:]:
                if open[0] == adj_pos:
                    found_dup = True

                    # calculate new f function for this new coordination
                    adj_h = calculate_h(adj_pos)
                    adj_g = g_matrix[x_pos][y_pos] + 1
                    adj_f = adj_h + adj_g

                    # and compare it with previous value
                    if adj_f < open[1]:
                        # new value is better

                        # update g matrix
                        g_matrix[x_pos_adj][y_pos_adj] = adj_g

                        # update parent matrix
                        parent_matrix[x_pos_adj][y_pos_adj] = (x_pos, y_pos)

                        # update open list
                        open_list.remove(open)
                        open_list.append((adj_pos, adj_f))

            # if coordination is fresh and not in open list!
            if not found_dup:
                adj_h = calculate_h(adj_pos)
                adj_g = g_matrix[x_pos][y_pos] + 1
                g_matrix[x_pos_adj][y_pos_adj] = adj_g
                adj_f = adj_h + adj_g

                open_list.append((adj_pos, adj_f))

                parent_matrix[x_pos_adj][y_pos_adj] = (x_pos, y_pos)

            if visit_matrix[x_pos_adj][y_pos_adj] == 'G':
                visit_matrix[x_pos_adj][y_pos_adj] = 'D'
                find_target = True
                break

    # finding path
    x = target_x_pos
    y = target_y_pos
    path = []
    while parent_matrix[x][y] != (-1, -1):
        # if there is no way to target
        if parent_matrix[x][y] == "G":
            print("There is no Path!")
            break

        # identify movements
        x_pr, y_pr = parent_matrix[x][y]
        if x - x_pr == -1 or (x - x_pr) == (rows - 1):
            path.append("Up")
        elif x - x_pr == 1 or (x - x_pr) == (1 - rows):
            path.append("Down")
        elif y - y_pr == 1 or (y - y_pr) == (1 - columns):
            path.append("Right")
        elif y - y_pr == -1 or (y - y_pr) == (columns - 1):
            path.append("Left")
        x = x_pr
        y = y_pr

    path.reverse()
    print(" ".join(path))


# a* search
a_star()
