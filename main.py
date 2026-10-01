import msvcrt
import time
import random as r
import sqlite3 as sql



RED = lambda text: f"\033[31m{text}\033[0m"

BLUE = lambda text: f"\033[34m{text}\033[0m"

YELLOW = lambda text: f"\033[33m{text}\033[0m"

GREEN = lambda text: f"\033[32m{text}\033[0m"

BROWN = lambda text: f"\033[38;5;94m{text}\033[0m"

PURPLE = lambda text: f"\033[35m{text}\033[0m"



con = sql.connect("game_data.db")
cur = con.cursor()


cur.execute("""
CREATE TABLE IF NOT EXISTS score(
    score,
    difficulty
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS settings(
    difficulty
)
""")

con.commit()


cur.execute("SELECT difficulty FROM settings LIMIT 1")
saved_difficulty = cur.fetchone()

if saved_difficulty is None:
    cur.execute("INSERT INTO settings VALUES (?)", ("Normal",))
    con.commit()
    difficulty_int = 2
else:
    saved_difficulty = saved_difficulty[0]

    if saved_difficulty == "Easy":
        difficulty_int = 1
    elif saved_difficulty == "Normal":
        difficulty_int = 2
    elif saved_difficulty == "Hard":
        difficulty_int = 5




def defficulty_():
    global difficulty_int , difficulty_name

    while True:
        difficulty = input(f"""
{YELLOW("Select the difficulty level")}
{GREEN("Easy")}
{GREEN("Normal")}
{GREEN("Hard")}
{PURPLE("It is set to Normal by default.")}
: """)

        if difficulty in ["easy","Easy","آسون","آسان","ایزی"]:
            difficulty_int = 1
            difficulty_name = "Easy"
            break

        elif difficulty in ["normal","Normal","نرمال","معمولی"]:
            difficulty_int = 2
            difficulty_name = "Normal"
            break

        elif difficulty in ["hard","Hard","هارد","سخت"]:
            difficulty_int = 5
            difficulty_name = "Hard"
            break

        else:
            print(RED("Please select one of the options: easy, normal, or hard."))

    cur.execute(
        "UPDATE settings SET difficulty = ?",
        (difficulty_name,)
    )
    con.commit()

score = 0 
FreeR = 0
FreeL = 0

def max_score():
    res = cur.execute("SELECT MAX(score) FROM score")
    max_score = res.fetchone()[0]

    if max_score is None:
        print("No scores yet!")
    else:
        print("Your max score is", GREEN(max_score))

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


def game_over():
    print(f"\n{RED('GAME OVER!')}\nyour score: {BLUE(score)}")

    cur.execute(
        "INSERT INTO score VALUES (?, ?)",
        (score, difficulty_name)
    )

    con.commit()

def nextline():
    global score
    global FreeR
    global FreeL

    C = r.randint(0, difficulty_int)
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

def Game():
    print(f"start: press {YELLOW("Space")}\nquit: press {YELLOW("Esc")}\nMove: {YELLOW(" arrow buttons (left & right)")}\nmax score: press {YELLOW("m")}\nDifficulty level : press {YELLOW("d")}")

    # --- main loop and logic ---

    while True:

        if msvcrt.kbhit():

            key = msvcrt.getch()

            if key == b"m":
                max_score()
                break

            elif key == b'd':
                defficulty_()
            
            if key == b'\xe0':
                key = msvcrt.getch()
                    
                # LEFT
                if key == b'K':
                    if game[9][0] == " ":
                        game[9][0] = "@"
                        game[9][2] = " "
                    elif game[9][0] == f"{GREEN("-")}":
                        game_over()
                        break

                # RIGHT
                elif key == b'M':
                    if game[9][2] == " ":
                        game[9][2] = "@"
                        game[9][0] = " "
                    elif game[9][2] == f"{GREEN("-")}":
                        game_over()
                        break

                result = move()

                if result == False:
                    game_over()
                    break

                if "@" not in game[9]:
                    game_over()
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
                game_over()
                break

        time.sleep(0.01)

Game()