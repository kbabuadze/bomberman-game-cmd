
from random import randint
from curses import wrapper
import curses


class Board:
    def __init__(self,width,bombs: int,) -> None:
        self.width = width
        self.bombs = bombs
        self.marks_counter = 0
        self.bombs_init = bombs
        self.game_status = "undefined"

        if bombs > (width**2)-1:
            raise ValueError("Number of bombs should be less then the number of cells")

        self.board = [[[0,False] for _ in range(width)] for _ in range(width)]
        self.marks = [[False for _ in range(width)] for _ in range(width)]
        self.plant_bombs()

    # enumberate cells around bombs
    def enumerate_cell(self,x,y:int)-> None:
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if  x+i >= 0 and y+j >= 0 and x+i < self.width and y+j < self.width and self.board[x+i][y+j][0] != -1:
                    self.board[x+i][y+j][0] += 1

    # pant bombs randomly
    def plant_bombs(self):
        count = 0
        while count < self.bombs:
            i = randint(0,self.width-1)
            j = randint(0,self.width-1)

            if self.board[i][j][0] != -1:
                self.board[i][j][0] = -1
                count += 1
        
        for i in range(self.width):
            for j in range(self.width):
                if self.board[i][j][0] == -1:
                    self.enumerate_cell(i,j)

    # mark cell
    def handle_mark(self,x,y:int):
        if not self.marks[x][y]:
            self.marks_counter += 1
            self.marks[x][y] = True
        else:
            self.marks_counter -= 1
            self.marks[x][y] = False
        
        if self.board[x][y][0] == -1 and self.marks[x][y]:
            self.bombs-=1
        
        if self.bombs == 0 and self.marks_counter == self.bombs_init:
            self.game_status = "won"
            self.reveal_all()

    # handle cell opening operation
    def handle_space(self,x,y: int):
        if self.board[x][y][0] != -1:
            self.reveal_part(x,y)
            return

        self.reveal_all()
        self.game_status = "lost"
        

    # reveal all the cells, happens once per game
    def reveal_all(self):
        for r in range(len(self.board)):
            for c in range(len(self.board)):
                self.board[r][c][1] = True
    
    # when user clicks empty cell all the neighbours
    # and their neighbours without a bomb are revealed
    # recursive solution
    def reveal_part(self,x,y: int)-> None:
        if x < 0 or x > self.width-1 or y < 0 or y > self.width-1 or self.board[x][y][1] == True or self.board[x][y][0] == -1:
            return

        if self.board[x][y][0] > 0:
            self.board[x][y][1] = True
            return

        self.board[x][y][1] = True
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                self.reveal_part(x+i,y+j)

def main(stdscr):

    curses.echo()

    # Clear screen
    stdscr = curses.initscr()

    stdscr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_WHITE)

    stdscr.addstr("Please enter the board width:")
    board_width = int(stdscr.getstr(0,29, 1))

    stdscr.addstr("Please enter the number of bombs:")
    bombs_num = int(stdscr.getstr(1,33, 2))
    
    stdscr.addstr("\n\n")
    stdscr.addstr("Please hit SPACE BAR to open the cell and hit \"m\"-key to mark the cell with a bomb\n")
    stdscr.addstr("Mark all bombs to win!\n") 
    stdscr.addstr("Hit any key to start!\n") 

    b = Board(board_width,bombs_num)

    curr_x = 0 
    curr_y = 0

    while True:
        k = stdscr.getch()
        if b.game_status != "undefined":
            exit()
        stdscr.clear()

        if k == 260 and curr_y > 0:
            curr_y -= 1

        if k == 261 and curr_y < board_width-1:
            curr_y += 1

        if k == 259 and curr_x > 0:
            curr_x-= 1

        if k == 258 and curr_x < board_width-1:
            curr_x += 1

        if k == 32:
            b.handle_space(curr_x,curr_y)
        
        if k == 109:
            b.handle_mark(curr_x,curr_y)
 
        for i,r in enumerate(b.board):
            for j,c in enumerate(r):
                display = c[0]
                if c[1] == 0:
                    display = "x"
                if b.marks[i][j]:
                    display = "m"
                if j == curr_y and i == curr_x:
                    stdscr.addstr("{:^3}".format(str(display)),curses.color_pair(1))
                else:
                    stdscr.addstr("{:^3}".format(str(display)))
            stdscr.addstr('\n')
        if b.game_status == "lost":
            stdscr.addstr("{:^3}\n".format("You lost!"),curses.A_BOLD)
        
        if b.game_status == "won":
            stdscr.addstr("{:^3}\n".format("You won!"),curses.A_BOLD)

        stdscr.refresh()

wrapper(main)()