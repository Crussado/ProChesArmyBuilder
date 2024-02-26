import pygame
from abc import ABC, abstractmethod

from elements import StandardButton

class Scene(ABC):
    @abstractmethod
    def __init__(self, game_state) -> None:
        self.game_state = game_state
        self.next = self
        super().__init__()

    @abstractmethod
    def check_event(self, events):
        pass

    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def draw(self, screen):
        pass

    def switch_to(self, next_scene):
        self.next = next_scene

    def terminate(self):
        self.switch_to(None)

class TitleScene(Scene):
    def __init__(self, game_state) -> None:
        super().__init__(game_state)
        sector_screen_sizes = self.game_state.height // 6
        self.padding = 30
        self.buttons_config = {
            'x': self.game_state.width // 2,
            'y': sector_screen_sizes,
            'width': self.game_state.width // 3,
            'height': sector_screen_sizes - self.padding,
            'color': 'purple', # change to ocre
            'type': {
                'PLAY': lambda: self.switch_to(GameScene(self.game_state)),
                'ARMY BUILD': self.terminate, #lambda: self.switch_to(LoadingScene(self.game_state)),
                'CONFIG': self.terminate, #lambda: self.switch_to(ConfigScene(self.game_state)),
                'EXIT': self.terminate,
            },
            'font_size': 30,
        }

        self.buttons = pygame.sprite.Group()
        for i, tipo in enumerate(self.buttons_config['type']):
            button = StandardButton(
                self.buttons_config['x'],
                self.buttons_config['y'] + (i+1) * (self.buttons_config['height'] + self.padding),
                self.buttons_config['width'],
                self.buttons_config['height'],
                (0,0,0),
                (200,200,200),
                tipo,
                self.game_state.font(self.buttons_config['font_size']),
            )

            self.buttons.add(button)

    def check_event(self, events):
        super().check_event(events)
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.buttons.update(event)
    
    def update(self):
        super().update()
        for button in self.buttons:
            if button.consume_action():
                self.buttons_config['type'][button.text]()

    def draw(self, screen):
        super().draw(screen)
        screen.fill((0,0,0))
        text_renderizado = self.game_state.font(70).render('Warhammer Chess', True, (200,200,200))
        rect_text = text_renderizado.get_rect(center=(self.game_state.width//2, self.padding*2))
        screen.blit(text_renderizado, rect_text)

        self.buttons.draw(screen)

class GameScene(Scene):
    def __init__(self, game_state) -> None:
        super().__init__(game_state)
        # Groups
        self.all_sprites = pygame.sprite.Group()

        # self.fail = pygame.mixer.Sound('./sounds/fail.mp3')

        # self.draw_screen(screen)

    def draw(self, screen):
        super().draw(screen)
        # Draw screen
        self.draw_screen(screen)
        self.all_sprites.draw(screen)

        # rich_text = RichText(20)
        # rich_text.render(text=f'Score:\n{self.game_state.score}\nX{2**int(self.game_state.combo)}', color=GOLDEN)
        # rich_text.get_rect(ROWS[0]//2, BASE//2)
        # rich_text.blit(screen)

    # def create_buttons(self):
    #     for note in range(self.game_state.cant_buttons):
    #         button = Button(note)
    #         self.all_sprites.add(button)
    #         self.buttons.add(button)

    def draw_screen(self, screen):
        padding = 30
        x_init = padding
        x_end = self.game_state.width - padding
        y_init = padding
        y_end = self.game_state.height - padding
        x_cant = 16
        y_cant = 8
        x_size = (x_end - x_init) / x_cant
        y_size = (y_end - y_init) / y_cant
        colors = ['red','blue']
        screen.fill('grey')
        color = 0
        for x in range(x_cant):
            color += 1
            color = color % 2

            for y in range(y_cant):
                rect = pygame.Rect(x_init + x*x_size, y_init + y*y_size, x_size, y_size)
                pygame.draw.rect(screen, colors[color], rect)
                color += 1
                color = color % 2
        # for row in ROWS:
        #     pygame.draw.line(screen, GREY, (row, 0), (row, self.game_state.height), 2)
        # pygame.draw.line(screen, GREY, (ROWS[0], BASE), (self.game_state.width, BASE), 2)

    def check_event(self, events):
        return
        super().check_event(events)
        for event in events:
            if event.type == pygame.KEYDOWN and event.key in KEYS:
                button = self.get_button_by_key(event.key)
                button.key_down()
                collisions = pygame.sprite.spritecollide(button, self.tokens, False)
                if collisions:
                    self.particles += [Particle(6 + self.game_state.render_combo() * SCORE, button.x, button.y)]
                    self.all_sprites.remove(collisions[0])
                    self.tokens.remove(collisions[0])
                    self.game_state.score += self.game_state.render_combo() * SCORE
                    self.game_state.increase_combo()
                else:
                    self.fail.play()
            elif event.type == pygame.KEYUP and event.key in KEYS:
                button = self.get_button_by_key(event.key)
                button.key_up()

    # def add_token(self, index):
    #         token = Token(index % self.game_state.cant_buttons)
    #         self.all_sprites.add(token)
    #         self.tokens.add(token)
    #         self.last_tokens.append(token)
    #         if len(self.last_tokens) > len(ROWS):
    #             self.last_tokens = self.last_tokens[1:]

    def update(self):
        return
        super().update()
        # Drop beat
        actual_time = (pygame.time.get_ticks() - self.initial_time) / 1000
        draw = []
        self.synchronize(actual_time)
        draw += self.check_time_rules(self.times, actual_time)
        # draw += self.check_time_rules(self.event_times, actual_time)
        if draw and self.own_rules():
            if len(self.croma[0]) > 0:
                self.croma = list(map(lambda r: r[1:], self.croma))
            for index in draw:
                self.add_token(index)

        self.all_sprites.update()
        
        for token in self.tokens:
            if token.destroy(self.game_state.height):
                self.fail.play()
                self.game_state.reset_combo()
                self.all_sprites.remove(token)
                self.tokens.remove(token)    
