import time
import pygame
from pygame import mixer
from random import randrange as rnd


game_width = 1200
game_height = 800
fps = 60
# paddle1 settings
paddle1_w = 30
paddle1_h = 120
paddle1_speed = 15
paddle1 = pygame.Rect(game_width - paddle1_w - 10, game_height // 2 - paddle1_h // 2, paddle1_w, paddle1_h)
# paddle2 settings
paddle2_w = 30
paddle2_h = 120
paddle2_speed = 15
paddle2 = pygame.Rect(paddle2_w - 10, game_height // 2 - paddle2_h // 2,  paddle2_w, paddle2_h)
# ball settings
ball_radius = 20
ball_speed = 6
ball_rect = int(ball_radius * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, game_width - ball_rect), game_height // 2, ball_rect, ball_rect)
dx, dy = 1, -1

pygame.init()
pygame.font.init()
sc = pygame.display.set_mode((game_width, game_height))
clock = pygame.time.Clock()

# background
img = pygame.image.load('1.jpg').convert()
mixer.music.load('arp.wav')
mixer.music.play(-1)
score1 = 0
score2 = 0
font = pygame.font.Font('Arial.ttf', 48)
fontgoal = pygame.font.Font('Arial.ttf', 126)

def detect_collision(dx, dy, ball, rect):
    if dx > 0 or -dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0 or -dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

def countdown(num_of_secs):
    show_score = fontgoal.render(str(score1) + " - " + str(score2), True, 'white')
    sc.blit(show_score, [game_width // 2, game_height // 2])
    while num_of_secs:
        time.sleep(1)
        num_of_secs -= 1

game_over = False

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
                continue
    # sc.fill('black')
    sc.blit(img, (0, 0))
    # drawing world
    pygame.draw.rect(sc, pygame.Color('pink'), paddle1)
    pygame.draw.rect(sc, pygame.Color('purple'), paddle2)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
    if not game_over:
        show_score = font.render(str(score1) + " - " + str(score2), True, 'white')
        sc.blit(show_score, [game_width / 2, 15])

    # ball movement
    ball.x += ball_speed * dx
    ball.y += ball_speed * dy

    # collision top bottom
    if ball.centery < ball_radius or ball.centery > game_height - ball_radius:
        collision = mixer.Sound('ballcollision.wav')
        collision.play()
        dy = -dy
    # collision paddle
    if ball.colliderect(paddle1) and dx > 0:
        collision2 = mixer.Sound('ballcollision2.wav')
        collision2.play()
        dx = -dx
    if ball.colliderect(paddle2) and -dx > 0:
        collision2 = mixer.Sound('ballcollision2.wav')
        collision2.play()
        dx, dy = detect_collision(dx, dy, ball, paddle2)
        # if dx > 0:
        #     dx, dy = (-dx, -dy) if ball.centerx < paddle.centerx else (dx, -dy)
        # else:
        #     dx, dy = (-dx, -dy) if ball.centerx >= paddle.centerx else (dx, -dy)

    # control
    key = pygame.key.get_pressed()
    if key[pygame.K_UP] and paddle1.top > 0:
        paddle1_key = mixer.Sound('paddle1up.wav')
        paddle1_key.play()
        paddle1.top -= paddle1_speed
    if key[pygame.K_DOWN] and paddle1.bottom < game_height:
        paddle1_key = mixer.Sound('paddle1down.wav')
        paddle1_key.play()
        paddle1.bottom += paddle1_speed
    if key[pygame.K_w] and paddle1.top > 0:
        paddle2.top -= paddle2_speed
        paddle2_key = mixer.Sound('paddle2up.wav')
        paddle2_key.play()
    if key[pygame.K_s] and paddle2.bottom < game_height:
        paddle2.bottom += paddle2_speed
        paddle2_key = mixer.Sound('paddle2up.wav')
        paddle2_key.play()
    if key[pygame.K_ESCAPE]:
        quit()
    # scoring
    if ball.centerx < ball_radius:
        score1 += 1
        ball = pygame.Rect(game_width // 2, game_height // 2, ball_rect, ball_rect)
        pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
        countdown(2)
    if ball.centerx > game_width - ball_radius:
        score2 += 1
        ball = pygame.Rect(game_width // 2, game_height // 2, ball_rect, ball_rect)
        pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_radius)
        countdown(2)
        # update screen
    pygame.display.flip()

    clock.tick(fps)

pygame.quit()
