import pygame
import random
import math

# Определение цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW=(255, 255, 0)

# Инициализация Pygame
pygame.init()

screensize = pygame.display.list_modes()
window_width=screensize[1][0]
window_height=screensize[1][1]

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("SPACE ASSAULT")

game_width = int(window_width/2.4)
game_height = window_height

#Размер моделей
model_width=model_height=game_width//8

#Размер пули
bullet_size=(model_width)/10

#фон
background_image=pygame.image.load('source/background.jpg')
background_image=pygame.transform.scale(background_image, (game_width, game_height))

#Шрифты
font_size=model_width//5
font = pygame.font.SysFont("Verdana", font_size)
font_for_failed=pygame.font.SysFont("Creepster", font_size*5)

# Класс для звёзд
class Star:
    def __init__(self):
        self.reset()

    def update(self):
        self.y += self.speed
        if self.y > game_height:
            self.reset()

    def reset(self):
        self.x = random.randrange(game_width)
        self.y = random.randrange(-200, -50)
        self.speed = random.randrange(7, 20)

    def draw(self):
        pygame.draw.circle(screen, WHITE, (self.x + (window_width - game_width) // 2, self.y), 1)
# Базовый класс для вражеских кораблей
class EnemyShip:
    def __init__(self, speed, image_path):
        left_boundary = (window_width - game_width) // 2
        right_boundary = (window_width + game_width) // 2 - model_width

        self.x = random.randrange(left_boundary, right_boundary)
        self.y = random.randrange(-100, -40)
        self.speed = speed
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (model_width, model_height))
        self.image.set_colorkey(WHITE)
        
    def update(self):
        self.y += self.speed

    def reset(self) :
        left_boundary = (window_width - game_width) // 2
        right_boundary = (window_width + game_width) // 2 - model_width

        self.x = random.randrange(left_boundary, right_boundary)
        self.y = random.randrange(-100, -40)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
# Класс для стандартного вражеского корабля
class Cobblestone(EnemyShip):
    def __init__(self, speed):
        super().__init__(speed, 'source/cobblestone.png')
        self.speed=speed*1.5
        
    def update(self):
        super().update()
        if self.y > game_height:
            self.reset()
# Класс для вражеского корабля, который стреляет
class ShootingEnemyShip(EnemyShip):
    def __init__(self, speed):
        super().__init__(speed, 'source/spaceship_enemy.jpg') 
        self.shoot_timer = 0
        self.speed = speed/2

    def update(self):
        super().update()
        if self.y > game_height:
            self.reset()
        self.shoot_timer += 1
        if self.shoot_timer >= 90:
            bullet_x = self.x + model_width//2
            bullet_y = self.y + model_height 
            bullet_speed_x = 0 
            bullet_speed_y = bullet_size*1.5 
            self.shoot_timer = 0
            return Bullet(bullet_x, bullet_y, bullet_speed_x, bullet_speed_y)
#Класс для вражеского корабля, который двиагется по кругу
class CircularEnemyShip(EnemyShip):
    def __init__(self, speed):
        super().__init__(speed, 'source/alien.png')
        self.angle = 0
        self.radius = 200
        
    def update(self):
        self.angle += 0.075
        self.x = (window_width // 2) + (self.radius * math.cos(self.angle)) - (model_width // 2)
        self.y += self.speed*1.25
        if self.y > game_height:
            self.reset()

    def draw(self, screen):
        super().draw(screen)
# Класс для космического корабля
class Spaceship:
    def __init__(self, screen_width, screen_height):
        self.image = pygame.image.load('source/spaceship.png')
        self.image = pygame.transform.scale(self.image, (model_width, model_height))
        self.image.set_colorkey(WHITE)
        self.image_rect = self.image.get_rect()
        self.image_rect.center = (screen_width // 2, screen_height - model_height // 2)

        self.x = self.image_rect.x
        self.y = self.image_rect.y
        self.width = self.image_rect.width
        self.height = self.image_rect.height
        self.score = 0

    def draw(self, screen):
        screen.blit(self.image, self.image_rect)

    def move(self, dx):
        self.x += dx
        self.image_rect.x = self.x

        if self.x > (window_width + game_width) // 2 - self.width:
            self.x = (window_width + game_width) // 2 - self.width
        elif self.x < (window_width - game_width) // 2:
            self.x = (window_width - game_width) // 2
            
    def move_up_down(self, dy):
        self.y += dy / 1.5
        self.image_rect.y = self.y
        if self.y > game_height - self.height:
            self.y = game_height - self.height
        elif self.y < 0:
            self.y = 0
            
    def reset_position(self,screen_width, screen_height):
        self.image_rect.center = (screen_width // 2, screen_height - model_height // 2)
        self.x = self.image_rect.x
        self.y = self.image_rect.y
# Класс для пуль
class Bullet:
    def __init__(self, x, y, speed_x=0, speed_y=-(bullet_size*2)):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.y += self.speed_y

    def draw(self, screen):
        pygame.draw.rect(screen,YELLOW, (self.x, self.y, bullet_size, bullet_size * 2))

def draw_button(text, x, y, width, height):
    button_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, WHITE, button_rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=button_rect.center)
    screen.blit(text_surface, text_rect)
    return button_rect

def can_spawn_enemy(enemy_ships, new_enemy):
    for enemy in enemy_ships:
        if abs(enemy.x - new_enemy.x) < 60 and abs(enemy.y - new_enemy.y) < 60:
            return False
    return True

def main():
    pygame.mixer.music.load('source/cosmo_music.mp3')
    pygame.mixer.music.play()
    star_list = [Star() for _ in range(50)]
    enemy_ships = []
    spaceship = Spaceship(window_width, window_height)
    bullets = []
    enemy_bullets = []
    flag_start_game = False
    paused = False
    flag_start_window = False
    restart_button = None
    play_button = None
    exit_button = None
    # Таймер для спавна вражеских кораблей и уровня сложности
    spawn_timer = 0
    game_time = 0
    # Таймер для стрельбы
    bullet_timer = 0
    bullets_per_burst = 3
    burst_delay = 15

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if play_button and play_button.collidepoint(event.pos) and not flag_start_window:
                    flag_start_window=True
                    flag_start_game = True
                    spaceship.score = 0
                    enemy_ships.clear()
                    bullets.clear()
                    enemy_bullets.clear()
                    game_time = 0
                elif restart_button and restart_button.collidepoint(event.pos) and not flag_start_game:
                    flag_start_game = True
                    spaceship.score = 0
                    enemy_ships.clear()
                    bullets.clear()
                    enemy_bullets.clear()
                    game_time = 0
                    spaceship = Spaceship(window_width, window_height)
                elif exit_button and exit_button.collidepoint(event.pos):
                    pygame.quit()
                    quit()
                    
        if flag_start_game and not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                spaceship.move(-bullet_size)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                spaceship.move(bullet_size)
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                spaceship.move_up_down(-bullet_size)
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                spaceship.move_up_down(bullet_size)
            if keys[pygame.K_SPACE]:
                bullet_timer += 1
                if bullet_timer % burst_delay == 0 and len(bullets) < bullets_per_burst:
                    bullets.append(Bullet(spaceship.x + spaceship.width // 2 - bullet_size // 2, spaceship.y))
            
            window_area = pygame.Rect(0, 0, window_width, window_height)
            pygame.draw.rect(screen, BLACK, window_area) 
            
            bullets[:] = [bullet for bullet in bullets if bullet.y > 0]
            enemy_bullets[:] = [bullet for bullet in enemy_bullets if bullet.y < game_height]

            spawn_timer += 1
            game_time += 1 / 3600
            speed = 5
            if spawn_timer >= max(70 - int(game_time // 30), 20):
                speed += 0.1
                enemy_type = random.choice([Cobblestone(speed), ShootingEnemyShip(speed), CircularEnemyShip(speed)])
                if can_spawn_enemy(enemy_ships, enemy_type):
                    enemy_ships.append(enemy_type)
                spawn_timer = 0

            for star in star_list:
                star.update()

            for enemy in enemy_ships[:]:
                enemy.update()
                if isinstance(enemy, ShootingEnemyShip):
                    new_bullet = enemy.update()
                    if new_bullet:
                        enemy_bullets.append(new_bullet)
                   
            for bullet in bullets[:]:
                bullet.update()

            for enemy_bullet in enemy_bullets[:]:
                enemy_bullet.update()

            # Проверка на столкновения между пулями игрока и врагами
            for bullet in bullets[:]:
                for enemy in enemy_ships[:]:
                    if (bullet.x >= enemy.x and bullet.x <= enemy.x + model_width and bullet.y <= enemy.y + model_height and bullet.y >= enemy.y):
                        bullets.remove(bullet)
                        enemy_ships.remove(enemy)
                        spaceship.score += 1
                        break

            # Проверка на столкновения между пулями врагов и игроком
            for bullet in enemy_bullets[:]:
                bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet_size, bullet_size * 2)
                spaceship_rect = pygame.Rect(spaceship.x, spaceship.y, model_width, model_height)

                if bullet_rect.colliderect(spaceship_rect):
                    flag_start_game = False
                    break  # Выходим из цикла при столкновении

            # Проверка на столкновения между игроком и вражескими кораблями
            for enemy in enemy_ships[:]:
                if (spaceship.x < enemy.x + model_width and spaceship.x + spaceship.width > enemy.x and spaceship.y < enemy.y + model_height and spaceship.y + spaceship.height > enemy.y):
                    flag_start_game = False
                    break

            screen.blit(background_image, ((window_width - game_width) / 2, window_height - game_height))
            game_area_rect = pygame.Rect(window_width // 2 - game_width // 2, window_height // 2 - game_height // 2, game_width, game_height) 
            pygame.draw.rect(screen, WHITE, game_area_rect, 2)
            
            for star in star_list:
                star.draw()
            for enemy in enemy_ships:
                enemy.draw(screen)
            spaceship.draw(screen)
            for bullet in bullets:
                bullet.draw(screen)
            for enemy_bullet in enemy_bullets:
                enemy_bullet.draw(screen)

            score_text = font.render(f'Score: {spaceship.score}', True, WHITE)
            screen.blit(score_text, (10, 10))
        elif paused and flag_start_game:
            pause_text = font_for_failed.render("PAUSED", True, WHITE)
            screen.blit(pause_text, pause_text.get_rect(center=(game_area_rect.centerx, game_area_rect.centery)))
            exit_button = draw_button('Exit', game_area_rect.centerx - (game_width // 12), game_area_rect.centery + (game_height // 7), game_width // 6, game_height // 14)
        else:
            screen.blit(background_image, ((window_width - game_width) / 2, window_height - game_height))
            game_area_rect = pygame.Rect(window_width // 2 - game_width // 2, window_height // 2 - game_height // 2, game_width, game_height)
            pygame.draw.rect(screen, WHITE, game_area_rect, 2)
            if flag_start_window:
                failed_text = font_for_failed.render("MISSION FAILED", True, WHITE)
                screen.blit(failed_text, failed_text.get_rect(center=(game_area_rect.centerx, 2 * game_width // 8)))

                final_score_text = font.render(f'Your final score: {spaceship.score}', True, WHITE)
                screen.blit(final_score_text, final_score_text.get_rect(center=(game_area_rect.centerx, game_area_rect.centery)))

                restart_button = draw_button('Retry', game_area_rect.centerx - (game_width // 12), game_area_rect.centery + (game_height // 28), game_width // 6, game_height // 14)
                exit_button = draw_button('Exit', game_area_rect.centerx - (game_width // 12), game_area_rect.centery + (game_height // 7), game_width // 6, game_height // 14)
            else:
                name_game = font_for_failed.render("SPACE ASSAULT", True, WHITE)
                screen.blit(name_game, name_game.get_rect(center=(game_area_rect.centerx, 2 * game_width // 8)))

                play_button = draw_button('Play', game_area_rect.centerx - (game_width // 12), game_area_rect.centery + (game_height // 28), game_width // 6, game_height // 14)
                exit_button = draw_button('Exit', game_area_rect.centerx - (game_width // 12), game_area_rect.centery + (game_height // 7), game_width // 6, game_height // 14)
        pygame.display.update()
        pygame.time.Clock().tick(60)
if __name__ == '__main__':
    main()