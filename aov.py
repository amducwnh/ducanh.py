import pygame
import math

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 120, 255)
RED = (255, 50, 50)
GREEN = (0, 255, 0)
GRASS = (34, 139, 34)
BLACK = (0, 0, 0)

class Champion:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.speed = 5
        self.size = 40
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self, keys):
        if keys[pygame.K_a] and self.x > 0: self.x -= self.speed
        if keys[pygame.K_d] and self.x < WIDTH - self.size: self.x += self.speed
        if keys[pygame.K_w] and self.y > 0: self.y -= self.speed
        if keys[pygame.K_s] and self.y < HEIGHT - self.size: self.y += self.speed
        self.rect.topleft = (self.x, self.y)

    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, self.rect)

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.hp = 100
        self.max_hp = 100

    def draw(self, surface):
        if self.hp > 0:
            # Vẽ kẻ địch
            pygame.draw.rect(surface, BLACK, self.rect)
            # Vẽ thanh máu
            hp_ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, RED, (self.rect.x, self.rect.y - 10, 40, 5))
            pygame.draw.rect(surface, GREEN, (self.rect.x, self.rect.y - 10, 40 * hp_ratio, 5))

class Skillshot:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x, self.y = start_x, start_y
        self.speed, self.radius = 12, 10
        angle = math.atan2(target_y - start_y, target_x - start_x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius*2, self.radius*2)

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, surface):
        pygame.draw.circle(surface, RED, (int(self.x), int(self.y)), self.radius)

player = Champion(100, HEIGHT // 2)
dummy = Enemy(600, HEIGHT // 2) # Tạo một mục tiêu đứng yên
skills = []

running = True
while running:
    screen.fill(GRASS)
    
    keys = pygame.key.get_pressed()
    player.move(keys)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: 
            mx, my = pygame.mouse.get_pos()
            skills.append(Skillshot(player.x + 20, player.y + 20, mx, my))

    for skill in skills[:]:
        skill.update()
        skill.draw(screen)
        
        # Xử lý va chạm: Nếu chiêu chạm vào kẻ địch
        if dummy.hp > 0 and skill.rect.colliderect(dummy.rect):
            dummy.hp -= 20 # Trừ 20 máu
            skills.remove(skill) # Chiêu biến mất khi trúng mục tiêu
            continue
            
        if not (0 <= skill.x <= WIDTH and 0 <= skill.y <= HEIGHT):
            skills.remove(skill)

    player.draw(screen)
    dummy.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
