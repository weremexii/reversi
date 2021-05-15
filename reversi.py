from itertools import accumulate
from re import search
import numpy as np

class Board:
    def __init__(self) -> None:
        # init
        # 0 stands for empty, 1 for black and 2 for white
        board = np.zeros((8, 8), dtype='int_')
        board[2][3] = 1
        #board[3:5, 3:5] = [[2, 1], [1, 2]]
        board[3:5, 3:5] = [[1, 1], [2, 2]]
        board[4][2] = 2

        # for history, its a 3-tuple containing the player, position and the resulting board
        self._history = []
        self._history.append([None, None, board.copy()])
        
        # for actions, update after call next_stage()
        self._actions = None
        # for style
        self.pieces = ("+", "●", "○")
    
    def _position(self, start_position: tuple, direction: tuple) -> list:
        '''Generate a line-like list
        '''
        x, y = start_position
        dx, dy = direction
        board = self._history[-1][2]
        r = []
        r.append(((x, y), board[x][y]))
        status = True
        while(status):
            try:
                x, y = x+dx, y+dy
                temp = board[x][y]
                r.append(((x, y), temp))
            except Exception:
                status = False
        return r

    def _action(self, line: list, player: int) -> list:
        '''Return a list containing positions of actionable
        line: a list of 2-tuples containing positions and piece
        '''
        pieces = ''.join((map(lambda item: str(item[1]), line)))
        pattern = r'12+0' if player == 1 else r'21+0'
        r = []
        import re
        search_r = re.search(pattern, pieces)
        while(search_r):
            # append position
            r.append(line[search_r.span()[1]-1][0])
            # slice for two sequences
            pieces = pieces[search_r.span()[1]:]
            line = line[search_r.span()[1]:]
            # re-search
            search_r = re.search(pattern, pieces)
        return r
    def _winner(self) -> int:
        ''' 0 for not end, 1 for black and 2 for white'''

    def do_action(self, action: tuple) -> bool:
        '''
        action is a tuple stands for position
        '''
        if action in self._action:
            
            return True
        else:
            self.display('info', 'Invalid')
            return False

    def next_stage(self, select_player=None) -> tuple:
        '''Return a 3-tuple containing which player can perform next action, the available action(a list of positons) and the current board'''
        pre_board_status = self._history[-1]
        pre_board = self._history[-1][2]
        player = 1 if (pre_board_status[0] == 2 or pre_board_status[0] == None) else 2
        if not select_player:
            player = select_player
        actions = []
        # for xie
        for i in range(15):
            x, y = (0 if i <= 7 else i - 7, 7-i if i <=7 else 0) #03
            actions.extend(self._action(self._position((x, y), (1, 1)), player))
        for i in range(15):
            x, y = (i if i <= 7 else 7, 7 if i <=7 else 14-i) #30
            actions.extend(self._action(self._position((x, y), (-1, -1)), player))
        for i in range(15):
            x, y = (0 if i <= 7 else i - 7, i if i <=7 else 7) #12
            actions.extend(self._action(self._position((x, y), (1, -1)), player))
        for i in range(15):
            x, y = (i if i <= 7 else 7, 0 if i <=7 else i-7) #21
            actions.extend(self._action(self._position((x, y), (-1, 1)), player))

        # for zheng
        actions.extend(self._action([((i, j), pre_board[(i, j)]) for i in range(8) for j in range(8)], player)) #right
        actions.extend(self._action([((i, j), pre_board[(i, j)]) for i in range(8) for j in reversed(range(8))], player)) #left
        actions.extend(self._action([((j, i), pre_board[(j, i)]) for i in range(8) for j in range(8)], player)) #down
        actions.extend(self._action([((j, i), pre_board[(j, i)]) for i in range(8) for j in reversed(range(8))], player))

        # no actions update player and call self with selected player
        if len(actions) == 0:
            player = 1 if player == 2 else 2
            self.display('info', 'No available action, pass.')
            return self.next_stage(select_player=player)
        else:
            # delete repeated actions and sort
            actions = list(set(actions))
            actions.sort()
            self._action = actions
            self._player = player
            self.display('info', 'available actions: ', actions)
            return player, actions, pre_board

    def display(self, mode='board', *message):
        ''' 'board', 'info' '''
        if mode == 'board':
            #empty_unit = self.piece[0]
            #balck_unit = self.piece[1]
            #white_unit = self.piece[2]
            board = self._history[-1][2]
            # abcdef
            print("--" * 9)
            row_str = "{:<2}" * 8
            print("  " + row_str.format(*list(range(8))))
            for i in range(8):
                board_row = []
                for j in range(8):
                    board_row.append(self.pieces[board[i][j]])
                row_str = "{:<2d}".format(i) + " ".join(board_row)
                print(row_str)
            print("--" * 9)

        if mode == 'info':
            print(message)

if __name__ == '__main__':
    board = Board()
    board.display()
    board.next_stage()
    board.do_action(tuple(input().split()))
