import pygame

class StandardButton(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, normal_color, border_color, text, font):
        super().__init__()

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.vertices = (0, 0, width, height)
        self.normal_color = normal_color
        self.border_color = border_color
        pygame.draw.rect(self.image, normal_color, self.vertices)
        pygame.draw.rect(self.image, self.border_color, self.vertices, 3)

        self.rect = self.image.get_rect(center=(x, y))

        self.text = text
        self.color_text = (200,200,200)
        self.font = font

        text_renderizado = self.font.render(self.text, True, self.color_text)
        rect_text = text_renderizado.get_rect(center=(self.rect.width//2, self.rect.height//2))
        self.image.blit(text_renderizado, rect_text)

        self.pressed = False

    def update(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                pass
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.pressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            self.pressed = False

    def consume_action(self):
        if self.pressed:
            self.pressed = False
            return True
        return False
  