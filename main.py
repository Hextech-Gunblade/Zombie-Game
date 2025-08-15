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
        self.direction = 1 # หันหน้าไปทางซ้าย
        self.step_count = 0 # ตัวนับการเคลื่อนไหว (ใช้เปลี่ยนภาพอนิเมชัน , คล้ายๆ Array Walk)

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
            self.rect.move_ip(-BASE_SPEED,0) # เคลื่อนที่ไปทางซ้าย


hero = Hero() # สร้างออบเจ็กต์ตัวละครผู้เล่น
all_sprites =  pygame.sprite.Group() #ไม่รู้
all_sprites.add(hero) #ไม่รู้

#สร้างฉากในเกม
def draw_window(display , background , hero):
    #สร้าง Background
    display.blit(background,(0,0))
    #สร้่าง Hero
    current_hero_sprite = hero.walk_animation[0] #ไม่รู้
    display.blit(current_hero_sprite, hero.rect) #ไม่รู้
    pygame.display.update()#ไม่รู้

#Game Loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    draw_window(DISPLAY, BG , hero) #ไม่รู้
    hero.move() #ไม่รู้
    print(time.time()) #ไม่รู้
    FPS.tick(60) #ไม่รู้