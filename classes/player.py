import pygame
from classes.projectile import Projectile

class Player(pygame.sprite.Sprite):
    def __init__(self, shoot_sound):
        super().__init__()
        self.original_image = pygame.image.load("images/space_jet.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (self.original_image.get_width() * 2 // 10, self.original_image.get_height() * 2 // 10))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = 300
        self.speed = 5
        self.health = 100
        self.lives = 3
        self.shoot_sound = shoot_sound

    def move(self, dy):
        self.rect.y += dy
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > 600 - self.rect.height:
            self.rect.y = 600 - self.rect.height

    def shoot(self, all_sprites, projectiles):
        projectile = Projectile(self.rect.right, self.rect.centery)
        all_sprites.add(projectile)
        projectiles.add(projectile)
        self.shoot_sound.play()

    def update(self, keys, all_sprites, projectiles):
        if keys[pygame.K_UP]:
            self.move(-self.speed)
        if keys[pygame.K_DOWN]:
            self.move(self.speed)
        if keys[pygame.K_SPACE]:
            self.shoot(all_sprites, projectiles)

    def draw(self, screen):
        screen.blit(self.image, self.rect)