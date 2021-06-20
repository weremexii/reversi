import numpy as np
import copy
from mcts import MCTS, TreeNode, random_rollout_policy

class TreeNode_Value(TreeNode):

    def __init__(self, parent, prob, action: str) -> None:
        super().__init__(parent, prob)
        self.action = action

    def expand(self, action_probs):
        """
        Expand tree by creating new children.
        action_priors: a list of tuples of actions and their probability
        """
        if len(action_probs) == 0:
            # a node that can't put piece
            self._children['skip'] = TreeNode_Value(self, 1.0, 'skip')
        else:
            for action, prob in action_probs:
                if action not in self._children.keys():
                    self._children[action] = TreeNode_Value(self, prob, action)

    def get_value(self, c_puct):

        weight_matrix = np.array([[100,-25, 20, 10 ,10 ,20,-25,100],
                                [-25, -60,  -3,  1, 1, -3, -60,  -25],
                                [20,  -3, 3, 1, 1,  3,  -3,  20],
                                [10,  1, 1, 1, 1,  1,  1,  10],
                                [10,  1, 1, 1,  1, 1, 1,  10],
                                [20,  -3,  3,  1, 1, 3,  -3,  20],
                                [-25, -60, -3, 1,  1,  -3,-60,  -25],
                                [100,  -25, 20, 10, 10, 20, -25, 100]])

        weight_matrix = weight_matrix/(weight_matrix.max()-weight_matrix.min())
        weight = 0
        if self.action != 'skip':
            weight = weight_matrix[eval(self.action)]
        
        self._u = (c_puct * self._P *
                   np.sqrt(self._parent._n_visits) / (1 + self._n_visits))
        return self._Q + self._u + weight

class MCTS_Value(MCTS):
    def __init__(self, rollout_value_fn, n_playout, c_puct):
        super().__init__(rollout_value_fn, n_playout=n_playout, c_puct=c_puct)
        self._root = TreeNode_Value(None, 1.0, 'skip')
        
class MCTS_Value_Player(object):
    def __init__(self, c_puct=5, n_playout=100):
        self.mcts = MCTS(random_rollout_policy, c_puct, n_playout)

    def do_action(self, board):
        if not self.mcts._root.is_leaf():
            # black begin
            if len(board.history) == 1:
                pass
            else:
                last_move = board.history[-1]['add_piece']
                self.mcts.update_with_one_move(last_move)
        #self.mcts.update_with_move(board)
        move, value = self.mcts.get_move(board)
        self.mcts.update_with_one_move(move)
        #print(move)
        board.do_action(move)
        #print(value)