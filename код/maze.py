from pygame import *

'''Необхідні класи'''
 
#клас-батько для спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        #кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 20:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 20:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 400:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 30:
            self.direction = "right"
        if self.rect.x >= 600:
            self.direction = "left"
        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
            
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.haight = wall_height
        self.image =Surface((self.width, self.haight))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#Ігрова сцена:
win_width = 700
win_height = 500
 
window = display.set_mode((win_width, win_height))
display.set_caption("Maze")
background = transform.scale(image.load("картинки/background.jpg"), (win_width, win_height))
 
k1_get = False
k2_get = False

final_get = False

fon_lose = rect.Rect(0, 0, win_width, win_height)
fon_won = rect.Rect(0, 0, win_width, win_height)

#Персонажі гри:
player = Player('картинки/мауглі.png', 300, win_height - 80, 2)
monster = Enemy('картинки/змія.png', win_width - 80, 280, 2)
final = GameSprite('картинки/background.png', win_width - 120, win_height - 80, 0)
key_1 = GameSprite('картинки/ключ_синій.png', win_width - 660, win_height - 410, 0)
key_2 = GameSprite('картинки/ключ_жовтий.png', win_width - 300, win_height - 475, 0)

w1 = Wall(7, 242, 76, 690, 0, 10, 500)
w2 = Wall(7, 242, 76, 540, 350, 10, 150)
w3 = Wall(7, 242, 76, 140, 350, 400, 10)
w4 = Wall(7, 242, 76, 140, 100, 10, 160)
w5 = Wall(7, 242, 76, 300, 100, 250, 10)
w6 = Wall(7, 242, 76, 380, 0, 10, 100)
w7 = Wall(7, 242, 76, 300, 250, 150, 10)
w8 = Wall(7, 242, 76, 550, 250, 150, 10)
w9 = Wall(7, 242, 76, 0, 170, 150, 10)
w10 = Wall(7, 242, 76, 0, 490, 700, 10)
w11 = Wall(7, 242, 76, 380, 110, 10, 140)
w12 = Wall(7, 242, 76, 0, 0, 10, 500)
w13 = Wall(7, 242, 76, 0, 0, 700, 10)

w_list = [w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13]

w_key_1 = Wall(3, 3, 252, 550, 350, 140, 10)
w_key_2 = Wall(232, 252, 3, 550, 365, 140, 10)

finish = False
game = True
clock = time.Clock()
FPS = 60

font.init()
f1 = font.Font(None, 56)
f2 = font.Font(None, 36)
 
#музика
mixer.init() # Створює музичний плеєр
mixer.music.load('музика/jungles.ogg') # завантажує музику
mixer.music.play(-1) # зациклює і програє її
 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
 
        window.blit(background,(0, 0))
        player.reset()
        monster.reset()

        if not k1_get:
            key_1.reset()
            w_key_1.reset()
        if not k2_get:
            key_2.reset()
            w_key_2.reset()

        if not final_get:
            final.reset()

        for w in w_list:
            w.reset()
            if player.rect.colliderect(monster.rect) or player.rect.colliderect(w.rect):
                mixer.music.stop()
                finish = True
                draw.rect(window, (255, 170, 0), fon_lose)
                lose = f2.render("Не переживай, в грі ще багато раундів!", True, (0, 0, 0))
                window.blit(lose, (130, 245))
                break

        if (player.rect.colliderect(w_key_1.rect) and not k1_get) or (player.rect.colliderect(w_key_2.rect) and not k2_get):
            mixer.music.stop()
            finish = True
            a = f1.render("Потрібно взять ключ!", True, (200, 50, 50))
            window.blit(a, (10, 200))
        
        if player.rect.colliderect(key_1.rect):
            k1_get = True

        if player.rect.colliderect(key_2.rect):
            k2_get = True

        if player.rect.colliderect(final.rect):
            final_get = True
            finish = True
            mixer.music.stop()
            draw.rect(window, (34, 255, 0), fon_won)
            lose = f1.render("Ти виграв!", True, (0, 0, 0))
            window.blit(lose, (250, 230))

        player.update()
        monster.update()

        display.update()
    clock.tick(FPS)