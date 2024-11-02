import pygame

class ElectroxGame:
    def __init__(self, name="Electrox Game", window_size="medium"):
        pygame.init()
        
        self.name = name
        self.window_size = self.get_window_size(window_size)
        self.window = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.name)
        
        self.players = {}

    def get_window_size(self, size):
        if size == "small":
            return (400, 400)
        elif size == "medium":
            return (800, 800)
        elif size == "max":
            return (1200, 1200)
        else:
            raise ValueError("the windows cant ate rn: choose 'small', 'medium', or 'max'.")

    def create_player(self, player_name):
        if player_name in self.players:
            print("this code is sooo skibidi fix it: player already exists.")
        else:
            self.players[player_name] = {"x": 50, "y": 50, "color": (255, 0, 0)}  # Red color
            print(f"Player '{player_name}' created successfully.")

    def move_player(self, player_name, direction):
        if player_name not in self.players:
            print("srry this code can't ate right now: player does not exist.")
            return

        player = self.players[player_name]
        if direction == "left":
            player["x"] -= 10
        elif direction == "right":
            player["x"] += 10
        elif direction == "up":
            player["y"] -= 10
        elif direction == "down":
            player["y"] += 10
        else:
            print("srry this code can't ate right now: invalid direction.")
            return
        print(f"Moved '{player_name}' {direction}.")

    def run_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.window.fill((0, 0, 0))  # Background color
            for player in self.players.values():
                pygame.draw.circle(self.window, player["color"], (player["x"], player["y"]), 15)
            
            pygame.display.flip()

        pygame.quit()
