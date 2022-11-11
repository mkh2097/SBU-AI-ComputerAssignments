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


def bfs_route():
    # make queue for each coordination
    queue_x_pos = deque()
    queue_y_pos = deque()

    # add root element to queue
    queue_x_pos.append(start_x_pos)
    queue_y_pos.append(start_y_pos)

    # matrix for visited coordination
    visit_matrix = temp_matrix.copy()
    visit_matrix[start_x_pos][start_y_pos] = True

    # matrix for holding each coordination's parent
    parent_matrix = temp_matrix.copy()
    parent_matrix = parent_matrix.astype(object)
    parent_matrix[start_x_pos][start_y_pos] = (-1, -1)

    find_target = False

    while len(queue_x_pos) > 0:
        if find_target:
            break

        # pop from queue (dequeue)
        x_pos = queue_x_pos.popleft()
        y_pos = queue_y_pos.popleft()
        visit_matrix[x_pos][y_pos] = True

        adjacent = [[0, 1], [1, 0], [-1, 0], [0, -1]]

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
            # visited
            if visit_matrix[x_pos_adj][y_pos_adj] == 'T':
                continue
            # obstacle
            if visit_matrix[x_pos_adj][y_pos_adj] == '1':
                continue

            # push to queue (enqueue)
            queue_x_pos.append(x_pos_adj)
            queue_y_pos.append(y_pos_adj)
            parent_matrix[x_pos_adj][y_pos_adj] = (x_pos, y_pos)

            # reach the target
            if visit_matrix[x_pos_adj][y_pos_adj] == 'G':
                visit_matrix[x_pos_adj][y_pos_adj] = 'D'
                find_target = True
                break

            visit_matrix[x_pos_adj][y_pos_adj] = True

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


# bfs search
bfs_route()
