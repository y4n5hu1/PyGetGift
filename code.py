import pygame
from pygame.locals import *
from sys import exit
import random


# 封装鼠标类
class MouseCur(pygame.sprite.Sprite):
    def __init__(self):
        self.m_img = pygame.image.load('Assert/mouse.png').convert_alpha()  # 设置光标
        self.m_left, self.m_top = pygame.mouse.get_pos()  # 获取鼠标的屏幕坐标
        # 计算光标图片宽度的一半
        # 光标图片的left=鼠标坐标的left-图片宽度的一半
        # 图片的中心点应该与光标重合
        self.m_left -= self.m_img.get_width() / 2
        self.m_top -= self.m_img.get_height() / 2
        self.m_width, self.m_height = self.m_img.get_size()
        self.rect = pygame.Rect(self.m_left, self.m_top, self.m_width, self.m_height)  # 光标图片的位置
        GameCont.screen.blit(self.m_img, self.rect)  # 将图片绘制在矩形上

    def update(self):
        # 计算光标图片宽度的一半
        # 光标图片的left=鼠标坐标的left-图片宽度的一半
        # 图片的中心点应该与光标重合
        self.m_left, self.m_top = pygame.mouse.get_pos()
        self.m_left -= self.m_img.get_width() / 2
        self.m_top -= self.m_img.get_height() / 2
        self.rect = pygame.Rect(self.m_left, self.m_top, self.m_width, self.m_height)  # 光标图片的位置
        GameCont.screen.blit(self.m_img, self.rect)  # 将图片绘制在矩形上


# 封装礼物类
class Gift(pygame.sprite.Sprite):
    def __init__(self):
        self.g_top = 0  # 顶部
        self.g_left = random.randint(130, 950)  # 宽度上随机位置
        self.g_img = pygame.image.load('Assert/gift.png').convert_alpha()
        self.g_width, self.g_height = self.g_img.get_size()
        self.rect = pygame.Rect(self.g_left, self.g_top, self.g_width, self.g_height)  # 更新位置
        GameCont.screen.blit(self.g_img, self.rect)   # 将礼物绘制到矩形

    def update(self):
        self.g_top += 1  # top+1 向下移动
        self.rect = pygame.Rect(self.g_left, self.g_top, self.g_width, self.g_height)  # 更新位置
        GameCont.screen.blit(self.g_img, self.rect)   # 将礼物绘制到矩形


class GameCont(pygame.sprite.Sprite):
    screen = None

    def __init__(self):
        pygame.init()
        self.score = 0
        self.speed = 100
        self.window_width, self.window_height = 1024, 647
        GameCont.screen = pygame.display.set_mode((self.window_width, self.window_height), 0, 32)
        pygame.display.set_caption("圣诞快乐")
        pygame.mixer.music.load('Assert/song.mp3')
        self.background = pygame.image.load('Assert/bg.jpg').convert()
        pygame.mixer.music.play()
        self.small_font = pygame.font.Font(None, 40)
        self.big_font = pygame.font.Font(None, 80)
        self.gifts = []
        self.mouseCur = MouseCur()

    def update(self):
        gen_i = 0  # i增量，控制礼物生成i=speed时生成礼物
        while True:
            if gen_i == self.speed:
                self.gifts.append(Gift())
                gen_i = 0
            gen_i += 1
            text = self.small_font.render('Score:' + str(self.score), True, (0, 0, 0))  # 渲染分数
            self.screen.blit(self.background, (0, 0))  # 更新背景
            self.screen.blit(text, (0, 100))  # 更新分数
            for n in range(0, len(self.gifts) - 1):
                self.gifts[n].update()
            self.mouseCur.update()
            pygame.mouse.set_visible(False)  # 隐藏鼠标
            for n in range(0, len(self.gifts)):
                if self.gifts[n].g_top > self.window_height:  # 掉落到地面
                    self.stop()
            for event in pygame.event.get():
                if event.type == QUIT:  # 退出
                    exit()
                if event.type == MOUSEBUTTONDOWN:  # 鼠标按下
                    for n in range(0, len(self.gifts) - 1):  # 遍历礼物列表
                        if pygame.sprite.collide_rect(self.gifts[n], self.mouseCur):  # 检测鼠标碰撞到礼物
                            del self.gifts[n]  # 销毁礼物
                            self.score += 10  # 分数+10
            pygame.display.update()

    def stop(self):
        self.screen.blit(self.background, (0, 0))
        stop_text = self.big_font.render('GAME OVER', True, (0, 0, 0))
        self.screen.blit(stop_text, (350, 200))
        score_text = self.small_font.render('Score:' + str(self.score), True, (0, 0, 0))
        self.screen.blit(score_text, (450, 300))
        self.mouseCur.update()


if __name__ == "__main__":
    game = GameCont()
    game.update()