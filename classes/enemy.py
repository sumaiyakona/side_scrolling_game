import pygame
import random
from classes.projectile import EnemyProjectile
from classes.bomb import Bomb

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        enemy_images = [
            pygame.image.load("images/enemy1.png").convert_alpha(),
            pygame.image.load("images/enemy2.png").convert_alpha(),
            pygame.image.load("images/enemy3.png").convert_alpha()
        ]
        self.original_image = random.choice(enemy_images)
        self.image = pygame.transform.scale(self.original_image, (self.original_image.get_width() * 3 // 10, self.original_image.get_height() * 3 // 10))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        self.health = 50
        self.shoot_timer = 0
        self.bomb_timer = 0

    def update(self, all_sprites, enemy_projectiles, bombs):
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.kill()

        # Shooting logic
        self.shoot_timer += 1
        if self.shoot_timer > 60:  # Shoot every second
            self.shoot(all_sprites, enemy_projectiles)
            self.shoot_timer = 0

        # Bomb dropping logic
        self.bomb_timer += 1
        if self.bomb_timer > 120:  # Drop bomb every 2 seconds
            self.drop_bomb(all_sprites, bombs)
            self.bomb_timer = 0

    def shoot(self, all_sprites, enemy_projectiles):
        enemy_projectile = EnemyProjectile(self.rect.left, self.rect.centery)
        all_sprites.add(enemy_projectile)
        enemy_projectiles.add(enemy_projectile)

    def drop_bomb(self, all_sprites, bombs):
        bomb = Bomb(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bomb)
        bombs.add(bomb)

    def draw(self, screen):
        screen.blit(self.image, self.rect)