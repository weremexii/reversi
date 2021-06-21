import numpy as np
from mcts import MCTS, TreeNode, MCTSPlayer, random_rollout_policy
def weight_rollout_policy(board):
    weight_matrix = np.array([[100,-25, 20, 10 ,10 ,20,-25,100],
                                [-25, -60,  -3,  1, 1, -3, -60,  -25],
                                [20,  -3, 3, 1, 1,  3,  -3,  20],
                                [10,  1, 1, 1, 1,  1,  1,  10],
                                [10,  1, 1, 1,  1, 1, 1,  10],
                                [20,  -3,  3,  1, 1, 3,  -3,  20],
                                [-25, -60, -3, 1,  1,  -3,-60,  -25],
                                [100,  -25, 20, 10, 10, 20, -25, 100]])
    weight_matrix = weight_matrix/(weight_matrix.max()-weight_matrix.min())
    probs = []
    if len(board.action.keys()) == 0:
        pass
    else:
        for str_action in board.action.keys():
            weight = weight_matrix[eval(str_action)]
            probs.append(weight)
    return list(zip(board.action.keys(), probs))

class MCTS_Change(MCTS):
    def playout(self, copied_board):
        if len(copied_board.history) <= 20:
            self._rollout_policy = random_rollout_policy
            self._c_puct = 5
        elif 20 < len(copied_board.history) and len(copied_board.history) <= 55:
            self._root = TreeNode(None, 1.0)
            self._rollout_policy = weight_rollout_policy
            self._c_puct = 1
        else:
            self._root = TreeNode(None, 1.0)
            self._rollout_policy = random_rollout_policy
            self._c_puct = 1
        super().playout(copied_board)

class MCTS_Change_Player(MCTSPlayer):
    def __init__(self, c_puct=5, n_playout=100):
        self.mcts = MCTS_Change(random_rollout_policy, n_playout, c_puct)

class MCTS_Value_Player_2(object):
    def __init__(self, c_puct=5, n_playout=100):
        self.mcts = MCTS(weight_rollout_policy, c_puct, n_playout)

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