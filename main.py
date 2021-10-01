from sys import exit
from random import randint
import pygame


def display_score():
    score = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = game_font.render(f"Score: {score}", False, text_colour)
    score_rect = score_surf.get_rect(center=(400, 50))
    pygame.draw.rect(screen, box_colour, score_rect)
    pygame.draw.rect(screen, box_colour, score_rect, 10)
    screen.blit(score_surf, score_rect)

    return score


def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 4

            screen.blit(snail_surf, obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []


start_time = 0
game_score = 0
game_active = False
text_colour = (64, 64, 64)
box_colour = "#c0e8ec"

gravity = 0.9
player_gravity = 0
player_on_ground = False

pygame.init()
fps = 60
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()
game_font = pygame.font.Font("font/Pixeltype.ttf", 50)

sky_surf = pygame.image.load("graphics/Sky.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()


snail_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_rect = snail_surf.get_rect(midbottom=(600, 300))

obstacle_rect_list = []

player_surf = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_rect = player_surf.get_rect(midbottom=(50, 200))

player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

game_name = game_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))
game_message = game_font.render("Press Space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 360))


obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obstacle_timer:
                obstacle_rect_list.append(
                    snail_surf.get_rect(midbottom=(randint(900, 1100), 300))
                )

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_on_ground:
                    player_gravity = -20
                    player_on_ground = False
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                snail_rect.x = 1000
                start_time = pygame.time.get_ticks()

    if game_active:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        game_score = display_score()

        screen.blit(snail_surf, snail_rect)

        player_gravity += gravity
        player_rect.y += player_gravity
        if player_rect.bottom > 300:
            player_rect.bottom = 300
            player_on_ground = True
        screen.blit(player_surf, player_rect)

        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        if snail_rect.colliderect(player_rect):
            game_active = False
    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = game_font.render(
            f"Your score: {game_score}", False, (111, 196, 169)
        )
        score_message_rect = score_message.get_rect(center=(400, 360))

        screen.blit(game_name, game_name_rect)
        if game_score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(fps)
