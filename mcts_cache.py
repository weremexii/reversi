from diskcache import Cache
from mcts import MCTS, random_rollout_policy
import numpy as np
import copy
#if __name__ == '__main__':
#    mcts = MCTS(rollout_policy, c_puct=5, n_playout=100)
#    cache = Cache(r'./cache')
#    for _ in range(64):
#        mcts.playout(Board())
#    cache.set('mcts', mcts, expire=None)

#if __name__ == '__main__':
#    cache = Cache(r'./cache')
#    mcts = cache.get('mcts')
#    for _ in range(64):
#        mcts.playout(Board())
#    if cache.delete('mcts'):
#        cache.set('mcts', mcts, expire=None)

class MCTS_Q(MCTS):
    def __init__(self, rollout_value_fn, n_playout, c_puct):
        super().__init__(rollout_value_fn, n_playout=n_playout, c_puct=c_puct)
        self._keep_root = copy.copy(self._root)
    
    def reset(self):
        self._root = copy.copy(self._keep_root)

    def get_move(self, board):
        for i in range(self._n_playout):
            copied_board = copy.deepcopy(board)
            self.playout(copied_board)

        action, node = sorted(self._root._children.items(),
                        key=lambda act_node: act_node[1]._Q)[-1]
        return action, node._Q
class MCTS_Cache_Player:
    def __init__(self, cache_folder, key, player) -> None:
        self.cache = Cache(cache_folder)
        mcts = self.cache.get(key)
        if mcts == None:
            mcts = MCTS_Q(random_rollout_policy, c_puct=5, n_playout=40)
        self.mcts = mcts
        self.player = player
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
    
    def store(self):
        self.mcts.reset()
        self.cache.delete('mcts')
        self.cache.set('mcts', self.mcts)
#if __name__ == '__main__':
#    cache = Cache(r'./cache')
#    mcts = cache.get('mcts')
#    if mcts == None:
#        mcts = MCTS(rollout_policy, c_puct=5, n_playout=10)
#        cache.set('mcts', mcts)
#    else:
#        for _ in range(64):
#            mcts.playout(Board())
#        cache.delete('mcts')
#    cache.set('mcts', mcts)