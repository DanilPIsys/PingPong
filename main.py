
import pygame
from random import *

pygame.init()


class Hitbox():

    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw_hitbox(self, frame):
        pygame.draw.rect(screen, self.color, self.rect, frame)
    def is_clicked(self, mouse_position):
        return self.rect.collidepoint(mouse_position[0], mouse_position[1])

class Picture(Hitbox):
    def __init__(self, x, y, width, height, color, path):
        Hitbox.__init__(self, x, y, width, height, color)
        self.path = path
        if self.path != None:
            self.image = pygame.transform.scale(pygame.image.load(self.path), (self.width, self.height))
            self.right_image = self.image
            self.left_image = pygame.transform.flip(self.image, True, False)
        if self.path == None:
            self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_picture(self):
        if self.path != None:
            screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.path == None:
            pygame.draw.rect(screen, self.color, self.rect)


class Player(Picture):
    def __init__(self, x, y, width, height, color, path, speed, health):
        Picture.__init__(self, x, y, width, height, color, path)
        self.speed = speed
        self.sspeed = speed
        self.dx = 0
        self.dy = 0
        self.delta = 1
        self.health = health
        self.durspeed = speed - 1
        self.durpoint = 0
        self.durability = False
    
    def move(self):
        self.rect.x += int(self.speed * self.dx * self.delta)
        self.rect.y += int(self.speed * self.dy * self.delta)
    
    def normalize(self):
        if self.dx * self.dy != 0:
            self.delta = 1 / (2 ** 0.5)
        else:
            self.delta = 1
    
    def controller(self, player_id):
        keys = pygame.key.get_pressed()

        if player_id == 1:
            if keys[pygame.K_w] and not keys[pygame.K_s]:
                self.dy = -1 - self.speed
            elif keys[pygame.K_s] and not keys[pygame.K_w]:
                self.dy = 1 + self.speed
            else:
                self.dy = 0

        elif player_id == 2:
            if keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                self.dy = -1 - self.speed
            elif keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
                self.dy = 1 + self.speed
            else:
                self.dy = 0
        
        if self.rect.y < 0:
            self.rect.y = 0
            self.rect.y += 1
        if self.rect.y > 426:
            self.rect.y = 426
            self.rect.y -= 1
    
    def auto_controller(self, enemy):
        if enemy.rect.x > 400:
            if not self.rect.centery == enemy.rect.centery:
                if self.rect.y > enemy.rect.y:
                    self.dy = -1 - self.speed
                elif self.rect.y < enemy.rect.y:
                    self.dy = 1 + self.speed
                else:
                    self.dy = 0
            if self.rect.centery == enemy.rect.centery:
                self.dy = 0
                self.rect.centery == enemy.rect.centery
        else:
            self.dy = 0
    
    def collideb(self, bul):
        if self.rect.left == bul.rect.left and (bul.rect.y - self.rect.y) < 74 and (self.rect.y - bul.rect.y) < 8:
            self.durability = True

        if self.durability == True:
            if self.durpoint < 300:
                self.speed = self.durspeed
                self.durpoint += 1
            if self.durpoint >= 300:
                self.durpoint = 0
                self.durability = False
                self.speed = self.sspeed


class Enemy(Picture):
    def __init__(self, x, y, width, height, color, path, speed):
        Picture.__init__(self, x, y, width, height, color, path)
        self.speed = speed
        self.dx = int(choice(['-1', '1']))
        self.dy = 0
        self.delta = 1
        self.normal_speed = self.dx
    
    def move(self):
        self.rect.x += int(self.speed * self.dx * self.delta)
        self.collide_player(players, 'horizontal')
        self.collide_wall(wlist, 'horizontal')
        self.rect.y += int(self.speed * self.dy * self.delta)
        self.collide_player(players, 'vertical')
        self.collide_wall(wlist, 'vertical')
    
    def normalize(self):
        if self.dx * self.dy != 0:
            self.delta = 1 / (2 ** 0.5)
        else:
            self.delta = 1

    def moving(self, start, stop):
        global skipped_title
        if self.rect.bottom < start:
            self.rect.bottom = start
            self.dy /= 500
            self.dy *= -1
        #elif self.rect.top > stop:
        #    self.rect.top = stop
        #    self.dy *= -1
        elif self.rect.top > stop:
            skipped_title += 1
            self.rect.top = stop
            self.rect.x = randint(20, 600)
            self.speed += randint(-1, 1)
            if self.speed > 4:
                self.speed -= randint(1, 2)
            elif self.speed == 0:
                self.speed += 1
            self.dy *= -500
    
    def collide_player(self, players, direction):
        keys = pygame.key.get_pressed()
        for sprite in players:
            if self.rect.colliderect(sprite.rect):
                if direction == 'vertical':
                    if self.dy < 0:
                        self.rect.top = sprite.rect.bottom
                        self.dy *= -1
                    elif self.dy > 0:
                        self.rect.bottom = sprite.rect.top
                        self.dy *= -1
                if direction == 'horizontal':
                    if self.dx < 0:
                        self.rect.left = sprite.rect.right
                        self.dx *= -1
                        self.dx *= (1 + 0.06)
                        if sprite.dy < 0:
                            self.rect.left = sprite.rect.right
                            if self.dy < 0:
                                self.dy *= -1
                            self.dy = -1 - self.speed * (1 - 0.8)
                        if sprite.dy > 0:
                            self.rect.left = sprite.rect.right
                            if self.dy > 0:
                                self.dy *= -1
                            self.dy = 1 + self.speed * (1 - 0.8)

                        if players.index(sprite) == 0:
                            if keys[pygame.K_a] and not keys[pygame.K_d]:
                                self.dy = -1 - sprite.speed
                            if keys[pygame.K_d] and not keys[pygame.K_a]:
                                self.dy = 1 + sprite.speed
                        if players.index(sprite) == 1:
                            if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
                                self.dy = -1 - sprite.speed
                            if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
                                self.dy = 1 + sprite.speed
                    elif self.dx > 0:
                        self.rect.right = sprite.rect.left
                        self.dx *= -1
                        self.dx *= (1 + 0.06)
        
    def collide_scene(self):
        global oldright
        global oldleft
        global left_score
        global right_score

        if self.rect.y < 0:
            self.rect.y = 0
            self.dy *= -1
        elif self.rect.y > 460:
            self.rect.y = 460
            self.dy *= -1

        if self.rect.x < -50:
            if 1 > (right_score - oldright):
                right_score += 1
            if self.rect.x < -250:
                self.rect.y = 220
                self.rect.x = 320
                self.dx = self.normal_speed
                self.dx *= -1
                oldright += 1
        elif self.rect.x > 750:
            if 1 > (left_score - oldleft):
                left_score += 1
            if self.rect.x > 950:
                self.rect.y = 220
                self.rect.x = 320
                self.dx = self.normal_speed
                self.dx *= -1
                oldleft += 1
    
    def collide_wall(self, walls, direction):
        keys = pygame.key.get_pressed()
        for sprite in walls:
            if self.rect.colliderect(sprite.rect):
                if direction == 'vertical':
                    if self.dy < 0:
                        self.rect.top = sprite.rect.bottom
                        self.dy *= -1
                    elif self.dy > 0:
                        self.rect.bottom = sprite.rect.top
                        self.dy *= -1
                if direction == 'horizontal':
                    if self.dx < 0:
                        self.rect.left = sprite.rect.right
                        self.dx *= -1
                        if self.dy < 0:
                            self.rect.left = sprite.rect.right
                            if self.dy < 0:
                                self.dy *= -1
                            self.dy = -1 - self.speed * (1 - 0.8)
                        if self.dy > 0:
                            self.rect.left = sprite.rect.right
                            if self.dy > 0:
                                self.dy *= -1
                            self.dy = 1 + self.speed * (1 - 0.8)
                    elif self.dx > 0:
                        self.rect.right = sprite.rect.left
                        self.dx *= -1


class Font():
    def __init__(self, x, y, size, color, title):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.title = title
        self.main_font = pygame.font.SysFont(None, size)
        self.text = self.main_font.render(self.title, True, color)
    
    def write_text(self):
        screen.blit(self.text, (self.rect.x, self.rect.y))


class Bullet(Picture):
    def __init__(self, x, y, width, height, color, path, speed):
        Picture.__init__(self, x, y, width, height, color, path)
        self.pl = p1
        self.speed = speed
        self.dx = 1
        self.dy = 0
        self.delta = 1
    
    def move(self):
        self.rect.x += int(self.speed * self.dx * self.delta)
        self.rect.y += int(self.speed * self.dy * self.delta)
    
    def normalize(self):
        if self.dx * self.dy != 0:
            self.delta = 1 / (2 ** 0.5)
        else:
            self.delta = 1

class Wall():
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw_card(self):
        pygame.draw.rect(screen, self.color, self.rect)







screen_width = 700
screen_height = 500
screen_size = (screen_width, screen_height)
screen_color = (0, 0, 0)

screen = pygame.display.set_mode(screen_size)
bg = Picture(0, 0, 700, 500, (100, 0, 0), 'galaxy.jpg')

p1 = Player(50, 250, 15, 75, (41, 204, 27), None, 2, 1)
p2 = Player(650, 250, 15, 75, (41, 204, 27), None, 2, 1)
p2clone = Player(650, 250, 15, 45, (21, 130, 24), None, 1, 1)
players = [p1, p2, p2clone]

ball = Enemy(350, 250, 50, 50, (0, 0, 0), 'ufo.png', 4)

blist = list()
b = Bullet(0, 0, 14, 14, (255, 0, 0), None, 12)
wlist = list()
w = Wall(0, 0, 10, 10, (0, 85, 255))

menu = Font(310, 20, 40, (255, 255, 255), 'MENU')
menu_com = Font(332, 42+1, 24, (255, 255, 255), '(tab)')
menu_esc = Font(310, 15, 40, (204, 27, 27), 'ESCAPE')
mesc_com = Font(425, 29, 20, (204, 27, 27), '(esc)')
menu_menu = Font(55, 50, 30, (255, 255, 255), '<--(1)   -->(2)   <+(3)   +>(4)   --(5)   ++(6)   *(7)   -fps(8)   +fps(9)')


fps = 60
clock = pygame.time.Clock()





drawing = False
fpct = 'fps: 60'
shooter = False
waller = False
da = False
clone_act = 0
oldspeed_x = 0
menuopen = 0
autop2 = 0
oldright = 0
oldleft = 0
left_score = 0
right_score = 0
right_font = Font(670, 20, 42+8, (255, 255, 255), str(right_score))
left_font = Font(10, 20, 42+8, (255, 255, 255), str(left_score))
fpc = Font(330, 465, 24, (255, 255, 255), fpct)

is_on = True
while is_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_on = False

    fpct = 'fps: ' + str(fps)
    keys = pygame.key.get_pressed()

    #if shooter == True:

    bg.draw_picture()

    if keys[pygame.K_7] and shooter == True:
        b = Bullet(0, 0, 16, 16, (255, 0, 0), None, 12)
        b.rect.x = p1.rect.x
        b.rect.y = p1.rect.y + 29
        blist.append(b)

    for b in blist:
        b.draw_picture()
        b.move()
        b.normalize()
        p2.collideb(b)
        if b.rect.x > 705:
            blist.remove(b)
    
    if event.type == pygame.MOUSEBUTTONDOWN and waller == True:
        drawing = True
    elif event.type == pygame.MOUSEBUTTONUP and waller == True:
        drawing = False

    if drawing == True:
        w = Wall(0, 0, 10, 10, (0, 85, 255))
        w.rect.center = pygame.mouse.get_pos()
        #b.rect.y = p1.rect.y + 29
        wlist.append(w)

    for w in wlist:
        w.draw_card()
        #ball.collide_wall(wlist)
        if keys[pygame.K_SPACE]:
            wlist.remove(w)

    p1.draw_picture()
    p1.move()
    p1.normalize()
    p1.controller(1)
    #p1.collideb(b)
    p2.draw_picture()
    p2.move()
    p2.normalize()
    if autop2 == 0:
        p2.controller(2)

    if keys[pygame.K_o]:
        autop2 = 1
    if autop2 == 1:
        #p2.dy = 1 + p2.speed
        #if p2.rect.y < 0:
        #    p2.rect.y = 0
        #    p2.dy = 1 + p2.speed
        #if p2.rect.y > 426:
        #    p2.rect.y = 300
        #    p2.dy = -1 - p2.speed

        p2.auto_controller(ball)

    ball.draw_picture()
    ball.move()
    ball.normalize()
    ball.collide_scene()
    #ball.collide_player(p2)
    #ball.collide_player(p1)

    fpc = Font(330, 465, 24, (255, 255, 255), fpct)
    fpc.write_text()


    if right_font.rect.x > 670:
        right_font.rect.x = 670
    right_font.write_text()
    if ball.rect.x > 750:
        left_font = Font(10, 20, 42+8, (255, 255, 255), str(left_score))
    if ball.rect.x < 0:
        right_font = Font(670, 20, 42+8, (255, 255, 255), str(right_score))
    left_font.write_text()



    if keys[pygame.K_TAB]:
        menuopen = 1
    elif keys[pygame.K_ESCAPE]:
        menuopen = 0

    if menuopen == 0:
        menu.write_text()
        menu_com.write_text()
    elif menuopen == 1:
        menu_esc.write_text()
        mesc_com.write_text()
        menu_menu.write_text()
        if keys[pygame.K_1]:
            if ball.dx > 0:
                ball.dx *= -1
        elif keys[pygame.K_2]:
            if ball.dx < 0:
                ball.dx *= -1
        elif keys[pygame.K_3]:
            ball.dx -= 0.1
        elif keys[pygame.K_4]:
            ball.dx += 0.1
        elif keys[pygame.K_5]:
            ball.dy = 0
        elif keys[pygame.K_6]:
            clone_act = 1
        elif keys[pygame.K_7]:
            shooter = True
        elif keys[pygame.K_8]:
            fps -= 1
        elif keys[pygame.K_9]:
            fps += 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            waller = True
        if clone_act == 1:
            p2clone.draw_picture()
            p2clone.move()
            p2clone.normalize()
            p2clone.auto_controller(ball)


    if p2.durability == True:
        if p2.durpoint < 150:
            p2.speed = p2.durspeed
            p2.color = (55, 140, 73)
            p2.durpoint += 1
        if p2.durpoint >= 150:
            p2.durpoint = 0
            p2.durability = False
            p2.speed = p2.sspeed
            p2.color = (41, 204, 27)




    pygame.display.update()
    clock.tick(fps)