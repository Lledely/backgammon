import pygame 
import pprint
import random

FPS = 50


def draw_piece(display, color, x, y):
    pygame.draw.circle(display, 'white' if color == 'w' else 'black', [x, y], 20)
    pygame.draw.circle(display, 'black' if color == 'w' else 'white', [x, y], 20, 3)

def roll_dice():
    n1 = random.randint(1, 6)
    n2 = random.randint(1, 6)
    lst = []
    lst.append([n1, n2])
    if n1 == n2:
        lst.append([n1 for _ in range(4)])
    else:
        lst.append([n1, n2])
    return lst

def transform_dice(thing):
    n1, n2 = list(map(int, thing.split()))
    lst = []
    lst.append([n1, n2])
    if n1 == n2:
        lst.append([n1 for _ in range(4)])
    else:
        lst.append([n1, n2])
    return lst

def dropshadow(screen, text, size, x, y, colour=(0,0,0), drop_colour=(128,128,128), font='Helvetica'):
    dropshadow_offset = 1 + (size // 15)
    text_font = pygame.font.SysFont(font, size)
    text_bitmap = text_font.render(text, True, drop_colour)
    screen.blit(text_bitmap, text_bitmap.get_rect(center=(x+dropshadow_offset, y+dropshadow_offset)))
    text_bitmap = text_font.render(text, True, colour)
    
    screen.blit(text_bitmap, text_bitmap.get_rect(center=(x, y)))

class Board():
    def __init__(self, display, orientation):
        self.orientation = orientation
        self.board = []
        if self.orientation == 'b':
            self.board = [['bbbbbbbbbbbbbbb', '', '', '', '', '', '', '', '', '', '', ''], ['wwwwwwwwwwwwwww', '', '', '', '', '', '', '', '', '', '', '']]
        elif self.orientation == 'w':
            self.board = [['wwwwwwwwwwwwwww', '', '', '', '', '', '', '', '', '', '', ''], ['bbbbbbbbbbbbbbb', '', '', '', '', '', '', '', '', '', '', '']]
        self.enddeck = ['', '']
        self.display = display
        self.movenumber = 1
        self.movesfromhead = 0

    def returnrevor(self, orien):
        if orien == 'w':
            return 'b'
        else:
            return 'w'

    def convertfen(self, pos):
        if self.orientation == 'w':
            if isinstance(pos, list):
                temp = ['e' if x=='' else x for x in pos[0] + pos[1]]
                return ' '.join(temp)

            elif isinstance(pos, str):
                temp = ['' if x=='e' else x for x in pos.split(' ')]
                return [temp[:12], temp[12:]]
        else:
            if isinstance(pos, list):
                temp = ['e' if x=='' else x for x in pos[1] + pos[0]]
                return ' '.join(temp)

            elif isinstance(pos, str):
                temp = ['' if x=='e' else x for x in pos.split(' ')]
                return [temp[12:], temp[:12]]


    def printboard(self):
        pp = pprint.PrettyPrinter()
        pp.pprint(self.board)
    def draw_pieces(self):
        #first_half
        for i in range(12):
            if self.board[0][i] == '':
                pass
            else:
                for j in range(len(self.board[0][i])):
                    if i < 6:
                        draw_piece(self.display, self.board[0][i][j], 70+94*i, 800-50-j*30)
                    else:
                        draw_piece(self.display, self.board[0][i][j], 95+94*i, 800-50-j*30)
        for i in range(12):
            if self.board[1][i] == '':
                pass
            else:
                for j in range(len(self.board[1][i])):
                    if i < 6:
                        draw_piece(self.display, self.board[1][i][j], 1200-70-94*i, 50+j*30)
                    else:
                        draw_piece(self.display, self.board[1][i][j], 1200-95-94*i, 50+j*30)
        for j in range(len(self.enddeck[0])):
            draw_piece(self.display, self.enddeck[0][0], 70, 800-50-j*30)
        for j in range(len(self.enddeck[1])):
            draw_piece(self.display, self.enddeck[1][0], 1200-70, 50+j*30)
    def move_piece(self, row1, place1, row2, place2, dice):
        try:
            if row1 == 2: row1 == 0
            if row2 == 2: row2 == 0
            if (self.movenumber % 2 == 1 and self.orientation == 'w') or (self.movenumber % 2 == 0 and self.orientation == 'b'):
                if self.board[row1][place1] != '':
                    piece1 = self.board[row1][place1][-1]
                    if ((piece1 == 'w' and self.movenumber % 2 == 1) or (piece1 == 'b' and self.movenumber % 2 == 0)) and [row1, place1] != [row2, place2]:
                        
                        piece1 = self.board[row1][place1][-1]
                        self.board[row1][place1] = self.board[row1][place1][:-1]
                        self.board[row2][place2] += piece1

                        if row1 == row2 and place2 - place1 in dice:
                            dice.remove(place2-place1)
                        elif row1 == 0 and row2 == 1 and self.movenumber % 2 == 1-int(self.orientation == 'b'):
                            if place2+12-place1 in dice:
                                dice.remove(place2+12-place1)
                        elif row1 == 1 and row2 == 0 and self.movenumber % 2 == 0+int(self.orientation == 'b'):
                            if place2+12-place1 in dice:
                                dice.remove(place2+12-place1)

                        
                        elif row1 == 1 and row2 == 0 and self.movenumber % 2 == 1-int(self.orientation == 'b'):
                            
                            if 12-place1 in dice:
                                dice.remove(12-place1)
                                piece2 = self.board[row2][place2][-1]
                                self.board[row2][place2] = self.board[row2][place2][:-1]
                                self.enddeck[0] += piece2
                            elif 12-place1 < max(dice):
                                dice.remove(max(dice))
                                piece2 = self.board[row2][place2][-1]
                                self.board[row2][place2] = self.board[row2][place2][:-1]
                                self.enddeck[0] += piece2
                        elif row1 == 0 and row2 == 1 and self.movenumber % 2 == 0+int(self.orientation == 'b'):
                            
                            if 12-place1 in dice:
                                dice.remove(12-place1)
                                piece2 = self.board[row2][place2][-1]
                                self.board[row2][place2] = self.board[row2][place2][:-1]
                                self.enddeck[1] += piece2
                            elif 12-place1 < max(dice):
                                dice.remove(max(dice))
                                piece2 = self.board[row2][place2][-1]
                                self.board[row2][place2] = self.board[row2][place2][:-1]
                                self.enddeck[0] += piece2
                        
                        if place1 == 0:
                            self.movesfromhead += 1
        except Exception as e:
            print(e)
                
            

    def check_move(self, row1, place1, row2, place2, fdice):
        try:
            
            if not (0 <= place2 <= 11 and 0 <= place2 <= 11):
                return False
            if row1 == 2: row1 == 0
            if row2 == 2: row2 == 0
            dice = fdice[1]
            validmove0 = False
            if self.board[row2][place2] == '':
                validmove0 = True
            if not validmove0:
                if self.board[row1][place1][-1] == self.board[row2][place2][-1]:
                    validmove0 = True

            validmove1 = True
            if place1 == 0:
                if (self.movenumber == 2 or self.movenumber == 1) and (len(list(set(fdice[0]))) == 1 and list(set(fdice[0]))[0] in [3, 4, 6]):
                    if self.movesfromhead >= 2:
                        validmove1 = False
                else:
                    if self.movesfromhead >= 1:
                        validmove1 = False
                
            if self.board[row1][place1] != '' and validmove0 and validmove1:
                piece1 = self.board[row1][place1][-1]
                if (((piece1 == 'w' and self.movenumber % 2 == 1) or (piece1 == 'b' and self.movenumber % 2 == 0)) and [row1, place1] != [row2, place2]):
                    if row1 == row2 and place2 - place1 in dice:
                        return True
                    elif row1 == 0 and row2 == 1 and self.movenumber % 2 == 1-int(self.orientation == 'b'):
                        if place2+12-place1 in dice:
                            return True
                    elif row1 == 1 and row2 == 0 and self.movenumber % 2 == 0+int(self.orientation == 'b'):
                        if place2+12-place1 in dice:
                            return True
                    
                    elif (row1 == 1 and row2 == 0 and self.movenumber % 2 == 1-int(self.orientation == 'b')) and (self.orientation not in ''.join(self.board[row2]) and self.orientation not in ''.join(self.board[row1][:6])):
                        if 12-place1 in dice:
                            return True
                        if 12-place1 < max(dice):
                            if self.orientation not in ''.join(self.board[row1][:(12-place1)]):
                                return True
                    elif (row1 == 0 and row2 == 1 and self.movenumber % 2 == 0+int(self.orientation == 'b')) and (self.returnrevor(self.orientation) not in ''.join(self.board[row2]) and self.returnrevor(self.orientation) not in ''.join(self.board[row1][:6])):
                        if 12-place1 in dice:
                            return True
                        if 12-place1 < max(dice):
                            if self.returnrevor(self.orientation) not in ''.join(self.board[row1][:(12-place1)]):
                                return True
            return False
        except Exception as e:
            return True


if __name__ == '__main__':
    exec(open("main.py").read()) 