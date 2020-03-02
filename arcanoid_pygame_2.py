# coding=utf-8
import os
import pygame
pygame.mixer.pre_init(44100, 16, 2, 512)
pygame.init()
window_width = 600
window_height = 660
window = pygame.display.set_mode(size=(window_width,window_height))
pygame.display.set_caption("ARCANOID")


def draw_ball(pos_x, pos_y):
    hsv = ball_color.hsva
    ball_color.hsva = (hsv[0], hsv[1], 30, hsv[3])
    pygame.draw.circle(window, ball_color, (pos_x, pos_y), ball_rad)
    ball_color.hsva = (hsv[0], hsv[1], 70, hsv[3])
    pygame.draw.circle(window, ball_color, (pos_x-1, pos_y-1), int(ball_rad*0.8))
    ball_color.hsva = (hsv[0], hsv[1], 100, hsv[3])
    pygame.draw.circle(window, ball_color, (pos_x-3, pos_y-3), int(ball_rad*0.5))
    
def draw_floor():
    hsv = floor_color.hsva     
    j = 1
    for i in range(1,floor_level-pad_y_pos-pad_size[1]+1,2):
        if hsv[2]-j>0:
            floor_color.hsva = (hsv[0], hsv[1], hsv[2]-j, hsv[3])
        pygame.draw.line(window, floor_color, (0, (pad_y_pos+pad_size[1]+i)), (window_width,(pad_y_pos+pad_size[1]+i)))
        pygame.draw.line(window, floor_color, (0, (pad_y_pos+pad_size[1]+i+1)), (window_width,(pad_y_pos+pad_size[1]+i+1)))
        j += 1
    floor_color.hsva = hsv
    
def draw_info_section():
    b = 8
    pygame.draw.rect(window, (150,150,150), (0, floor_level+1, window_width,window_height-floor_level))
    pygame.draw.polygon(window, (210,210,210), ((0, floor_level+1), (window_width,floor_level+1),(window_width-b, floor_level+b),(b, floor_level+b)))
    pygame.draw.polygon(window, (220,220,220), ((0, floor_level+2), (b,floor_level+b),(b,window_height-b),(0,window_height)))
    pygame.draw.polygon(window, (100,100,100), ((0,window_height),(b,window_height-b),(window_width-b,window_height-b),(window_width,window_height)))
    pygame.draw.polygon(window, (70,70,70), ((window_width-b,window_height-b),(window_width-b,floor_level+b+1),(window_width,floor_level+1),(window_width,window_height)))    
    
def draw_text():
    text_1 = font.render("SCORE: " + str(score), 1, (255, 255, 255))
    text_1_shadow = font.render("SCORE: " + str(score), 1, (10, 10, 10))
    text_2 = font.render("LEVEL: " + str(level), 1, (255, 255, 255))
    text_2_shadow = font.render("LEVEL: " + str(level), 1, (10, 10, 10))
    text_3 = font.render("LIVES: " + str(lives), 1, (255, 255, 255))
    text_3_shadow = font.render("LIVES: " + str(lives), 1, (10, 10, 10))
    
    window.blit(text_1_shadow, (33, 614))
    window.blit(text_1, (30, 612))
    window.blit(text_2_shadow, ((window_width // 2) - (text_2.get_width() // 2) + 3, 614))
    window.blit(text_2, ((window_width // 2) - (text_2.get_width() // 2), 612))
    window.blit(text_3_shadow, (window_width - text_3.get_width() - 30 + 3, 614))
    window.blit(text_3, (window_width - text_3.get_width() - 30, 612))
    
    if not game_start and bricks_map:
        text_4 = font.render("press SPACE to start", 1, (255, 255, 255))
        text_4_shadow = font.render("press SPACE to start", 1, (10, 10, 10))
        window.blit(text_4_shadow, (((window_width // 2) - (text_4.get_width() // 2))+3, 402))
        window.blit(text_4, (((window_width // 2 - text_4.get_width() // 2)), 400))
                     
def draw_text_2(txt, color):
    text = font.render(txt, 1, color)
    window.blit(text, (((window_width // 2 - text.get_width() // 2)), window_height // 2))
    
def draw_pad(pos_x, pos_y):
    hsv = pad_color.hsva
    pad_color.hsva = (hsv[0], hsv[1], 100, hsv[3])
    pygame.draw.rect(window, pad_color, (pos_x, pos_y, pad_size[0], pad_size[1]))
    pad_color.hsva = (hsv[0], hsv[1], 10, hsv[3])
    pygame.draw.rect(window, pad_color, (pos_x+10, pos_y, pad_size[0]-20, pad_size[1]-10))
    
def draw_brick(pos_x, pos_y, brick_type):
    if brick_type == 1:
        b = 3
        pygame.draw.rect(window, (150,150,150), (pos_x, pos_y, brick_size[0],brick_size[1]))
        pygame.draw.polygon(window, (210,210,210), ((pos_x, pos_y), (pos_x+brick_size[0]-1,pos_y),(pos_x+brick_size[0]-1-b,pos_y+b),(pos_x+b, pos_y+b)))
        pygame.draw.polygon(window, (225,225,225), ((pos_x, pos_y), (pos_x+b, pos_y+b),(pos_x+b,pos_y+brick_size[1]-1-b),(pos_x, pos_y+brick_size[1]-1)))
        pygame.draw.polygon(window, (100,100,100), ((pos_x+b+1,pos_y+brick_size[1]-1-b), (pos_x+brick_size[0]-1-b, pos_y+brick_size[1]-1-b),(pos_x+brick_size[0]-1,pos_y+brick_size[1]-1),(pos_x+1, pos_y+brick_size[1]-1)))
        pygame.draw.polygon(window, (70,70,70), ((pos_x+brick_size[0]-1-b, pos_y+brick_size[1]-1-b),(pos_x+brick_size[0]-1-b,pos_y+b),(pos_x+brick_size[0]-1,pos_y), (pos_x+brick_size[0]-1,pos_y+brick_size[1]-1)))
    if brick_type == 2:
        b = 3
        pygame.draw.rect(window, (150,150,150), (pos_x, pos_y, brick_size[0],brick_size[1]))
        pygame.draw.polygon(window, (210,210,210), ((pos_x, pos_y), (pos_x+brick_size[0]-1,pos_y),(pos_x+brick_size[0]-1-b,pos_y+b),(pos_x+b, pos_y+b)))
        pygame.draw.polygon(window, (225,225,225), ((pos_x, pos_y), (pos_x+b, pos_y+b),(pos_x+b,pos_y+brick_size[1]-1-b),(pos_x, pos_y+brick_size[1]-1)))
        pygame.draw.polygon(window, (100,100,100), ((pos_x+b+1,pos_y+brick_size[1]-1-b), (pos_x+brick_size[0]-1-b, pos_y+brick_size[1]-1-b),(pos_x+brick_size[0]-1,pos_y+brick_size[1]-1),(pos_x+1, pos_y+brick_size[1]-1)))
        pygame.draw.polygon(window, (70,70,70), ((pos_x+brick_size[0]-1-b, pos_y+brick_size[1]-1-b),(pos_x+brick_size[0]-1-b,pos_y+b),(pos_x+brick_size[0]-1,pos_y), (pos_x+brick_size[0]-1,pos_y+brick_size[1]-1)))
        pygame.draw.rect(window, (250,250,250), (pos_x+2*b, pos_y+2*b, brick_size[0]-4*b-1,brick_size[1]-4*b-1))
    if brick_type == 3:
        b = 3
        pygame.draw.rect(window, (10,10,10), (pos_x, pos_y, brick_size[0],brick_size[1]))
        pygame.draw.polygon(window, (250,250,250), ((pos_x, pos_y), (pos_x+brick_size[0]-1,pos_y),(pos_x+brick_size[0]-1-b,pos_y+b),(pos_x+b, pos_y+b)),1)
        pygame.draw.polygon(window, (250,250,250), ((pos_x, pos_y), (pos_x+b, pos_y+b),(pos_x+b,pos_y+brick_size[1]-1-b),(pos_x, pos_y+brick_size[1]-1)),1)
        pygame.draw.polygon(window, (250,250,250), ((pos_x+b+1,pos_y+brick_size[1]-1-b), (pos_x+brick_size[0]-1-b, pos_y+brick_size[1]-1-b),(pos_x+brick_size[0]-1,pos_y+brick_size[1]-1),(pos_x+1, pos_y+brick_size[1]-1)),1)
        pygame.draw.polygon(window, (250,250,250), ((pos_x+brick_size[0]-1-b, pos_y+brick_size[1]-1-b),(pos_x+brick_size[0]-1-b,pos_y+b),(pos_x+brick_size[0]-1,pos_y), (pos_x+brick_size[0]-1,pos_y+brick_size[1]-1)),1)
        
        
def fade_in():
    for i in range (64):
        fade_surface.set_alpha(i)
        window.blit(fade_surface,(0,0))
        pygame.display.flip()        
        clock.tick(fps)
           
def brick_hit(brick_x_pos, brick_y_pos):
     #касание левого верхнего угла
    if ball_x_pos < brick_x_pos and ball_y_pos < brick_y_pos:
        pass
    #касание правого верхнего угла
    if ball_x_pos > brick_x_pos + brick_size[0] and ball_y_pos < brick_y_pos:
        pass
    #касание левого нижнего угла
    if ball_x_pos < brick_x_pos and ball_y_pos > brick_y_pos + brick_size[1]:
        pass
    #   sa  w   касание правого нижнего угла
    if ball_x_pos > brick_x_pos + brick_size[0] and ball_y_pos > brick_y_pos + brick_size[1]:
        pass
    
    #касание верхней грани
    if ball_x_pos >= brick_x_pos and ball_x_pos <= brick_x_pos + brick_size[0]:
        if ball_y_pos + ball_rad >= brick_y_pos and ball_y_pos < brick_y_pos:
            vector[1] = -1
            return True            
    #касание левой грани

    if ball_y_pos >= brick_y_pos and ball_y_pos <= brick_y_pos + brick_size[1]:
        if ball_x_pos + ball_rad >= brick_x_pos and ball_x_pos + ball_rad < brick_x_pos+10:
            vector[0] = -1
            return True
    #касание правой грани

    if ball_y_pos >= brick_y_pos and ball_y_pos <= brick_y_pos + brick_size[1]:
        if ball_x_pos - ball_rad <= brick_x_pos + brick_size[0] and ball_x_pos - ball_rad > brick_x_pos + brick_size[0]-10:
            vector[0] = 1
            return True
    #касание нижней грани
    if ball_x_pos >= brick_x_pos and ball_x_pos <= brick_x_pos + brick_size[0]:
        if ball_y_pos - ball_rad <= brick_y_pos + brick_size[1] and ball_y_pos > brick_y_pos:
            vector[1] = 1
            return True
        
        
intro= True    
running = True
game_start = False
game_over = True

fade_surface = pygame.Surface((window_width,window_height))
fade_surface.fill((0,0,0))

bg_color = pygame.Color(50,50,50)

floor_color = pygame.Color(50,50,50)
floor_level = 600

font = pygame.font.Font('DATA/aressence.ttf', 30)

sound_pad_hit = pygame.mixer.Sound("DATA/hit_1.wav")
sound_brick_hit = pygame.mixer.Sound("DATA/hit_2.wav")
sound_border_hit = pygame.mixer.Sound("DATA/border_hit.wav")
sound_ball_lose = pygame.mixer.Sound("DATA/ball_lose.wav")

pad_color = pygame.Color(255, 255, 255)
pad_size = [90, 20]
pad_x_pos = int((window_width-pad_size[0])/2)
pad_y_pos = floor_level - 50
pad_moving = 'STOP'

ball_color = pygame.Color(0,0,255)
ball_rad = 10

brick_color = pygame.Color(180,180,180)
brick_size = (40,20)
bricks_map = []

with open('DATA/levels.txt', 'r') as mapFile:
    level_map = [line.strip() for line in mapFile]

fps = 60
ball_speed = 180
pad_speed = 360

vector = [0,0] #вектор движения мяча
delta = 0 #расстояние от центра мяча до угла прямоугольника. сравнивается с радиусом для определения коснулся ли мяч объекта

lives = 3
level = 1
score = 0
win = False
max_score =  0   #добавить получение из файла
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)


fullname = os.path.join('DATA', 'logo.png')
image = pygame.image.load(fullname)
image.convert_alpha()
window.blit(image,((window_width // 2) - (image.get_width() // 2),
                   (window_height // 2) - (image.get_height() // 2)))

txt = font.render("press any key", 1, (255, 255, 255))
window.blit(txt, ((window_width // 2) - (txt.get_width() // 2),
                   (window_height-(window_height // 4)) - (txt.get_height() // 2)))
pygame.display.flip()

while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass
            elif event.type == pygame.KEYDOWN:
                intro = False
        
        

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_start:
                    game_start = True
                    vector = [1,-1]
            if event.key == pygame.K_LEFT:
                pad_moving = 'LEFT'
            if event.key == pygame.K_RIGHT:
                pad_moving = 'RIGHT'
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                pad_moving = 'STOP'     
                
    if pad_moving != 'STOP':
        if pad_moving == 'LEFT' and pad_x_pos > 0:
            pad_x_pos -= int(pad_speed / fps)
        elif pad_moving == 'RIGHT' and pad_x_pos < window_width-pad_size[0]:
            pad_x_pos += int(pad_speed / fps)
            
    if not game_start:
        if not bricks_map:
            pad_x_pos = int((window_width-pad_size[0])/2)
            for i in range(14):
                s = level_map[0]
                del level_map[0]
                for j in range(15):
                    if s[j] == 'X':
                        bricks_map.append([(j*40),(i*20),1])
                    elif s[j] == 'H':
                        bricks_map.append([(j*40),(i*20),2])
                    elif s[j] == 'O':
                        bricks_map.append([(j*40),(i*20),3])
        ball_x_pos = pad_x_pos + 60
        ball_y_pos = pad_y_pos - ball_rad

    if game_start:
        
        if not bricks_map:
            if level_map[0] == 'END':
                win = True
                running = False
            del level_map[0]
            game_start = False
            level += level
            ball_speed = 180
               
        ball_x_pos += int(ball_speed / fps) * vector[0]
        ball_y_pos += int(ball_speed / fps) * vector[1]
        
        if ball_x_pos >= window_width-ball_rad:
            sound_border_hit.play()
            vector[0] = -1
        if ball_x_pos <= ball_rad:
            sound_border_hit.play()
            vector[0] = 1
        if ball_y_pos >= floor_level - (ball_rad+5):
            sound_ball_lose.play()
            pygame.time.wait(1300)
            lives -= 1
            if lives == 0:
                running = False
            else: 
                game_start = False
        if ball_y_pos <= ball_rad:
            sound_border_hit.play()
            vector[1] = 1
                  
        # проверка на касание платформы (сверху или сбоку)  
            
        #касание левого угла платформы
        if ball_x_pos < pad_x_pos and ball_y_pos < pad_y_pos:
            delta = ( (pad_x_pos-ball_x_pos)**2  + (pad_y_pos-ball_y_pos)**2)**0.5
            if ball_rad >= int(delta):
                ball_speed += 2
                sound_pad_hit.play()
                if pad_x_pos-ball_x_pos < pad_y_pos-ball_y_pos:
                    vector[0] = -1
                    vector[1] = -1
                else:
                    vector[0] = -1
                    
        #касание правого угла платформы                
        if ball_x_pos > pad_x_pos+pad_size[0] and ball_y_pos < pad_y_pos:
            delta = ( (pad_x_pos+pad_size[0]-ball_x_pos)**2  + (pad_y_pos-ball_y_pos)**2)**0.5
            if ball_rad >= int(delta):
                ball_speed += 2
                sound_pad_hit.play()
                if pad_x_pos+pad_size[0]-ball_x_pos < pad_y_pos-ball_y_pos:
                    vector[0] = 1
                    vector[1] = -1
                else:
                    vector[0] = 1
             
        #касание правой грани платформы
        if ball_y_pos >= pad_y_pos and ball_y_pos <= pad_y_pos + pad_size[1]:
             if ball_x_pos - ball_rad <= pad_x_pos + pad_size[0] and ball_x_pos - ball_rad > pad_x_pos + pad_size[0]-10:
                 sound_pad_hit.play()
                 vector[0] = 1
                
        #касание левой грани платформы
        if ball_y_pos >= pad_y_pos and ball_y_pos <= pad_y_pos + pad_size[1]:
             if ball_x_pos + ball_rad >= pad_x_pos and ball_x_pos + ball_rad < pad_x_pos+10:
                 sound_pad_hit.play()
                 vector[0] = -1          
    
        #касание верха платформы
        if ball_x_pos >= pad_x_pos and ball_x_pos <= pad_x_pos + pad_size[0]:
             if ball_y_pos + ball_rad >= pad_y_pos and ball_y_pos < pad_y_pos:
                 sound_pad_hit.play()
                 ball_speed += 1
                 vector[1] = -1
                    
        # проверка касания каждого кирпичика на уровне. если мяч коснулся, то кирпичик убирается из списка. 
        # вектор движения при этом меняется уже в самой функции brick_hit
        for id, item in enumerate(bricks_map):
            if brick_hit(item[0], item[1]):
                ball_speed += 1
                sound_brick_hit.play()
                if item[2] == 1:
                    del bricks_map[id]
                elif item[2] == 2:
                    item[2] = 1
                score += 50
                break
        if ball_speed > 480: ballspeed = 480

    window.fill(bg_color)
    draw_floor()
    draw_info_section()
    draw_text()    
    draw_ball(ball_x_pos, ball_y_pos)    
    draw_pad(pad_x_pos, pad_y_pos)    
    
    for i in bricks_map:
        draw_brick(i[0], i[1], i[2])
        
    pygame.display.flip()        
               
    clock.tick(fps)
    
    if not game_start and not bricks_map and running:
        fade_in()
    
fade_in()
    
if win:
    draw_text_2('Congratulations !',(255,255,255))
else:
    draw_text_2('GAME OVER',(255,255,255))
pygame.display.flip()
    
while game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False
        elif event.type == pygame.KEYDOWN:
            game_over = False
    
pygame.quit()
exit()