
import pygame, sys
from pygame.locals import *
from pathlib import Path
import ctypes

class Text:
    def __init__(self, text:str, pos:tuple, font_size:int):
        self.text = text
        self.pos = pos
        self.font_size = font_size
        self.font_color = (255, 255, 255)
        self.font_name = "data\\font\\arial.ttf"
        self.font = self.set_font()
        self.text_image = self.render()

    def set_font(self):
        return pygame.font.Font(self.font_name, self.font_size)



    def render(self):
        return self.font.render(self.text, True, self.font_color)

    def draw(self, surface):
        surface.blit(self.text_image, self.pos)

    def set_pos(self, pos:tuple):
        self.pos = pos

    def get_pos(self):
        return self.pos

    def get_dimensions(self):
        rect = self.text_image.get_rect()
        return rect.width, rect.height

class Button:
    def __init__(self, name:str, image_path:str):
        self.__name = name
        self.__x = 0
        self.__y = 0
        self.image = self.__load_image(image_path)

    def set_x_y_pos(self, x:int, y:int):
        self.__x = x
        self.__y = y

    def get_x_y_pos(self):
        return self.__x, self.__y

    def get_name(self):
        return self.__name

    def __load_image(self, image_path:str):
        return pygame.image.load(image_path)

    def is_clicked(self, x, y):
        width, height = self.get_dimensions()
        if x >= self.__x and y >= self.__y and x <= self.__x + width and y <= self.__y + height:
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.get_x_y_pos())

    def get_dimensions(self):
        if self.image is None:
            return 0, 0
        return self.image.get_size()

    def __lt__(self, other):
        return self.__name < other.get_name()



class GameScreen:

    class TextEdit:
        def __init__(self, text="", pos=(0, 0)):
            self.__text = text
            self.__pos = pos
            self.__font_color = (255, 255, 255)
            self.__font_name = "data\\font\\arial.ttf"
            self.__font = None
            self.__font_size = 40
            self.__image = None

        def get_pos(self):
            return self.__pos

        def set_pos(self, pos=tuple):
            self.__pos = pos

        def set_font_size(self, size):
            self.__font_size = size

        def get_text(self):
            return self.__text.strip()

        def get_dimensions(self):
            rect = self.__image.get_rect()
            return rect.width, rect.height

        def __set_font(self):
            self.__font = pygame.font.Font(self.__font_name, self.__font_size)

        def is_empty(self):
            support = ""
            for char in self.__text.strip():
                support += char
            return support == ""

        def __render_text(self):
            self.__image = self.__font.render(self.__text, True, self.__font_color)

        def draw(self, surface):
            self.__set_font()
            self.__render_text()
            x, y = self.__pos
            x += self.get_dimensions()[0]
            cursor = Rect((x, y), (3, self.get_dimensions()[1]))
            surface.blit(self.__image, self.__pos)
            pygame.draw.rect(surface, self.__font_color, cursor)

        def write(self, event):
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE and len(self.__text) > 0:
                    self.__text = self.__text[ : len(self.__text) - 1]

                elif len(self.__text) < 10 and event.key != K_BACKSPACE:
                    self.__text += event.unicode


    pygame.init()

    GAME_TITLE = "Match3Lines"
    GAME_ICON_PATH = "data\\images\\icon_title\\icon_title.png"

    NOT_CLICKED_TILE_PATH = "data\\images\\tiles\\not_clicked_tile.png"
    CLICKED_TILE_PATH = "data\\images\\tiles\\clicked_tile.png"
    ADVISED_TILE_PATH = "data\\images\\tiles\\advised_tile.png"
    IMAGE_PATH = "data\\images\\tile_images"


    # --------------BUTTON PATH------------------------------------
    #main menu
    PLAY_BUTTON_IMAGE_PATH = "data\\images\\buttons\\main_menu\\play.png"
    STATISTIC_BUTTON_IMAGE_PATH = "data\\images\\buttons\\main_menu\\statistic.png"
    QUIT_MAIN_MENU_BUTTON_IMAGE_PATH = "data\\images\\buttons\\main_menu\\quit.png"
    ABOUT_BUTTON_IMAGE_PATH = "data\\images\\buttons\\main_menu\\about.png"

    #level
    PAUSE_BUTTON_IMAGE_PATH = "data\\images\\buttons\\level\\pause.png"
    HELP_BUTTON_IMAGE_PATH = "data\\images\\buttons\\level\\help.png"
    SOUND_ON_IMAGE_PATH = "data\\images\\buttons\\level\\sound_on.png"
    SOUND_OFF_IMAGE_PATH = "data\\images\\buttons\\level\\sound_off.png"

    #pause
    RESUME_GAME_BUTTON_IMAGE_PATH = "data\\images\\buttons\\pause_menu\\resume.png"
    QUIT_BUTTON_IMAGE_PATH = "data\\images\\buttons\\pause_menu\\quit.png"
    SURRENDER_BUTTON_IMAGE_PATH = "data\\images\\buttons\\pause_menu\\surrender.png"

    #game over
    SUBMIT_BUTTON_IMAGE_PATH = "data\\images\\buttons\\game_over\\submit.png"
    MAIN_MENU_BUTTON_IMAGE_PATH = "data\\images\\buttons\\game_over\\main_menu.png"

    #statistics
    RESET_STATISTICS_IMAGE_PATH = "data\\images\\buttons\\statistics\\reset_statistics.png"

    #won level
    NEXT_LEVEL_BUTTON_IMAGE_PATH = "data\\images\\buttons\\won_level\\next_level.png"
    END_GAME_BUTTON_IMAGE_PATH = "data\\images\\buttons\\won_level\\end_game.png"
    # -------------------------------------------------------------

    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 600

    # -----COLORS-------------
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255,0 ,0 )
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    ORANGE = (255, 128, 0)
    # ------------------------

    TIME_BAR_HEIGHT = 20

    DISPLAYSURF = None
    FPS = 30
    FPSCLOCK = pygame.time.Clock()



    # ---------------------------------------------
    # Sound
    ACCEPTED_SOUND_PATH = "data\\sound\\accepted.wav"
    ACCEPTED_SOUND = pygame.mixer.Sound(ACCEPTED_SOUND_PATH)
    WRONG_SOUND_PATH = "data\\sound\\wrong.wav"
    WRONG_SOUND = pygame.mixer.Sound(WRONG_SOUND_PATH)
    BACKGROUND_MUSIC_PATH = "data\\sound\\background.mp3"
    CLICKED_TILE_SOUND_PATH = "data\\sound\\clicked_tile.wav"
    CLICKED_TILE_SOUND = pygame.mixer.Sound(CLICKED_TILE_SOUND_PATH)
    GAME_OVER_MUSIC_PATH = "data\\sound\\game_over.mp3"
    NEXT_LEVEL_SOUND_PATH = "data\\sound\\next_level.wav"
    NEXT_LEVEL_SOUND = pygame.mixer.Sound(NEXT_LEVEL_SOUND_PATH)
    # ---------------------------------------------

    # ------------------------------------------------------------
    # Line path
    HORIZONTAL_PATH = "data\\images\\lines\\horizontal.png"
    VERTICAL_PATH = "data\\images\\lines\\vertical.png"
    LEFT_HALF_PATH = "data\\images\\lines\\left_half.png"
    RIGHT_HALF_PATH = "data\\images\\lines\\right_half.png"
    UP_HALF_PATH = "data\\images\\lines\\up_half.png"
    DOWN_HALF_PATH = "data\\images\\lines\\down_half.png"
    FROM_LEFT_TO_DOWN_PATH = "data\\images\\lines\\from_left_to_down.png"
    FROM_RIGHT_TO_DOWN_PATH = "data\\images\\lines\\from_right_to_down.png"
    FROM_LEFT_TO_UP_PATH = "data\\images\\lines\\from_left_to_up.png"
    FROM_RIGHT_TO_UP_PATH = "data\\images\\lines\\from_right_to_up.png"
    # -------------------------------------------------------------


    UP = "u"
    DOWN = "d"
    RIGHT = "r"
    LEFT = "l"
    # ----------------------------------------------------
    # These lines will be set in a tile where path turns.
    TURN_FROM_LEFT_TO_DOWN = "q"
    # _
    #  |
    TURN_FROM_RIGHT_TO_DOWN = "e"
    #  _
    # |
    TURN_FROM_RIGHT_TO_UP = "x"
    # |_
    TURN_FROM_LEFT_TO_UP = "z"
    # _|
    # ------------------------------------------------------
    # ------------------------------------------------------
    # This lines is for the first and last tile of a path, where the line is the half of its size.
    UP_HALF = "v"
    DOWN_HALF = "b"
    LEFT_HALF = "n"
    RIGHT_HALF = "m"
    # ------------------------------------------------------

    LINE_DICTIONARY = dict()

    TILE_SIZE = 50
    GAP_SIZE = 1
    BOARD_WIDTH = 12
    BOARD_HEIGHT = 10


    X_MARGIN = 0
    Y_MARGIN = 0



    def __init__(self, presenter):
        self.presenter = presenter
        #self.BOARD_WIDTH, self.BOARD_HEIGHT = self.presenter.get_board_dimension()
        self.set_window_constants()
        self.set_tile_size_constant()
        self.set_x_y_of_board()
        self.LINE_DICTIONARY = self.create_dictionary_of_line_images()
        self.set_line_dictionary()
        pygame.display.set_caption(self.GAME_TITLE)
        pygame.display.set_icon(pygame.image.load(self.GAME_ICON_PATH))
        self.__tile_image = self.__load_tile_images(self.IMAGE_PATH)

        self.not_clicked_tile_image = pygame.transform.scale(pygame.image.load(self.NOT_CLICKED_TILE_PATH), (self.TILE_SIZE, self.TILE_SIZE))
        self.clicked_tile_image = pygame.transform.scale(pygame.image.load(self.CLICKED_TILE_PATH), (self.TILE_SIZE, self.TILE_SIZE))
        self.advised_tile_image = pygame.transform.scale(pygame.image.load(self.ADVISED_TILE_PATH), (self.TILE_SIZE, self.TILE_SIZE))


        self.DISPLAYSURF = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT),flags=FULLSCREEN)
        #self.X_MARGIN = int((self.WINDOW_WIDTH - (self.TILE_SIZE + self.GAP_SIZE) * self.BOARD_WIDTH) / 2)
        #self.Y_MARGIN = int((self.WINDOW_HEIGHT - (self.TILE_SIZE + self.GAP_SIZE) * self.BOARD_HEIGHT) / 2)


        self.playing_music = True
        self.playing_background_music = False
        self.playing_game_over_music = False
        self.writing_name = True
        self.to_play_next_level_sound = True

        # ------BUTTONS AND INTERFACES-----------------------------------------
        #main menu
        self.play_button = Button("play", self.PLAY_BUTTON_IMAGE_PATH)
        self.statistic_button = Button("statistic", self.STATISTIC_BUTTON_IMAGE_PATH)
        self.about_button = Button("about", self.ABOUT_BUTTON_IMAGE_PATH)
        self.quit_main_menu_button = Button("quit", self.QUIT_MAIN_MENU_BUTTON_IMAGE_PATH)


        #level
        self.sound_on_button = Button("sound_on", self.SOUND_ON_IMAGE_PATH)
        self.sound_off_button = Button("sound_off", self.SOUND_OFF_IMAGE_PATH)
        self.pause_button = Button("pause", self.PAUSE_BUTTON_IMAGE_PATH)
        self.help_button = Button("help", self.HELP_BUTTON_IMAGE_PATH)

        #pause
        self.resume_game_button = Button("resume", self.RESUME_GAME_BUTTON_IMAGE_PATH)
        self.surrender_button = Button("surrender", self.SURRENDER_BUTTON_IMAGE_PATH)
        self.quit_button = Button("quit", self.QUIT_BUTTON_IMAGE_PATH)

        #game over
        self.submit_name_button = Button("submit", self.SUBMIT_BUTTON_IMAGE_PATH)
        self.main_menu_button = Button("main menu", self.MAIN_MENU_BUTTON_IMAGE_PATH)
        self.line_edit = self.TextEdit("My name")

        #statistics
        self.reset_statistics_button = Button("reset statistics", self.RESET_STATISTICS_IMAGE_PATH)

        #won level
        self.next_level_button = Button("next_level", self.NEXT_LEVEL_BUTTON_IMAGE_PATH)
        self.end_game_button = Button("end_game", self.END_GAME_BUTTON_IMAGE_PATH)
        # -----------------------------------------------

    def set_window_constants(self):

        resolution = ctypes.windll.user32
        self.WINDOW_WIDTH = resolution.GetSystemMetrics(0)
        self.WINDOW_HEIGHT = resolution.GetSystemMetrics(1)

    def set_tile_size_constant(self):

        self.TILE_SIZE = (self.WINDOW_HEIGHT - self.TIME_BAR_HEIGHT) // self.BOARD_HEIGHT

    def set_x_y_of_board(self):
        self.X_MARGIN = int((self.WINDOW_WIDTH - (self.TILE_SIZE + self.GAP_SIZE) * self.BOARD_WIDTH) / 2)
        self.Y_MARGIN = int(((self.WINDOW_HEIGHT + self.TIME_BAR_HEIGHT) - (self.TILE_SIZE + self.GAP_SIZE) * self.BOARD_HEIGHT) / 2)



    def set_level_constants(self):
        self.BOARD_WIDTH, self.BOARD_HEIGHT = self.presenter.get_board_dimension()
        self.X_MARGIN = int((self.WINDOW_WIDTH - (self.TILE_SIZE + self.GAP_SIZE) * self.BOARD_WIDTH) / 2)
        self.Y_MARGIN = int((self.WINDOW_HEIGHT - (self.TILE_SIZE + self.GAP_SIZE) * self.BOARD_HEIGHT) / 2)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                elif event.type == MOUSEBUTTONUP:
                    x,y = event.pos
                    if self.presenter.is_playing_game():
                        self.click_in_tile(x, y)
                        self.click_in_level_buttons(x, y)
                    elif self.presenter.is_main_menu():
                        self.click_in_main_menu(x, y)
                    elif self.presenter.is_paused_game():
                        self.click_in_pause_menu_buttons(x, y)
                    elif self.presenter.is_won_game():
                        self.click_in_won_level_buttons(x, y)
                    elif self.presenter.is_game_over():
                        self.click_in_game_over_buttons(x, y)
                    elif self.presenter.is_statistic():
                        self.click_in_statistic_menu(x, y)
                    elif self.presenter.is_about_menu():
                        self.click_in_about_menu(x, y)
                elif self.presenter.is_game_over() and self.writing_name:
                    self.line_edit.write(event)

            if self.presenter.is_paused_game():
                self.draw_pause_menu()
            elif self.presenter.is_main_menu():
                self.draw_main_menu()
            elif self.presenter.is_statistic():
                self.draw_statistic()
            elif self.presenter.is_game_over():
                self.draw_game_over()
            elif self.presenter.is_won_game():
                self.draw_won_level(self.presenter.get_user_level(), self.presenter.get_user_points())
            elif self.presenter.is_playing_game():
                self.draw_level(self.presenter.get_user_level(), self.presenter.get_user_points())
            elif self.presenter.is_about_menu():
                self.draw_about()
            pygame.display.flip()
            self.FPSCLOCK.tick(self.FPS)


    def __load_tile_images(self, image_path:str):
        images = []
        path = Path(image_path)
        for image_file in path.iterdir():
            current_image = image_path + "\\" + image_file.name
            images.append(pygame.transform.scale(pygame.image.load(current_image), (self.TILE_SIZE, self.TILE_SIZE)) )
        return images

    def draw_tile(self, i:int, j:int):
        coordinates = self.x_y_position_from_i_j(i, j)
        if self.presenter.is_clicked_tile(i, j):
            self.DISPLAYSURF.blit(self.clicked_tile_image, coordinates)

        elif self.presenter.is_advised_tile(i, j) and not self.presenter.is_help_time_over():
            self.DISPLAYSURF.blit(self.advised_tile_image, coordinates)

        else:
            self.DISPLAYSURF.blit(self.not_clicked_tile_image, coordinates)


    def draw_board(self):
        self.DISPLAYSURF.fill(self.BLACK)
        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH):
                image_index = self.presenter.get_id_board_element(i, j)
                if image_index != -1:
                    coordinates = self.x_y_position_from_i_j(i, j)
                    self.draw_tile(i, j)
                    self.DISPLAYSURF.blit(self.__tile_image[image_index], coordinates)
                #-------this is for debugging-------
                #else:
                #    x_coordenate = self.X_MARGIN + (self.TILE_SIZE + self.GAP_SIZE) * j
                #    y_coordenate = self.Y_MARGIN + (self.TILE_SIZE + self.GAP_SIZE) * i
                #    self.DISPLAYSURF.blit(self.clicked_tile_image, (x_coordenate, y_coordenate))
                #-----------------------------------------

    def x_y_position_from_i_j(self, i, j):
        """Return the position(i,j) of the tile in the board, given the coordinate in the screen.
        If there is not a tile in the position (x, y) this method will return (-1, -1)"""
        x_coordinate = self.X_MARGIN + (self.TILE_SIZE + self.GAP_SIZE) * j
        y_coordinate = self.Y_MARGIN + (self.TILE_SIZE + self.GAP_SIZE) * i
        return x_coordinate, y_coordinate

    def detect_click_in_tile(self, x, y):
        i = -1
        j = -1
        if x > self.X_MARGIN + ((self.TILE_SIZE + self.GAP_SIZE) * self.BOARD_WIDTH) or x < self.X_MARGIN:
            return i, j
        elif y > self.Y_MARGIN + ((self.TILE_SIZE + self.GAP_SIZE) * self.BOARD_HEIGHT) or y < self.Y_MARGIN:
            return i,j
        i = (y - self.Y_MARGIN) // (self.TILE_SIZE + self.GAP_SIZE)
        j = (x - self.X_MARGIN) // (self.TILE_SIZE + self.GAP_SIZE)
        if (y - self.Y_MARGIN) % (self.TILE_SIZE + self.GAP_SIZE) > 0:
            i += 1
        if (x - self.X_MARGIN) % (self.TILE_SIZE + self.GAP_SIZE) > 0:
            j += 1
        return i - 1,j - 1

    def click_in_tile(self, x, y):
        i, j = self.detect_click_in_tile(x, y)
        if i != -1 and j != -1 and self.presenter.is_a_tile(i, j):
            self.play_clicked_tile_sound()
        if self.presenter.is_clicked_tile(i, j):
            self.presenter.remove_selected_tile(i, j)
        else:
            self.presenter.add_selected_tile(i, j)

        if self.presenter.is_max_selected_tiles():
            self.presenter.play_movement()


    def draw_line_images(self, positions:list, lines:str):
        if len(positions) == 0:
            self.play_wrong_sound()


        for index_line in range(len(positions)):
            i = positions[index_line][0]
            j = positions[index_line][1]
            self.DISPLAYSURF.blit(self.LINE_DICTIONARY[lines[index_line]], self.x_y_position_from_i_j(i, j))
        pygame.display.flip()
        self.play_accepted_sound()
        self.presenter.delay_thread(0.25)

    def create_dictionary_of_line_images(self):
        dictionary = dict()
        dictionary[self.UP] = self.VERTICAL_PATH
        dictionary[self.DOWN] = self.VERTICAL_PATH
        dictionary[self.LEFT] = self.HORIZONTAL_PATH
        dictionary[self.RIGHT] = self.HORIZONTAL_PATH
        dictionary[self.UP_HALF] = self.UP_HALF_PATH
        dictionary[self.DOWN_HALF] = self.DOWN_HALF_PATH
        dictionary[self.LEFT_HALF] = self.LEFT_HALF_PATH
        dictionary[self.RIGHT_HALF] = self.RIGHT_HALF_PATH
        dictionary[self.TURN_FROM_RIGHT_TO_UP] = self.FROM_RIGHT_TO_UP_PATH
        dictionary[self.TURN_FROM_LEFT_TO_UP] = self.FROM_LEFT_TO_UP_PATH
        dictionary[self.TURN_FROM_RIGHT_TO_DOWN] = self.FROM_RIGHT_TO_DOWN_PATH
        dictionary[self.TURN_FROM_LEFT_TO_DOWN] = self.FROM_LEFT_TO_DOWN_PATH
        return dictionary

    def set_line_dictionary(self):
        """The dictionary parameter is a dictionary, where its keys are the constant lines of the class GameScreen
        and its values are the path of the image which that represent to every line."""
        for line in self.LINE_DICTIONARY:
            self.LINE_DICTIONARY[line] = pygame.transform.scale(pygame.image.load(self.LINE_DICTIONARY[line]), (self.TILE_SIZE, self.TILE_SIZE))

    def play_clicked_tile_sound(self):
        if self.playing_music:
            self.CLICKED_TILE_SOUND.play()

    def play_accepted_sound(self):
        if self.playing_music:
            self.ACCEPTED_SOUND.play()

    def play_wrong_sound(self):
        if self.playing_music:
            self.WRONG_SOUND.play()

    def play_next_level_sound(self):
        if self.playing_music:
            self.NEXT_LEVEL_SOUND.play()

    def play_background_music(self):
        if self.is_music_playing() and not self.playing_background_music:
            self.playing_music = True
            self.playing_background_music = True
            pygame.mixer.music.load(self.BACKGROUND_MUSIC_PATH)
            pygame.mixer.music.play(-1)

    def stop_background_music(self):
        if self.playing_background_music:
            self.playing_background_music = False
            pygame.mixer.music.stop()

    def play_game_over_music(self):
        if self.is_music_playing() and not self.playing_game_over_music:
            self.playing_game_over_music = True
            pygame.mixer.music.load(self.GAME_OVER_MUSIC_PATH)
            pygame.mixer.music.play(-1)

    def stop_game_over_music(self):
        if self.playing_game_over_music:
            self.playing_game_over_music = False
            pygame.mixer.music.stop()

    def pause_background_music(self):
        self.playing_music = False
        pygame.mixer.music.pause()

    def unpause_background_music(self):
        self.playing_music = True
        pygame.mixer.music.unpause()

    def is_music_playing(self):
        return self.playing_music

    def __calculate_time_bar_percent(self, percent:int):
        """Return the size of the time bar given the percent that is visible."""
        width = self.BOARD_WIDTH * ( self.TILE_SIZE + self.GAP_SIZE)
        return int((percent * width) / 100)

    def __draw_time_bar(self, percent:int):
        color = self.WHITE
        if percent >= 75:
            color = self.GREEN
        elif percent >= 50 and percent < 75:
            color = self.YELLOW
        elif percent >= 25 and percent < 50:
            color = self.ORANGE
        elif percent < 25:
            color = self.RED
        x1, y1 = self.X_MARGIN, self.Y_MARGIN // 4
        x2, y2 = self.__calculate_time_bar_percent(percent), y1 + self.TIME_BAR_HEIGHT
        pygame.draw.rect(self.DISPLAYSURF, color, (x1,y1, x2, y2), 0)

    def __set_pause_menu_button_pos(self):
        gap = 30
        y_pos = self.WINDOW_HEIGHT // 4
        x_pos = (self.WINDOW_WIDTH // 2) - (self.resume_game_button.get_dimensions()[0] // 2)
        self.resume_game_button.set_x_y_pos(x_pos, y_pos)
        y_pos += gap + self.resume_game_button.get_dimensions()[1]
        self.surrender_button.set_x_y_pos(x_pos, y_pos)
        y_pos += gap + self.surrender_button.get_dimensions()[1]
        self.quit_button.set_x_y_pos(x_pos, y_pos)

    def __set_level_button_pos(self):
        gap = 20
        x_pos = (self.X_MARGIN + (self.BOARD_WIDTH * (self.TILE_SIZE + self.GAP_SIZE)) + self.WINDOW_WIDTH) // 2
        y_pos = self.Y_MARGIN + 20
        self.pause_button.set_x_y_pos(x_pos, y_pos)
        y_pos += gap + self.pause_button.get_dimensions()[1]
        self.help_button.set_x_y_pos(x_pos, y_pos)
        y_pos += gap + self.help_button.get_dimensions()[1]
        self.sound_on_button.set_x_y_pos(x_pos, y_pos)
        self.sound_off_button.set_x_y_pos(x_pos, y_pos)


    def draw_level(self, level:int, points:int):
        self.play_background_music()
        self.writing_name = True
        self.draw_board()
        self.draw_level_buttons()
        self.__draw_time_bar(self.presenter.get_current_percent())
        points_text = Text("Level: " + str(level) + " Points: " + str(points), (0, 0), 16)
        width, height = points_text.get_dimensions()
        x = (((self.X_MARGIN + (self.BOARD_WIDTH * (self.TILE_SIZE + self.GAP_SIZE))) + self.WINDOW_WIDTH) // 2) - (width // 2)
        y = self.Y_MARGIN
        points_text.set_pos((x, y))
        points_text.draw(self.DISPLAYSURF)


    def draw_level_buttons(self):
        self.__set_level_button_pos()
        self.pause_button.draw(self.DISPLAYSURF)
        self.help_button.draw(self.DISPLAYSURF)
        if self.is_music_playing():
            self.sound_on_button.draw(self.DISPLAYSURF)
        else:
            self.sound_off_button.draw(self.DISPLAYSURF)

    def pause_game(self):
        self.presenter.pause_game()

    def click_in_level_buttons(self, x, y):
        if self.presenter.is_playing_game():
            if self.pause_button.is_clicked(x, y):
                self.presenter.pause_game()
            elif self.help_button.is_clicked(x, y):
                self.presenter.set_advised_tile()
            elif self.is_music_playing() and self.sound_on_button.is_clicked(x, y):
                self.pause_background_music()
            elif not self.is_music_playing() and self.sound_off_button.is_clicked(x, y):
                self.unpause_background_music()

    def quit(self):
        pygame.quit()
        sys.exit()

    def click_in_pause_menu_buttons(self, x, y):
        if self.presenter.is_paused_game():
            if self.resume_game_button.is_clicked(x, y):
                self.presenter.resume_game()
            elif self.surrender_button.is_clicked(x, y):
                self.presenter.game_over()
            elif self.quit_button.is_clicked(x, y):
                self.quit()

    def draw_pause_menu(self):
        self.__set_pause_menu_button_pos()
        self.DISPLAYSURF.fill(self.BLACK)
        self.resume_game_button.draw(self.DISPLAYSURF)
        self.surrender_button.draw(self.DISPLAYSURF)
        self.quit_button.draw(self.DISPLAYSURF)


    def __draw_won_level_texts(self, level:int, points:int):
        gap = 10
        text_size = 50
        won_level_text = Text("Congratulations, You have won the level " + str(level), (0, 0), text_size)
        width, height = won_level_text.get_dimensions()
        x, y = (self.WINDOW_WIDTH // 2) - (width // 2), self.WINDOW_HEIGHT // 6
        won_level_text.set_pos((x, y))
        points_text = Text("Your points are: " + str(points), (0, 0), text_size)
        width, height = points_text.get_dimensions()
        x, y = (self.WINDOW_WIDTH // 2) - (width // 2), won_level_text.get_pos()[1] + won_level_text.get_dimensions()[1] + gap
        points_text.set_pos((x, y))
        won_level_text.draw(self.DISPLAYSURF)
        points_text.draw(self.DISPLAYSURF)

    def __set_won_level_buttons_pos(self):
        #gap = 20
        x = (self.WINDOW_WIDTH // 2) - (self.next_level_button.get_dimensions()[0] // 2)
        y = (self.WINDOW_HEIGHT // 2) - (self.next_level_button.get_dimensions()[1] // 2)
        self.next_level_button.set_x_y_pos(x, y)
        #y += gap + self.next_level_button.get_dimensions()[1]
        #self.end_game_button.set_x_y_pos(x, y)

    def draw_won_level(self, level:int, points:int):
        if self.to_play_next_level_sound:
            self.play_next_level_sound()
            self.to_play_next_level_sound = False
        self.DISPLAYSURF.fill(self.BLACK)
        self.__set_won_level_buttons_pos()
        self.__draw_won_level_texts(level, points)
        self.next_level_button.draw(self.DISPLAYSURF)
        #self.end_game_button.draw(self.DISPLAYSURF)

    def click_in_won_level_buttons(self, x, y):
        if self.presenter.is_won_game():
            if self.next_level_button.is_clicked(x, y):
                self.presenter.next_level()
                self.to_play_next_level_sound = True

    def draw_game_over(self):
        self.DISPLAYSURF.fill(self.BLACK)
        self.stop_background_music()
        self.play_game_over_music()
        self.draw_table(self.presenter.get_players())
        row_size = self.WINDOW_HEIGHT // 13
        game_over_text = Text("Game Over", (0, 0), 50)
        width, height = game_over_text.get_dimensions()
        x, y = (self.WINDOW_WIDTH // 2) - (width // 2), 0
        game_over_text.set_pos((x, y))
        game_over_text.draw(self.DISPLAYSURF)

        x = (self.WINDOW_WIDTH // 3) // 2
        y = self.WINDOW_HEIGHT - row_size


        if self.writing_name and self.presenter.is_new_record():
            horizontal_gap = 10
            new_record_text = Text("New record, write your name:", (x,y), 30)
            new_record_text.draw(self.DISPLAYSURF)
            x += horizontal_gap + new_record_text.get_dimensions()[0]
            self.line_edit.set_pos((x, y))
            self.line_edit.draw(self.DISPLAYSURF)
            self.line_edit.set_font_size(30)
            x += self.line_edit.get_dimensions()[0] + horizontal_gap
            self.submit_name_button.set_x_y_pos(x, y)
            self.submit_name_button.draw(self.DISPLAYSURF)
        else:
            self.main_menu_button.set_x_y_pos(x, y)
            self.main_menu_button.draw(self.DISPLAYSURF)

    def click_in_game_over_buttons(self, x, y):
        if self.writing_name and self.submit_name_button.is_clicked(x, y) and self.presenter.is_new_record():
            if not self.line_edit.is_empty():
                self.presenter.insert_player(self.line_edit.get_text())
                self.presenter.update_players()
                self.writing_name = False
        elif (not self.writing_name or not self.presenter.is_new_record()) and self.main_menu_button.is_clicked(x, y):
            self.stop_game_over_music()
            self.play_background_music()
            self.presenter.main_menu()



    def draw_table(self, table:list):
        vertical_gap = 30
        header = ["Name", "Level", "Points"]
        column_size = self.WINDOW_WIDTH // 3
        row_size = self.WINDOW_HEIGHT // 13
        y = row_size
        header_size = 30
        for table_header in range(len(header)):
            x = ((table_header * column_size) + ((table_header + 1) * column_size))
            current_header = Text(header[table_header], (0, 0), header_size)
            x = (x // 2) - (current_header.get_dimensions()[0] // 2)
            current_header.set_pos((x, y))
            current_header.draw(self.DISPLAYSURF)

        counter = 2
        text_size = 18
        for row in range(len(table)):
            for column in range(len(table[row])):
                x = (column * column_size) + ((column + 1) * column_size)
                y = row_size * counter
                current_text = Text(str(table[row][column]), (0, 0), text_size)
                x = (x // 2) - (current_text.get_dimensions()[0] // 2)
                current_text.set_pos((x, y))
                current_text.draw(self.DISPLAYSURF)
            counter += 1

    def draw_main_menu(self):
        self.play_background_music()
        self.DISPLAYSURF.fill(self.BLACK)
        gap = 20
        y = self.WINDOW_HEIGHT // 3
        x = (self.WINDOW_WIDTH // 2) - (self.play_button.get_dimensions()[0] // 2)
        self.play_button.set_x_y_pos(x, y)
        y += gap + self.play_button.get_dimensions()[1]
        self.statistic_button.set_x_y_pos(x, y)
        y += gap + self.statistic_button.get_dimensions()[1]
        self.about_button.set_x_y_pos(x, y)
        y += gap + self.about_button.get_dimensions()[1]
        self.quit_main_menu_button.set_x_y_pos(x, y)
        self.play_button.draw(self.DISPLAYSURF)
        self.statistic_button.draw(self.DISPLAYSURF)
        self.about_button.draw(self.DISPLAYSURF)
        self.quit_main_menu_button.draw(self.DISPLAYSURF)

    def click_in_main_menu(self, x, y):
        if self.presenter.is_main_menu():
            if self.play_button.is_clicked(x, y):
                self.presenter.play()
                self.set_level_constants()
            elif self.statistic_button.is_clicked(x, y):
                self.presenter.statistic()
            elif self.about_button.is_clicked(x, y):
                self.presenter.about_menu()
            elif self.quit_main_menu_button.is_clicked(x, y):
                self.quit()

    def click_in_statistic_menu(self, x, y):
        if self.presenter.is_statistic():
            if self.main_menu_button.is_clicked(x, y):
                self.presenter.main_menu()
            elif self.reset_statistics_button.is_clicked(x, y):
                self.presenter.reset_statistics()

    def draw_statistic(self):
        self.DISPLAYSURF.fill(self.BLACK)
        self.draw_table(self.presenter.get_players())
        x = (self.WINDOW_WIDTH // 4) - (self.main_menu_button.get_dimensions()[0] // 2)
        y = self.WINDOW_HEIGHT - (self.WINDOW_HEIGHT // 13)
        self.main_menu_button.set_x_y_pos(x, y)
        self.main_menu_button.draw(self.DISPLAYSURF)
        x = (((self.WINDOW_WIDTH // 2) + self.WINDOW_WIDTH) // 2) - (self.reset_statistics_button.get_dimensions()[0] // 2)
        self.reset_statistics_button.set_x_y_pos(x, y)
        self.reset_statistics_button.draw(self.DISPLAYSURF)


    def draw_about(self):
        self.DISPLAYSURF.fill(self.BLACK)
        text1 = Text("Created by Rolando Juan Rio Garaboa", (0,0), 30)
        text2 = Text("email: rolandorio06@nauta.cu", (0, 0), 30)
        text3 = Text("Images from: www.pixabay.com", (0,0), 30)
        text4 = Text("Sounds from: www.pacdv.com/sounds/", (0,0), 30)

        gap = 20
        x = (self.WINDOW_WIDTH // 2) - (text1.get_dimensions()[0] // 2)
        y = (self.WINDOW_HEIGHT // 4) - (text1.get_dimensions()[1] // 2)
        text1.set_pos((x, y))
        text1.draw(self.DISPLAYSURF)
        x = (self.WINDOW_WIDTH // 2) - (text2.get_dimensions()[0] // 2)
        y += text1.get_dimensions()[1] + gap
        text2.set_pos((x, y))
        text2.draw(self.DISPLAYSURF)
        x = (self.WINDOW_WIDTH // 2) - (text3.get_dimensions()[0] // 2)
        y += text2.get_dimensions()[1] + gap + 50
        text3.set_pos((x, y))
        text3.draw(self.DISPLAYSURF)
        x = (self.WINDOW_WIDTH // 2) - (text4.get_dimensions()[0] // 2)
        y += text3.get_dimensions()[1] + gap
        text4.set_pos((x, y))
        text4.draw(self.DISPLAYSURF)
        x = (self.WINDOW_WIDTH // 2) - (self.main_menu_button.get_dimensions()[0] // 2)
        y += text4.get_dimensions()[1] + gap
        self.main_menu_button.set_x_y_pos(x, y)
        self.main_menu_button.draw(self.DISPLAYSURF)

    def click_in_about_menu(self, x, y):
        if self.presenter.is_about_menu():
            if self.main_menu_button.is_clicked(x, y):
                self.presenter.main_menu()