from copy import deepcopy
class Fake_mcts_node:
    def __init__(self, board, depth: int, max_d: int, player: int) -> None:
        self.node = {}
        self.board = board
        self.player = player
        if depth == max_d:
            pass
        else:
            board.next_stage()
            for action in board.action.keys():
                node_board = deepcopy(board)
                node_board.displayer = None
                node_board.do_action(action)
                self.node[action] = Fake_mcts_node(node_board, depth+1, max_d, player)
    def r(self):
        score = 0
        score += self.board.rate[self.player]
        if len(self.node.keys()) != 0:   
            for v in self.node.values():
                score += v.r()
        return score

class Fake_mcts_root:
    def __init__(self, board, player: int, depth) -> None:
        board.displayer = None
        self.board = board
        self.player = player
        self.node = {}
        for action in board.action.keys():
            node_board = deepcopy(board)
            node_board.displayer = None
            node_board.do_action(action)
            self.node[action] = Fake_mcts_node(node_board, 0, depth, self.player)
    def result(self):
        node_result = {}
        for k, v in self.node.items():
            node_result[k] = v.r()
        node_result = list(sorted(node_result.items(), key=lambda item: item[1]))
        return node_result[-1][0]

class Fake_mcts_player:
    def __init__(self, depth) -> None:
        self.depth = depth
    def do_action(self, board):
        available_action = list(board.action.keys())
        if len(available_action) != 0:
            # need to do actual action, don't need copy the board.
            tree = Fake_mcts_root(deepcopy(board), board.player, self.depth)
            select = tree.result()
            return board.do_action(select)