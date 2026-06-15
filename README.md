# Arkanoid 🧱🏓

A classic clone of the popular game Arkanoid (Breakout) written in **Python**. The project is organized in a modular, object-oriented way and offers complete gameplay, including breaking bricks, a level system, and various power-ups.

## 🌟 Main Features

* **Retro-style Gameplay:** Control the paddle, bounce the ball, and destroy all the bricks on the screen.
* **Level System (`levels.py`):** Various maps with increasing difficulty.
* **Power-Ups (`powerup.py`):** Collect falling bonuses that modify the gameplay.
* **Lasers (`laser.py`):** Ability to shoot at bricks after acquiring the specific power-up.
* **Particle System (`particle.py`):** Satisfying visual effects when destroying elements.
* **Multiple Screens (`screens.py`):** Smooth transitions between the main menu, gameplay, and end screens (Win/Game Over).
* **Audiovisual Design:** Custom graphics (`img/`), sounds (`sounds/`), and fonts (`fonts/`).

## 📁 File Structure

```text
Arkanoid/
├── ball.py         # Ball logic, movement, and collisions
├── brick.py        # Brick objects on the map
├── helpers.py      # Helper functions and constants
├── laser.py        # Mechanics for shooting projectiles from the paddle
├── levels.py       # Configurations for individual levels
├── main.py         # Application entry point and main game loop
├── paddle.py       # Player-controlled paddle mechanics
├── particle.py     # Logic and rendering of particle effects
├── powerup.py      # Classes for bonuses falling after destroying bricks
├── screens.py      # Screen management (Menu, Game Over, etc.)
├── fonts/          # Font files (.ttf)
├── img/            # Graphical assets (.png)
└── sounds/         # Sound effects (.wav / .mp3)
```
## 🚀 Requirements and Installation
The project is written in Python and uses the Pygame library for rendering graphics and handling events.

Clone the repository:

```bash
git clone [https://github.com/Emil0ne/Arkanoid.git](https://github.com/Emil0ne/Arkanoid.git)
cd Arkanoid
```
Install the required libraries:
Assuming the project uses Pygame, run the following command in your terminal:

```bash
pip install pygame
```
Run the game:

```bash
python main.py
```
## 🎮 Controls (Default)
Left Arrow / A - Move paddle left

Right Arrow / D - Move paddle right

Space - Release the ball / Shoot (when the laser power-up is active)

ESC - Exit to menu / Close game

## 👤 Author
Emil0ne
