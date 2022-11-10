import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, FONT_STYLE, GAMEOVER
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager

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
        self.running = False
    
    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def reset_all(self):
        self.obstacle_manager.reset_obstacle()
        self.game_speed = 20
        self.score = 0

    def run(self):
        # Game loop: events - update - draw
        self.reset_all()
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self)
        self.update_score()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def opening(self, half_screen_width, half_screen_height):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render('Press any key to start ....', True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (half_screen_width, half_screen_height)
        self.screen.blit(text, text_rect)
    
    def show_menu(self):
        self.screen.fill((255, 255,255))
        half_screen_height = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2
        
        if self.death_count == 0:
           self.opening(half_screen_width, half_screen_height)
        else:
            self.screen.blit(GAMEOVER, (half_screen_width - 100, half_screen_height - 100))
            


            font = pygame.font.Font(FONT_STYLE, 30)
            text = font.render("Your score: " + str(self.score), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height + 50)
            self.screen.blit(text, text_rect)

            text = font.render("Best score: " + str(self.high_score), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height + 150)
            self.screen.blit(text, text_rect)
            
            text = font.render("Total Deaths: " + str(self.death_count), True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (half_screen_width, half_screen_height + 100)
            self.screen.blit(text, text_rect)
            
            
            

        self.screen.blit(ICON, (half_screen_width - 50, half_screen_height- 140))
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

    def update_score(self):
        self.score += 1

        if self.score % 100 == 0 and self.game_speed < 500:
            self.game_speed += 5
        
        if self.score > self.total_points:
            self.total_points = self.score  

    def increased_death_count(self):
        self.death_count += 1


    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed
