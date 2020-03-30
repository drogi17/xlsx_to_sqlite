import os


def processbar(now_posm: int, max_pos: int):
    # os.system('clear')

    rows, columns = os.popen('stty size', 'r').read().split()
    # if notations:
    #     for notation in notations:
    #         print(notation)
    #     for _ in range(int(rows)-len(notations)-2):
    #         print('')
    # else:
    #     for _ in range(int(rows)-2):
    #         print('')
    columns = int(columns)-20
    one_p = columns/100
    pos_one_p = max_pos/100
    pos_p = now_posm / pos_one_p
    procent = round(one_p*pos_p)
    for _ in range(procent):
        print("█", end='')
    for _ in range(columns-procent):
        print(" ", end='')

    print("%s / %s" % (now_posm+1, max_pos), end='\r')