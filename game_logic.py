import pygame
import random
from classes.player import Player
from classes.enemy import Enemy
from classes.boss import Boss
from classes.collectible import Collectible
from classes.projectile import Projectile, EnemyProjectile  # Import the Projectile and EnemyProjectile classes
from classes.bomb import Bomb  # Import the Bomb class
from interface import game_over_screen

def main_game_loop(screen, WHITE):
    # Load sound effects
    shoot_sound = pygame.mixer.Sound("sounds/shoot.wav")
    hit_sound = pygame.mixer.Sound("sounds/hit.wav")
    explosion_sound = pygame.mixer.Sound("sounds/explosion.wav")
    game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")

    # Load background music
    pygame.mixer.music.load("sounds/background_music.wav")

    # Groups
    all_sprites = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    enemy_projectiles = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()

    player = Player(shoot_sound)
    all_sprites.add(player)

    clock = pygame.time.Clock()
    running = True
    score = 0  # Initialize score
    boss_spawned = False  # Initialize boss spawn flag
    boss_defeated = False  # Initialize boss defeated flag
    enemy_spawn_rate = 1000  # Initial enemy spawn rate (milliseconds)

    # Enemy spawn event
    ENEMY_SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(ENEMY_SPAWN_EVENT, enemy_spawn_rate)  # Spawn an enemy every second

    def draw_health_bar(screen, x, y, health):
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (health / 100) * BAR_LENGTH
        border_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        pygame.draw.rect(screen, (0, 255, 0), fill_rect)
        pygame.draw.rect(screen, (0, 0, 0), border_rect, 2)

    def increase_difficulty(score, enemy_spawn_rate):
        if score % 50 == 0 and score != 0:  # Increase difficulty every 50 points
            enemy_spawn_rate = max(200, enemy_spawn_rate - 100)  # Decrease spawn rate to a minimum of 200ms
            pygame.time.set_timer(ENEMY_SPAWN_EVENT, enemy_spawn_rate)
            for enemy in enemies:
                enemy.speed += 1  # Increase enemy speed
                enemy.health += 10  # Increase enemy health
        return enemy_spawn_rate

    # Play background music
    pygame.mixer.music.play(-1)  # Play the music in a loop

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == ENEMY_SPAWN_EVENT:
                if not boss_spawned or boss_defeated:
                    enemy = Enemy(800, random.randint(0, 600 - 30))
                    all_sprites.add(enemy)
                    enemies.add(enemy)

        keys = pygame.key.get_pressed()
        player.update(keys, all_sprites, projectiles)
        for sprite in all_sprites:
            if isinstance(sprite, (Enemy, Boss)):
                sprite.update(all_sprites, enemy_projectiles, bombs)
            elif isinstance(sprite, Projectile):
                sprite.update()
            elif isinstance(sprite, Bomb):
                sprite.update()
            elif isinstance(sprite, EnemyProjectile):
                sprite.update()

        # Collision detection
        for projectile in projectiles:
            enemy_hit = pygame.sprite.spritecollideany(projectile, enemies)
            if enemy_hit:
                enemy_hit.health -= 10
                if enemy_hit.health <= 0:
                    if isinstance(enemy_hit, Boss):
                        boss_defeated = True
                        boss_spawned = False
                    enemy_hit.kill()
                    score += 10  # Increase score when an enemy is defeated
                    explosion_sound.play()  # Play explosion sound
                    enemy_spawn_rate = increase_difficulty(score, enemy_spawn_rate)  # Increase difficulty based on score
                projectile.kill()

        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                player.health -= 10  # Reduce player's health when hit by an enemy
                enemy.kill()
                hit_sound.play()  # Play hit sound

        for enemy_projectile in enemy_projectiles:
            if pygame.sprite.collide_rect(player, enemy_projectile):
                player.health -= 5  # Reduce player's health when hit by an enemy projectile
                enemy_projectile.kill()
                hit_sound.play()  # Play hit sound

        for bomb in bombs:
            if pygame.sprite.collide_rect(player, bomb):
                player.health -= 20  # Reduce player's health when hit by a bomb
                bomb.kill()
                explosion_sound.play()  # Play explosion sound

        for collectible in collectibles:
            if pygame.sprite.collide_rect(player, collectible):
                collectible.apply_effect(player)

        # Check if player's health is zero
        if player.health <= 0:
            game_over_sound.play()  # Play game over sound
            game_over_screen(screen, WHITE, score)
            reset_game()
            return

        # Spawn boss when score reaches 100 and boss is not already spawned
        if score >= 100 and not boss_spawned and not boss_defeated:
            boss = Boss(800, 300)
            all_sprites.add(boss)
            enemies.add(boss)
            boss_spawned = True

        screen.fill(WHITE)
        all_sprites.draw(screen)

        # Draw health bar
        draw_health_bar(screen, 10, 10, player.health)

        # Draw score
        score_text = pygame.font.SysFont(None, 36).render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (800 - 150, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()