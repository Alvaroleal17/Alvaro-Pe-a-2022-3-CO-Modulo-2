import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, DEFAULT_TYPE, GAMEOVER
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.message import draw_message

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.score = 0
        self.total_points = 0
        self.death_count = 0
        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.running = False

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        # Game loop: events - update - draw
        self.reset_all()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.power_up_manager.update(self)
        self.update_score()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.draw_power_up_time()
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def show_menu(self):
        self.screen.fill((255, 255,255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        
        if self.death_count == 0:
            draw_message('Press any key to restart ...', self.screen)
        else:
            draw_message('Press any key to restart ...', self.screen)
            draw_message(f'Your Score: {self.score}', self.screen, pos_y_center = half_screen_height + 50)
            draw_message(f'Best Score: {self.total_points}', self.screen, pos_y_center = half_screen_height + 100)
            draw_message(f'Total Deaths: {self.death_count}', self.screen, pos_y_center = half_screen_height + 150)
            GAMEOVER_RECT = GAMEOVER.get_rect()
            GAMEOVER_RECT.center = (half_screen_width, half_screen_height)
            self.screen.blit(GAMEOVER, (GAMEOVER_RECT.x, GAMEOVER_RECT.y - 100))
           

        pygame.display.update()
        self.handle_events_on_menu()

    def handle_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def draw_score(self):
       font = pygame.font.Font(FONT_STYLE, 30)
       text = font.render(f'Score: {self.score}', True, (0, 0, 0))
       text_rect = text.get_rect()
       text_rect.center = (1000, 50)
       self.screen.blit(text, text_rect)

    def draw_power_up_time(self):
        if self.player.has_power_up:
            time_to_show = round((self.player.power_time_up - pygame.time.get_ticks())/1000, 2)
            if time_to_show >= 0:
                draw_message(
                    f'{self.player.type} enable for {time_to_show} seconds',
                    self.screen,
                    font_size=18,
                    pos_x_center = 500,
                    pos_y_center = 50
                )
            else:
                self.player.has_power_up = False
                self.player.type = DEFAULT_TYPE

    def update_score(self):
        if self.score % 100 == 0 and self.game_speed < 500:
            self.game_speed += 5
        self.score += 1   
        if self.score > self.total_points:
            self.total_points = self.score  

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def reset_all(self):
        self.obstacle_manager.reset_obstacle()
        self.power_up_manager.reset_power_ups()
        self.playing = True
        self.game_speed = 20
        self.score = 0
