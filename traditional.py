class Greedy_Player:
    def do_action(self, board):
        available_action = list(board.action.keys())
        if len(available_action) != 0:
            action_len_sort = sorted(range(len(available_action)), key=lambda i: len(board.action[available_action[i]]))
            select = available_action[action_len_sort[-1]]
        
            return board.do_action(select)