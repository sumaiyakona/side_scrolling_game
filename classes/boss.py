import pygame
from classes.projectile import EnemyProjectile
from classes.bomb import Bomb

class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = pygame.image.load("images/dave.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (self.original_image.get_width(), self.original_image.get_height()))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        self.health = 500
        self.shoot_timer = 0
        self.bomb_timer = 0

    def update(self, all_sprites, enemy_projectiles, bombs):
        self.rect.x -= self.speed
        if self.rect.x < 400:
            self.rect.x = 400

        # Shooting logic
        self.shoot_timer += 1
        if self.shoot_timer > 30:  # Shoot every half second
            self.shoot(all_sprites, enemy_projectiles)
            self.shoot_timer = 0

        # Bomb dropping logic
        self.bomb_timer += 1
        if self.bomb_timer > 60:  # Drop bomb every second
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