
from model.game import Game
from view.game_screen import GameScreen

class PrincipalController:
    WIDTH = 10
    HEIGHT = 8
    IMAGE_PATH = "data\\images\\tile_images"
    NOT_CLICKED_TILE_PATH = "data\\images\\tiles\\not_clicked_tile.png"
    CLICKED_TILE_PATH = "data\\images\\tiles\\clicked_tile.png"

    DATABASE_PATH = "database\\players.db"

    def __init__(self):
        self.game = Game(self.WIDTH, self.HEIGHT)
        self.view = None
        self.players = []

    def run_game(self):
        self.view = GameScreen(self)
        self.view.run()

    def play(self):

        self.game.run_game()

    def pause_game(self):
        self.game.pause_game()

    def resume_game(self):
        self.game.resume_game()

    def get_board_dimension(self):
        """
        Return (WIDTH, HEIGHT).
        """
        return self.game.get_board_dimension()

    def is_main_menu(self):
        return self.game.is_main_menu()

    def is_playing_game(self):
        return self.game.is_playing_game()

    def is_paused_game(self):
        return self.game.is_paused_game()

    def is_game_over(self):
        return self.game.is_game_over()

    def is_statistic(self):
        return self.game.is_statistic()

    def is_won_game(self):
        return self.game.is_won_game()

    def get_current_percent(self):
        return self.game.get_current_time_percent()

    def get_id_board_element(self, i, j):
        """This return an integer representing the id and the index of the image
        of the tile in the position (i,j) of the board.
        This mathod return -1 if there is not tile in that position."""
        return self.game.get_id_board_element(i, j)

    def is_a_tile(self, i, j):
        return self.game.is_a_tile(i, j)

    def is_clicked_tile(self, i, j):
        return self.game.is_clicked_tile(i, j)

    def is_advised_tile(self, i, j):
        return self.game.is_advised_tile(i, j)

    def is_help_time_over(self):
        if self.game.is_advised_tile_chronometer_done():
            self.game.reset_advised_tile_chronometer()
            self.game.reset_advised_tiles()
            return True
        return False

    def set_advised_tile(self):
        self.game.set_a_advised_tile_pair()


    def is_max_selected_tiles(self):
        return self.game.is_max_selected_tiles()

    def add_selected_tile(self, i, j):
        self.game.add_selected_tile(i, j)

    def remove_selected_tile(self, i, j):
        self.game.remove_selected_tile(i, j)

    def play_movement(self):
        lines = self.game.play_movement()
        self.view.draw_line_images(lines.get_positions(), lines.get_lines())

    def delay_thread(self, seconds:float):
        self.game.delay_thread(seconds)

    def get_user_level(self):
        return self.game.get_user_level()

    def get_user_points(self):
        return self.game.get_user_points()

    def next_level(self):
        self.game.next_level()

    def get_players(self):
        return self.game.get_players_from_memory()

    def update_players(self):
        self.game.update_players_from_memory()

    def game_over(self):
        self.update_players()
        self.game.game_over()


    def is_new_record(self):
        return self.game.is_new_record()

    def insert_player(self, name):
        self.game.insert_player(name)

    def main_menu(self):
        self.game.main_menu()

    def about_menu(self):
        self.game.about_menu()

    def is_about_menu(self):
        return self.game.is_about_menu()

    def statistic(self):
        self.game.statistic()

    def reset_statistics(self):
        self.game.reset_statistics()
        self.update_players()