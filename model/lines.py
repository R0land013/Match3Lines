


class Lines:
    def __init__(self, lines:str, positions:list):
        self.__lines = lines
        self.__positions = positions

    def __str__(self):
        return self.__lines + "\n" + str(self.__positions)

    def is_empty(self):
        return len(self.__lines) == 0


    def get_positions(self):
        return self.__positions

    def get_lines(self):
        return self.__lines