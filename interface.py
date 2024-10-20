import pygame
import json

# High Scores File
HIGH_SCORES_FILE = "high_scores.json"

# Load high scores
def load_high_scores():
    try:
        with open(HIGH_SCORES_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return [0, 0, 0]

# Save high scores
def save_high_scores(high_scores):
    with open(HIGH_SCORES_FILE, "w") as file:
        json.dump(high_scores, file)

# Update high scores
def update_high_scores(score, high_scores):
    high_scores.append(score)
    high_scores.sort(reverse=True)
    return high_scores[:3]

def home_page(screen, WHITE):
    font = pygame.font.SysFont(None, 36)
    home = True
    while home:
        screen.fill(WHITE)
        title_text = font.render("Space Impact", True, (0, 0, 0))
        screen.blit(title_text, (400 - title_text.get_width() // 2, 100))

        start_button = pygame.Rect(400 - 100, 200, 200, 50)
        scores_button = pygame.Rect(400 - 100, 300, 200, 50)
        quit_button = pygame.Rect(400 - 100, 400, 200, 50)

        pygame.draw.rect(screen, (0, 255, 0), start_button)
        pygame.draw.rect(screen, (0, 0, 255), scores_button)
        pygame.draw.rect(screen, (255, 0, 0), quit_button)

        start_text = font.render("Start", True, (255, 255, 255))
        scores_text = font.render("Scores", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))

        screen.blit(start_text, (start_button.x + (start_button.width - start_text.get_width()) // 2, start_button.y + (start_button.height - start_text.get_height()) // 2))
        screen.blit(scores_text, (scores_button.x + (scores_button.width - scores_text.get_width()) // 2, scores_button.y + (scores_button.height - scores_text.get_height()) // 2))
        screen.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2, quit_button.y + (quit_button.height - quit_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    home = False
                elif scores_button.collidepoint(event.pos):
                    show_scores(screen, WHITE)
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

def show_scores(screen, WHITE):
    font = pygame.font.SysFont(None, 36)
    scores = True
    high_scores = load_high_scores()
    while scores:
        screen.fill(WHITE)
        scores_text = font.render("Top 3 Scores", True, (0, 0, 0))
        screen.blit(scores_text, (400 - scores_text.get_width() // 2, 100))

        for i, score in enumerate(high_scores):
            score_text = font.render(f"{i + 1}. {score}", True, (0, 0, 0))
            screen.blit(score_text, (400 - score_text.get_width() // 2, 200 + i * 50))

        back_button = pygame.Rect(400 - 100, 400, 200, 50)
        pygame.draw.rect(screen, (255, 0, 0), back_button)
        back_text = font.render("Back", True, (255, 255, 255))
        screen.blit(back_text, (back_button.x + (back_button.width - back_text.get_width()) // 2, back_button.y + (back_button.height - back_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    scores = False

def game_over_screen(screen, WHITE, score):
    font = pygame.font.SysFont(None, 36)
    high_scores = load_high_scores()
    high_scores = update_high_scores(score, high_scores)
    save_high_scores(high_scores)

    game_over = True
    while game_over:
        screen.fill(WHITE)
        game_over_text = font.render("Game Over", True, (0, 0, 0))
        screen.blit(game_over_text, (400 - game_over_text.get_width() // 2, 100))

        replay_button = pygame.Rect(400 - 100, 300, 200, 50)
        quit_button = pygame.Rect(400 - 100, 400, 200, 50)

        pygame.draw.rect(screen, (0, 255, 0), replay_button)
        pygame.draw.rect(screen, (255, 0, 0), quit_button)

        replay_text = font.render("Replay", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))

        screen.blit(replay_text, (replay_button.x + (replay_button.width - replay_text.get_width()) // 2, replay_button.y + (replay_button.height - replay_text.get_height()) // 2))
        screen.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2, quit_button.y + (quit_button.height - quit_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if replay_button.collidepoint(event.pos):
                    game_over = False
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()