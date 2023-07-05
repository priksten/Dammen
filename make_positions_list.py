# Class for making position list of the middle of the squares of an ungiven board size.
# start_x is parameter for the x coordinate of the first square (x-coordinaat van linkerrand van het dambord (x=0))
# start_y is parameter for the y coordinate of the first square (y coordinaat van de bovenrand van het dambord (y=0))
# We take the middle of the squares because this is easier to work with when drawing sprites or circles
# (0,0) is het vakje helemaal linksboven(!!!) en (9,9) helemaal rechtsonder(!!!)


class PosList:
    def __init__(self, rows, columns, start_x, start_y, square_width):
        self.list_white_perspective = dict()
        self.list_black_perspective = dict()
        self.start_x = start_x
        self.start_y = start_y
        self.rows = [i for i in range(rows)]
        self.columns = [i for i in range(columns)]
        self.square_width = square_width
        self.make_list()

    def make_list(self):
        start_x_square = self.start_x - (self.square_width // 2)
        start_y_square = self.start_y - (self.square_width // 2)
        new_y = start_y_square
        for row in self.rows:
            new_x = start_x_square
            new_y += self.square_width
            for column in self.columns:
                new_x += self.square_width
                self.list_white_perspective[row, column] = [new_x, new_y]

        return self.list_white_perspective

    def make_list_black(self):
        start_x_square = self.start_x + (len(self.rows) * self.square_width) + (self.square_width // 2)
        start_y_square = self.start_x + (len(self.columns) * self.square_width) +  (self.square_width // 2)
        new_y = start_y_square
        for row in self.rows:
            new_x = start_x_square
            new_y -= self.square_width
            for column in self.columns:
                new_x -= self.square_width
                self.list_white_perspective[row, column] = [new_x, new_y]

        return self.list_white_perspective

# Example. Comment out when using this class as import
p = PosList(10, 10, 0, 0, 70)
# print(p.make_list())



