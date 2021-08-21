import copy
from random import shuffle


class Tile:
    def __init__(self, id):
        self.id = id  # Id for the tile
        #self.image = image_path  # image of the tile

        self.is_eliminated = False  # if it was eliminated from the board
        self.is_clicked = False  # if the tile was clicked

        self.board_position_i = -1  # row of the board
        self.board_position_j = -1  # column of board
        self.window_position_x = -1  # position x on the window
        self.window_position_y = -1  # position y on the window

    def __str__(self):
        return str(self.id)

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return False
        return self.id == other.id

    def get_board_position(self):
        return (self.board_position_i, self.board_position_j)

    def get_board_pos_i(self):
        return self.board_position_i

    def get_board_pos_j(self):
        return self.board_position_j


    def set_board_position(self, i_j: tuple):
        self.board_position_i = i_j[0]
        self.board_position_j = i_j[1]

    def get_window_position(self):
        return (self.window_position_x, self.window_position_y)

    def get_window_pos_x(self):
        return self.window_position_x

    def get_window_pos_y(self):
        return self.window_position_y

    def set_window_position(self, x_y: tuple):
        self.window_position_x = x_y[0]
        self.window_position_y = x_y[1]

    def has_board_pos(self):
        return self.board_position_i != -1 and self.board_position_j != -1

    def has_window_pos(self):
        return self.window_position_x != -1 and self.window_position_y != -1


class Board:

    UP = "u"
    DOWN = "d"
    RIGHT = "r"
    LEFT = "l"
    # ----------------------------------------------------
    #These lines will be set in a tile where path turns.
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
    #------------------------------------------------------

    # ----------------------------------------
    # This lines is for the first and last tile of a path, where the line is the half of its size.
    UP_HALF = "v"
    DOWN_HALF = "b"
    LEFT_HALF = "n"
    RIGHT_HALF = "m"
    # ------------------------------------------------------

    #

    ADVISED_TILE_ERROR = [[-1, -1], [-1, -1]]
    FINISH = "finish"
    PLAYING = "play"

    def __init__(self, width:int, height:int):
        if (width * height) % 2 != 0:
            raise Exception("There is not an even tile quantity.")
        self.width = width
        self.height = height

        self.tile_data = self.__set_tile_data()  # All tile will always be here, and will not be deleted from here

        self.tile_board = None  # The board to play

        self.tile_data_position = list(range(len(self.tile_data)))  # This is for the tile position in the board, it is helpful
        # to find the if there is a possible movement in the game

        self.eliminated_tiles = 0

        self.game_state = self.PLAYING


    def get_tile_index(self, i:int, j:int):
        tile = self.tile_board[i][j]
        if tile is None:
            return -1
        return tile.id

    def __set_tile_data(self):
        data_tiles = []
        id = 0
        for tile in range((self.height * self.width) // 2):
                current_tile = Tile(id)
                data_tiles.append(copy.deepcopy(current_tile))
                id += 1
        return data_tiles

    def is_finished(self):
        return self.eliminated_tiles == (self.width * self.height) // 2

    def __reset_eliminated_tiles(self):
        self.eliminated_tiles = 0

    def reset_board(self):
        self.init_board()
        self.__reset_eliminated_tiles()
        self.game_state = self.PLAYING

    def init_board(self):
        if ((int(self.width * self.height) / 2) > len(self.tile_data)):
            raise Exception("There are not enough tiles to create the board.")
        self.__reset_eliminated_tiles()
        self.tile_board = self.__separate_by_row()
        self.__generate_playable_board()

    def __separate_by_row(self):
        linear_board = []
        for tile_index in range((self.width * self.height) // 2):
            linear_board.append(copy.deepcopy(self.tile_data[tile_index]))
            linear_board.append(copy.deepcopy(self.tile_data[tile_index]))
        shuffle(linear_board)

        board = [self.__row_of_none(self.width)]
        current_index = 0
        while current_index + self.width <= len(linear_board):
            current_row = [None]
            current_row += linear_board[current_index: current_index + self.width] + [None]
            board.append(current_row)
            current_index += self.width
        board.append(self.__row_of_none(self.width))
        return board

    def __row_of_none(self, width: int):
        row = list(range(width + 2))
        for i in range(len(row)):
            row[i] = None
        return row

    def print_board(self):
        for i in range(len(self.tile_board)):
            for j in range(len(self.tile_board[0])):
                if self.tile_board[i][j] is None:
                    print("*", end=" ")
                else:
                    print(self.tile_board[i][j], end=" ")
            print()
        print()

    def get_board_size(self):
        """
        Return (width, height) of the board.
        """
        if self.tile_board is None:
            return -1, -1
        return len(self.tile_board[0]), len(self.tile_board)

    def is_a_tile(self,i:int, j:int):
        return not self.tile_board[i][j] is None

    def __is_possible_cell(self, i, j):
        if i >= len(self.tile_board) or i < 0 or j >= len(self.tile_board[0]) or j < 0:
            return False
        return True

    def __is_crashed(self, i, j):
        if self.tile_board[i][j] != None:
            return True
        return False

    def __same_column_tiles(self, I1, J1, I2, J2):
        # I1 and J1 are variables tha represent the tile which is above
        lines = ""
        i = I1
        j = J1
        while self.__is_possible_cell(i, j):
            i += 1
            if not self.__is_possible_cell(i, j):
                break
            if self.__is_crashed(i, j):
                if i == I2 and j == J2:
                    lines += (self.DOWN * (I2 - I1))
                else:
                    break
        return lines

    def __to_left_right_side(self, i1: int, j1: int, i2: int, j2: int):
        """
        I1 and J1 belong to the position of the tile which is above
        This form:
        -   -
        |    |
        -   -
        """
        lines = ""
        i = i1
        j = j1
        found = False
        # From left side of the tile-----------------------------------------------
        while self.__is_possible_cell(i, j) and not found:
            is_vertical_fail = False
            i = i1
            j -= 1
            if not self.__is_possible_cell(i, j) or self.__is_crashed(i, j):
                break

            for vertical_i in range(i1 + 1, i2 + 1, 1):  # To check if there is an empty column between rows I1 and I2
                if self.__is_crashed(vertical_i, j):
                    is_vertical_fail = True
                    break
            if not is_vertical_fail:
                for horizontal_j in range(j + 1, j2 + 1, 1):
                    if self.__is_crashed(i2, horizontal_j):  # I2, because there is a column free until I2
                        if horizontal_j == j2:
                            found = True
                            lines = (self.LEFT * abs(j1 - j)) + (self.DOWN * abs(i2 - i1)) + (self.RIGHT * (j2 - j))
                        else:
                            break
        # -----------------------------------------------------------------------

        # From right side of the tile--------------------------------------------------------
        i = i1
        j = j1
        while self.__is_possible_cell(i, j) and not found:
            j += 1
            if not self.__is_possible_cell(i, j) or self.__is_crashed(i, j):
                break
            vertical_fail = False
            for vertical_i in range(i1 + 1, i2 + 1, 1):
                if self.__is_crashed(vertical_i, j):
                    vertical_fail = True
                    break
            if not vertical_fail:
                for horizontal_j in range(j - 1, j2 - 1, -1):
                    if self.__is_crashed(i2, horizontal_j):
                        if horizontal_j == j2:
                            found = True
                            lines = (self.RIGHT * abs(j - j1)) + (self.DOWN * abs(i2 - i1)) + (self.LEFT * abs(j - j2))
                        else:
                            break
        # -----------------------------------------------------------------------------------
        return lines

    def __same_row_tiles(self, I1: int, J1: int, I2: int, J2: int, left: bool):
        # I1 and J1 are variables tha represent the tile which is in left side
        lines = ""
        i = I1
        j = J1
        increment = 1
        if not left:
            increment = -1
        while self.__is_possible_cell(i, j):
            j += increment
            if not self.__is_possible_cell(i, j):
                break
            if self.__is_crashed(i, j):
                if i == I2 and j == J2:
                    if left:
                        lines += (self.RIGHT * abs(J2 - J1))
                    else:
                        lines += (self.LEFT * abs(J2 - J1))
                else:
                    break
        return lines

    def __to_up_down_side(self, I1: int, J1: int, I2: int, J2: int, left: bool):
        """
        This form:
         _
        | | |_|
        """
        lines = ""
        i = I1
        j = J1
        found = False
        one = 1
        if not left:
            one = -1

        # From up side of the tile-----------------------------------------------------------------
        while self.__is_possible_cell(i, j) and not found:
            is_horizontal_fail = False
            j = J1
            i -= 1
            if not self.__is_possible_cell(i, j) or self.__is_crashed(i, j):
                break
            for horizontal_j in range(J1 + one, J2 + one, one):  # To check if there is an empty column between rows I1 and I2
                if self.__is_crashed(i, horizontal_j):
                    is_horizontal_fail = True
                    break
            if not is_horizontal_fail:
                for vertical_i in range(i + 1, I2 + 1, 1):
                    if self.__is_crashed(vertical_i, J2):  # I2, because there is a column free until I2
                        if vertical_i == I2:
                            found = True
                            if left:
                                lines = (self.UP * abs(I1 - i)) + (self.RIGHT * abs(J2 - J1)) + (self.DOWN * abs(I2 - i))
                            else:
                                lines = (self.UP * abs(I1 - i)) + (self.LEFT * abs(J1 - J2)) + (self.DOWN * abs(I2 - i))
                        else:
                            break
        # ---------------------------------------------------------------------------------------------

        # From down side of the tile-------------------------------------------------------------------
        i = I1
        while self.__is_possible_cell(i, j) and not found:
            is_horizontal_fail = False
            j = J1
            i += 1
            if not self.__is_possible_cell(i, j) or self.__is_crashed(i, j):
                break
            for horizontal_j in range(J1 + one, J2 + one, one):
                if self.__is_crashed(i, horizontal_j):
                    is_horizontal_fail = True
                    break
            if not is_horizontal_fail:
                for vertical_i in range(i - 1, I2 - 1, -1):
                    if self.__is_crashed(vertical_i, J2):  # I2, because there is a column free until I2
                        if vertical_i == I2:
                            found = True
                            if left:
                                lines = (self.DOWN * abs(i - I1)) + (self.RIGHT * abs(J2 - J1)) + (self.UP * abs(i - I2))
                            else:
                                lines = (self.DOWN * abs(i - I1)) + (self.LEFT * abs(J1 - J2)) + (self.UP * abs(i - I2))
                        else:
                            break
        # --------------------------------------------------------------------------------------------
        return lines

    def __border_side_lines(self, I1: int, J1: int, I2: int, J2: int, to_left: bool):
        lines = ""
        i = I1
        j = J1
        found = False
        increment = 1
        if not to_left:
            increment = -1
        # From a side of the tile----------------------------------------------------------------
        # _   _
        #  | |
        horizontal_fail = False
        for horizontal_j in range(J1 + increment, J2 + increment, increment):
            if self.__is_crashed(I1, horizontal_j):
                horizontal_fail = True
                break
        if not horizontal_fail:
            for vertical_i in range(I1 + 1, I2 + 1, 1):
                if self.__is_crashed(vertical_i, J2):
                    if vertical_i == I2:
                        if to_left:
                            lines = (self.RIGHT * abs(J2 - J1)) + (self.DOWN * abs(I2 - I1))
                        else:
                            lines = (self.LEFT * abs(J1 - J2)) + (self.DOWN * abs(I2 - I1))
                        found = True
                    break
        # -----------------------------------------------------------------------

        # From down side of the tile------------------------------------------------------------
        # |_  _|
        if not found:
            vertical_fail = False
            for vertical_i in range(I1 + 1, I2 + 1, 1):
                if self.__is_crashed(vertical_i, J1):
                    vertical_fail = True
                    break
            if not vertical_fail:
                for horizontal_j in range(J1 + increment, J2 + increment, increment):
                    if self.__is_crashed(I2, horizontal_j):
                        if horizontal_j == J2:
                            if to_left:
                                lines = (self.DOWN * abs(I2 - I1)) + (self.RIGHT * abs(J2 - J1))
                            else:
                                lines = (self.DOWN * abs(I2 - I1)) + (self.LEFT * abs(J1 - J2))
                        break
        # --------------------------------------------------------------------
        return lines

    def __stair_side(self, i1: int, j1: int, i2: int, j2: int, to_left):
        """
        I1 and J1 are the coordinates of the tile that is above.
        This Form:
        |_    _|      _  _
          |  |      _|    |_
        """
        lines = ""
        found = False
        i = i1
        j = j1
        increment = 1
        if not to_left:
            increment = -1
        # Stair from down side--------------------------------------------------
        while self.__is_possible_cell(i, j) and not found:
            i += 1
            j = j1
            horizontal_fail = False
            if not self.__is_possible_cell(i, j) or self.__is_crashed(i, j):
                break

            for horizontal_j in range(j + increment, j2 + increment, increment):
                if self.__is_crashed(i, horizontal_j):
                    horizontal_fail = True
                    break

            if not horizontal_fail:
                for vertical_i in range(i + 1, i2 + 1, 1):
                    if self.__is_crashed(vertical_i, j2):
                        if vertical_i == i2:
                            if to_left:
                                lines = (self.DOWN * abs(i - i1)) + (self.RIGHT * abs(j2 - j1)) + (self.DOWN * abs(i2 - i))
                            else:
                                lines = (self.DOWN * abs(i - i1)) + (self.LEFT * abs(j1 - j2)) + (self.DOWN * abs(i2 - i))
                            found = True
                        else:
                            break
        # ----------------------------------------------------------------------------------------------

        # Stair fom a side------------------------------------------------------------------------------
        if not found:
            i = i1
            j = j1
            increment = 1
            if not to_left:
                increment = -1
        while self.__is_possible_cell(i, j) and not found:
            j += increment
            if not self.__is_possible_cell(i, j) or self.__is_crashed(i, j):
                break
            vertical_fail = False
            for vertical_i in range(i1 + 1, i2 + 1, 1):
                if self.__is_crashed(vertical_i, j):
                    vertical_fail = True
                    break
            if not vertical_fail:
                for horizontal_j in range(j + increment, j2 + increment, increment):
                    if self.__is_crashed(i2, horizontal_j):
                        if horizontal_j == j2:
                            if to_left:
                                lines = (self.RIGHT * abs(j - j1)) + (self.DOWN * abs(i2 - i1)) + (self.RIGHT * abs(j2 - j))
                            else:
                                lines = (self.LEFT * abs(j1 - j)) + (self.DOWN * abs(i2 - i1)) + (self.LEFT * abs(j - j2))
                            found = True
                        break
        return lines

    def __generate_playable_board(self):
        while not self.__is_possible_play():
            self.__shuffle_tiles()

    def __movement_done(self):
        self.eliminated_tiles += 1
        if self.eliminated_tiles == (self.width * self.height) // 2:
            self.ready_to_play = False

    def __get_positions_by_line(self, incomplete_lines:str, i:str, j:str):
        """incomplete_lines will content the lines without turns.
        i and j are variables to store the initial position of a path."""
        positions = [(i, j)]
        for line in incomplete_lines:
            if line == self.RIGHT:
                j += 1
            elif line == self.LEFT:
                j -= 1
            elif line == self.UP:
                i -= 1
            elif line == self.DOWN:
                i += 1
            positions.append((i, j))
        return positions


    def play_movement(self, i1, j1, i2, j2):
        lines = ""
        if not self.__is_possible_cell(i1, j1) or not self.__is_possible_cell(i2, j2):
            return lines
        elif not self.tile_board[i1][j1] == self.tile_board[i2][j2]:
            return lines
        initial_i = 0
        initial_j = 0
        positions = []
        if i1 <= i2:
            lines = self.__make_lines(i1, j1, i2, j2)
            initial_i = i1
            initial_j = j1
        else:
            lines = self.__make_lines(i2, j2, i1, j1)
            initial_i = i2
            initial_j = j2

        if lines != "":
            self.tile_board[i1][j1] = None
            self.tile_board[i2][j2] = None
            self.__movement_done()
            positions = self.__get_positions_by_line(lines, initial_i,initial_j)  # To get the psitions of every tile in the path
            lines = self.__get_correct_lines(lines)
            if self.is_finished():
                self.game_state = self.FINISH
            elif not self.is_finished() and not self.__is_possible_play():
                self.__generate_playable_board()

        return positions

    def __shuffle_tiles(self):
        tile_positions = []
        tile_id = []
        for i in range(len(self.tile_board)):
            for j in range(len(self.tile_board[0])):
                if not self.tile_board[i][j] is None:
                    tile_positions.append([i, j])
                    tile_id.append(self.tile_board[i][j].id)
        shuffle(tile_id)
        id_index = 0
        for position_index in tile_positions:
            self.tile_board[position_index[0]][position_index[1]] = copy.deepcopy(self.tile_data[tile_id[id_index]])

            id_index += 1

    def get_advised_tile_pair(self):

        if not self.__is_possible_play():
            return self.ADVISED_TILE_ERROR
        tile_index_position = list(range(len(self.tile_data)))
        tile_index_position = list(map(lambda x: [], tile_index_position))
        # This piece of code is to store all the tile pairs in an equal index
        # In this we can prove faster the path from a tile to another one.
        # -------------------------------------------------------------
        for i in range(len(self.tile_board)):
            for j in range(len(self.tile_board[0])):
                if not self.tile_board[i][j] is None:
                    tile_index_position[self.tile_board[i][j].id].append(i)
                    tile_index_position[self.tile_board[i][j].id].append(j)
        # -----------------------------------------------------------
        for tile_pair in tile_index_position:
            if not len(tile_pair) == 0:
                # This line is to sort the tiles by the I index
                # This line could raise an Exception. If there is a tile that has not pair
                # the program will raise an index out of range Exception
                indexes = self.__above_tile(tile_pair[0], tile_pair[1], tile_pair[2], tile_pair[3])
                lines = self.__make_lines(indexes[0], indexes[1], indexes[2], indexes[3])
                if lines != "":
                    return [[indexes[0], indexes[1]], [indexes[2], indexes[3]]]
        return self.ADVISED_TILE_ERROR

    def __is_possible_play(self):
        tile_index_position = list(range(len(self.tile_data)))
        tile_index_position = list(map(lambda x: [], tile_index_position))
        # This piece of code is to store all the tile pairs in an equal index
        # In this we can prove faster the path from a tile to another one.
        # -------------------------------------------------------------
        for i in range(len(self.tile_board)):
            for j in range(len(self.tile_board[0])):
                if not self.tile_board[i][j] is None:
                    tile_index_position[self.tile_board[i][j].id].append(i)
                    tile_index_position[self.tile_board[i][j].id].append(j)
        # -----------------------------------------------------------
        for tile_pair in tile_index_position:
            if not len(tile_pair) == 0:
                # This line is to sort the tiles by the I index
                # This line could raise an Exception. If there is a tile that has not pair
                # the program will raise an index out of range Exception
                indexes = self.__above_tile(tile_pair[0], tile_pair[1], tile_pair[2], tile_pair[3])
                lines = self.__make_lines(indexes[0], indexes[1], indexes[2], indexes[3])
                if lines != "":
                    return True
        return False

    def __get_correct_lines(self, lines):
        correct_lines = ""
        x = 0
        y = 1
        correct_lines += lines[x]
        while x <= len(lines) - 1:
            if x == len(lines) - 1:
                correct_lines += lines[x]
                x += 1
                y += 1
                continue
            characters = lines[x : y + 1]
            if self.LEFT in characters and self.UP in characters:
                if self.LEFT == characters[0]:
                    correct_lines += self.TURN_FROM_RIGHT_TO_UP
                else:
                    correct_lines += self.TURN_FROM_LEFT_TO_DOWN

            elif self.RIGHT in characters and self.UP in characters:
                if self.RIGHT == characters[0]:
                    correct_lines += self.TURN_FROM_LEFT_TO_UP
                else:
                    correct_lines += self.TURN_FROM_RIGHT_TO_DOWN

            elif self.LEFT in characters and self.DOWN in characters:
                if self.LEFT == characters[0]:
                    correct_lines += self.TURN_FROM_RIGHT_TO_DOWN
                else:
                    correct_lines += self.TURN_FROM_LEFT_TO_UP
            elif self.RIGHT in characters and self.DOWN in characters:
                if self.RIGHT == characters[0]:
                    correct_lines += self.TURN_FROM_LEFT_TO_DOWN
                else:
                    correct_lines += self.TURN_FROM_RIGHT_TO_UP
            else:
                correct_lines += lines[x]
            x += 1
            y += 1
        return correct_lines

    def __above_tile(self, i1, j1, i2, j2):
        if i1 <= i2:
            return i1, j1, i2, j2
        return i2, j2, i1, j1

    def __make_lines(self, i1, j1, i2, j2):
        lines = ""
        if self.tile_board[i1][j1] == self.tile_board[i2][j2]:
            if i1 < i2:
                if j1 == j2:  # In the same column
                    lines = self.__same_column_tiles(i1, j1, i2, j2)
                    if lines == "":
                        lines = self.__to_left_right_side(i1, j1, i2, j2)

                if j1 < j2 and lines == "":  # (i1, j1) In the left

                    lines = self.__border_side_lines(i1, j1, i2, j2, True)
                    if lines == "":
                        lines = self.__stair_side(i1, j1, i2, j2, True)
                    if lines == "":
                        lines = self.__to_left_right_side(i1, j1, i2, j2)
                    if lines == "":
                        lines = self.__to_up_down_side(i1, j1, i2, j2, True)

                if j1 > j2 and lines == "":  # (i1, j1) In the right
                    lines = self.__border_side_lines(i1, j1, i2, j2, False)
                    if lines == "":
                        lines = self.__stair_side(i1, j1, i2, j2, False)
                    if lines == "":
                        lines = self.__to_left_right_side(i1, j1, i2, j2)
                    if lines == "":
                        lines = self.__to_up_down_side(i1, j1, i2, j2, False)
            elif i1 == i2:
                if j1 < j2:
                    lines = self.__same_row_tiles(i1, j1, i2, j2, True)
                    if lines == "":
                        lines = self.__to_up_down_side(i1, j1, i2, j2, True)
                elif j1 > j2:
                    lines = self.__same_row_tiles(i1, j1, i2, j2, False)
                    if lines == "":
                        lines = self.__to_up_down_side(i1, j1, i2, j2, False)
        return lines

    def get_lines_by_position(self, positions: list):
        x = -1
        y = 0
        z = 1
        lines = ""

        while y <= len(positions) - 1:
            current_line = ""
            if y == 0:
                current_line = self.__get_line_given_3_positions(None, positions[y], positions[z])
            elif y == len(positions) - 1:
                current_line = self.__get_line_given_3_positions(positions[x], positions[y], None)
            else:
                current_line = self.__get_line_given_3_positions(positions[x], positions[y], positions[z])
            lines += current_line
            x += 1
            y += 1
            z += 1
        return lines

    def __get_line_given_3_positions(self, x=None, y=None, z=None):
        line = ""
        row = 0
        column = 1
        if x is None:
            if y[column] == z[column]:
                if y[row] > z[row]:
                    line = self.UP_HALF
                elif y[row] < z[row]:
                    line = self.DOWN_HALF
            elif y[row] == z[row]:
                if y[column] > z[column]:
                    line = self.LEFT_HALF
                elif y[column] < z[column]:
                    line = self.RIGHT_HALF
        elif z is None:
            if y[column] == x[column]:
                if y[row] > x[row]:
                    line = self.UP_HALF
                elif y[row] < x[row]:
                    line = self.DOWN_HALF
            elif y[row] == x[row]:
                if y[column] > x[column]:
                    line = self.LEFT_HALF
                elif y[column] < x[column]:
                    line = self.RIGHT_HALF
        else:
            if x[column] != z[column] and x[row] != z[row]:
                line = self.__get_turned_line(x, y, z)
            elif x[row] == z[row]:
                if x[column] < z[column]:
                    line = self.RIGHT
                elif x[column] > z[column]:
                    line = self.LEFT
            elif x[column] == z[column]:
                if x[row] < z[row]:
                    line = self.DOWN
                elif x[row] > z[row]:
                    line = self.UP
        return line

    def __get_turned_line(self, pos_x, pos_y, pos_z):
        row = 0
        column = 1
        line = ""
        if pos_x[row] > pos_z[row]:
            if pos_x[column] < pos_z[column]:
                if pos_x[row] - 1 == pos_y[row]:
                    line = self.TURN_FROM_RIGHT_TO_DOWN
                else:
                    line = self.TURN_FROM_LEFT_TO_UP
            elif pos_x[column] > pos_z[column]:
                if pos_x[row] - 1 == pos_y[row]:
                    line = self.TURN_FROM_LEFT_TO_DOWN
                else:
                    line = self.TURN_FROM_RIGHT_TO_UP

        elif pos_x[row] < pos_z[row]:
            if pos_x[column] < pos_z[column]:
                if pos_x[row] + 1 == pos_y[row]:
                    line = self.TURN_FROM_RIGHT_TO_UP
                else:
                    line = self.TURN_FROM_LEFT_TO_DOWN
            elif pos_x[column] > pos_z[column]:
                if pos_x[row] + 1 == pos_y[row]:
                    line = self.TURN_FROM_LEFT_TO_UP
                else:
                    line = self.TURN_FROM_RIGHT_TO_DOWN

        return line

