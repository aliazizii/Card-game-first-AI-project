import sys
from typing import List
import copy
import time

class Card:
    def __init__(self, number: int, color: str):
        self.number = number
        self.color = color
    def __str__(self):
        return str(self.number) + self.color
    def __repr__(self):
        return str(self.number) + self.color
    def __eq__(self, other):
        return self.number == other.number and self.color == other.color

class Node:
    def __init__(self, board_game: list, last_move: str = None, parent = None, depth: int = 0):
        self.board_game = board_game
        self.parent = parent
        self.last_move = last_move
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

k, m, n = 0, 0, 0
created = 0
expanded = 0

"This function read inputs from a text file and finally return our initial node"

def read_input():
    board_game = []
    f = open("testcase.txt", "r")
    global n, m, k
    k, m, n = map(int, f.readline().split())
    for i in range(k):
        row = []
        l = f.readline().split()
        flag = True
        if "#" in l:
            board_game.append([])
            flag = False
        else:
            for element in l:
                card = Card(element[:-1], element[-1])
                row.append(card)
        if flag:
            board_game.append(row)
    f.close()
    init_node = Node(board_game)
    return init_node

def is_all_element_are_equal(l: list):
    if len(l) == 0:
        return True
    else:
        return l.count(l[0]) == len(l)

def check_arr_of_cards(l: list):
    test_list = []
    test_list2 = []
    for element in l:
        test_list.append(element.number)
        test_list2.append(element.color)
    test_list = list(map(int, test_list))
    if test_list == list(reversed(sorted(test_list))) and is_all_element_are_equal(test_list2):
        return True
    else:
        return False

def check_goal(node: Node):
    for r in node.board_game:
        if not check_arr_of_cards(r):
            return False
    return True

def find_move(l: List[List[Card]]):
    last_element = []
    moves = []
    for i in range(k):
        try:
            last_element.append(l[i][-1].number)
        except:
            last_element.append(sys.maxsize)
    for i in range(len(last_element)):
        for j in range(len(last_element)):
            if int(last_element[i]) < int(last_element[j]):
                moves.append((i, j))
    return moves

def generate_children(node: Node):
    copy_node = copy.deepcopy(node)
    moves = find_move(copy_node.board_game)
    children = []
    for i,j in moves:
        list_child_node = copy.deepcopy(node.board_game)
        last_move = "Add the last element of column {} to the end of column {} ({})".format(i+1, j+1, copy_node.board_game[i][-1])
        child_node = Node(list_child_node, last_move, node)
        temp_card = child_node.board_game[i].pop()
        child_node.board_game[j].append(temp_card)
        children.append(child_node)
    return children

def dls(node: Node, limit):
    if check_goal(node):
        return node, True
    if limit == 0:
        return None, True
    global created
    global expanded
    expanded = expanded + 1
    if limit > 0:
        cutoff_occurred = False
        for child in generate_children(node):
            created = created + 1
            found, cutoff = dls(child, limit - 1)
            if found:
                return found, True
            if cutoff:
                cutoff_occurred = True
        return None, cutoff_occurred

def ids(root: Node, base_levels: int = 0):
    for depth in range(base_levels, 1000):
        found, cutoff = dls(root, depth)
        if found:
            return found
        elif not cutoff:
            return None

def print_line():
    print("`" * 70)

def print_board_game(l: List[List[Card]]):
    for col in l:
        print(*col)

def print_path(node: Node):
    path = []
    while node.parent != None:
        path.append(node.last_move)
        node = node.parent
    print_line()
    print("Actions :")
    for i in range(len(path)):
        print(path.pop())
    print_line()
    print("--- created nodes =", created,"---")
    print("--- expanded nodes =", expanded,"---")

if __name__ == '__main__':
    created = 0
    expanded = 0
    start_time = time.time()
    init_node = read_input()
    goal = ids(init_node)
    end_time = time.time()
    print("-"*32, "IDS", "-"*32)
    print("initial state :")
    print_board_game(init_node.board_game)
    print_line()
    print("goal state :")
    print_board_game(goal.board_game)
    print_line()
    print("depth :", goal.depth)
    print_path(goal)
    print_line()
    print("--- %s minutes and %s seconds ---" % (int((end_time - start_time) // 60), float((end_time - start_time) % 60)))