import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("assets/character/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("assets/character/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("assets/character/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(80, 400)) 
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("assets/Audio/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 400: 
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 400: 
            self.rect.bottom = 400

    def animation_state(self):
        if self.rect.bottom < 400: 
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        
        if type == 'dragon':
            dragon = pygame.image.load("assets/character/dragon1.png").convert_alpha()
            dragon_1 = pygame.image.load("assets/character/dragon.png").convert_alpha()
            self.frames = [dragon,dragon_1]
            y_pos = 300  
        else:
            robott = pygame.image.load("assets/character/robott.png").convert_alpha()
            robott_1 = pygame.image.load("assets/character/robott_1.png").convert_alpha()
            self.frames = [robott,robott_1]
            y_pos  = 400  

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(900,1100),y_pos))  

    def animation_state(self):
        self.animation_index += 0.1 
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100: 
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 500) - start_time + score_multiplier
    score_surf = test_font.render(f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

pygame.init()
screen = pygame.display.set_mode((800, 600)) 
pygame.display.set_caption('Run Labi Run!')

clock = pygame.time.Clock()
test_font = pygame.font.Font("assets/font/Pixeltype.ttf", 50)
game_active = False
start_time = 0
score_multiplier = 0
score = 0
bg_music = pygame.mixer.Sound("assets/Audio/mega.mp3")
bg_music.play(loops=-1)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load("assets/sky_and_ground/sky.png").convert()
ground_surface = pygame.image.load("assets/sky_and_ground/ground.jpg").convert()

# Intro screen
player_stand = pygame.image.load("assets/character/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center=(400, 250))  

game_name = test_font.render('Run Labi Run', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 50))  

game_message = test_font.render('Press space to run', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 500))  

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

score_multiplier = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['dragon', 'robot', 'robot', 'robot'])))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    score_multiplier += 20 
        else:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_SPACE or event.key == pygame.K_RETURN):
                game_active = True
                start_time = int(pygame.time.get_ticks() / 500) + score_multiplier

    if game_active:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 400)) 
        score = display_score()
        
        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(player_stand, player_stand_rect)

        score_message = test_font.render(f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 500))  
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)