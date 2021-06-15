from reversi import Board, Displayer
from mcts import MCTSPlayer
from multiprocessing import Pool
import traceback
def game(display: bool):
    if display:
        board = Board(displayer=Displayer())
    else:
        board = Board()
    computer_2 = MCTSPlayer(c_puct=10, n_playout=5)
    computer_1 = MCTSPlayer(n_playout=5)
    player = {board.black: computer_1.do_action, board.white: computer_2.do_action}
    # Game
    status = False
    winner = None
    player[board.player](board)
    try:
        while(not status):
            status, winner = board.end()
            if not status:
                player[board.player](board)
        return winner
    except:
        error=traceback.format_exc()
        print(error)
        raise Exception(error)

if '__main__' == __name__:
    pool = Pool()
    r = pool.map(game, [True, False, False, False, False, False, False, False])
    print(r)