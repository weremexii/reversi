from os import stat
import numpy as np
from numpy.lib.function_base import select

class Board:
    def __init__(self) -> None:
        self.empty = 0
        self.black = 1
        self.white = 2
        self.avail = 3 # a status won't be stored
        self.name = {self.white: 'white', self.black: 'black', self.empty: 'empty', self.avail: 'avail'}
        self.piece = dict([(self.empty, " "), (self.black, "●"), (self.white, "○"), (self.avail, "+")])
        self.board = np.array([
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 1, 2, 0, 0, 0],
       [0, 0, 0, 2, 1, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0]])
        self.player = 1
        self.action = {}
        self._history = []

        # record
        self._record()
        self._success()

    def _record(self, add_piece=None):
        # Pay attention to mutable objects
        self._history.append(dict(player=self.player, 
        action=self.action.copy(), 
        add_piece=add_piece,
        board=self.board.copy()))

    def _position_generator(self, start_p: tuple, direction: tuple) -> list:
        x, y = start_p
        dx, dy = direction
        board = self.board
        r = []
        r.append(((x, y), board[x][y]))
        status = True
        while(status):
            try:
                x, y = x+dx, y+dy
                if x < 0 or y < 0:
                    raise Exception
                temp = board[x][y]
                r.append(((x, y), temp))
            except Exception:
                status = False
        return r
    
    def _available_action(self, line: list, player: int) -> list:
        '''Return a list contains origin_actions
        line: a list of 2-tuples containing positions and piece
        '''
        pieces = ''.join((map(lambda item: str(item[1]), line)))
        pattern = r'12+0' if player == 1 else r'21+0'
        r = []
        import re
        search_r = re.search(pattern, pieces)
        while(search_r):
            # append position
            start = search_r.span()[0]
            end = search_r.span()[1]-1
            # action is a dict containing 'action': tuple and 'reversi': list of tuples
            action = line[end][0]
            reversi = [ line[i][0] for i in range(start+1, end)]
            r.append(dict(action=action, reversi=reversi))
            # slice for two sequences
            pieces = pieces[search_r.span()[1]:]
            line = line[search_r.span()[1]:]
            # re-search
            search_r = re.search(pattern, pieces)
        return r
    
    def _success(self):
        "Decide who wins and modify the current pieces rate"
        self.rate = {self.black: 0, self.white: 0}
        rate = self.rate
        board = self.board
        for x in range(8):
            for y in range(8):
                if board[x][y] != self.empty:
                    rate[board[x][y]] += 1
        
        if rate[self.black] + rate[self.white] == 64:
            if rate[self.black] == rate[self.white]:
                self.display(mode='info', message=['Both you win and both you lose.'])
                return None
            else:
                winner = self.black if rate[self.black] > rate[self.white] else self.white
                self.display(mode='info', message=['Winner is {}'.format(self.name[winner])])
                return True
        else:
            return False

    def next_stage(self):
        player = self.player
        origin_action = []
        board = self.board
        # for xie
        for i in range(15):
            x, y = (0 if i <= 7 else i - 7, 7-i if i <=7 else 0) #03
            origin_action.extend(self._available_action(self._position_generator((x, y), (1, 1)), player))
        for i in range(15):
            x, y = (i if i <= 7 else 7, 7 if i <=7 else 14-i) #30
            origin_action.extend(self._available_action(self._position_generator((x, y), (-1, -1)), player))
        for i in range(15):
            x, y = (0 if i <= 7 else i - 7, i if i <=7 else 7) #12
            origin_action.extend(self._available_action(self._position_generator((x, y), (1, -1)), player))
        for i in range(15):
            x, y = (i if i <= 7 else 7, 0 if i <=7 else i-7) #21
            origin_action.extend(self._available_action(self._position_generator((x, y), (-1, 1)), player))

        # for zheng
        for i in range(8):
            origin_action.extend(self._available_action([((i, j), board[(i, j)]) for j in range(8)], player))
        for i in range(8):
            origin_action.extend(self._available_action([((i, j), board[(i, j)]) for j in reversed(range(8))], player))
        for i in range(8):
            origin_action.extend(self._available_action([((j, i), board[(j, i)]) for j in range(8)], player))
        for i in range(8):
            origin_action.extend(self._available_action([((j, i), board[(j, i)]) for j in reversed(range(8))], player))

        self.display(mode='info', message=['现在是{}'.format(self.piece[self.player]), '当前比分：黑{}:{}白'.format(self.rate[self.black], self.rate[self.white])])

        # make a decision about next player
        if len(origin_action) == 0:
            # change player
            player = 1 if player == 2 else 2
            self.display(mode='info', message=[r'No available action, pass to', self.name[player]])
            self.player = player

            
            return self.player

        else:
            # wash actions
            # str_position: set of reversi positions
            d_action = {}
            for d in origin_action:
                action = d['action']
                action = str(action)
                reversi = d['reversi']
                if d_action.get(action):
                    d_action[action].update(reversi)
                else:
                    d_action[action] = set(reversi)
            
            self.action = d_action
            #self.display(mode='action')
            return self.player

    def do_action(self, str_action: str=None):
        # Input
        if not str_action:
            str_action = '({}, {})'.format(*(input().split()))
            # to do: kill list
            while(str_action not in self.action.keys()):
                self.display(mode='info', message=['Invalid action'])
                str_action = '({}, {})'.format(*(input().split()))
        
        # for change
        player = self.player
        board = self.board
        reversi = self.action[str_action]
        # reversi
        for position in reversi:
            x, y = position
            board[x][y] = player
        # put piece
        x, y = eval(str_action)
        board[x][y] = player
        self._record(add_piece=(x, y))
        
        status = self._success()
        if status:
            return 64
        elif status == None:
            return 32
        elif status == False:
            # for next stage
            self.player = 1 if player == 2 else 2
            return 0
    
    def display(self, mode='board', message=[]):
        ''' 'board', 'info', 'action' '''
        if mode == 'board':
            #empty_unit = self.piece[0]
            #balck_unit = self.piece[1]
            #white_unit = self.piece[2]
            board = self.board.copy()
            keys  = list(self.action.keys())
            for action in self.action.keys():
                action = eval(action)
                x, y = action
                board[x][y] = 3
            # abcdef
            print("--" * 9)
            row_str = "{:<2}" * 8
            print("  " + row_str.format(*list(range(8))))
            for i in range(8):
                board_row = []
                for j in range(8):
                    board_row.append(self.piece[board[i][j]])
                row_str = "{:<2d}".format(i) + " ".join(board_row)
                print(row_str)
            print("--" * 9)

        if mode == 'info':
            for m in message:
                print(m)
        if mode == 'action':
            print('Available Actions are')
            print(','.join(self.action.keys()))

class Numb_Player:
    def __init__(self, player: int) -> None:
        self.standfor = player
    def do_action(self, board: Board):
        available_action = list(board.action.keys())
        select = available_action[0]
        for str_action in available_action:
            if len(board.action[str_action]) > len(board.action[select]):
                select = str_action
        board.do_action(select)

if __name__ == '__main__':
    def do(board: Board):
        board.do_action()
    board = Board()
    computer = Numb_Player(2)
    player = {board.black: do, board.white: computer.do_action}
    status = False
    while(not status):
        player[board.next_stage()](board)
        board.display()
        
