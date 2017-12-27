#!/usr/bin/python3


import sys
import copy
from math import sqrt

import time


class TreeNode:
    def __init__(self, state, cost, h_x, branch):
        self.state = state
        self.cost = cost
        self.h_x = h_x
        self.branch = branch


# heuristic - Manhattan distance
def heuristic_helper(board, goal_state):
    heuristic = 0
    for i in range(0, 4):
        for j in range(0, 4):
            temp = board[i][j]
            index = get_blank_location(goal_state, temp)
            cur_manhattan_distance = abs(index[0] - i) + abs(index[1] - j)
            heuristic = heuristic + cur_manhattan_distance
    return heuristic


# heuristic - Euclidean distance
def heuristic_euclid(board, goal_state):
    heuristic = 0
    for i in range(0, 4):
        for j in range(0, 4):
            temp = board[i][j]
            index = get_blank_location(goal_state, temp)
            cur_manhattan_distance = sqrt((index[0] - i) ** 2 + (index[1] - j) ** 2)
            heuristic = heuristic + cur_manhattan_distance
    return heuristic



def permutation_invertions(board):
    temp = list()
    for i in range(4):
        for j in range(4):
            temp.append(int(board[i][j]))
    per_inv = 0
    for i in range(16):
        for j in range(i, 16):
            if temp[i] != 0 and temp[j] != 0 and temp[i] > temp[j]:
                per_inv += 1
    return per_inv


def move(row, col, board, direction):
    temp = copy.deepcopy(board)
    if direction[0] is "U":
        tile_count = int(direction[1])
        for count in range(tile_count):
            temp[row + count][col], temp[row + count + 1][col] = temp[row + count + 1][col], temp[row + count][col]

    if direction[0] is "D":
        tile_count = int(direction[1])
        for count in range(tile_count):
            temp[row - count][col], temp[row - count - 1][col] = temp[row - count - 1][col], temp[row - count][col]

    if direction[0] is "L":
        tile_count = int(direction[1])
        for count in range(tile_count):
            temp[row][col + count], temp[row][col + count + 1] = temp[row][col + count + 1], temp[row][col + count]
    if direction[0] is "R":
        tile_count = int(direction[1])
        for count in range(tile_count):
            temp[row][col - count], temp[row][col - count - 1] = temp[row][col - count - 1], temp[row][col - count]

    return temp


def successor(cur_state_object):
    node = cur_state_object[1]
    cur_state = node.state
    index = get_blank_location(cur_state, '0')
    r, c = index
    successors = list()
    moves = []
    if r == 0:
        moves.extend(("U1", "U2", "U3"))
    elif r == 1:
        moves.extend(("U1", "U2", "D1"))
    elif r == 2:
        moves.extend(("U1", "D1", "D2"))
    else:
        moves.extend(("D1", "D2", "D3"))

    if c == 0:
        moves.extend(("L1", "L2", "L3"))
    elif c == 1:
        moves.extend(("L1", "L2", "R1"))
    elif c == 2:
        moves.extend(("L1", "R1", "R2"))
    else:
        moves.extend(("R1", "R2", "R3"))

    for i in range(len(moves)):
        if moves[i][0] is "U" or moves[i][0] is "D":
            moves[i] = moves[i] + str(r + 1)
        if moves[i][0] is "L" or moves[i][0] is "R":
            moves[i] = moves[i] + str(c + 1)

    for direction in moves:
        branch = node.branch[:]
        branch.append(direction)
        successors.append(TreeNode(move(r, c, cur_state, direction), node.cost, node.h_x, branch))
    return successors


# A* Search
def a_star_search(curr_state):
    goal_state = [['1', '2', '3', '4'], ['5', '6', '7', '8'], ['9', '10', '11', '12'], ['13', '14', '15', '0']]
    if curr_state == goal_state:
        return []
    heuristic = get_h_x(TreeNode(curr_state, 0, 0, []), goal_state)
    fringe = list()
    temp_fringe_elem = TreeNode(curr_state, 0, heuristic, [])
    temp_total_cost = temp_fringe_elem.cost + temp_fringe_elem.h_x
    fringe.append([temp_total_cost, temp_fringe_elem])
    visited = [curr_state]
    while len(fringe) > 0:
        min = float('inf')
        for element in fringe:
            if element[0] < min:
                min = element[0]
                min_element = element
        for s in successor(fringe.pop(fringe.index(min_element))):
            if s.state == goal_state:
                return s.branch
            s.cost = s.cost + 1
            s.h_x = get_h_x(s, goal_state)
            temp_total_cost = s.cost + s.h_x
            if s.state not in visited:
                visited.append(s.state)
            else:
                for i in range(len(fringe)):
                    if fringe[i][1].state == s.state and fringe[i][0] > temp_total_cost:
                        fringe.insert(i, [temp_total_cost, s])
                        break
                continue
            fringe.append([temp_total_cost, s])
    return False


# code from http://stackoverflow.com/questions/6518291/using-index-on-multidimensional-lists
def get_blank_location(state, node):
    for row, i in enumerate(state):
        try:
            column = i.index(node)
        except ValueError:
            continue
        return row, column
    return -1


# calculating the heuristic for a given state
def get_h_x(node, goal_state):
    heuristic = heuristic_helper(node.state, goal_state)
    row, col = get_blank_location(node.state, "0")
    if len(node.branch) == 0:
        return heuristic

    moves = []
    if row == 0:
        moves.extend(("U1", "U2", "U3"))
    elif row == 1:
        moves.extend(("U1", "U2", "D1"))
    elif row == 2:
        moves.extend(("U1", "D1", "D2"))
    else:
        moves.extend(("D1", "D2", "D3"))

    if col == 0:
        moves.extend(("L1", "L2", "L3"))
    elif col == 1:
        moves.extend(("L1", "L2", "R1"))
    elif col == 2:
        moves.extend(("L1", "R1", "R2"))
    else:
        moves.extend(("R1", "R2", "R3"))

    for i in range(len(moves)):
        if moves[i][0] is "U" or moves[i][0] is "D":
            moves[i] = moves[i] + str(row + 1)
        if moves[i][0] is "L" or moves[i][0] is "R":
            moves[i] = moves[i] + str(col + 1)

    for direction in moves:
        temp = copy.deepcopy(node.state)
        temp = move(row, col, temp, direction)
        temp_h = heuristic_helper(temp, goal_state)
        if temp_h < heuristic:
            heuristic = temp_h
    return heuristic


def init_board(filename):
    board = []
    with open(filename) as file:
        lines = file.read().splitlines()
        for line in lines:
            board.append(line.split(' '))
    return board


# code inspired from http://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
def is_solvable(board):
    per_inv = permutation_invertions(board)
    index = get_blank_location(board, "0")
    pos_from_bottom = (3 - index[0]) + 1
    if (pos_from_bottom % 2 == 0 and per_inv % 2 != 0) or (pos_from_bottom % 2 != 0 and per_inv % 2 == 0):
        return True
    else:
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Invalid Input!")
    else:
        start_time = time.time()
        board = init_board(sys.argv[1])
        if is_solvable(board):
            print(" ".join(a_star_search(board)))
            # print(time.time() - start_time)
            # print(a_star(board))
        else:
            print("Not Solvable")
