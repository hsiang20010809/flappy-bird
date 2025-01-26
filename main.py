import pygame
from bird import Bird
from pipe import Pipe
import random

SCREEN_WIDTH = 780
SCREEN_HEIGHT = 600
FPS = 75

def generate_pipes(last_generate_pipe_time, pipe_frequency, pipe_sprite):
    now = pygame.time.get_ticks()
    if now - last_generate_pipe_time > pipe_frequency:
        random_height = random.randint(-75, 75)
        pipe_bottom = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT/2 + pipe_gap/2 + random_height, pipe_img, False)
        pipe_top = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT/2 - pipe_gap/2 + random_height, flip_pipe_img, True)
        pipe_sprite.add(pipe_bottom)
        pipe_sprite.add(pipe_top)
        return now
    return last_generate_pipe_time

pygame.init()


window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('flappy_bird')
clock = pygame.time.Clock()


bg_img = pygame.image.load('img/bg.png')
bg_img = pygame.transform.scale(bg_img, (780, 600))# 修改圖片尺寸
# bird1_img = pygame.transform.rotate(bird_img, 60)
# bird1_img = pygame.transform.flip(bird_img, True, False)# 水平翻轉 垂直翻轉
ground_img = pygame.image.load('img/ground.png')
pipe_img = pygame.image.load('img/pipe.png')
flip_pipe_img = pygame.transform.flip(pipe_img, False, True)# 垂直翻轉
bird_imgs = []
for i in range(1, 4):# range只會跑到n-1
    bird_imgs.append(pygame.image.load(f'img/bird{i}.png'))

pygame.display.set_icon(bird_imgs[0])

ground_x = 0 
ground_speed = 4
pipe_gap = 150
pipe_frequency = 1250
last_generate_pipe_time = pygame.time.get_ticks() - pipe_frequency

# 建立鳥
bird = Bird(100, SCREEN_HEIGHT/2, bird_imgs)
bird_sprite = pygame.sprite.Group() #設定sprite繼承群組
bird_sprite.add(bird)

# 建立管子群組
pipe_sprite = pygame.sprite.Group()


running = True
while running:
    clock.tick(FPS)
    # 取得輸入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False





    # 遊戲更新
    pipe_sprite.update()
    bird_sprite.update()
    last_generate_pipe_time = generate_pipes(last_generate_pipe_time, pipe_frequency, pipe_sprite)
    ground_x -= ground_speed
    if ground_x < -100:
        ground_x = 0







    # 畫面顯示
    window.blit(bg_img, (0, 0))
    bird_sprite.draw(window)
    pipe_sprite.draw(window)
    window.blit(ground_img, (ground_x, SCREEN_HEIGHT-100))
    # window.blit(bird1_img, (100, 100))
    # window.blit(pipe_img, (300, 400))
    pygame.display.update()


pygame.quit()