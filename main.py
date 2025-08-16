import pygame, sys, os, random, time 
from pygame.locals import * # import ทุกอย่างจาก pygame local 

pygame.init() #ติดตั้ง pygame

#ค่าต่างๆ
SIZE = WIDTH , HEIGHT  = (1000 , 600)
DISPLAY = pygame.display.set_mode(SIZE) # set ขนาดหน้่าจอ
FPS = pygame.time.Clock() #FPS ของเกม

BASE_SPEED = 7 #ความเร็วที่ตัวละครเราเดินได้
BASE_HEALTH = 300 #พลังชีวิต

GREEN_SCREEN  = (0,255,0) # ตัวแปรเก็บค่าสีเขียว
RED_SCREEN = (255,0,0) # แดง
RED_OVERLAY = (255,50,50) # แดงเข้ม
BG = pygame.image.load(os.path.join("Assets\GrassField.png")).convert() #ตัวแปรเก็บ BackGround
FONT = pygame.font.SysFont('Arial', 60) #ตัวแปรเก็บ Font

score = 0 

# ตัวละคร
class Character(pygame.sprite.Sprite): # คลาสพื้นฐาน (template) ของตัวละคร
    def __init__(self, type): # ไม่รู้
        super().__init__() # ไม่รู้
        self.walk_animation = [ # list สำหรับเก็บไฟล์ ภาพตอนเดินสถานะต่างๆ
            pygame.image.load(os.path.join("Assets",type,f"{type}_Standing.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets",type,f"{type}_L_Step.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets",type,f"{type}_Standing.png")).convert_alpha(),
            pygame.image.load(os.path.join("Assets",type,f"{type}_R_Step.png")).convert_alpha(),
        ]
        self.surface = pygame.Surface((100 , 150)) #ตั้งขนาด Character
        self.direction = 1 # หันหน้าไปทางขวา
        self.step_count = 0 # ตัวนับการเคลื่อนไหว (ใช้เปลี่ยนภาพอนิเมชัน , คล้ายๆ Array Walk)

class Zombie(Character):
    def __init__(self):
        Character.__init__(self,"Zombie")
        self.rect = self.surface.get_rect(center = ( random.randint(50,WIDTH-50) , random.randint(75,HEIGHT-75)))
        self.x_speed = random.randint(1,5)
        self.y_speed = random.randint(1,5)
    def move(self):
        self.step_count %= 59
        self.rect.move_ip(self.x_speed , self.y_speed)
        if(self.rect.right > WIDTH) or (self.rect.left < 0) :
            self.x_speed *= -1
            self.direction *= -1

        if(self.rect.bottom > HEIGHT) or (self.rect.top < 0):
            self.y_speed *= -1
        
        self.step_count += 1
            

class Hero(Character): # Class สำหรับสร้าง Hero (มาจาก Character)
    def __init__(self): #ไม่รู้
        Character.__init__(self , "Hero") #ไม่รู้
        self.hurt = pygame.image.load(os.path.join("Assets" , "Hero" , "Hero_Hurt.png")) # สถานะตอนเจ็บ
        self.rect = self.surface.get_rect(center = (WIDTH/2,HEIGHT/2)) #จุดเกิดตัวละคร (ตรงกลาง)
        self.x_speed = BASE_SPEED #ความเร็ว
        self.y_speed = BASE_SPEED #ความเร็ว
        self.health = BASE_HEALTH #พลังชีวิต

    def move(self): # Function เดิน
        pressed_keys = pygame.key.get_pressed() # เก็บสถานะกดปุ่ม <-
        if self.rect.left > 0 and pressed_keys[K_LEFT]: #ถ้ายังไม่ติดขอบ และ กด <- อยู่
            if self.direction == 1 :
                self.step_count = 0
            self.direction = 0
            self.step_count += 1
            self.rect.move_ip(-BASE_SPEED,0) # เคลื่อนที่ไปทางซ้าย
        if self.rect.right < WIDTH  and pressed_keys[K_RIGHT]: #ถ้ายังไม่ติดขอบ และ กด <- อยู่
            if self.direction == 0 :
                self.step_count = 0
            self.direction = 1
            self.step_count += 1
            self.rect.move_ip(+BASE_SPEED,0) # เคลื่อนที่ไปทางซ้าย
        if self.rect.top > 0 and pressed_keys[K_UP]:
            self.rect.move_ip(0,-BASE_SPEED)
        if self.rect.top < HEIGHT and pressed_keys[K_DOWN]:
            self.rect.move_ip(0,+BASE_SPEED)

        self.step_count %= 60 
        

hero = Hero() # สร้างออบเจ็กต์ตัวละครผู้เล่น
zombie = Zombie()
zombie_count = 1
zombies = pygame.sprite.Group()
zombies.add(zombie)
all_sprites =  pygame.sprite.Group() #ไม่รู้
all_sprites.add(zombie ,hero) #ไม่รู้


#สร้างฉากในเกม
def draw_window(display , background , hero , zombies):
    #วาด Background
    display.blit(background,(0,0)) 
    #วาด Zombie
    for character in zombies :
        current_zomb_sprite = character.walk_animation[character.step_count//15]
        if character.direction == -1:
            current_zomb_sprite = pygame.transform.flip(current_zomb_sprite,True,False)
        display.blit(current_zomb_sprite,character.rect)
    #Collision
    if pygame.sprite.spritecollideany(hero, zombies):
        hero.health -= 1
        current_hero_sprite = hero.hurt
        display.fill(RED_OVERLAY , special_flags = BLEND_MULT)
    else :
        current_hero_sprite = hero.walk_animation[hero.step_count//15] 
    #วาด Hero
    if hero.direction == 0: #หันขวา
        current_hero_sprite = pygame.transform.flip(current_hero_sprite, True, False)
    #หลอดเลือด
    pygame.draw.rect(display,RED_SCREEN, (20,20,300,20))
    pygame.draw.rect(display,GREEN_SCREEN, (20,20 , hero.health, 20))
    
     #ไม่รู้ 
    display.blit(current_hero_sprite, hero.rect) #ไม่รู้
    score_text = FONT.render(f"TIME SURVIVED : {score//60}" , True, (200,200,200))
    display.blit(score_text , (WIDTH/2,20))
    pygame.display.update()#ไม่รู้

# จบเกม
def game_over():
    #render ข้อความ
    while True :
        game_over_text = FONT.render("GAME OVER",True,(200,200,200))
        end_score_text = FONT.render(f"SCORE : {score//60} SECONDS",True,(200,200,200))
        zombie_count_text = FONT.render(f"AMOUNT OF ZOMBIES : {zombie_count}",True,(200,200,200))
        press_text = FONT.render(f"PRESS ENTER OR EXIT TO EXIT",True,(200,200,200))
        #วาดข้อความ
        DISPLAY.fill((0,0,0))
        DISPLAY.blit(game_over_text, (WIDTH/2 - game_over_text.get_width()/2 , 100))
        DISPLAY.blit(end_score_text, (WIDTH/2 - end_score_text.get_width()/2 , 200))
        DISPLAY.blit(zombie_count_text, (WIDTH/2 - zombie_count_text.get_width()/2 , 300))
        DISPLAY.blit(press_text, (WIDTH/2 - press_text.get_width()/2 , 400))
        for chara in all_sprites:
            chara.kill()
        pygame.display.update()
        for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        pygame.quit()
                        sys.exit()



#Event
SPAWN_ZOMB = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ZOMB , 7000)

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SPAWN_ZOMB:
            new_zombie = Zombie()
            zombies.add(new_zombie)
            all_sprites.add(new_zombie)
            zombie_count += 1
    draw_window(DISPLAY, BG , hero, zombies) #ไม่รู้

    if(hero.health <= 0):
        game_over()

    score += 1

    for chara in all_sprites :
        chara.move()

    FPS.tick(60) #ไม่รู้