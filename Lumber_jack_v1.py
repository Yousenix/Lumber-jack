import msvcrt
import time
import random as r

score = 0 
FreeR = 0
FreeL = 0

game = [
    [" ", "|", " "],
    [" ", "|", " "],
    [" ", "|", "-"],
    [" ", "|", "-"],
    [" ", "|", " "],
    ["-", "|", " "],
    ["-", "|", " "],
    [" ", "|", " "],
    [" ", "|", " "],
    [" ", "|", "@"],
]

def nextline():
    global score
    global FreeR
    global FreeL

    C = r.randint(0, 5)
    score += 1

    if C == 0:
        FreeR = 0
        FreeL = 0
        return [" ", "|", " "]

    side = r.randint(0, 1)

    if FreeL > 0:
        if FreeL < 2 and side == 0:
            FreeL += 1
            return ["-", "|", " "]

        FreeL = 0
        FreeR = 0
        return [" ", "|", " "]

    if FreeR > 0:
        if FreeR < 2 and side == 1:
            FreeR += 1
            return [" ", "|", "-"]

        FreeL = 0
        FreeR = 0
        return [" ", "|", " "]

    if side == 0:
        FreeL = 1
        return ["-", "|", " "]
    else:
        FreeR = 1
        return [" ", "|", "-"]


def move():
    player_pos = game[9].index("@")
    for m in range(9, 0, -1):
        game[m] = game[m - 1].copy()

    game[0] = nextline()
    if game[9][player_pos] == "-":
        return False
    game[9][player_pos] = "@"
    
    return True


print("start : press Space\nquit : press Esc\nPlay using the directional buttons")

while True:

    if msvcrt.kbhit():

        key = msvcrt.getch()

        if key == b'\xe0':
            key = msvcrt.getch()

            # LEFT
            if key == b'K':
                if game[9][0] == " ":
                    game[9][0] = "@"
                    game[9][2] = " "
                elif game[9][0] == "-":
                    print(f"you lose \nyour score : {score}")
                    break

            # RIGHT
            elif key == b'M':
                if game[9][2] == " ":
                    game[9][2] = "@"
                    game[9][0] = " "
                elif game[9][2] == "-":
                    print(f"you lose \nyour score : {score}")
                    break

            result = move()

            if result == False:
                print(f"you lose \nyour score : {score}")
                break
                break
            if "@" not in game[9]:
                print(f"you lose \nyour score : {score}")
                break

            for _ in range(50):
                print("")
            for row in game:
                print("".join(row))

        elif key == b' ':
            for _ in range(50):
                print("")
            for row in game:
                print("".join(row))

        elif key == b'\x1b':
            break

    time.sleep(0.01)