import pygame
import pygame_gui
from pygame_gui.elements import UIPanel, UIButton, UILabel, UITextBox, UIWindow, UIImage
import random
import math
import time
import os

os.chdir(os.getcwd()) # Set working directory

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKBLUE = (33, 40, 45)
LIGHTBLUE = (0, 176, 240)
RED = (210, 30, 0)
ORANGE = (242, 131, 0)
YELLOW = (255, 220, 80)


class Game():
    def __init__(self):
        self.map_choice = 3
        self.is_paused = False
        self.game_started = True
        self.ball_size = 16
        self.paddle_size = 200
        self.ball_speed = 10
        self.lives = 3
        self.carryOn = True
        self.score = 0
        self.collided = False
        size = (800, 600)
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Brick breaker")

    def main_window(self):
        background = pygame.Surface((800, 600))
        background.fill(WHITE)

        manager = pygame_gui.UIManager((800, 600), "window.json")

        main_panel = UIPanel(relative_rect=pygame.Rect((0, 0), (800, 600)),
                             starting_layer_height=1,
                             manager=manager)

        button_layout = UIPanel(relative_rect=pygame.Rect((300, 80), (200, 500)),
                                starting_layer_height=1,
                                manager=manager,
                                object_id="#button_layout",
                                container=main_panel)

        # -- Draw interactive UI elements --
        bricks_label = UILabel(relative_rect=pygame.Rect((345, 5), (100, 50)),
                               text="Bricks",
                               manager=manager,
                               object_id="#bricks_label",
                               container=main_panel)

        new_game = UIButton(relative_rect=pygame.Rect((45, 55), (100, 50)),
                            text="New game",
                            manager=manager,
                            container=button_layout)

        quit_game = UIButton(relative_rect=pygame.Rect((45, 200), (100, 50)),
                             text="Exit",
                             manager=manager,
                             container=button_layout)

        # -- Confirmation pop-up --

        confirm_popup = UIWindow(rect=pygame.Rect((250, 150), (300, 160)),
                                 manager=manager,
                                 window_display_title="Confirmation",
                                 visible=False)

        yes_btn = UIButton(relative_rect=pygame.Rect((80, 50), (50, 30)),
                           text="Yes",
                           manager=manager,
                           container=confirm_popup)

        no_btn = UIButton(relative_rect=pygame.Rect((140, 50), (50, 30)),
                          text="No",
                          manager=manager,
                          container=confirm_popup)

        confirm_label = UILabel(relative_rect=pygame.Rect((0, 15), (270, 20)),
                                text="Are you sure you want to exit?",
                                manager=manager,
                                container=confirm_popup)

        # -- UI Event handling --
        clock = pygame.time.Clock()
        is_running = True

        while is_running:
            time_delta = clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == new_game:
                            is_running = False
                            self.map_choice = 3
                            self.ball_size = 16
                            self.paddle_size = 200
                            self.ball_speed = 10
                            self.options_window()
                        if event.ui_element == yes_btn:
                            self.carryOn = False
                            is_running = False
                        if event.ui_element == quit_game:
                            confirm_popup.show()
                            confirm_popup.set_blocking(True)
                        if event.ui_element == no_btn:
                            confirm_popup.hide()
                            confirm_popup.set_blocking(False)

                manager.process_events(event)

            manager.update(time_delta)
            self.screen.blit(background, (0, 0))
            manager.draw_ui(self.screen)

            pygame.display.update()

    def options_window(self):
        background = pygame.Surface((800, 600))
        background.fill(WHITE)

        manager = pygame_gui.UIManager((800, 600), 'window.json')
        manager2 = pygame_gui.UIManager((800, 600), 'window.json')

        main_panel = UIPanel(relative_rect=pygame.Rect((0, 0), (800, 600)),
                             starting_layer_height=1,
                             manager=manager)

        button_layout = UIPanel(relative_rect=pygame.Rect((300, 80), (200, 500)),
                                starting_layer_height=1,
                                manager=manager,
                                object_id= "#button_layout",
                                container=main_panel)

        # -- Draw interactive UI elements --
        back_btn = UIButton(relative_rect=pygame.Rect((25, 500), (100, 50)),
                            text="Back",
                            manager=manager,
                            container=main_panel)

        bricks_label = UILabel(relative_rect=pygame.Rect((345, 5), (100, 50)),
                               text="Bricks",
                               manager=manager,
                               object_id="#bricks_label",
                               container=main_panel)

        difficulty_label = UILabel(relative_rect=pygame.Rect((45, 25), (100, 50)),
                                   text="Difficulty",
                                   manager=manager,
                                   container=button_layout)

        easy_btn = UIButton(relative_rect=pygame.Rect((45, 100), (100, 50)),
                            text="Easy",
                            manager=manager,
                            container=button_layout,
                            tool_tip_text="Large ball, large paddle, small brick field and slow movement")

        medium_btn = UIButton(relative_rect=pygame.Rect((45, 200), (100, 50)),
                              text="Medium",
                              manager=manager,
                              container=button_layout,
                              tool_tip_text="Medium ball, medium paddle, medium brick field and normal movement")

        hard_btn = UIButton(relative_rect=pygame.Rect((45, 300), (100, 50)),
                            text="Hard",
                            manager=manager,
                            container=button_layout,
                            tool_tip_text="Small ball, small paddle, large brick field and fast movement")

        custom_btn = UIButton(relative_rect=pygame.Rect((45, 400), (100, 50)),
                              text="Custom",
                              manager=manager,
                              container=button_layout)

        # -- Window for custom settings --
        custom_window = UIWindow(rect=pygame.Rect((150, 50), (500, 500)),
                                 manager=manager2,
                                 window_display_title="Custom settings",
                                 visible=False)

        custom_close_btn = UIButton(relative_rect=pygame.Rect((280, 370), (100, 50)),
                                    text="Cancel",
                                    manager=manager2,
                                    container=custom_window)

        sticksize_label = UILabel(relative_rect=pygame.Rect((70, 25), (100, 20)),
                                  text="Stick size",
                                  manager=manager2,
                                  container=custom_window)

        ballsize_label = UILabel(relative_rect=pygame.Rect((300, 25), (100, 20)),
                                 text="Ball size",
                                 manager=manager2,
                                 container=custom_window)

        brickfieldsize_label = UILabel(relative_rect=pygame.Rect((70, 250), (100, 20)),
                                       text="Field size",
                                       manager=manager2,
                                       container=custom_window)

        ballspeed_label = UILabel(relative_rect=pygame.Rect((300, 250), (100, 20)),
                                  text="Ball speed",
                                  manager=manager2,
                                  container=custom_window)

        reduce_sticksize = UIButton(relative_rect=pygame.Rect((10, 75), (80, 40)),
                                    text="",
                                    object_id="#arrow_reduce",
                                    manager=manager2,
                                    container=custom_window)

        grow_sticksize = UIButton(relative_rect=pygame.Rect((150, 75), (80, 40)),
                                  text="",
                                  object_id="#arrow_grow",
                                  manager=manager2,
                                  container=custom_window)

        stick_image = UIImage(relative_rect=pygame.Rect((100, 85), (40, 20)),
                              image_surface=pygame.image.load("stick.png"),
                              manager=manager2,
                              container=custom_window)

        reduce_ballsize = UIButton(relative_rect=pygame.Rect((250, 75), (80, 40)),
                                   text="",
                                   object_id="#arrow_reduce",
                                   manager=manager2,
                                   container=custom_window)

        grow_ballsize = UIButton(relative_rect=pygame.Rect((380, 75), (80, 40)),
                                 text="",
                                 object_id="#arrow_grow",
                                 manager=manager2,
                                 container=custom_window)

        ball_image = UIImage(relative_rect=pygame.Rect((335, 80), (40, 40)),
                             image_surface=pygame.image.load("ball.png"),
                             manager=manager2,
                             container=custom_window)

        reduce_fieldsize = UIButton(relative_rect=pygame.Rect((10, 300), (80, 40)),
                                    text="",
                                    object_id="#arrow_reduce",
                                    manager=manager2,
                                    container=custom_window)

        grow_fieldsize = UIButton(relative_rect=pygame.Rect((150, 300), (80, 40)),
                                  text="",
                                  object_id="#arrow_grow",
                                  manager=manager2,
                                  container=custom_window)

        field_image = UILabel(relative_rect=pygame.Rect((95, 300), (50, 40)),
                              text="Large",
                              manager=manager2,
                              container=custom_window)

        reduce_ballspeed = UIButton(relative_rect=pygame.Rect((250, 300), (80, 40)),
                                    text="",
                                    object_id="#arrow_reduce",
                                    manager=manager2,
                                    container=custom_window)

        grow_ballspeed = UIButton(relative_rect=pygame.Rect((380, 300), (80, 40)),
                                    text="",
                                    object_id="#arrow_grow",
                                    manager=manager2,
                                    container=custom_window)

        ballspeed_image = UILabel(relative_rect=pygame.Rect((335, 300), (40, 40)),
                                  text="2x",
                                  manager=manager2,
                                  container=custom_window)

        start_game_custom = UIButton(relative_rect=pygame.Rect((100, 370), (100, 50)),
                                     text="Start",
                                     manager=manager2,
                                     container=custom_window)

        # -- UI Event handling --
        clock = pygame.time.Clock()
        is_running = True

        while is_running:
            time_delta = clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == back_btn:
                            is_running = False
                            self.main_window()
                        if event.ui_element == easy_btn:
                            is_running = self.start_game(5, 16, 200, 1)
                        if event.ui_element == medium_btn:
                            is_running = self.start_game(7, 13, 125, 2)
                        if event.ui_element == hard_btn:
                            is_running = self.start_game(10, 8, 70, 3)
                        if event.ui_element == custom_btn:
                            custom_window.show()
                            button_layout.disable()
                        if event.ui_element == custom_close_btn:
                            custom_window.hide()
                            button_layout.enable()

            # -- Event handling: Stick size --
                        if event.ui_element == reduce_sticksize:
                            if stick_image.relative_rect.width == 30:
                                stick_image.relative_rect.x += (int((30-20)/2))
                                stick_image.set_dimensions((20, 20))
                                self.paddle_size = 70
                            if stick_image.relative_rect.width == 40:
                                stick_image.relative_rect.x += (int((40-30)/2))
                                stick_image.set_dimensions((30, 20))
                                self.paddle_size = 125
                        if event.ui_element == grow_sticksize:
                            if stick_image.relative_rect.width == 30:
                                stick_image.relative_rect.x -= (int((30-20)/2))
                                stick_image.set_dimensions((40, 20))
                                self.paddle_size = 200
                            if stick_image.relative_rect.width == 20:
                                stick_image.relative_rect.x -= (int((20-10)/2))
                                stick_image.set_dimensions((30, 20))
                                self.paddle_size = 125

            # -- Event handling: Ball size --
                        if event.ui_element == reduce_ballsize:
                            if ball_image.relative_rect.width == 30:
                                ball_image.relative_rect.x += (int((30-20)/2))
                                ball_image.relative_rect.y += (int((30-20)/2))
                                ball_image.set_dimensions((20, 20))
                                self.ball_size = 8
                            if ball_image.relative_rect.width == 40:
                                ball_image.relative_rect.x += (int((40-30)/2))
                                ball_image.relative_rect.y += (int((40-30)/2))
                                ball_image.set_dimensions((30, 30))
                                self.ball_size = 13
                        if event.ui_element == grow_ballsize:
                            if ball_image.relative_rect.width == 30:
                                ball_image.relative_rect.x -= (int((30-20)/2))
                                ball_image.relative_rect.y -= (int((30-20)/2))
                                ball_image.set_dimensions((40, 40))
                                self.ball_size = 16
                            if ball_image.relative_rect.width == 20:
                                ball_image.relative_rect.x -= (int((20-10)/2))
                                ball_image.relative_rect.y -= (int((20-10)/2))
                                ball_image.set_dimensions((30, 30))
                                self.ball_size = 13

            # -- Event handling: Fields --
                        if event.ui_element == reduce_fieldsize:
                            if field_image.text == "Medium":
                                field_image.set_text("Small")
                                self.map_choice = 1
                            if field_image.text == "Large":
                                field_image.set_text("Medium")
                                self.map_choice = 2
                        if event.ui_element == grow_fieldsize:
                            if field_image.text == "Medium":
                                field_image.set_text("Large")
                                self.map_choice = 3
                            if field_image.text == "Small":
                                field_image.set_text("Medium")
                                self.map_choice = 2

            # -- Event handling: Ball speed --
                        if event.ui_element == reduce_ballspeed:
                            if ballspeed_image.text == "1x":
                                ballspeed_image.set_text("0.5x")
                                self.ball_speed = 5
                            if ballspeed_image.text == "2x":
                                ballspeed_image.set_text("1x")
                                self.ball_speed = 7
                        if event.ui_element == grow_ballspeed:
                            if ballspeed_image.text == "1x":
                                ballspeed_image.set_text("2x")
                                self.ball_speed = 10
                            if ballspeed_image.text == "0.5x":
                                ballspeed_image.set_text("1x")
                                self.ball_speed = 7

                        if event.ui_element == start_game_custom:
                            is_running = self.start_game(self.ball_speed,
                                                         self.ball_size,
                                                         self.paddle_size,
                                                         self.map_choice)

                manager.process_events(event)
                manager2.process_events(event)

            manager.update(time_delta)
            manager2.update(time_delta)

            self.screen.blit(background, (0, 0))
            manager.draw_ui(self.screen)

            controls_image = pygame.image.load("controls.png")
            self.screen.blit(controls_image, (530, 200))

            manager2.draw_ui(self.screen)

            pygame.display.update()

    def pause(self):
        background = pygame.Surface((800, 600))
        background.fill(DARKBLUE)
        self.screen.blit(background, (0, 0))

        manager = pygame_gui.UIManager((800, 600), "window.json")

        font = pygame.font.Font(None, 74)

        text = font.render("PAUSED", 1, WHITE)
        self.screen.blit(text, (300, 200))
        pygame.display.flip()

        # -- Draw interactive UI elements --
        continue_btn = UIButton(relative_rect=pygame.Rect((300, 300), (200, 100)),
                              text="Continue",
                              manager=manager)

        main_menu = UIButton(relative_rect=pygame.Rect((300, 420), (200, 100)),
                              text="Main menu",
                              manager=manager)

        # -- UI Event handling --
        clock = pygame.time.Clock()
        is_running = True

        while is_running:
            time_delta = clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == continue_btn:
                            is_running = False
                            self.is_paused = False
                        if event.ui_element == main_menu:
                            is_running = False
                            self.is_paused = False
                            self.main_window()

                manager.process_events(event)

            manager.update(time_delta)
            manager.draw_ui(self.screen)

            pygame.display.update()

    def game_end(self, complete):
        background = pygame.Surface((800, 600))
        background.fill(DARKBLUE)
        self.screen.blit(background, (0, 0))

        manager = pygame_gui.UIManager((800, 600), "window.json")

        font = pygame.font.Font(None, 74)

        if complete:
            text = font.render("CONGRATULATIONS", 1, WHITE)
            self.screen.blit(text, (145, 200))
            pygame.display.flip()
        else:
            text = font.render("GAME OVER", 1, WHITE)
            self.screen.blit(text, (250, 200))
            pygame.display.flip()

        # -- Draw interactive UI elements --
        play_again = UIButton(relative_rect=pygame.Rect((300, 300), (200, 100)),
                              text="Play again",
                              manager=manager)

        main_menu = UIButton(relative_rect=pygame.Rect((300, 420), (200, 100)),
                              text="Main menu",
                              manager=manager)

        # -- UI Event handling --
        clock = pygame.time.Clock()
        is_running = True

        while is_running:
            time_delta = clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == play_again:
                            is_running = False
                            self.start_game(self.ball_speed,
                                            self.ball_size,
                                            self.paddle_size,
                                            self.map_choice)
                        if event.ui_element == main_menu:
                            is_running = False
                            self.main_window()

                manager.process_events(event)

            manager.update(time_delta)
            manager.draw_ui(self.screen)

            pygame.display.update()

    def game_screen(self):
        # -- Setup game variables --
        self.score = 0

        all_sprites_list = pygame.sprite.Group()

        paddle = Paddle(LIGHTBLUE, self.paddle_size, 10)
        paddle.rect.x = 350
        paddle.rect.y = 560

        ball = Ball(WHITE, self.ball_size, self.ball_speed, random.randint(210, 330))
        ball.rect.x = 345
        ball.rect.y = 500

        all_bricks = self.create_map(self.map_choice)

        for brick in all_bricks:
            all_sprites_list.add(brick)

        all_sprites_list.add(paddle)
        all_sprites_list.add(ball)

        clock = pygame.time.Clock()

        # -- Game logic loop --
        while self.carryOn:
            self.gameloop(ball,
                          paddle,
                          all_sprites_list,
                          all_bricks,
                          clock)

    def intro_message(self):
        self.game_started = False
        self.screen.fill(DARKBLUE)
        pygame.draw.line(self.screen, WHITE, [0, 38], [800, 38], 2)

        font = pygame.font.Font(None, 34)
        text = font.render("Score: " + str(self.score), 1, WHITE)
        self.screen.blit(text, (20, 10))
        text = font.render("Lives: " + str(self.lives), 1, WHITE)
        self.screen.blit(text, (650, 10))

        font = pygame.font.Font(None, 74)
        text = font.render("Break all the bricks!", 1, WHITE)
        self.screen.blit(text, (150, 200))

        pygame.display.flip()
        pygame.time.wait(3000)

    def gameloop(self, ball, paddle, sprite_list, all_bricks, clock):
        # -- Handle pygame events and keypresses --
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.carryOn = False
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            paddle.moveLeft(10)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            paddle.moveRight(10)
        if keys[pygame.K_ESCAPE]:
            self.is_paused = True

        if self.is_paused:
            self.pause()

        sprite_list.update()

        # -- Handle wall collisions --
        if ball.rect.x >= (800-self.ball_size):
            if ball.velocity_x > 0:
                ball.velocity_x = -ball.velocity_x
        if ball.rect.x <= 0:
            if ball.velocity_x < 0:
                ball.velocity_x = -ball.velocity_x
        if ball.rect.y > (600-self.ball_size):
            self.lives -= 1
            if self.lives == 0:
                self.carryOn = False
                self.game_end(False)
            self.game_screen()
        if ball.rect.y < 40:
            if ball.velocity_y < 0:
                ball.velocity_y = -ball.velocity_y

        # -- Handle ball collision with objects --
        if pygame.sprite.collide_mask(ball, paddle):
            ball.rect.x -= ball.velocity_x
            ball.rect.y -= ball.velocity_y
            ball.bounce(True, collision(ball, paddle))

        brick_list = pygame.sprite.spritecollide(ball, all_bricks, False)
        for brick in brick_list:
            if not self.collided:
                ball.bounce(False, collision(ball, brick))
                self.collided = True
            self.score += 1
            brick.kill()
            if len(all_bricks) == 0:
                self.carryOn = False
                self.game_end(True)
        self.collided = False

        # -- Update screen --
        if self.game_started:
            self.intro_message()

        self.screen.fill(DARKBLUE)
        pygame.draw.line(self.screen, WHITE, [0, 38], [800, 38], 2)

        font = pygame.font.Font(None, 34)
        text = font.render("Score: " + str(self.score), 1, WHITE)
        self.screen.blit(text, (20, 10))
        text = font.render("Lives: " + str(self.lives), 1, WHITE)
        self.screen.blit(text, (650, 10))
        if self.ball_speed == 5:
            text = font.render("0.5x", 1, WHITE)
            self.screen.blit(text, (5, 575))
        elif self.ball_speed == 7:
            text = font.render("1x", 1, WHITE)
            self.screen.blit(text, (5, 575))
        elif self.ball_speed == 10:
            text = font.render("2x", 1, WHITE)
            self.screen.blit(text, (5, 575))

        sprite_list.draw(self.screen)

        pygame.display.flip()

        clock.tick(60)

    def start_game(self, ball_speed, ball_size, paddle_size, map_choice):
        self.carryOn = True
        self.game_started = True
        self.lives = 3
        self.ball_speed = ball_speed
        self.ball_size = ball_size
        self.paddle_size = paddle_size
        self.map_choice = map_choice
        self.game_screen()
        return False

    def create_map(self, map_choice):
        all_bricks = pygame.sprite.Group()
        if map_choice == 1:
            for i in range(14):
                for j in range(10):
                    if j <= 1:
                        color = RED
                    if j > 1 and j <= 3:
                        color = ORANGE
                    if j > 3 and j <= 10:
                        color = YELLOW

                    brick = Brick(color, 45, 20)
                    brick.rect.x = 50 + i * 50
                    brick.rect.y = 100 + j * 25
                    all_bricks.add(brick)

        if map_choice == 2:
            _range = 14
            start_x = 50
            for i in range(7):
                for j in range(_range):
                    if i <= 1:
                        color = RED
                    if i > 1 and i <= 3:
                        color = ORANGE
                    if i > 3 and i <= 10:
                        color = YELLOW

                    brick = Brick(color, 45, 20)
                    brick.rect.x = start_x + j * 50
                    brick.rect.y = 100 + i * 25
                    all_bricks.add(brick)
                start_x += 25
                _range -= 1

        if map_choice == 3:
            _range = 7
            start_x = 50
            for c in range(2):
                descending = True
                for i in range(7):
                    for j in range(_range):
                        if i <= 1:
                            color = RED
                        if i > 1 and i <= 3:
                            color = ORANGE
                        if i > 3 and i <= 10:
                            color = YELLOW

                        brick = Brick(color, 45, 20)
                        brick.rect.x = start_x + j * 50
                        brick.rect.y = 100 + i * 25
                        all_bricks.add(brick)
                    if _range == 4:
                        descending = False
                    if descending:
                        _range -= 1
                        start_x += 25
                    else:
                        _range += 1
                        start_x -= 25
                start_x = 400
                _range = 7

        return all_bricks

# -- Get collision angle to determine collision side --
def collision(body1, body2):
    body2_x = body2.rect.center[0]
    body2_y = body2.rect.center[1]
    x_center = body1.rect.center[0] - body2_x
    y_center = body1.rect.center[1] - body2_y
    center_a = math.atan2(x_center, y_center)

    bl_x = body2.rect.bottomleft[0] - body2_x
    bl_y = body2.rect.bottomleft[1] - body2_y
    bl_a = math.atan2(bl_x, bl_y)
    tl_x = body2.rect.topleft[0] - body2_x
    tl_y = body2.rect.topleft[1] - body2_y
    tl_a = math.atan2(tl_x, tl_y)
    tr_x = body2.rect.topright[0] - body2_x
    tr_y = body2.rect.topright[1] - body2_y
    tr_a = math.atan2(tr_x, tr_y)
    br_x = body2.rect.bottomright[0] - body2_x
    br_y = body2.rect.bottomright[1] - body2_y
    br_a = math.atan2(br_x, br_y)

    direction = "bottom"
    if tl_a > center_a or center_a > tr_a:
        direction = "top"
    if br_a < center_a and center_a < tr_a:
        direction = "left"
    if bl_a < center_a and center_a < br_a:
        direction = "bottom"
    if bl_a > center_a and center_a > tl_a:
        direction = "right"

    return direction

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        self.width = width

        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()

    def moveLeft(self, pixels):
        self.rect.x -= pixels

        if self.rect.x < 0:
            self.rect.x = 0

    def moveRight(self, pixels):
        self.rect.x += pixels

        if self.rect.x > (800-self.width):
            self.rect.x = (800-self.width)

class Ball(pygame.sprite.Sprite):
    def __init__(self, color, size, velocity, angle):
        super().__init__()

        self.image = pygame.Surface([size, size])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, size, size])

        angle = math.radians(angle)

        self.velocity = velocity
        self.velocity_x = self.velocity * math.cos(angle)
        self.velocity_y = self.velocity * math.sin(angle)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

    def bounce(self, paddle_collision, direction):
        if direction == "left" or direction == "right":
            self.velocity_x = -self.velocity_x
        if direction == "top" or direction == "bottom":
            self.velocity_y = -self.velocity_y

        if paddle_collision:
            angle = math.radians(random.randint(210, 330))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                angle = math.radians(random.randint(210, 240))
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                angle = math.radians(random.randint(300, 330))

            self.velocity_x = self.velocity * math.cos(angle)
            self.velocity_y = self.velocity * math.sin(angle)


class Brick(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.rect = self.image.get_rect()


if __name__ == '__main__':
    game = Game()
    game.main_window()
