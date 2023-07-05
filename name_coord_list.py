from make_positions_list import PosList


class NameList:
    
    def __init__(self):
        self.pos_list = PosList(10,10,0,0,70)
        self.pos_list = self.pos_list.make_list()
        self.new_pos_list = dict()
        self.square_coord_name = dict()
        self.make_list()


    def make_list(self):
        for square in self.pos_list:
            row = square[0]
            column = square[1]
            if row % 2 == 0 and column % 2 == 1 \
                    or row % 2 == 1 and column % 2 == 0:
                self.new_pos_list[row, column] = self.pos_list[row, column]
        coord_list = self.new_pos_list.values()
        square_number = 0
        for square in coord_list:
            x = square[0]
            y = square[1]
            square_number += 1
            self.square_coord_name[x, y] = square_number

    def get_list(self):
        return self.square_coord_name

