# search.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Jongdeog Lee (jlee700@illinois.edu) on 09/12/2018

"""
This file contains search functions.
"""
# Search should return the path and the number of states explored.
# The path should be a list of tuples in the form (alpha, beta, gamma) that correspond
# to the positions of the path taken by your search algorithm.
# Number of states explored should be a number.
# maze is a Maze object based on the maze from the file specified by input filename
# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)
# You may need to slight change your previous search functions in MP1 since this is 3-d maze
import queue as Q
import sys


class Node:
    """A node value that encapsulates the node data and its heuristic value

        Attributes:
            position: a (row -> int, column -> int) tuple
            heuristic_value: an int that captures the heuristic value of the Node
    """

    def __init__(self, position, heuristic_value=0.0):
        """Return a Node Object"""
        self.position = (position[0], position[1])
        self.heuristic_value = heuristic_value

    def __str__(self):
        return "Position: " + str(self.position) + " Heuristic Value: " + str(self.heuristic_value)

    def __hash__(self):
        return hash(str(self.position))

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.heuristic_value < other.heuristic_value


def search(maze, searchMethod):
    return {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod, [])(maze)

def bfs(maze):
    # TODO: Write your code here
    return [], 0

def dfs(maze):
    # TODO: Write your code here
    return [], 0

def greedy(maze):
    # TODO: Write your code here
    return [], 0

# ASTAR SEARCH

# SEARCH

def astar_executor(maze, start_state, objectives):
    """
    The astar search works just like Greedy, other than the fact that the hueristic is the sum of a heuristic function
    and the cost to reach the current state
    We tried out different heuristics, most of which are admissible
    We got the best results from a weighted minimum manhattan distance to the nearest goal and have used that as the default one
    Each Heuristic has been described in the corresponding sections
    :param maze:
    :param start_state:
    :param objectives:
    :return:
    """
    frontier = Q.PriorityQueue()
    start_node = Node(start_state, getAstarHeuristicMinDistanceToAnyObjective(start_state, objectives) + 0)
    frontier.put(start_node)
    visited = set()
    parent_map = {}
    num_states_explored = 0
    flag = False
    while frontier and frontier.qsize() > 0:
        print("Frontier Size: " + str(frontier.qsize()))
        #print("Frontier " + str(frontier))
        current_node = frontier.get()
        current_position = current_node.position
        if current_position in visited:
            continue
        visited.add(current_position)
        print("Exploring " + str(current_position))
        num_states_explored += 1

        if current_position in objectives:
            current_goal = current_position
            flag = True
            break
        neighbour_nodes = maze.getNeighbors(current_position[0], current_position[1])
        print("Neighbours:" + str(neighbour_nodes))
        for each_neighbour in neighbour_nodes:
            if maze.isValidMove(each_neighbour[0], each_neighbour[1]) and each_neighbour not in visited:
                print("Adding Neighbour" + str(each_neighbour))
                parent_map[each_neighbour] = current_position
                frontier.put(Node(each_neighbour, getAstarHeuristicMinDistanceToAnyObjective(each_neighbour, objectives) +
                                                  len(backtrace(parent_map, start_state, current_position))))
    if not flag:
        print("Map is not solvable!")
        return [], 0
    return backtrace(parent_map, start_state, current_goal), num_states_explored


def astar(maze):
    """
    The driver for Astar
    :param maze:
    :return: full_path, total_states_explored
    """
    start_state = maze.getStart()
    objectives = maze.getObjectives()
    return astar_executor(maze, start_state, objectives)




# HEURISTICS


def getAstarHeuristicMinDistanceToAnyObjective(current_state, objectives):
    """
    This is a simple Manhattan Distance heuristic
    We return the minimum manhattan distance to the nearest goal
    :param current_state:
    :param objectives:
    :return: heuritic value
    """
    min_heuristic = sys.maxsize
    for each_objective in objectives:
        manhattan_objective = abs(current_state[0] - each_objective[0]) + abs(current_state[1] - each_objective[1])
        if manhattan_objective < min_heuristic:
            min_heuristic = manhattan_objective
    return min_heuristic

def getWeightedAstarHeuristicMinDistanceToAnyObjective(current_state, objectives):
    """
       This is a wighted Manhattan Distance heuristic
       We return the minimum manhattan distance to the nearest goal and multiply it by a constant factor
       Another implementation could have been where we vary the constant weight to see what gives the best result
       :param current_state:
       :param objectives:
       :return: heuritic value
       """
    min_heuristic = sys.maxsize
    for each_objective in objectives:
        manhattan_objective = abs(current_state[0] - each_objective[0]) + abs(current_state[1] - each_objective[1])
        if manhattan_objective < min_heuristic:
            min_heuristic = manhattan_objective
    if len(objectives) > 2:
        return 2 * min_heuristic
    else:
        return min_heuristic


def getAstarHeuristicSumOfAllGoals(current_state, objectives):
    """
       This is the sum of all manhattan distance from current to all goal state
       This would not be admissible as it overestimates the cost to traverse all goals
       :param current_state:
       :param objectives:
       :return: heuritic value
       """
    sum_heuristic = 0
    for each_objective in objectives:
        sum_heuristic += abs(current_state[0] - each_objective[0]) + abs(current_state[1] - each_objective[1])
    return sum_heuristic


def getAstarHeuristicSumOfMinimumConnectedGoals(current_state, objectives):
    """
    Here we find the manhattan distance to the nearest goal, and then we sum it recursively with
    the path costs from that goal to the next nearest goal
    :param current_state:
    :param objectives:
    :return: value
    """
    if not objectives:
        return 0
    min_heuristic = sys.maxsize
    for each_objective in objectives:
        manhattan_objective = abs(current_state[0] - each_objective[0]) + abs(current_state[1] - each_objective[1])
        if manhattan_objective < min_heuristic:
            min_heuristic = manhattan_objective
            min_objective = each_objective
    new_objectives = objectives.remove(min_objective)
    return min_heuristic + getAstarHeuristicSumOfMinimumConnectedGoals(min_objective, new_objectives)


def getAstarHeuristicSumOfMinimumConnectedGoalsPreComputed(current_state, objectives):
    """
        This is used in association with the next method (aggregatedCostFromObjectiveToAllOthers)
        The logic is that we precompute the manhattan distance from a each objective to every other objective
        Then we calculate the heuristic value as
        h(x) = cost from current to nearest goal, dijkstra cost from that to all other goals
        This was our most promising effort, but sadly we are getting a suboptimal result with this heuristic
        :param current_state:
        :param objectives:
        :return: heuristic value
        """
    min_heuristic = sys.maxsize
    for each_objective in objectives:
        manhattan_objective = abs(current_state[0] - each_objective[0]) + abs(current_state[1] - each_objective[1])
        if manhattan_objective < min_heuristic:
            min_heuristic = manhattan_objective
            min_objective = each_objective
    return min_heuristic + aggregatedCostFromObjectiveToAllOthers(min_objective, objectives)


def aggregatedCostFromObjectiveToAllOthers(current, objectives):
    """
    Calculates the Dijkstra single source all paths distance between each goal state
    We make use of the pre computed distance matrix
    :param current:
    :param objectives:
    :return:
    """
    dijkstraMap = {}
    for each_objective in objectives:
        dijkstraMap[each_objective] = sys.maxsize
    dijkstraMap[current] = 0
    new_objectives = objectives[:]
    while new_objectives:
        current_vertex = min(new_objectives, key=lambda objective: dijkstraMap[objective])
        if dijkstraMap[current_vertex] == sys.maxsize:
            break
        for neighbour, cost in dijkstraMap.items():
            if neighbour == current_vertex:
                continue
            alternative_route = dijkstraMap[current_vertex] + distanceMap[current_vertex, neighbour]
            if alternative_route < dijkstraMap[neighbour]:
                dijkstraMap[neighbour] = alternative_route
        new_objectives.remove(current_vertex)
    sum_distances = 0
    for distances in dijkstraMap.values():
        sum_distances += distances
    return sum_distances


def backtrace(parent_map, start, end):
    """
    This method is a utility function.
    It helps us trace the solution path from start to goal.
    :param parent_map:
    :param start:
    :param end:
    :return: list of path from start to end
    """
    path = [end]
    while path[-1] != start:
        path.append(parent_map[path[-1]])
    path.reverse()
    return path
