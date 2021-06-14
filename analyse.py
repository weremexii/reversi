from reversi import Board
from mcts import MCTSPlayer
total = 10
black_win = 0
white_win = 0
for _ in range(total):
    #board = Board(displayer=Displayer())
    board = Board()
    computer_2 = MCTSPlayer(c_puct=10, n_playout=100)
    computer_1 = MCTSPlayer(n_playout=100)
    player = {board.black: computer_1.do_action, board.white: computer_2.do_action}
    # Game
    status = False
    winner = None
    player[board.player](board)
    while(not status):
        status, winner = board.end()
        if not status:
            player[board.player](board)
    if winner == board.black:
        black_win += 1
    elif winner == board.white:
        white_win += 1
    print(board.name[winner])