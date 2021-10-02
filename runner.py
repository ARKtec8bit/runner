from sys import exit
from random import randint, choice
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1_surf = pygame.image.load(
            "graphics/Player/player_walk_1.png"
        ).convert_alpha()
        player_walk2_surf = pygame.image.load(
            "graphics/Player/player_walk_2.png"
        ).convert_alpha()

        self.player_jump_surf = pygame.image.load(
            "graphics/Player/jump.png"
        ).convert_alpha()
        self.player_walk = [player_walk1_surf, player_walk2_surf]
        self.player_index = 0

        self.image = self.player_walk[self.player_index]

        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0.9
        self.player_gravity = 0
        self.player_on_ground = False

        self.jump_sound = pygame.mixer.Sound("audio/jump.ogg")
        self.jump_sound.set_volume(0.2)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.player_on_ground:
            self.player_gravity = -20
            self.player_on_ground = False
            self.jump_sound.play()

    def apply_gravity(self):
        self.player_gravity += self.gravity
        self.rect.y += self.player_gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.player_on_ground = True

    def player_animation(self):

        if self.rect.bottom < 300:
            self.image = self.player_jump_surf
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == "Fly":
            fly1_surf = pygame.image.load("graphics/Fly/Fly1.png").convert_alpha()
            fly2_surf = pygame.image.load("graphics/Fly/Fly2.png").convert_alpha()
            self.frames = [fly1_surf, fly2_surf]
            y_pos = 210
            self.animation_speed = 0.5
            self.speed = 6
        else:
            snail1_surf = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail2_surf = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail1_surf, snail2_surf]
            y_pos = 300
            self.animation_speed = 0.1
            self.speed = 4

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += self.animation_speed
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= self.speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


def display_score():
    score = int((pygame.time.get_ticks() - start_time) / 1000)
    score_surf = game_font.render(f"Score: {score}", False, text_colour)
    score_rect = score_surf.get_rect(center=(400, 50))
    pygame.draw.rect(screen, box_colour, score_rect)
    pygame.draw.rect(screen, box_colour, score_rect, 10)
    screen.blit(score_surf, score_rect)

    return score


def colission_sprites():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


# initialise pygame
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Runner")
clock = pygame.time.Clock()

# settings
start_time = 0
game_score = 0
game_active = False
text_colour = (64, 64, 64)
box_colour = "#c0e8ec"
fps = 60

# import assets
bg_music = pygame.mixer.Sound("audio/music.ogg")
bg_music.set_volume(0.08)
bg_music.play(-1)
sky_surf = pygame.image.load("graphics/Sky.png").convert()
ground_surf = pygame.image.load("graphics/ground.png").convert()

player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 200))

# start screen
game_font = pygame.font.Font("font/Pixeltype.ttf", 50)
game_name = game_font.render("Pixel Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))
game_message = game_font.render("Press Space to run", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 360))

# initialise player
player = pygame.sprite.GroupSingle()
player.add(Player())

# intialise obstacles
obstacle_group = pygame.sprite.Group()
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1600)

# game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:

            if event.type == obstacle_timer:
                obstacle_group.add(
                    Obstacle(
                        choice(
                            ["Fly", "Snail", "Snail", "Snail", "Snail", "Snail", "Fly"]
                        )
                    )
                )

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = pygame.time.get_ticks()

    if game_active:

        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        game_score = display_score()

        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = colission_sprites()

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
