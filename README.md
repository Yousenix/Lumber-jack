# 🪓 Lumber Jack

A simple terminal-based game made with Python.

The player controls `@` and tries to avoid the branches while moving through the forest. The game uses keyboard input and randomly generates the path ahead, making the game progressively challenging.

## 🎮 Features

* 🪓 Terminal-based gameplay
* ⌨️ Real-time keyboard input
* 🌲 Randomly generated branches
* 🎯 Three difficulty levels:

  * Easy
  * Normal
  * Hard
* 🏆 Score tracking
* 💾 SQLite database for storing game data
* 📊 Scores are stored together with the difficulty used for each game
* ⚙️ Saves the last selected difficulty
* 🔄 Automatically restores the last selected difficulty when the game starts
* 🎨 Colored terminal output using ANSI escape codes
* 📈 Increasing difficulty as the game continues

## 🎮 Controls

| Key       | Action                          |
| --------- | ------------------------------- |
| `←`    | Move left                       |
| `→`    | Move right                      |
| `Space` | Start / display the game        |
| `Esc`   | Quit the game                   |
| `M`     | Show the maximum recorded score |
| `D`     | Change difficulty               |

## ⚙️ Difficulty Levels

The game has three difficulty levels:

### Easy

Sets the difficulty value to `1`.

### Normal

Sets the difficulty value to `2`.

### Hard

Sets the difficulty value to `5`.

The difficulty affects the random generation of the path and therefore changes how often branches appear.

The difficulty menu accepts both English and several Persian inputs.

The selected difficulty is saved in the database and is automatically restored the next time the game starts.

## 🏆 Score System

The game keeps track of the player's score during a run.

When the game ends, the score and the difficulty used during that game are stored in a SQLite database named:

```text
lumberjack.db
```

The maximum recorded score can be displayed by pressing:

```text
M
```

If there are no recorded scores yet, the game displays a message indicating that no scores are available.

## 💾 Database

Lumber Jack uses SQLite to store game data.

The database is:

```text
lumberjack.db
```

It contains two tables:

```text
lumberjack.db
├── score
└── settings
```

### `score`

Stores the score achieved in each game together with the difficulty used for that game.

### `settings`

Stores the last selected difficulty so it can be restored when the game starts again.

## 🎨 Colors

The game uses ANSI escape codes to add colors to the terminal output.

Different colors are used for elements such as:

* Player and game information
* Branches
* The forest
* Difficulty messages
* Game-over messages

## 🛠️ Built With

* **Python**
* `msvcrt` — keyboard input
* `time` — game loop timing
* `random` — random path generation
* `sqlite3` — game data storage

All of these modules are used directly in the Python source code.

## 📁 Project Structure

```text
Lumber-jack/
├── main.py
├── README.md
├── LICENSE
├── .gitignore
├── .gitattributes
└── lumberjack.db
```

The main game logic is currently contained in `main.py`.

> `lumberjack.db` is the SQLite database used by the game.

## ▶️ Running the Game

Run the main Python file:

```bash
python main.py
```

The game displays the available controls when it starts.

## 📌 About

Lumber Jack was created as a Python practice project.

The project focuses on:

* Keyboard input
* Game loops
* Random generation
* Basic game logic
* Functions
* Global game state
* SQLite database usage
* Persistent game settings
* Terminal-based UI and colors

## 📄 License

This project is licensed under the license included in this repository.
