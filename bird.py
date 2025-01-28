import pygame

class Bird(pygame.sprite.Sprite): # 繼承PYGAME的遊戲更新 碰撞檢測等函式
    def __init__(self, x, y, imgs):
        super().__init__()
        self.origin_x = x
        self.origin_y = y
        self.imgs = imgs
        self.img_index = 0
        self.image = self.imgs[self.img_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedy = 0 
        self.last_pic_time = pygame.time.get_ticks()# 回傳從遊戲開始到現在經過的毫秒數
        self.img_frequency = 50
        self.fly = True

    def update(self, ground_top):
        # 飛翔動畫
        if self.fly:
            now = pygame.time.get_ticks()
            if now - self.last_pic_time > self.img_frequency:
                self.img_index += 1
                if self.img_index >= len(self.imgs):
                    self.img_index = 0
                self.image = pygame.transform.rotate(self.imgs[self.img_index], -(self.speedy * 2))
                self.last_pic_time = now

        # 重力
        self.speedy += 0.5
        if self.speedy >= 8:
            self.speedy = 8 # 掉落最大速度
        self.rect.y += self.speedy # 重力
        if self.rect.bottom >= ground_top:
            self.rect.bottom = ground_top

    def jump(self):
        self.speedy = -8

    def game_over(self):
        self.fly = False
        self.image = pygame.transform.rotate(self.imgs[self.img_index], -90)

    def reset(self):
        self.img_index = 0
        self.rect.center = (self.origin_x, self.origin_y)
        self.speedy = 0 
        self.last_pic_time = pygame.time.get_ticks()# 回傳從遊戲開始到現在經過的毫秒數
        self.fly = True