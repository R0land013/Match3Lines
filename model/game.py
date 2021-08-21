
from model.database_controller import DatabaseController
from model.board import Board
from model.lines import Lines
from model.user_counter import UserCounter
from model.chronometer import Chronometer

class Game:

    # Game states-------------------------
    PLAYING = 0
    PAUSED = 1
    GAME_OVER = 2
    WON_GAME = 3
    MAIN_MENU = 4
    STATISTIC = 5
    ABOUT = 6
    # ------------------------------------

    # --------------------------------------
    POINTS_FOR_CORRECT = 10
    POINTS_FOR_INCORRECT = 5
    TIME_TO_SPEND_FOR_INCORRECT = 0.5
    POINTS_FOR_HELP = 50
    TIME_TO_SPEND_FOR_HELP = 2
    TIME_TO_SEE_HELP = 1
    # --------------------------------------

    def __init__(self, width:int = 10, height:int = 8, user_time:int = 150, database_path:str = "database\\players.db"):
        self.__width = width
        self.__height = height

        # To measure time-------------------
        self.__user_time = user_time
        self.__passed_time = 0
        self.__chronometer = Chronometer()
        # ------------------------------------

        # To store the pair of coordinates that were clicked
        self.__clicked_coordinates = []
        #---------------------------------------------------

        self.__advised_tiles_coordinates = []
        self.__advised_tiles_chronometer = Chronometer()
        self.__end_time_see_help = 0

        self.__game_state = self.MAIN_MENU

        self.__user_counter = UserCounter()
        self.__board = Board(width, height)
        self.__database = DatabaseController(database_path)
        self.__players = self.__database.get_players_sort_by_points()
        self.__new_record = False


    def get_id_board_element(self, i, j):
        """This return an integer representing the id and the index of the image
        of the tile in the position (i,j) of the board.
        This mathod return -1 if there is not tile in that position."""
        return self.__board.get_tile_index(i,j)

    def get_board_dimension(self):
        """
        Return (WIDTH, HEIGHT).
        """
        return self.__board.get_board_size()

    def is_a_tile(self, i, j):
        return self.__board.is_a_tile(i, j)

    def is_clicked_tile(self, i, j):
        if len(self.__clicked_coordinates) < 2:
            return False
        elif self.__clicked_coordinates[0] == i and self.__clicked_coordinates[1] == j:
            return True
        elif len(self.__clicked_coordinates) == 2:
            return False
        elif self.__clicked_coordinates[2] == i and self.__clicked_coordinates[3] == j:
            return True
        return False

    def is_advised_tile(self, i, j):
        if self.__advised_tiles_coordinates == self.__board.ADVISED_TILE_ERROR:
            return False
        return [i, j] in self.__advised_tiles_coordinates

    def __reset_clicked_tiles(self):
        self.__clicked_coordinates.clear()

    def is_max_selected_tiles(self):
        return len(self.__clicked_coordinates) == 4

    def remove_selected_tile(self, i:int, j:int):
        if not self.is_max_selected_tiles() and self.is_clicked_tile(i, j):
            self.__reset_clicked_tiles()

    def add_selected_tile(self, i:int, j:int):
        if self.__board.is_a_tile(i,j) and not self.is_max_selected_tiles():
            self.__clicked_coordinates.append(i)
            self.__clicked_coordinates.append(j)

    def set_a_advised_tile_pair(self):
        if self.__user_counter.are_points_bigger_than(self.POINTS_FOR_HELP):
            self.__advised_tiles_coordinates = self.__board.get_advised_tile_pair()
            if self.__advised_tiles_coordinates != self.__board.ADVISED_TILE_ERROR:
                self.__user_counter.decrease_points(self.POINTS_FOR_HELP)
                self.__chronometer.increase_time(self.TIME_TO_SPEND_FOR_HELP)
                self.__advised_tiles_chronometer.start()
                self.__end_time_see_help = self.__advised_tiles_chronometer.get_current_time() + self.TIME_TO_SEE_HELP


    def is_advised_tile_chronometer_done(self):
        return self.__advised_tiles_chronometer.get_current_time() >= self.__end_time_see_help

    def reset_advised_tile_chronometer(self):
        self.__advised_tiles_chronometer.reset()

    def reset_advised_tiles(self):
        self.__advised_tiles_coordinates = self.__board.ADVISED_TILE_ERROR

    def play_movement(self) -> Lines:
        to_return = Lines("", [])
        if self.is_max_selected_tiles():
            positions = self.__board.play_movement(*self.__clicked_coordinates)

            lines = self.__board.get_lines_by_position(positions)
            to_return = Lines(lines, positions)
            self.__reset_clicked_tiles()
            if to_return.is_empty():
                self.__user_counter.decrease_points(self.POINTS_FOR_INCORRECT)
            else:
                self.__user_counter.increase_points(self.POINTS_FOR_CORRECT)
            if self.__board.is_finished():
                self.won_level()
        return to_return


    def __calculate_passed_time(self):
        self.__passed_time = self.__chronometer.get_current_time()

    def __calculate_percent(self):
        self.__calculate_passed_time()
        if self.__passed_time > self.__user_time:
            self.__game_state = self.GAME_OVER
            self.game_over()
            return 0
        return 100 - ((self.__passed_time * 100) / self.__user_time)

    def get_current_time_percent(self):
        return self.__calculate_percent()


    def is_playing_game(self):
        return self.__game_state == self.PLAYING

    def is_paused_game(self):
        return self.__game_state == self.PAUSED

    def is_game_over(self):
        return self.__game_state == self.GAME_OVER

    def is_won_game(self):
        return self.__game_state == self.WON_GAME

    def is_main_menu(self):
        return self.__game_state == self.MAIN_MENU

    def is_statistic(self):
        return self.__game_state == self.STATISTIC

    def is_about_menu(self):
        return self.__game_state == self.ABOUT

    def run_game(self):
        self.__game_state = self.PLAYING
        self.__set_user_time(self.__user_counter.get_level())
        self.__reset_passed_time()
        self.__reset_clicked_tiles()
        self.__board.init_board()
        self.__chronometer.start()

    def reset_game(self):
        self.__chronometer.reset()
        self.__user_counter.reset()
        self.run_game()

    def statistic(self):
        self.__game_state = self.STATISTIC

    def main_menu(self):
        self.__game_state = self.MAIN_MENU

    def pause_game(self):
        self.__game_state = self.PAUSED
        self.__chronometer.pause()
        self.__game_state = self.PAUSED


    def resume_game(self):
        if self.is_paused_game():
            self.__chronometer.start()
            self.__game_state = self.PLAYING
            self.reset_advised_tiles()
            self.reset_advised_tiles()

    def won_level(self):
        self.reset_advised_tile_chronometer()
        self.reset_advised_tiles()
        self.__game_state = self.WON_GAME
        self.__user_counter.won_level(self.__user_time - self.__passed_time)


    def next_level(self):
        self.__chronometer.reset()
        self.__user_counter.increase_level()
        self.run_game()
        self.reset_advised_tile_chronometer()
        self.reset_advised_tiles()
        self.__game_state = self.PLAYING

    def game_over(self):
        self.__game_state = self.GAME_OVER
        self.__new_record = self.__database.is_new_record(self.__user_counter.get_points())
        self.__chronometer.pause()
        self.__chronometer.reset()
        self.reset_advised_tiles()
        self.reset_advised_tile_chronometer()

    def about_menu(self):
        self.__game_state = self.ABOUT

    def get_players_from_memory(self):
        return self.__players

    def update_players_from_memory(self):
        self.__players = self.get_all_players()

    def get_all_players(self):
        return self.__database.get_players_sort_by_points()

    def insert_player(self, name:str):
        return self.__database.insert_player(name, self.__user_counter.get_level(), self.__user_counter.get_points())

    def delay_thread(self, seconds):
        self.__chronometer.delay_thread(seconds)

    def __set_user_time(self, level):
        self.__user_time = self.__user_time - ((level - 1) * 0.25)

    def __reset_passed_time(self):
        self.__passed_time = 0

    def get_user_level(self):
        return self.__user_counter.get_level()

    def get_user_points(self):
        return self.__user_counter.get_points()

    def is_new_record(self):
        return self.__new_record

    def reset_statistics(self):
        self.__database.delete_all_players()

    def get_clicked_tile_positions(self):
        return self.__clicked_coordinates

