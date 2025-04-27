from pygame import *

# Класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Класс-наследник для ракеток
class Player(GameSprite):
    def update_r(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed
            
    def update_l(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_s] and self.rect.y < win_height - self.rect.height:
            self.rect.y += self.speed

# Инициализация
init()
back = (200, 255, 255)
win_width = 600
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Ping-Pong")
window.fill(back)

# Игровые переменные
game = True
finish = False
clock = time.Clock()
FPS = 60

# Создание объектов
racket1 = Player('racket.png', 30, 200, 4, 50, 150)
racket2 = Player('racket.png', 520, 200, 4, 50, 150)
ball = GameSprite('tenis_ball.png', 200, 200, 4, 50, 50)

# Шрифты и счёт
font.init()
main_font = font.Font(None, 50)
score_font = font.Font(None, 70)
lose1 = main_font.render('PLAYER 1 WINS!', True, (0, 200, 0))
lose2 = main_font.render('PLAYER 2 WINS!', True, (0, 200, 0))
restart_text = main_font.render('SPACE - Restart', True, (0, 0, 180))
exit_text = main_font.render('ESC - Exit', True, (0, 0, 180))

score1 = 0  # Левый игрок
score2 = 0  # Правый игрок

# Параметры мяча
speed_x = 3
speed_y = 3

def reset_game():
    global finish, speed_x, speed_y, score1, score2
    finish = False
    score1 = 0
    score2 = 0
    speed_x = 3
    speed_y = 3
    ball.rect.x = 200
    ball.rect.y = 200
    racket1.rect.y = 200
    racket2.rect.y = 200

# Основной игровой цикл
while game:
    # Обработка событий
    for e in event.get():
        if e.type == QUIT:
            game = False

    # Получаем состояние всех клавиш
    keys = key.get_pressed()
    
    # Обработка ESC - выход из игры
    if keys[K_ESCAPE]:
        game = False
    
    # Обработка SPACE - перезапуск при завершении игры
    if keys[K_SPACE] and finish:
        reset_game()

    # Логика игры
    if not finish:
        # Обновление позиций
        window.fill(back)
        racket1.update_l()
        racket2.update_r()
        ball.rect.x += speed_x
        ball.rect.y += speed_y

        # Коллизия с ракетками
        if sprite.collide_rect(racket1, ball):
            ball.rect.left = racket1.rect.right
            speed_x = abs(speed_x)
        
        if sprite.collide_rect(racket2, ball):
            ball.rect.right = racket2.rect.left
            speed_x = -abs(speed_x)
        
        # Отскок от верхней/нижней границы
        if ball.rect.bottom > win_height or ball.rect.top < 0:
            speed_y *= -1

        # Проверка проигрыша и обновление счёта
        if ball.rect.x < -50:  # Мяч ушёл за левую ракетку
            score2 += 1  # Очко правому игроку
            ball.rect.x = 300
            ball.rect.y = 250
            speed_x = 3
            speed_y = 3
            
        if ball.rect.x > win_width + 50:  # Мяч ушёл за правую ракетку
            score1 += 1  # Очко левому игроку
            ball.rect.x = 300
            ball.rect.y = 250
            speed_x = 3
            speed_y = 3

        # Проверка победы
        if score1 >= 3 or score2 >= 3:
            finish = True

        # Отрисовка объектов
        racket1.reset()
        racket2.reset()
        ball.reset()

        # Отрисовка счёта с тенью
        score_display = score_font.render(f"{score1} : {score2}", True, (0, 0, 0))
        window.blit(score_display, (win_width//2 - 50, 20))

    # Экран завершения игры
    if finish:
        window.fill(back)
        if score1 >= 3:
            window.blit(lose1, (200, 200))  # Победил левый игрок (Player 1)
        else:
            window.blit(lose2, (200, 200))  # Победил правый игрок (Player 2)
        window.blit(restart_text, (200, 250))
        window.blit(exit_text, (200, 300))

    # Обновление экрана
    display.update()
    clock.tick(FPS)

quit()
