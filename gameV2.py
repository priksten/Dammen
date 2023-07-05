# Create game class
class Game:
    def __init__(self):
        self.white_win = False
        self.black_win = False
        self.draw_by_agreement = False
        self.draw_by_position = False
        self.draw_by_material = False
        self.white_to_play = True
        self.black_to_play = False
        self.position_list = dict()
        self.square_name_list = dict()
        self.forced_capture = False
        self.capture_possible = False
        self.legal_moves_white = list()
        self.legal_moves_black = list()
        self.capture_list_white = list()
        self.capture_list_black = list()
        self.main_list()
        self.name_square_list()
        self.legal_moves_list("white")

    def main_list(self):
        """Make a list of the start position of the board"""
        for i in range(10):
            row = i
            for j in range(10):
                column = j
                self.position_list[row, column] = []

        self.position_list[0, 1] = ["black", "stone"]
        self.position_list[0, 3] = ["black", "stone"]
        self.position_list[0, 5] = ["black", "stone"]
        self.position_list[0, 7] = ["black", "stone"]
        self.position_list[0, 9] = ["black", "stone"]
        self.position_list[1, 0] = ["black", "stone"]
        self.position_list[1, 2] = ["black", "stone"]
        self.position_list[1, 4] = ["black", "stone"]
        self.position_list[1, 6] = ["black", "stone"]
        self.position_list[1, 8] = ["black", "stone"]
        self.position_list[2, 1] = ["black", "stone"]
        self.position_list[2, 3] = ["black", "stone"]
        self.position_list[2, 5] = ["black", "stone"]
        self.position_list[2, 7] = ["black", "stone"]
        self.position_list[2, 9] = ["black", "stone"]
        self.position_list[3, 0] = ["black", "stone"]
        self.position_list[3, 2] = ["black", "stone"]
        self.position_list[3, 4] = ["black", "stone"]
        self.position_list[3, 6] = ["black", "stone"]
        self.position_list[3, 8] = ["black", "stone"]
        
        self.position_list[6, 1] = ["white", "stone"]
        self.position_list[6, 3] = ["white", "stone"]
        self.position_list[6, 5] = ["white", "stone"]
        self.position_list[6, 7] = ["white", "stone"]
        self.position_list[6, 9] = ["white", "stone"]
        self.position_list[7, 0] = ["white", "stone"]
        self.position_list[7, 2] = ["white", "stone"]
        self.position_list[7, 4] = ["white", "stone"]
        self.position_list[7, 6] = ["white", "stone"]
        self.position_list[7, 8] = ["white", "stone"]
        self.position_list[8, 1] = ["white", "stone"]
        self.position_list[8, 3] = ["white", "stone"]
        self.position_list[8, 5] = ["white", "stone"]
        self.position_list[8, 7] = ["white", "stone"]
        self.position_list[8, 9] = ["white", "stone"]
        self.position_list[9, 0] = ["white", "stone"]
        self.position_list[9, 2] = ["white", "stone"]
        self.position_list[9, 4] = ["white", "stone"]
        self.position_list[9, 6] = ["white", "stone"]
        self.position_list[9, 8] = ["white", "stone"]
        

        # Try out position
        # self.position_list[4, 3] = ["white", "stone"]
        # self.position_list[3, 4] = ["black", "stone"]
        # self.position_list[3, 6] = ["black", "stone"]
        # self.position_list[1, 4] = ["black", "stone"]
        # self.position_list[5, 8] = ["black", "stone"]
        # self.position_list[1, 6] = ["black", "stone"]
        # self.position_list[1, 8] = ["black", "stone"]
        # self.position_list[5, 2] = ["black", "stone"]
        # self.position_list[7, 2] = ["black", "stone"]
        # self.position_list[6, 9] = ["white", "stone"]

    def make_move(self, old_pos, new_pos, capture_square = None):
        self.position_list[new_pos] = self.position_list[old_pos]
        if capture_square:
            self.position_list[capture_square] = []
        self.position_list[old_pos] = []

    def name_square_list(self):
        square_number = 0
        for square in self.position_list:
            row = square[0]
            column = square[1]
            if row % 2 == 0 and column % 2 == 1 \
                    or row % 2 == 1 and column % 2 == 0:
                square_number += 1
                self.square_name_list[row, column] = square_number

    def check_forced_capture(self, check_color):
        """We check if a capture is available. And if so it's a forced move. We set a value to true so the
        function for making a legal moves list skips over the non capture moves"""

        self.forced_capture = False
        # make a copy of the position list to later restore it in the original state
        pos_list_copy = self.position_list.copy()

        # Determine which color pieces has the opponent
        if check_color == "white":
            enemy_color = "black"
        else:
            enemy_color = "white"
        # loop through all squares to look for pieces of the color we want to check.
        # We do this in four directions. We also take the square behind the square we want to check.
        # THen we check if the check_square has a enemypiece on it and the behind_square is empty.
        # If so we adjust the position list and call another function to check for further captures (on the same move)
        for square in self.position_list:
            if str(check_color) in self.position_list[square]:
                row = int(square[0])
                column = int(square[1])
                if -1 < row + 1 < 10 \
                        and -1 < column + 1 < 10 \
                        and -1 < row + 2 < 10 \
                        and -1 < column + 2 < 10:
                    check_square = (row+1, column+1)
                    behind_square = (row+2, column+2)
                    if enemy_color in self.position_list[check_square] \
                            and self.position_list[behind_square] == []:
                        self.forced_capture = True
                        self.position_list[behind_square] = [str(check_color), "stone"]
                        self.position_list[check_square] = []
                        self.position_list[square] = []
                        move = f"{self.square_name_list[square]}-{self.square_name_list[behind_square]}"
                        self.check_capture_after_forced(behind_square, check_color, move)
                        self.position_list = pos_list_copy
                        pos_list_copy = self.position_list.copy()
                if -1 < row + 1 < 10 \
                        and -1 < column - 1 < 10 \
                        and -1 < row + 2 < 10 \
                        and -1 < row - 2 < 10:
                    check_square = (row+1, column-1)
                    behind_square = (row+2, column -2)
                    if enemy_color in self.position_list[check_square] \
                            and self.position_list[behind_square] == []:
                        self.forced_capture = True
                        self.position_list[behind_square] = [str(check_color), "stone"]
                        self.position_list[check_square] = []
                        self.position_list[square] = []
                        move = f"{self.square_name_list[square]}-{self.square_name_list[behind_square]}"
                        print(move)
                        self.check_capture_after_forced(behind_square, check_color, move)
                        self.position_list = pos_list_copy
                        pos_list_copy = self.position_list.copy()
                if -1 < row - 1 < 10 \
                        and -1 < column - 1 < 10\
                        and -1 < row -2 < 10 \
                        and -1 < column -2 < 10:
                    check_square = (row-1, column-1)
                    behind_square = (row-2, column-2)
                    if enemy_color in self.position_list[check_square] \
                            and self.position_list[behind_square] == []:
                        self.forced_capture = True
                        self.position_list[behind_square] = [str(check_color), "stone"]
                        self.position_list[check_square] = []
                        self.position_list[square] = []
                        move = f"{self.square_name_list[square]}-{self.square_name_list[behind_square]}"
                        print(move)
                        self.check_capture_after_forced(behind_square, check_color, move)
                        self.position_list = pos_list_copy
                        pos_list_copy = self.position_list.copy()
                if -1 < row - 1 < 10 \
                        and -1 < column + 1 < 10 \
                        and -1 < row -2 <  10 \
                        and -1 < column + 2 < 10:
                    check_square = (row-1, column+1)
                    behind_square = (row-2, column+2)
                    if enemy_color in self.position_list[check_square] \
                            and self.position_list[behind_square] == []:
                        self.forced_capture = True
                        self.position_list[behind_square] = [str(check_color), "stone"]
                        self.position_list[check_square] = []
                        self.position_list[square] = []
                        move = f"{self.square_name_list[square]}-{self.square_name_list[behind_square]}"
                        print(move)
                        self.check_capture_after_forced(behind_square, check_color, move)
                        self.position_list = pos_list_copy
                        pos_list_copy = self.position_list.copy()

        if check_color == "white" and self.forced_capture:
            largest_capture = max(self.capture_list_white, key=len)
            self.legal_moves_white.append(largest_capture)
            capture_count_largest = str(largest_capture).count("-")
            for capture in self.capture_list_white:
                capture_count_capture = str(capture).count("-")
                if capture_count_largest == capture_count_capture \
                        and capture != largest_capture:
                    self.legal_moves_white.append(capture)
        elif check_color == "black" and self.forced_capture:
            pass


    def check_capture_after_forced(self, new_square, color, move):
        move_copy = move
        pos_list_copy = self.position_list.copy()
        if color == "white":
            opponent_color = "black"
        else:
            opponent_color = "white"
        row  = int(new_square [0])
        column = int(new_square [1])
        if -1 < row + 1 < 10 \
                and -1 < column + 1 < 10 \
                and -1 < row + 2 < 10 \
                and -1 < column + 2 < 10:
            check_square = (row+1, column+1)
            behind_square = (row+2, column+2)
            if opponent_color in self.position_list[check_square] \
                    and self.position_list[behind_square] == []:
                self.position_list[behind_square] = [str(color), "stone"]
                self.position_list[check_square] = []
                self.position_list[new_square] = []
                new_move = f"-{self.square_name_list[behind_square]}"
                move = f"{move_copy}{new_move}"
                self.check_capture_after_forced(behind_square, color, move)
                self.position_list = pos_list_copy
        if -1 < row + 1 < 10 \
                and -1 < column - 1 < 10 \
                and -1 < row + 2 < 10 \
                and -1 < row -2 < 10:
            check_square = (row+1, column-1)
            behind_square = (row+2, column -2)
            if opponent_color in self.position_list[check_square] \
                    and self.position_list[behind_square] == []:
                self.position_list[behind_square] = [str(color), "stone"]
                self.position_list[check_square] = []
                self.position_list[new_square] = []
                new_move = f"-{self.square_name_list[behind_square]}"
                move = f"{move_copy}{new_move}"
                self.check_capture_after_forced(behind_square, color, move)
                self.position_list = pos_list_copy
        if -1 < row - 1 < 10 \
                and -1 < column - 1 < 10 \
                and -1 < row -2 < 10 \
                and -1 < column - 2 < 10:
            check_square = (row-1, column-1)
            behind_square = (row-2, column-2)
            if opponent_color in self.position_list[check_square] \
                    and self.position_list[behind_square] == []:
                self.position_list[behind_square] = [str(color), "stone"]
                self.position_list[check_square] = []
                self.position_list[new_square] = []
                new_move = f"-{self.square_name_list[behind_square]}"
                move = f"{move_copy}{new_move}"
                self.check_capture_after_forced(behind_square, color, move)
                self.position_list = pos_list_copy
        if -1 < row - 1 < 10 \
                and -1 < column + 1 < 10 \
                and -1 < row -2 < 10 \
                and -1 < column + 2 < 10:
            check_square = (row-1, column+1)
            behind_square = (row-2, column+2)
            if opponent_color in self.position_list[check_square] \
                    and self.position_list[behind_square] == []:
                self.position_list[behind_square] = [str(color), "stone"]
                self.position_list[check_square] = []
                self.position_list[new_square] = []
                new_move = f"-{self.square_name_list[behind_square]}"
                move = f"{move_copy}{new_move}"
                self.check_capture_after_forced(behind_square, color, move)
                self.position_list = pos_list_copy

        if color == "white":
            self.capture_list_white.append(move_copy)
        elif color == "black":
            self.capture_list_white.append(move_copy)

        print(f"white_list {self.capture_list_white}")
        print(f"black list {self.capture_list_black}")

    def legal_moves_list(self, color):
        """"Make a list of the legal moves for the color given as argument to this function"""
        if color == "white":
            enemy_color = "black"
        else:
            enemy_color = "white"

        # We first check if there is a forced capture
        self.check_forced_capture(color)
        # hello
        # If capture is not forced then we check for normal moves
        if not self.forced_capture:
            # print("no forced capture")
            # Check every square on the board
            for square in self.position_list:
                row = int(square[0])
                column = int(square[1])
                if color in self.position_list[square]:
                    if color == "white":
                        # print("checking white")
                        # IF square is inside board bounds
                        if -1 < row -1 < 10 \
                            and - 1 < column + 1 < 10:
                            # Potential square 1
                            pot_square = (row-1, column+1)
                            #Check if new square is not occupied by enemycolor
                            if enemy_color not in self.position_list[pot_square] \
                                and color not in self.position_list[pot_square]:
                                source_square = self.square_name_list[square]
                                dest_square = self.square_name_list[pot_square]
                                move = f"{source_square}-{dest_square}"
                                self.legal_moves_white.append(move)
                        if - 1 < row -1 < 10\
                            and -1 < column -1 < 10:
                            # Potential square 2
                            pot_square = (row-1, column-1)
                            if enemy_color not in self.position_list[pot_square] \
                                and color not in self.position_list[pot_square]:
                                source_square = self.square_name_list[square]
                                dest_square = self.square_name_list[pot_square]
                                move = f"{source_square}-{dest_square}"
                                self.legal_moves_white.append(move)
                    elif color == "black":
                        if -1 < row + 1 < 10\
                            and -1 < column + 1 < 10:
                            pot_square = (row+1, column+1)
                            if enemy_color not in self.position_list[pot_square] \
                                and color not in self.position_list[pot_square]:
                                source_square = self.square_name_list[square]
                                dest_square = self.square_name_list[pot_square]
                                move = f"{source_square}-{dest_square}"
                                self.legal_moves_black.append(move)
                        if -1 < row + 1 < 10 \
                            and -1 < column - 1 < 10:
                            pot_square = (row+1, column-1)
                            if enemy_color not in self.position_list[pot_square] \
                                and color not in self.position_list[pot_square]:
                                source_square = self.square_name_list[square]
                                dest_square = self.square_name_list[pot_square]
                                move = f"{source_square}-{dest_square}"
                                self.legal_moves_black.append(move)



        # print(f"white legal moves {self.legal_moves_white}")




# if __name__ == "__main__":
#    g = Game()

