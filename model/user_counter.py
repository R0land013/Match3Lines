


class UserCounter:

    def __init__(self):
        self.__level = 1
        self.__points = 0

    def get_level(self):
        return self.__level

    def get_points(self):
        return self.__points

    def won_level(self, time):
        time = int(time)
        self.__points += (time * 2)

    def increase_level(self, quantity:int = 1):
        self.__level += quantity

    def increase_points(self, points:int):
        self.__points += int(points)

    def decrease_points(self, points:int):
        if self.__points - points >= 0:
            self.__points -= int(points)
        else:
            self.__points = 0

    def reset(self):
        self.__level = 1
        self.__points = 0

    def are_points_bigger_than(self, quantity:int):
        return self.__points >= quantity