
# Lab 4 — Vibe Coding

# Scenario 14 — 2048

A terminal-based implementation of the 2048 game featuring directional movement, tile merging, score tracking, undo, and game-state handling.

## Project Files

- `main.py` — Application entry point.
- `game.py` — Game loop, commands, and game state.
- `board.py` — Grid movement, tile merging, and score logic.
- `requirements.txt` — Dependency declaration.

## Setup

Python is required to run the game. No additional package installation is required for the current implementation.

```bash
python main.py
```

## Controls

| Key | Action |
|---|---|
| `W` | Move tiles up |
| `A` | Move tiles left |
| `S` | Move tiles down |
| `D` | Move tiles right |
| `U` | Undo the previous successful move |
| `Q` | Quit the game |

## Implemented Features

### Correct Tile Merging

Each original tile can participate in at most one merge during a move. Tiles are compressed in the selected direction, and newly merged tiles cannot merge again in that same move.

For example, moving `[2, 2, 2, 2]` left produces `[4, 4, 0, 0]`.

### Game-State Handling

- Detects when a tile reaches 2048.
- Detects when no legal moves remain.
- Prevents unchanged moves from creating a new tile.

### Undo and Best Score

- Supports one-level undo with the `U` key.
- Restores the previous board and score when undoing a move.
- Tracks the best score achieved during the current run.

### Move Feedback

Provides concise feedback for successful moves and merges. Invalid inputs and unchanged moves do not report a successful move.

## Testing and Verification

The merge behaviour and score calculation were checked using a four-equal-tile test. Undo, best-score tracking, invalid-input handling, and move feedback were also manually checked during development.

Further verification should cover win detection, a board with no legal moves, unchanged moves, and score restoration after undo.

## LLM Chat History

The complete ChatGPT conversation used during development is available here:

**[View the complete ChatGPT conversation](https://chatgpt.com/g/g-p-6ad4c9b6b5e4819192bae30f8967aa5e-se-lab4/project)**


## Submission Materials

The submission includes:

- A 10-second gameplay video recorded before the code changes.
- A 10-second gameplay video recorded after the code changes.
- The complete LLM chat history.
- The updated project source files.

## Project Structure

```text
scenario-14-2048/
        |__ videos/
        │   ├── before.mp4
        │   └── after.mp4
        ├── source-code/
        │   ├── board.py
        │   ├── game.py
        │   ├── main.py
        │   └── requirements.txt
        ├── Chat_History.pdf
        ├── README.md
```

## Project Repository

https://github.com/kirthana17/14_2048
