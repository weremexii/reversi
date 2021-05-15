# %%
import numpy as np

board = np.arange(0, 64).reshape(8, 8)

# %%
board[(1, 1), (1, 2)]
# %%

def g_03(line: int) -> list:
    x, y = (0 if line <= 7 else line - 7, 7-line if line <=7 else 0) #03
    x, y = (0 if line <= 7 else line - 7, 7-line if line <=7 else 0) #30
    x, y = (0 if line <= 7 else line - 7, 7-line if line <=7 else 0) #
    x, y = (0 if line <= 7 else line - 7, 7-line if line <=7 else 0) #
    r = []
    r.append(((x, y), board[(x, y)]))
    status = True
    while(status):
        try:
            x, y = x+1, y+1
            temp = board[(x, y)]
            r.append(((x, y), temp))
        except Exception:
            status = False
    return r

for i in range(15):
    r = g_03(i)
    positions = list(map(lambda item: item[0], r))
    print(positions)

# %%

def action(line: list, player: int):
        pieces = ''.join((map(lambda item: str(item[1]), line)))
        pattern = r'12+0' if player == 1 else r'21+0'
        r = []
        import re
        search_r = re.search(pattern, pieces)
        while(search_r):
            r.append(line[search_r.span()[1]-1][0])
            pieces = pieces[search_r.span()[1]:]
            line = line[search_r.span()[1]:]
            search_r = re.search(pattern, pieces)
        return r

r = action([((1,1), 1),
        ((1,2), 1),
        ((1,3), 1),
        ((1,4), 2),
        ((1,5), 0),
        ((1,6), 1),
        ((1,7), 2),
        ((1,8), 0),
], 1)
print(r)
# %%
