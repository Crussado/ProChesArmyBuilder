import pygame
import sys

from scenes import TitleScene

class GameState():
    def __init__(self):
        self.actual_player = 1

        self.fps = 30

        self.screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
        self.width, self.height = pygame.display.get_surface().get_size()

    def font(self, size):
        return pygame.font.Font('MedievalSharp-Regular.ttf', size)

class Game():
    def __init__(self):
        # Pygame init
        pygame.init()
        pygame.mixer.init()
        self.game_state = GameState()

    def play(self):
        pygame.init()
        pygame.display.set_caption("Pro Chess Army Builder")
        clock = pygame.time.Clock()

        active_scene = TitleScene(self.game_state)

        while active_scene != None:
            # Event filtering
            filtered_events = []
            for event in pygame.event.get():
                quit_attempt = False
                if event.type == pygame.QUIT:
                    quit_attempt = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    quit_attempt = True
                if quit_attempt:
                    active_scene.terminate()
                else:
                    filtered_events.append(event)

            active_scene.check_event(filtered_events)
            active_scene.update()
            active_scene.draw(self.game_state.screen)

            active_scene = active_scene.next

            pygame.display.flip()
            clock.tick(self.game_state.fps)

        pygame.quit()

def main():
    game = Game()
    game.play()
    sys.exit()

main()
