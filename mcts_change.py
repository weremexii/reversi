from mcts import MCTS, TreeNode, MCTSPlayer, random_rollout_policy
from mcts_value_2 import weight_rollout_policy
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