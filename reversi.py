import numpy as np
from fake_mcts import Fake_mcts_player
class Board:
    def __init__(self, config: dict=None, history: bool=True, displayer=None) -> None:
        # player init
        self.empty = 0
        self.black = 1
        self.white = 2
        self.avail = 3 # a status won't be stored
        self.name = {self.white: 'white', self.black: 'black', self.empty: 'empty', self.avail: 'avail'}
        # game init
        self.board = np.array([
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 2, 1, 0, 0, 0],
       [0, 0, 0, 1, 2, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0]])
        self.player = self.black
        self.action = {}
        self._history = None
        if history:
            self._history = []

        # gui
        self.displayer = None
        if displayer:
            self.displayer = displayer
            self.displayer.init(self)
        # empty opening
        self._no_avail = 0
        self._record()
        self.success()
        # for next stage
        self.next_stage()

    def _record(self, add_piece=None):
        # Pay attention to mutable objects
        if self._history:
            self._history.append(dict(
                player=self.player, 
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
    
    def success(self):
        '''
        Decide who wins and modify the current pieces rate.
        if some wins, return True and the player_id. player_id is None when it is a tie
        else return False and None
        '''
        self.rate = {self.black: 0, self.white: 0}
        rate = self.rate
        board = self.board
        for x in range(8):
            for y in range(8):
                if board[x][y] != self.empty:
                    rate[board[x][y]] += 1
        
        if (rate[self.black] + rate[self.white] == 64) or self._no_avail == 2:
            if rate[self.black] == rate[self.white]:
                if self.displayer:
                    self.displayer.display()
                    self.displayer.display(mode='info', message=['Both you win and both you lose.'])
                return True, None
            else:
                winner = self.black if rate[self.black] > rate[self.white] else self.white
                if self.displayer:
                    self.displayer.display()
                    self.displayer.display(mode='info', message=['Winner is {}'.format(self.name[winner]), '比分：黑{}:{}白'.format(self.rate[self.black], self.rate[self.white])])
                return True, winner
        else:
            return False, None
    
    def switch(self, displayer, history):
        '''
        For displayer, give a object(None is OK)
        For history, False for off, True for on
        '''
        self.displayer = displayer
        if not history:
            self._history = None
            

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

        # make a decision about next player
        if len(origin_action) == 0:
            if self.displayer:
                self.displayer.display(mode='info', message=['现在是{}'.format(self.displayer.piece[self.player]), '当前比分：黑{}:{}白'.format(self.rate[self.black], self.rate[self.white])])
                self.displayer.display()
                # change player
                player = 1 if player == 2 else 2
                self.displayer.display(mode='info', message=[r'No available action, pass to', self.name[player]])
            else:
                player = 1 if player == 2 else 2
            # take effect
            self.player = player
            # no available action record
            self._no_avail += 1
            # update rate
            self.success()
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
            self._no_avail = 0
            if self.displayer:
                self.displayer.display(mode='info', message=['现在是{}'.format(self.displayer.piece[self.player]), '当前比分：黑{}:{}白'.format(self.rate[self.black], self.rate[self.white])])
                self.displayer.display()
            return self.player

    def do_action(self, str_action: str=None):
        # Input
        if not str_action:
            str_action = '({}, {})'.format(*(input().split()))
            # to do: kill list
            while(str_action not in self.action.keys()):
                if self.displayer:
                    self.displayer.display(mode='info', message=['Invalid action'])
                str_action = '({}, {})'.format(*(input().split()))
        
        # fetch data
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
        # empty action for correct display of pass-situation
        self.action = {}
        
        # for next stage change player
        self.player = 1 if player == 2 else 2
        self.next_stage()

    

class Displayer:
    "A displayer which supports no parameters init and later init."
    def __init__(self, board: Board=None, config: dict=None) -> None:
        if board:
            self.init(board, config)
    
    def init(self, board: Board, config: dict=None):
        self.board_object = board
        if config:
            self.piece = dict([(board.empty, config['empty']), (board.black, config['black']), (board.white, config['white']), (board.avail, config['avail'])])
        else:
            self.piece = dict([(board.empty, " "), (board.black, "●"), (board.white, "○"), (board.avail, "+")])

    def display(self, mode='board', message=[]):
        ''' 'board', 'info', 'action' '''
        if mode == 'board':
            board = self.board_object.board.copy()
            keys  = list(self.board_object.action.keys())
            for action in keys:
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
            print(','.join(self.board_object.action.keys()))

class Numb_Player:
    def __init__(self, player: int) -> None:
        self.standfor = player
    def do_action(self, board: Board):
        available_action = list(board.action.keys())
        if len(available_action) != 0:
            action_len_sort = sorted(range(len(available_action)), key=lambda i: len(board.action[available_action[i]]))
            select = available_action[action_len_sort[-1]]
        
            return board.do_action(select)

if __name__ == '__main__':

    def human_do(board: Board):
        return board.do_action()

    board = Board(displayer=Displayer())
    computer = Numb_Player(2)
    player = {board.black: human_do, board.white: computer.do_action}

    # Game
    status = False
    player[board.player](board)
    while(not status):
        status, winner = board.success()
        if not status:
            player[board.player](board)