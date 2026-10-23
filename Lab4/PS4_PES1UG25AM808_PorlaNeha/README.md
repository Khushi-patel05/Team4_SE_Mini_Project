# Lab 4: VibeCoding — Rock Paper Scissors

## 1. Project Overview

This project is an interactive Rock Paper Scissors game developed using Python and Pygame. The objective of this lab is to understand an existing codebase, fix bugs, implement additional features, test the application, and document the AI-assisted development process.

## 2. Objectives

- Understand the existing project structure and source code.
- Fix the inverted winner evaluation bug.
- Implement a First-to-X Wins match victory system.
- Implement adaptive AI using player move patterns.
- Add procedural gesture icons and a reveal animation.
- Test the application after modifications.
- Maintain separate Git commits for individual tasks.
- Document the AI-assisted development process.

## 3. Technologies Used

- **Programming Language:** Python
- **Game Library:** Pygame
- **Version Control:** Git and GitHub
- **AI Coding Assistant:** ChatGPT

## 4. Project Tasks

### Task 1: Fix Winner Evaluation

Correct the winner evaluation logic according to standard Rock Paper Scissors rules:

- Rock beats Scissors.
- Scissors beats Paper.
- Paper beats Rock.
- Identical choices result in a draw.

### Task 2: First-to-X Wins Match Victory

Implement a configurable match victory system in which the first player to reach the specified number of wins is declared the match winner.

### Task 3: Adaptive AI

Implement an adaptive computer opponent that tracks the player's previous moves and uses observed patterns to influence its future choices.

### Task 4: Procedural Gesture Icons and Reveal Animation

Add procedurally generated gesture icons and a reveal animation to improve the game's visual presentation.

## 5. Repository Structure

The project is organized as follows:

```text
PS4_PES1UG25AM808_PorlaNeha/
│
├── game/
│   ├── button.py
│   └── game_engine.py
│
├── videos/
│   ├── before.mp4
│   └── after.mp4
│
├── Chat_history.pdf
├── README.md
└── main.py
```

## 6. Installation and Execution

### Prerequisites

- Python 3 installed on the system.
- Pygame installed.
- Git installed for version control.

### Install Pygame

```bash
pip install pygame
```

### Run the Application

Open a terminal in the project directory and execute:

```bash
python main.py
```

Use the on-screen Rock, Paper, and Scissors buttons to play the game and verify the results.

## 7. Testing and Validation

The application should be tested to verify the following:

- All three choices work correctly.
- Winner evaluation follows standard rules.
- Draws are handled correctly.
- Player and computer scores update correctly.
- The match ends when the configured winning score is reached.
- Adaptive AI uses the player's previous choices.
- Gesture icons and reveal animations function correctly.
- The application runs without unexpected errors.

## 8. Before and After Demonstration

The `videos/` directory contains the demonstration recordings:

- **before.mp4:** Demonstrates the original application before modifications.
- **after.mp4:** Demonstrates the application after modifications.

## 9. Version Control

Git and GitHub are used to track project changes. Each task should have a separate commit with a descriptive commit message.

Example commit messages:

- `Fix inverted winner evaluation`
- `Add first-to-X match victory`
- `Implement adaptive AI pattern tracking`
- `Add procedural gesture icons and reveal animation`

The completed work should be pushed to the assigned personal GitHub repository according to the lab submission guidelines.

## 10. AI Chat History

The `Chat_history.pdf` file documents the AI conversation associated with the development process, including prompts, responses, debugging guidance, and implementation discussions.

## 11. Deliverables

The submission includes:

1. Project source code.
2. Before-modification demonstration video.
3. After-modification demonstration video.
4. AI chat history in PDF format.
5. Project README documentation.

## 12. Conclusion

This lab demonstrates AI-assisted software development through code understanding, debugging, feature implementation, testing, documentation, and Git-based version control.
