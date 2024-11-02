
def print_d(size):
    start = 1
    end = size + 1
    d_lines = []
    for row in range(start, end):
        line = ""
        for col in range(start, end):
            if col == start or (col == size and row != start and row != size) or (row == start or row == size) and col < size:
                line += "* "
            else:
                line += "  "
        d_lines.append(line)
    return d_lines

def print_i(size):
    start = 1
    end = size + 1
    middle = end // 2
    i_lines = []
    for i in range(start, end):
        line = ""
        for j in range(start, end):
            if i == start or i == size or j == middle:
                line += "* "
            else:
                line += "  "
        i_lines.append(line)
    return i_lines

def print_n(size):
    start = 1
    end = size + 1
    n_lines = []
    for i in range(start, end):
        line = ""
        for j in range(start, end):
            if j == start or j == size or i==j:
                line += "* "
            else:
                line += "  "
        n_lines.append(line)
    return n_lines

def print_e(size):
    start = 1
    end = size + 1
    middle = end // 2
    e_lines = []
    for i in range(start, end):
        line = ""
        for j in range(start, end):
            if i == start or i == size or i==middle or j==1:
                line += "* "
            else:
                line += "  "
        e_lines.append(line)
    return e_lines

def print_s(size):
    start = 1
    end = size + 1
    s_lines = []
    for i in range(start, end):
        line = ""
        for j in range(1, end):
            if i == 1 or i == size or i == size // 2 + 1 or (j == 1 and i < size // 2 + 1) or (j == size and i > size // 2 + 1):
                line += "* "
            else:
                line += "  "
        s_lines.append(line)
    return s_lines

def print_h(size):
    start = 1
    end = size + 1
    middle = end // 2
    h_lines = []
    for i in range(start, end):
        line = ""
        for j in range(start, end):
            if j == start or j == size or i == middle:
                line += "* "
            else:
                line += "  "
        h_lines.append(line)
    return h_lines

def print_dinesh(size):
    d_lines = print_d(size)
    i_lines = print_i(size)
    n_lines = print_n(size)
    e_lines = print_e(size)
    s_lines = print_s(size)
    h_lines = print_h(size)
    for i in range(size):
        print(d_lines[i] + "  " + i_lines[i] + "   " + n_lines[i] + "  " + e_lines[i] + "  " + s_lines[i] + "  " + h_lines[i])

print_dinesh(7)