from mcts import MCTSPlayer, TreeNode
from traditional import Greedy_Player
from mcts_cache import MCTS_Cache_Player
from mcts_value import MCTS_Value_Player
from reversi import *
if __name__ == '__main__':

    def human_do(board: Board):
        return board.do_action()


    board = Board(displayer=Displayer())
    computer_2 = Greedy_Player(2)
    computer_1 = MCTSPlayer(c_puct=1, n_playout=70)
    player = {board.black: computer_1.do_action, board.white: computer_2.do_action}

    # Game
    status = False
    player[board.player](board)
    while(not status):
        status, winner = board.end()
        if not status:
            player[board.player](board)
    
    #computer_1.store()