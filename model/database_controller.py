import sqlite3

class DatabaseController:
    def __init__(self, database_path:str):
        self.__connection = sqlite3.connect(database_path)
        self.__cursor = self.__connection.cursor()
        try:
            self.__create_table()
        except Exception as e:
            print(str(e))

    def __create_table(self):
        self.__cursor.execute('''CREATE TABLE player 
        (id INTEGER PRIMARY KEY, name TEXT, level INTEGER, points INTEGER)''')

    def insert_player(self, name:str, level:int, points:int):
        self.__cursor.execute('''SELECT id FROM player ORDER BY id''')
        player_ids = self.__cursor.fetchall()
        current_id = 0
        if len(player_ids) > 0:
            current_id = player_ids[len(player_ids) - 1][0] + 1
        # Inserting the player----------
        self.__cursor.execute('''INSERT INTO player VALUES (?, ?, ?, ?)''', (current_id, name, level, points))
        self.__connection.commit()
        # --------------------------

        # Proving if there are more than 10 player. If there are 10 players,
        # then erase the player with the lowest points
        self.__cursor.execute('''SELECT id, points FROM player ORDER BY points''')
        player_ids = self.__cursor.fetchall()
        if len(player_ids) > 10:
            lowest_point_player = player_ids[0][0]
            self.__cursor.execute('''DELETE FROM player WHERE id = ?''', (lowest_point_player, ))
        self.__connection.commit()

        self.__cursor.execute('''SELECT id FROM player WHERE id = ? ''', (current_id,))
        prove_id = self.__cursor.fetchall()
        if len(prove_id) > 0:
            return True
        return False
        # -------------------------------------------------------------------------------

    def get_players_sort_by_points(self):
        self.__cursor.execute('''SELECT name, level, points FROM player ORDER BY points''')
        players = self.__cursor.fetchall()
        players.reverse()
        return players

    def is_new_record(self, points):
        self.__cursor.execute('''SELECT points FROM player ORDER BY points''')
        sorted_points = self.__cursor.fetchall()
        new_record = False
        if len(sorted_points) >= 10 and points > sorted_points[0][0]:
            new_record = True
        elif len(sorted_points) < 10:
            new_record = True
        return new_record

    def delete_all_players(self):
        self.__cursor.execute('''DELETE FROM player''')
        self.__connection.commit()

