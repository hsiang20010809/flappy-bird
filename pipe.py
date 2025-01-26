import pygame

class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y,  img, top):
        super().__init__()
        self.image = img
        self.speedx = 4
        self.rect = self.image.get_rect() # 回傳圖片各點座標
        if top:
            self.rect.bottomleft = (x, y)
        else:
            self.rect.topleft = (x, y)

    def update(self):
        self.rect.x -= self.speedx
        if self.rect.right < 0:
            self.kill() # 超出邊界就刪除物件