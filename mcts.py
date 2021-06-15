import numpy as np
import copy


def rollout_policy(board):
    '''
    Return a list contain action and their random prob
    '''
    # randomly rollout
    probs = np.random.rand(len(board.action.keys()))
    return list(zip(board.action.keys(), probs))

def average_policy(board):
    '''
    Return a list contain action and an average prob
    '''
    probs = np.ones(len(board.action.keys()))/len(board.action.keys())
    return list(zip(board.action.keys(), probs))

class TreeNode(object):
    """A node in the MCTS tree. Each node keeps track of its own value Q,
    prior probability P, and its visit-count-adjusted prior score u.
    """

    def __init__(self, parent, prob) -> None:
        self._parent = parent
        self._children = {} # a map from action to TreeNode
        self._n_visits = 0
        self._Q = 0
        self._u = 0
        self._P = prob

    def expand(self, action_probs):
        """
        Expand tree by creating new children.
        action_priors: a list of tuples of actions and their probability
        """
        if len(action_probs) == 0:
            # a node that can't put piece
            self._children['skip'] = TreeNode(self, 1.0)
        else:
            for action, prob in action_probs:
                if action not in self._children.keys():
                    self._children[action] = TreeNode(self, prob)
    
    def select(self, c_puct):
        return max(self._children.items(),
                   key=lambda act_node: act_node[1].get_value(c_puct))
    
    def update(self, leaf_value):
        '''
        leaf_value is 1, -1 or 0
        '''
        # Count visit.
        self._n_visits += 1
        # Update Q, a running average of values for all visits.
        self._Q += 1.0*(leaf_value - self._Q) / self._n_visits
    
    def update_recursive(self, leaf_value):
        """Like a call to update(), but applied recursively for all ancestors.
        """
        # If it is not root, this node's parent should be updated first.
        if self._parent:
            self._parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def get_value(self, c_puct):

        self._u = (c_puct * self._P *
                   np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
        return self._Q + self._u

    def is_leaf(self):
        """Check if leaf node (i.e. no nodes below this have been expanded).
        """
        return self._children == {}

    def is_root(self):
        return self._parent is None

class MCTS(object):
    def __init__(self, policy_value_fn, c_puct=5, n_playout=10000):
        self._root = TreeNode(None, 1.0)
        self._policy = policy_value_fn
        self._c_puct = c_puct
        self._n_playout = n_playout
        self._move_history = []
    
    def _playout(self, copied_board):
        # disable displayer
        copied_board.switch(None, False)
        node = self._root
        while(True):
            if node.is_leaf():
                break
            action, node = node.select(self._c_puct)
            copied_board.do_action(action)

        # here we get a leaf
        action_probs = self._policy(copied_board)
        end, winner = copied_board.end(silent=True)
        if not end:
            node.expand(action_probs)

        # begin rollout
        leaf_value = self._rollout(copied_board)

        node.update_recursive(-leaf_value)

    def _rollout(self, board, limit=500):
        """Use the rollout policy to play until the end of the game,
        returning +1 if the current player wins, -1 if the opponent wins,
        and 0 if it is a tie.
        """
        player = board.player
        for i in range(limit):
            end, winner = board.end()
            if end:
                if winner == player:
                    return 1
                elif winner == None:
                    return 0
                else:
                    return -1
            action_probs = rollout_policy(board)
            if len(action_probs) == 0:
                action_probs = [('skip', 1.0), ]
            max_action, _ = max(action_probs, key=lambda action_prob: action_prob[1])

            board.do_action(max_action)
        else:
            print("WARNING: rollout reached move limit, please check your code")
            return 0
    
    def get_move(self, board):
        for i in range(self._n_playout):
            copied_board = copy.deepcopy(board)
            self._playout(copied_board)

        return sorted(self._root._children.items(),
                        key=lambda act_node: act_node[1]._n_visits)[-1]
    
    def update_with_move(self, board):
        if len(board.history) > 2:
            me = board.history[-2]['add_piece']
            opposite = board.history[-1]['add_piece']

            if self._root._children.get(me):
                self._root = self._root._children[me]
                if self._root._children.get(opposite):
                    self._root = self._root._children[opposite]
                    self._root._parent = None
                else:
                    print("Node lost")
                    raise Exception
            else:
                print("Node lost")
                raise Exception
    
    def update_with_one_move(self, move):
        if self._root._children.get(move):
            self._root = self._root._children[move]
        else:
            print("Node lost")
            raise Exception


        
class MCTSPlayer(object):
    def __init__(self, c_puct=5, n_playout=100):
        self.mcts = MCTS(average_policy, c_puct, n_playout)

    def do_action(self, board):
        if not self.mcts._root.is_leaf():
            last_move = board.history[-1]['add_piece']
            self.mcts.update_with_one_move(last_move)
        #self.mcts.update_with_move(board)
        move, node = self.mcts.get_move(board)
        self.mcts.update_with_one_move(move)
        #print(move)
        board.do_action(move)