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
        self.f = 0


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
    set_f(init_node)
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
        set_f(child_node)
        children.append(child_node)
    return children

def g(node: Node):
    return node.depth

def h_number_of_card(stateList: list):
    test_list = []
    y = []
    for i in stateList:
        test_list.append(i.number)
        y.append(i.number)
    sum = 0
    temp = test_list
    for i in range(len(stateList)):
        temp = temp[i:]
        if len(temp) != 0:
            tempMax = max(temp)
        if len(temp) != 0 and tempMax > y[i]:
            sum += 1
            index = temp.index(tempMax)
            index2 = y.index(tempMax)
            temp1 = temp.pop(index)
            temp2 = y.pop(index2)
            y.insert(0 , temp2)
            temp.insert(0, temp1)
    return sum

def h1(node: Node):
    board = node.board_game
    sum = 0
    for i in board:
        sum += h_number_of_card(i)
    return sum

def change_color(cards: List[Card]):
    s = 0
    for i in range(len(cards) - 1):
        if cards[i].color != cards[i+1].color:
            s += 1
    return s

def h2(node: Node):
    board = node.board_game
    sum = 0
    for col in board:
        sum += change_color(col)
    return sum

def set_f(node: Node):
    node.f = g(node) + max(h2(node), h1(node))

def f(node: Node):
    return node.f

def find_in_frontier(node: Node, l: List[Node]):
    board = node.board_game
    boards = []
    for i in l:
        boards.append(i.board_game)
    for i, b in enumerate(boards):
        if board == b:
            return l[i]

def is_in_frontier(node: Node, l: List[Node]):
    board = node.board_game
    boards = []
    for i in l:
        boards.append(i.board_game)
    if board in boards:
        return True
    else:
        return False

def a_star(node: Node):
    frontier = []
    explored = []
    frontier.append(node)
    while frontier:
        frontier.sort(key=f)
        current = frontier.pop(0)
        global expanded
        global created
        expanded += 1
        explored.append(current.board_game)
        if check_goal(current):
            return current
        children = generate_children(current)
        created += len(children)
        for child in children:
            if child.board_game not in explored:
                if is_in_frontier(child, frontier):
                    must_change = False
                    comparison_node = find_in_frontier(child, frontier)
                    if f(child) < f(comparison_node):
                        must_change = True
                    if must_change:
                        frontier.remove(comparison_node)
                        frontier.append(child)
                else:
                    frontier.append(child)
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
    goal = a_star(init_node)
    end_time = time.time()
    print("-"*32, "A_Star", "-"*32)
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