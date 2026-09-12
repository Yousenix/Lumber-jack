import msvcrt
import time
import random as r


RED = lambda text: f"\033[31m{text}\033[0m"

BLUE = lambda text: f"\033[34m{text}\033[0m"

YELLOW = lambda text: f"\033[33m{text}\033[0m"

GREEN = lambda text: f"\033[32m{text}\033[0m"

BROWN = lambda text: f"\033[38;5;94m{text}\033[0m"

PURPLE = lambda text: f"\033[35m{text}\033[0m"

score = 0 
FreeR = 0
FreeL = 0

game = [
    [" ", f"{BROWN("|")}", " "],
    [" ", f"{BROWN("|")}", " "],
    [" ", f"{BROWN("|")}", f"{GREEN("-")}"],
    [" ", f"{BROWN("|")}", f"{GREEN("-")}"],
    [" ", f"{BROWN("|")}", " "],
    [" ", f"{BROWN("|")}", " "],
    [f"{GREEN("-")}", f"{BROWN("|")}", " "],
    [" ", f"{BROWN("|")}", " "],
    [" ", f"{BROWN("|")}", " "],
    [" ", f"{BROWN("|")}", "@"],
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
        return [" ", f"{BROWN("|")}", " "]

    side = r.randint(0, 1)

    if FreeL > 0:
        if FreeL < 2 and side == 0:
            FreeL += 1
            return [f"{GREEN("-")}", f"{BROWN("|")}", " "]

        FreeL = 0
        FreeR = 0
        return [" ", f"{BROWN("|")}", " "]

    if FreeR > 0:
        if FreeR < 2 and side == 1:
            FreeR += 1
            return [" ", f"{BROWN("|")}", f"{GREEN("-")}"]

        FreeL = 0
        FreeR = 0
        return [" ", f"{BROWN("|")}", " "]

    if side == 0:
        FreeL = 1
        return [f"{GREEN("-")}", f"{BROWN("|")}", " "]
    else:
        FreeR = 1
        return [" ", f"{BROWN("|")}",f"{GREEN("-")}"]


def move():
    player_pos = game[9].index("@")
    for m in range(9, 0, -1):
        game[m] = game[m - 1].copy()

    game[0] = nextline()
    if game[9][player_pos] == f"{GREEN("-")}":
        return False
    game[9][player_pos] = "@"
    
    return True


print(f"start: press {YELLOW("Space")}\nquit: press {YELLOW("Esc")}\nMove: arrows button (left & right)")

# --- main loop and logic ---

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
                elif game[9][0] == f"{GREEN("-")}":
                    print(f"\n{RED("GAME OVER!")}\nyour score: {BLUE(score)}")
                    break

            # RIGHT
            elif key == b'M':
                if game[9][2] == " ":
                    game[9][2] = "@"
                    game[9][0] = " "
                elif game[9][2] == f"{GREEN("-")}":
                    print(f"\n{RED("GAME OVER!")}\nyour score: {BLUE(score)}")
                    break

            result = move()

            if result == False:
                print(f"\n{RED("GAME OVER!")}\nyour score: {BLUE(score)}")
                break
                break
            if "@" not in game[9]:
                print(f"\n{RED("GAME OVER!")}\nyour score: {BLUE(score)}")
                break

            for _ in range(30):
                print("")
            for row in game:
                print("".join(row))

        elif key == b' ':
            for _ in range(50):
                print("")
            for row in game:
                print("".join(row))

        elif key == b'\x1b':
            print(f"\nGoodBye 👋\nyour score: {BLUE(score)}")
            break

    time.sleep(0.01)
    