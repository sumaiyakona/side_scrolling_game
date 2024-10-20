import pygame

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0) if type == 'health' else (0, 0, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.type = type

    def apply_effect(self, player):
        if self.type == 'health':
            player.health += 20
        elif self.type == 'life':
            player.lives += 1
        self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)