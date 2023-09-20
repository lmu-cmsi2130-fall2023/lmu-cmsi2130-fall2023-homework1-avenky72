'''
CMSI 2130 - Homework 1
Author: <PLACE NAME HERE>

Modify only this file as part of your submission, as it will contain all of the logic
necessary for implementing the A* pathfinder that solves the target practice problem.
'''
from queue import Queue
from maze_problem import *
from dataclasses import *

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
    
    def __str__(self) -> str:  # sourcery skip: use-fstring-for-concatenation
        return "@: " + str(self.player_loc)
    
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

    frontier : Queue[SearchTreeNode] = Queue()
    
    #first/initial node
    initial = SearchTreeNode(player_loc = problem.get_initial_loc(), action = "", parent = None)

    frontier.put(initial)
    
    #expand next node
    while not frontier.empty():
        
        current: "SearchTreeNode" = frontier.get()

        children = problem.get_transitions(current.player_loc)
        
        for action, next_loc in children.items():
            child = SearchTreeNode(player_loc = next_loc, action = action, parent = current)
            if child.player_loc == problem.get_goal_loc():
                res: list[str]= []
                while child.parent != None:
                    res.insert(0, child.action)
                    child = child.parent
                return res
            frontier.put(child)

        
        
    return None
            
