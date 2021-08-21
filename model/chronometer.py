
import time

class Chronometer:

    def __init__(self):
        self.__initial_time = time.process_time()
        self.__final_time = time.process_time()
        self.__passed_time = 0
        self.__paused = True

    def start(self):
        self.__paused = False
        self.__initial_time = time.process_time()

    def get_current_time(self):
        if self.__paused:
            return self.__passed_time
        self.__final_time = time.process_time()
        self.__passed_time += self.__final_time - self.__initial_time
        self.__initial_time = time.process_time()
        return self.__passed_time

    def pause(self):
        self.__paused = True
        self.__initial_time = 0
        self.__final_time = 0

    def reset(self):
        self.__passed_time = 0

    def increase_time(self, seconds:float):
        self.__passed_time += seconds

    def delay_thread(self, seconds):
        time.sleep(seconds)