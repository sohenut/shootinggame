import pygame
import random

# 게임 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 캐릭터 클래스
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_width // 2, screen_height - 50)
        self.direction = "UP"
        self.health = 3  # 플레이어 생명 3개로 설정

    def update(self):
        keys = pygame.key.get_pressed()
        
        # 대각선 방향 처리 (2개의 키가 동시에 눌릴 경우)
        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            self.direction = "UP_LEFT"
            self.rect.x -= 5
            self.rect.y -= 5
        elif keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            self.direction = "UP_RIGHT"
            self.rect.x += 5
            self.rect.y -= 5
        elif keys[pygame.K_LEFT] and keys[pygame.K_DOWN]:
            self.direction = "DOWN_LEFT"
            self.rect.x -= 5
            self.rect.y += 5
        elif keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]:
            self.direction = "DOWN_RIGHT"
            self.rect.x += 5
            self.rect.y += 5
        elif keys[pygame.K_LEFT]:
            self.direction = "LEFT"
            self.rect.x -= 5
        elif keys[pygame.K_RIGHT]:
            self.direction = "RIGHT"
            self.rect.x += 5
        elif keys[pygame.K_UP]:
            self.direction = "UP"
            self.rect.y -= 5
        elif keys[pygame.K_DOWN]:
            self.direction = "DOWN"
            self.rect.y += 5

        # 화면 경계 체크
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

# 총알 클래스
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # 방향에 따라 이동
        if self.direction == "UP":
            self.rect.y -= 10
        elif self.direction == "DOWN":
            self.rect.y += 10
        elif self.direction == "LEFT":
            self.rect.x -= 10
        elif self.direction == "RIGHT":
            self.rect.x += 10
        elif self.direction == "UP_LEFT":
            self.rect.x -= 7  # X축으로 이동
            self.rect.y -= 7  # Y축으로 이동
        elif self.direction == "UP_RIGHT":
            self.rect.x += 7  # X축으로 이동
            self.rect.y -= 7  # Y축으로 이동
        elif self.direction == "DOWN_LEFT":
            self.rect.x -= 7  # X축으로 이동
            self.rect.y += 7  # Y축으로 이동
        elif self.direction == "DOWN_RIGHT":
            self.rect.x += 7  # X축으로 이동
            self.rect.y += 7  # Y축으로 이동

        # 화면을 벗어난 총알은 제거
        if (self.rect.right < 0 or self.rect.left > screen_width or
            self.rect.bottom < 0 or self.rect.top > screen_height):
            self.kill()


# 적 클래스
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(GREEN)  # 적 색상
        self.rect = self.image.get_rect()

        # 벽과 일정거리 떨어진 곳에서 생성되도록 설정
        margin = 50  # 벽과 떨어질 최소 거리 (원하는 거리로 조정 가능)
        
        # 상단, 하단, 좌측, 우측 경계 중 하나를 선택하여 생성
        side = random.choice(['top', 'bottom', 'left', 'right'])
        
        if side == 'top':
            self.rect.x = random.randint(margin, screen_width - margin)
            self.rect.y = margin  # 상단 벽에서 일정 거리 떨어진 곳에 생성
        elif side == 'bottom':
            self.rect.x = random.randint(margin, screen_width - margin)
            self.rect.y = screen_height - margin  # 하단 벽에서 일정 거리 떨어진 곳에 생성
        elif side == 'left':
            self.rect.x = margin  # 왼쪽 벽에서 일정 거리 떨어진 곳에 생성
            self.rect.y = random.randint(margin, screen_height - margin)
        elif side == 'right':
            self.rect.x = screen_width - margin  # 오른쪽 벽에서 일정 거리 떨어진 곳에 생성
            self.rect.y = random.randint(margin, screen_height - margin)

        # 적의 이동 유형을 랜덤으로 결정: 대각선 또는 직선
        self.is_diagonal = random.choice([True, False])
        
        # 대각선 이동일 경우, 방향을 랜덤하게 설정
        if self.is_diagonal:
            self.dx = random.choice([-1, 1])  # X축 대각선 방향 (왼쪽 또는 오른쪽)
            self.dy = random.choice([-1, 1])  # Y축 대각선 방향 (위 또는 아래)
        else:
            # 직선 이동일 경우, X 또는 Y 축 방향을 랜덤으로 결정
            self.dx = random.choice([-1, 1])  # X축 직선 방향 (왼쪽 또는 오른쪽)
            self.dy = 0  # Y축은 이동하지 않음
            # 또는 Y축 직선으로만 움직일 경우:
            # self.dy = random.choice([-1, 1])  # Y축 직선 방향 (위 또는 아래)
            # self.dx = 0  # X축은 이동하지 않음

    def update(self):
        # 적이 화면을 벗어나지 않도록 처리
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.dx *= -1  # 벽에 부딪히면 X축 방향 반전
        if self.rect.top < 0 or self.rect.bottom > screen_height:
            self.dy *= -1  # 벽에 부딪히면 Y축 방향 반전

        # 적의 위치를 이동시킴 (대각선 또는 직선)
        self.rect.x += self.dx * 5  # X축 이동
        self.rect.y += self.dy * 5  # Y축 이동



# 홈 화면 표시 함수
def show_home_screen():
    font = pygame.font.Font(None, 72)
    title_text = font.render("Welcome to the Game!", True, WHITE)
    start_text = font.render("Press 'S' to Start", True, WHITE)

    # 홈 화면 그리기
    screen.fill(BLACK)
    screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, screen_height // 2 - 100))
    screen.blit(start_text, (screen_width // 2 - start_text.get_width() // 2, screen_height // 2 + 50))

    pygame.display.flip()


def game_loop(skip_home_screen=False):  # skip_home_screen 플래그 추가
    running = True
    clock = pygame.time.Clock()

    # 플레이어와 스프라이트 초기화
    player = Player()
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    all_sprites.add(player)

    bullet_timer = 0
    enemy_spawn_timer = 0

    # 홈 화면 표시 (처음 실행 시에만)
    if not skip_home_screen:
        while running:
            show_home_screen()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        # 'S'를 누르면 게임 시작
                        running = False

            pygame.time.wait(100)  # 홈 화면에서 키 입력 대기

        running = True  # 게임 시작을 위해 다시 설정
    while running:
        screen.fill(BLACK)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 플레이어와 총알 업데이트
        all_sprites.update()

        # 총알과 적의 충돌 처리
        for bullet in bullets:
            enemy_hit = pygame.sprite.spritecollide(bullet, enemies, True)  # 총알과 적이 충돌하면 적 제거
            if enemy_hit:
                bullet.kill()  # 총알도 제거

        # 플레이어와 적의 충돌 체크
        if pygame.sprite.spritecollide(player, enemies, True):  # 플레이어와 적이 충돌하면 적 제거
            player.health -= 1  # 생명 1 감소

        # 게임 오버 체크
        if player.health <= 0:
            # 게임 오버 메시지 출력
            font = pygame.font.Font(None, 72)
            game_over_text = font.render("GAME OVER", True, RED)
            screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))

            restart_text = font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
            screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 50))

            pygame.display.flip()

            # 게임 오버 후 키 입력 받기
            waiting_for_input = True
            while waiting_for_input:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        waiting_for_input = False
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            # 'R'을 눌렀을 때 게임 재시작
                            game_loop(skip_home_screen=True)  # 재시작하려면 재귀적으로 호출
                            return
                        elif event.key == pygame.K_q:
                            # 'Q'을 눌렀을 때 게임 종료
                            running = False
                            waiting_for_input = False

            break  # 게임 오버 상태에서 탈출

        # 자동 발사 로직
        bullet_timer += 1
        if bullet_timer >= 15:
            # 플레이어의 방향에 맞게 총알 발사 방향 설정
            bullet = Bullet(player.rect.centerx, player.rect.centery, player.direction)
            all_sprites.add(bullet)
            bullets.add(bullet)
            bullet_timer = 0

        # 적 생성 로직
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= 120:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            enemy_spawn_timer = 0

        # 스프라이트 그리기 및 화면 갱신
        all_sprites.draw(screen)

        # 생명 표시
        font = pygame.font.Font(None, 36)
        health_text = font.render(f"Health: {player.health}", True, WHITE)
        screen.blit(health_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

game_loop() 