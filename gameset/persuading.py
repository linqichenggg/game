import shutil

import pygame
import os
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag
import string
import os
import pygame
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag

font_name = os.path.join("font.ttf")

def game_Init():
    WIDTH = 1000
    HEIGHT = 800
    FPS = 60

    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    BLACK = (0, 0, 0)

    # initialize
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    # title
    pygame.display.set_caption("Persuading")
    clock = pygame.time.Clock()

    # img
    # background
    background_img = pygame.image.load(os.path.join("img", "litang.jpg")).convert()
    # dingzhen
    actor_img = pygame.image.load(os.path.join("img", "dzsmoke.jpg")).convert()

WIDTH = 1000
HEIGHT = 800
FPS = 60

WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)
YELLOW = (255,255,0)
BLACK = (0,0,0)

#initialize
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1000,800))
#title
pygame.display.set_caption("Persuading")
clock = pygame.time.Clock()

#img
#background
background_img = pygame.image.load(os.path.join("img", "litang.jpg")).convert()
#dingzhen
actor_img = pygame.image.load(os.path.join("img", "dzsmoke.jpg")).convert()

#sound
# speak_sound = pygame.mixer.Sound(os.path.join("sound", "audio.wav"))
def play_latest_sound():
    original_path = os.path.join("sound", "audio.wav")
    temp_path = os.path.join("sound", "temp_audio.wav")

    # 复制文件到新的路径
    shutil.copyfile(original_path, temp_path)

    # 加载最新的音频文件
    speak_sound = pygame.mixer.Sound(temp_path)

    # 播放音频
    speak_sound.play()
pygame.mixer.music.load(os.path.join("sound","I Got Smoke.flac"))
pygame.mixer.music.set_volume(0.05)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
font_name = os.path.join("font.ttf")
def draw_init():
    draw_text(screen, '劝说丁真', 128, WIDTH/2, HEIGHT/4)
    draw_text(screen, '使用文字劝说丁真从抽电子烟转换为传统香烟', 44, WIDTH/2, HEIGHT/2)
    draw_text(screen, '若输入法错误切换输入法即可（任何输入法状态下都能进行打字）', 25, WIDTH/2, HEIGHT*3/4)
    draw_text(screen, '按任意键开始', 25, WIDTH/2, HEIGHT * 3.5/4)
    pygame.display.update()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False

class Text(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((900,70))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT-180)
        self.font = pygame.font.Font(font_name, 15)  #Choose an appropriate font size
        #Text generated by LLM
        self.result = "Hello, I'm Dingzhen"  # Initialize the result text
        #输出⬆️

    def update(self):
        self.image.fill(WHITE)  # Fill the background again to clear old text
        x_margin = 10  # Left margin
        y_margin = 10  # Top margin
        y_offset = y_margin  # Start below the top margin

        space = self.font.size(' ')[0]
        max_width, max_height = self.image.get_size()
        x_offset = x_margin

        for word in self.result.split():
            word_surface = self.font.render(word, True, BLACK)
            word_width, word_height = word_surface.get_size()

            # Check if the word exceeds the line width
            if x_offset + word_width >= max_width - x_margin:
                # Move to the next line
                y_offset += word_height
                x_offset = x_margin

                # Check if we exceed the box height, stop rendering more text
                if y_offset + word_height > max_height - y_margin:
                    break

            # Render the word and move x_offset
            self.image.blit(word_surface, (x_offset, y_offset))
            x_offset += word_width + space

            # If the word is the last on a line, account for space width
            if x_offset + space >= max_width - x_margin:
                y_offset += word_height
                x_offset = x_margin

class Dingzhen(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(actor_img, (68,70))
        self.rect = self.image.get_rect()
        self.rect.center = (150, HEIGHT - 250)

#input
class Input(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((600, 30))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT - 70)  # Positioned just below the Text box
        self.font = pygame.font.Font(font_name, 20)
        self.text = ""  # Variable to store the input text
        #输入⬆️
        self.active = True  # Indicates if the input box is active

    def update(self):
        if self.active:
            self.image.fill(BLACK)  # Active color
        else:
            self.image.fill(BLACK)  # Inactive color
        text_surface = self.font.render(self.text, True, BLACK)#mantianguohai
        self.image.blit(text_surface, (10, 10))  # Add some padding

    def add_character(self, char):
        if self.active:
            if len(char) == 1 and char.isprintable():  # 确保字符是可打印的
                self.text += char

    def backspace(self):
        if self.active:
            self.text = self.text[:-1]

    def clear_text(self):
        self.text = ""

class TextBox:
    def __init__(self, w, h, x, y, font=None, callback=None):
        """
        :param w:文本框宽度
        :param h:文本框高度
        :param x:文本框坐标
        :param y:文本框坐标
        :param font:文本框中使用的字体
        :param callback:在文本框按下回车键之后的回调函数
        """
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.text = ""  # 文本框内容
        self.callback = callback
        # 创建背景surface
        self.__surface = pygame.Surface((w, h))
        # 如果font为None,那么效果可能不太好，建议传入font，更好调节
        if font is None:
            self.font = pygame.font.Font(font_name, 20)
        else:
            self.font = font

        self.dagparams = DefaultDagParams()
        self.state = 0  # 0初始状态 1输入拼音状态
        self.page = 1  # 第几页
        self.limit = 5  # 显示几个汉字
        self.pinyin = ''
        self.word_list = []  # 候选词列表
        self.word_list_surf = None  # 候选词surface
        self.buffer_text = ''  # 联想缓冲区字符串

    def create_word_list_surf(self):
        """
        创建联想词surface
        """
        word_list = [str(index + 1) + '.' + word for index, word in enumerate(self.word_list)]
        text = " ".join(word_list)
        self.word_list_surf = self.font.render(text, True, (255, 255, 255))

    def draw(self, dest_surf):
        # 创建文字surf
        text_surf = self.font.render(self.text, True, (255, 255, 255))
        # 绘制背景色
        dest_surf.blit(self.__surface, (self.x, self.y))
        # 绘制文字
        dest_surf.blit(text_surf, (self.x, self.y + (self.height - text_surf.get_height())),
                       (0, 0, self.width, self.height))
        # 绘制联想词
        if self.state == 1:
            dest_surf.blit(self.word_list_surf,
                           (self.x, self.y + (self.height - text_surf.get_height()) - 30),
                           (0, 0, self.width, self.height)
                           )

    def key_down(self, event):
        unicode = event.unicode
        key = event.key

        # 退位键
        if key == 8:
            self.text = self.text[:-1]
            if self.state == 1:
                self.buffer_text = self.buffer_text[:-1]
            return

        # 切换大小写键
        if key == 301:
            return

        # 回车键
        if key == 13:
            if self.callback:
                self.callback(self.text)
            return

        # print(key)
        # 空格输入中文
        if self.state == 1 and key == 32:
            self.state = 0
            self.text = self.text[:-len(self.buffer_text)] + self.word_list[0]
            self.word_list = []
            self.buffer_text = ''
            self.page = 1
            return

        # 翻页
        if self.state == 1 and key == 61:
            self.page += 1
            self.word_list = self.py2hz(self.buffer_text)
            if len(self.word_list) == 0:
                self.page -= 1
                self.word_list = self.py2hz(self.buffer_text)
            self.create_word_list_surf()
            return

        # 回退
        if self.state == 1 and key == 45:
            self.page -= 1
            if self.page < 1:
                self.page = 1
            self.word_list = self.py2hz(self.buffer_text)
            self.create_word_list_surf()
            return

        # 选字
        if self.state == 1 and key in (49, 50, 51, 52, 53):
            self.state = 0
            if len(self.word_list) <= key - 49:
                return
            self.text = self.text[:-len(self.buffer_text)] + self.word_list[key - 49]
            self.word_list = []
            self.buffer_text = ''
            self.page = 1
            return

        if unicode != "":
            char = unicode
        else:
            char = chr(key)

        if char in string.ascii_letters:
            self.buffer_text += char
            self.word_list = self.py2hz(self.buffer_text)
            self.create_word_list_surf()
            # print(self.buffer_text)
            self.state = 1
        self.text += char

    def safe_key_down(self, event):
        try:
            self.key_down(event)
        except:
            self.reset()

    def py2hz(self, pinyin):
        result = dag(self.dagparams, (pinyin,), path_num=self.limit * self.page)[
                 (self.page - 1) * self.limit:self.page * self.limit]
        data = [item.path[0] for item in result]
        return data

    def reset(self):
        # 异常的时候还原到初始状态
        self.state = 0  # 0初始状态 1输入拼音状态
        self.page = 1  # 第几页
        self.limit = 5  # 显示几个汉字
        self.pinyin = ''
        self.word_list = []  # 候选词列表
        self.word_list_surf = None  # 候选词surface
        self.buffer_text = ''  # 联想缓冲区字符串

# #sprite group
# all_sprites = pygame.sprite.Group()
# text = Text()
# dz = Dingzhen()
# all_sprites.add(text)
# all_sprites.add(dz)
#
# # Add the input box to the sprite group
# input_box = Input()
# all_sprites.add(input_box)
#
# running = True
# #loop
# while running:
#     clock.tick(FPS)
#     #input
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RETURN:
#                 text.result = input_box.text  # 复制输入内容到 Text 实例
#                 input_box.clear_text()  # 清空输入框
#             elif input_box.active:
#                 if event.key == pygame.K_BACKSPACE:
#                     input_box.backspace()
#                 else:
#                     input_box.add_character(event.unicode)
#
#     #update
#     #Execute the update function for each object in this group
#     all_sprites.update()
#
#     #display
#     screen.fill(BLACK)
#     screen.blit(background_img, (0,0))
#     all_sprites.draw(screen)
#     #refresh
#     pygame.display.update()
#
# pygame.quit()