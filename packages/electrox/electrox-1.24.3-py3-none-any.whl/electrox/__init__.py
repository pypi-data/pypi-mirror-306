import pygame
from electrox import ElectroxGame  # Assuming your ElectroxGame class is in electrox.py

def main():
    """
    Starts and runs the Electrox game.
    """
    # Initialize Pygame
    pygame.init()

    # Create an instance of ElectroxGame
    game = ElectroxGame()

    # Run the game loop
    game.run_game()

if __name__ == "__main__":
    main()