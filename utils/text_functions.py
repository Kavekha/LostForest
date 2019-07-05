def get_biggest_line_len(text):
    if type(text) == str:
        lines = text.split('\n')
    else:
        lines = text
    biggest_len = 0
    for line in lines:
        if len(line) > biggest_len:
            biggest_len = len(line)
    return biggest_len