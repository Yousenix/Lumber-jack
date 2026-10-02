import msvcrt
import time
import random as r
import sqlite3 as sql

q = False
Game_running = False

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

cur.execute("""
CREATE TABLE IF NOT EXISTS statistics(
    total INT,
    easy INT,
    normal INT,
    hard INT
)
""")

cur.execute("SELECT * FROM statistics LIMIT 1")
saved_statistics = cur.fetchone()

if saved_statistics is None:
    cur.execute(
        "INSERT INTO statistics VALUES (?, ?, ?, ?)",
        (0, 0, 0, 0)
    )
    con.commit()

    saved_total = 0
    saved_easy = 0
    saved_normal = 0
    saved_hard = 0

else:
    saved_total = saved_statistics[0]
    saved_easy = saved_statistics[1]
    saved_normal = saved_statistics[2]
    saved_hard = saved_statistics[3]


cur.execute("SELECT difficulty FROM settings LIMIT 1")
saved_difficulty = cur.fetchone()

if saved_difficulty is None:
    difficulty_name = "Normal"
    cur.execute("INSERT INTO settings VALUES (?)", (difficulty_name,))
    con.commit()
    difficulty_int = 2

else:
    difficulty_name = saved_difficulty[0]

    if difficulty_name == "Easy":
        difficulty_int = 1
    elif difficulty_name == "Normal":
        difficulty_int = 2
    elif difficulty_name == "Hard":
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

def get_max_score():
    cur.execute("SELECT MAX(score) FROM score")
    return cur.fetchone()[0]

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
    global saved_normal , saved_hard , saved_easy , saved_total , Game_running

    Game_running = False
    
    if score != 0 :
        print(f"""\n{RED('GAME OVER!')}\nyour score: {BLUE(score)}
            

            """)

        cur.execute(
            "INSERT INTO score VALUES (?, ?)",
            (score, difficulty_name)
        )

        saved_total += 1

        if difficulty_name == "Easy":
            saved_easy += 1

        elif difficulty_name == "Normal":
            saved_normal += 1

        elif difficulty_name == "Hard":
            saved_hard += 1

        cur.execute(
            "UPDATE statistics SET total = ?, easy = ?, normal = ?, hard = ?",
            (saved_total, saved_easy, saved_normal, saved_hard)
        )

        con.commit()


def history():
    cur.execute("SELECT score, difficulty FROM score")
    history_data = cur.fetchall()

    if not history_data:
        print("No scores yet!")
    else:
        print("\nScore History:")
        for score_value, difficulty in history_data:
            print(f"Score: {score_value} | Difficulty: {difficulty}")

def Average():
    cur.execute("SELECT AVG(score) FROM score")
    average = cur.fetchone()[0]

    if average is None:
        return 0

    return average

def Statistics():
    highest = get_max_score()

    if highest is None:
        highest = "No scores yet!"

    print(f"""
========== {PURPLE('STATISTICS')} ==========

Total Games: {YELLOW(saved_total)}
Highest Score: {YELLOW(highest)}
Average Score: {YELLOW(f"{Average():.2f}")}

Easy Games: {YELLOW(saved_easy)}
Normal Games: {YELLOW(saved_normal)}
Hard Games: {YELLOW(saved_hard)}
""")

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


def reset_game():
    global game, score, FreeL, FreeR

    score = 0
    FreeL = 0
    FreeR = 0

    game = [
        [" ", f"{BROWN('|')}", " "],
        [" ", f"{BROWN('|')}", " "],
        [" ", f"{BROWN('|')}", f"{GREEN('-')}"],
        [" ", f"{BROWN('|')}", f"{GREEN('-')}"],
        [" ", f"{BROWN('|')}", " "],
        [" ", f"{BROWN('|')}", " "],
        [f"{GREEN('-')}", f"{BROWN('|')}", " "],
        [" ", f"{BROWN('|')}", " "],
        [" ", f"{BROWN('|')}", " "],
        [" ", f"{BROWN('|')}", "@"],
    ]


def Game():
    global Game_running , q

    Game_running = True
    
    print(f"start: press {YELLOW("Space")}\nquit: press {YELLOW("Esc")}\nMove: {YELLOW(" arrow buttons (left & right)")}\nStatistics: press {YELLOW("s")}\nDifficulty level : press {YELLOW("d")}\nHistory : press {YELLOW("h")}")

    # --- main loop and logic ---

    while True:

        if msvcrt.kbhit():

            key = msvcrt.getch()

            if key == b'd':
                defficulty_()

            elif key == b'h':
                history()

            elif key == b's':
                Statistics()
            
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
                q = True
                break

        time.sleep(0.01)

Game()

while Game_running == False and q == False:
    reset_game()
    Game()