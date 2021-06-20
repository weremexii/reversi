from mcts import MCTSPlayer
from traditional import Greedy_Player
from mcts_modify import MCTS_Change_Player, MCTS_Value_Player_2
from reversi import *
def human_do(board: Board):
    return board.do_action()
def select_computer():
    print('Please select a Computer Player')
    computer = ['Pure MCTS', 'MCTS with weight sheet', 'MCTS with changes', 'Greedy Computer']
    for i, c in enumerate(computer):
        print('[{}]: {}'.format(i, c))
    selection = eval(input())
    if selection != 3:
        playout_time = 100
        c_puct = 5
        print('Please input two parameters for MCTS:')
        print('For MCTS with changes c_puct is modified by code')
        print('Key:     playout_time, c_puct')
        print('Default: {},{}'.format(playout_time, c_puct))
        print('playout_time:')
        playout_time = int(input())
        print('c_puct:')
        c_puct = int(input())
        mcts = list((MCTSPlayer, MCTS_Value_Player_2, MCTS_Change_Player))
        target = mcts[selection](c_puct=c_puct, n_playout=playout_time)
        return target
    else:
        target = Greedy_Player()
        return target
def game_fn(display: bool, player_list: list=None):
    if display:
        board = Board(displayer=Displayer())
    else:
        board = Board(displayer=None)
    if player_list == None:
        computer_1 = MCTS_Change_Player(c_puct=5, n_playout=10)
        player = {board.black: computer_1.do_action, board.white: human_do}
    else:
        computer_1 = player_list[0]
        computer_2 = player_list[1]
    # Game
    status, winner = board.end()
    player[board.player](board)
    while(not status):
        status, winner = board.end()
        if not status:
            player[board.player](board)
    return winner

if __name__ == '__main__':
    board = Board()
    displayer = Displayer(board=board)
    board.switch(displayer, True)
    print('Your board will look like this, is it ok?[y/n]')
    for key, value in displayer.piece.items():
        print('{} stands for {}'.format(value, board.name[key]))
    selection = input()
    if selection != 'y':
        print('You can read the source code to change it!')
        exit()
    print('Which mode do you want to play?')
    mode = ['Player vs Player', 'Player vs Computer', 'Computer vs Player', 'Computer vs Computer']
    for i, m in enumerate(mode):
        print('[{}]: {}'.format(i, m))
    selection = eval(input())
    if selection == 0:
        player = {board.black: human_do, board.white: human_do}
    elif selection == 1:
        player = {board.black: human_do, board.white: select_computer().do_action}
        print(r'Please input piece like this: {row}: {col}')
    elif selection == 2:
        player = {board.black: select_computer().do_action, board.white: human_do}
        print(r'Please input piece like this: {row}: {col}')
    elif selection == 3:
        player = {board.black: select_computer().do_action, board.white: select_computer().do_action}
    print('Game Start!')
    displayer.display(mode='rate')
    displayer.display()
    status, winner = board.end()
    player[board.player](board)
    while(not status):
        status, winner = board.end()
        if not status:
            player[board.player](board)