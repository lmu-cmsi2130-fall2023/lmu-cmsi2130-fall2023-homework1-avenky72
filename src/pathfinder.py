'''
CMSI 2130 - Homework 1
Author: Atul

Modify only this file as part of your submission, as it will contain all of the logic
necessary for implementing the A* pathfinder that solves the target practice problem.
'''
import queue
from maze_problem import MazeProblem
from dataclasses import *
from typing import *

@dataclass
class SearchTreeNode:
    """
    SearchTreeNodes contain the following attributes to be used in generation of
    the Search tree:

    Attributes:
        player_loc (tuple[int, int]):
            The player's location in this node.
        action (str):
            The action taken to reach this node from its parent (or empty if the root).
        parent (Optional[SearchTreeNode]):
            The parent node from which this node was generated (or None if the root).
    """
    player_loc: "tuple[int, int]"
    action: str
    parent: Optional["SearchTreeNode"]
    cost: int
    targets_left: set[tuple[int, int]]
    h_cost: int
    
    def __str__(self) -> str:  # sourcery skip: use-fstring-for-concatenation
        return "@: " + str(self.player_loc)
    # need a __hash__ and __lt___
    
    def __lt__ (self, other: "SearchTreeNode") -> bool:
        #return the bool value of whether self.cost is less than other.cost; hcost + transition.cost()
        return ((self.cost + self.h_cost) < (other.cost + other.h_cost))
 
    def __hash__(self) -> int:
        return hash((self.player_loc, frozenset(self.targets_left)))
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SearchTreeNode):
            return False
        return (self.player_loc == other.player_loc and self.targets_left == other.targets_left)
    
    
def Manhattan_Distance(node_loc: tuple[int, int], targets_left: set[tuple[int, int]]) -> int:
#create a loop or smt to go through all the targets and ind the one with the shortest distance
    min_dist = float('inf')
    for targets in targets_left:
            min_d = abs(node_loc[0] - targets[0]) + abs(node_loc[1] - targets[1])
            if min_d < min_dist:
                min_dist = min_d
    return int(min_dist) if not min_dist == float("inf") else 0
            

def return_solution(node: "SearchTreeNode") -> list["str"]:
    res: list[str] = []
    while node.parent is not None:
        res.append(node.action)
        node = node.parent;
    res.reverse()
    return res
    
    
    
    #Also need to find if targets visible to shoot
    
def pathfind(problem: MazeProblem) -> Optional["list[str]"]:
    """
    The main workhorse method of the package that performs A* graph search to find the optimal
    sequence of actions that takes the agent from its initial state and shoots all targets in
    the given MazeProblem's maze, or determines that the problem is unsolvable.

    Parameters:
        problem (MazeProblem):
            The MazeProblem object constructed on the maze that is to be solved or determined
            unsolvable by this method.

    Returns:
        Optional[list[str]]:
            A solution to the problem: a sequence of actions leading from the 
            initial state to the goal (a maze with all targets destroyed). If no such solution is
            possible, returns None.
    """

    # TODO: Implement breadth-first tree search!   
    
    #initialize Queue
    frontier: queue.PriorityQueue["SearchTreeNode"] = queue.PriorityQueue()
    
    #first/initial node
    initial = SearchTreeNode(problem.get_initial_loc(), "", None, 0, problem.get_initial_targets(), 0)


    frontier.put(initial)
    
    graveyard: set["SearchTreeNode"] = set()

    #expand next node
    while not frontier.empty():
        current = frontier.get()
        if current in graveyard:
            continue
        graveyard.add(current)
        children = problem.get_transitions(current.player_loc, current.targets_left)
        if len(current.targets_left) == 0:
            return return_solution(current)
           
        for action, transition in children.items():
            curr_targets = current.targets_left - transition["targets_hit"]
            newh_cost = Manhattan_Distance(transition["next_loc"], curr_targets)
            new_cost = current.cost + transition["cost"]
            child = SearchTreeNode(transition["next_loc"], action, current, new_cost, curr_targets, newh_cost)
            if child in graveyard:
                continue
            frontier.put(child)
           
    
    return None
