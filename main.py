import pygame
from bird import Bird
from pipe import Pipe
import random

SCREEN_WIDTH = 780
SCREEN_HEIGHT = 600
FPS = 60

def generate_pipes(last_generate_pipe_time, pipe_frequency, pipe_group):
    now = pygame.time.get_ticks()
    if now - last_generate_pipe_time >= pipe_frequency:
        random_height = random.randint(-100, 100)
        pipe_bottom = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT/2 + pipe_gap/2 + random_height, pipe_img, False)
        pipe_top = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT/2 - pipe_gap/2 + random_height, flip_pipe_img, True)
        pipe_group.add(pipe_bottom)
        pipe_group.add(pipe_top)
        return now
    return last_generate_pipe_time

pygame.init()


window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('flappy_bird')
clock = pygame.time.Clock()

font = pygame.font.Font('微軟正黑體.ttf', 60)

bg_img = pygame.image.load('img/bg.png')
bg_img = pygame.transform.scale(bg_img, (780, 600))# 修改圖片尺寸
restart_img = pygame.image.load('img/restart.png')
restart_img_rect = restart_img.get_rect()
restart_img_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)# 把圖片(整個rect)移過去螢幕中心點
ground_img = pygame.image.load('img/ground.png')
pipe_img = pygame.image.load('img/pipe.png')
flip_pipe_img = pygame.transform.flip(pipe_img, False, True)# 垂直翻轉
bird_imgs = []
for i in range(1, 4):
    bird_imgs.append(pygame.image.load(f'img/bird{i}.png'))

pygame.display.set_icon(bird_imgs[0])

score = 0
game_over = False
ground_x = 0 
ground_speed = 4
ground_top = SCREEN_HEIGHT-100
pipe_gap = 200
pipe_frequency = 1250
last_generate_pipe_time = pygame.time.get_ticks() - pipe_frequency

# 建立鳥
bird = Bird(100, SCREEN_HEIGHT/2, bird_imgs)
bird_group = pygame.sprite.Group() #設定sprite繼承群組
bird_group.add(bird)

# 建立管子群組
pipe_group = pygame.sprite.Group()

start_time = pygame.time.get_ticks()


running = True
while running:
    clock.tick(FPS)
    # ---取得輸入---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over: #檢測滑鼠是否有被"按下去"
            if event.button == 1: #左鍵
                bird.jump()
        # 重新開始
        elif event.type == pygame.KEYDOWN and game_over == True:
            if event.key == pygame.K_SPACE:
                game_over = False
                score = 0
                last_generate_pipe_time = pygame.time.get_ticks() - pipe_frequency #重設管子生成時間
                bird.reset()
                Pipe.base_speed = 5
                pipe_frequency = 1250
                start_time = pygame.time.get_ticks()
                pipe_group.empty()#把遊戲群組裡的物件全部刪除


    # ---遊戲更新---
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000 #轉換為秒
    bird_group.update(ground_top)
    if not game_over:
        pipe_group.update()
        # 每5秒增加0.7的速度，最大速度為12
        Pipe.base_speed = min(12, 5 + (elapsed_time // 5) / 10 * 7)
        # 每5秒增加100的管子生成頻率，最大速度為600
        pipe_frequency = max(600, 1250 - (elapsed_time // 5) * 100)
        last_generate_pipe_time = generate_pipes(last_generate_pipe_time, pipe_frequency, pipe_group)

        # 分數判定
        score_label = font.render(f"{score}", True, '#FFFFFF')
        score_label_rect = score_label.get_rect()
        score_label_rect.centerx = SCREEN_WIDTH/2
        if len(pipe_group.sprites()) > 0:
            first_pipe = pipe_group.sprites()[0] #pipe_gruop.sprites()回傳pipe_group裡的物件資訊
            if not first_pipe.bird_pass:
                if first_pipe.rect.right < bird.rect.left: 
                    score += 1
                    first_pipe.bird_pass = True


        # 地板移速
        ground_x -= ground_speed
        if ground_x < -100:
            ground_x = 0

    # 碰撞檢測
    # pygame.sprite.groupcollide回傳字典，顯示正在碰撞的群組
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or\
        bird.rect.top <= 0 or bird.rect.bottom >= ground_top :
        game_over = True
        bird.game_over()
        
    # ---畫面顯示---
    window.blit(bg_img, (0, 0))
    bird_group.draw(window)
    pipe_group.draw(window)
    window.blit(ground_img, (ground_x, ground_top))
    window.blit(score_label, score_label_rect)
    if game_over:
        window.blit(restart_img, restart_img_rect)
    pygame.display.update()


pygame.quit()