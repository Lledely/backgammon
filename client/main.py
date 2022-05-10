import pygame
import sys
import bghelper
import tkinter
import tkinter.simpledialog
import requests
roomid = -1
gamejoined = False

def menu():
    global roomid, gamejoined
    def joinmenu(oldw):
        global roomid, gamejoined
        roomid = tkinter.simpledialog.askinteger("Lobby id", "Enter lobby id:", parent=oldw)
        if roomid != -1 and roomid is not None:
            gamejoined = True
            oldw.destroy()
            game()
    def creategame(oldw):
        global roomid, gamejoined
        a = requests.get("https://lledely.pythonanywhere.com/start").json()
        roomid = int(a["id"])
        if roomid != -1 and roomid is not None:
            gamejoined = False
            
            oldw.destroy()
            game()


    w = tkinter.Tk()
    w.title('menu')
    w.geometry('200x200')
    w.resizable(0, 0)
    L1 = tkinter.Label(w, text='Backgammon Menu', font=('Helvetica', 20))
    L1.place(relx=0.5, rely=0.2, anchor=tkinter.CENTER)
    b1 = tkinter.Button(w, text="Create game", command=lambda: creategame(w))
    b2 = tkinter.Button(w, text="Join game", command=lambda: joinmenu(w))
    b1.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)
    b2.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
    w.mainloop()



def game():
    global roomid, gamejoined
    
    pygame.init()
    pygame.font.init()
    clock = pygame.time.Clock()
    w, h = 1200, 800
    display = pygame.display.set_mode((w, h))
    
    if gamejoined:
        temporientation = 'b'
    else:
        temporientation = 'w'
    board = bghelper.Board(display, temporientation)
    temppos1 = []
    temppos2 = []
    inf = requests.get(f"https://lledely.pythonanywhere.com/get/{roomid}").json()
    cdice = bghelper.transform_dice(inf["dice"])
    cnt = 0
    
    while True:
        
        boardimg = pygame.image.load('bg2.png').convert()
        display.blit(boardimg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                temppos1.append(0) if y > 400 else temppos1.append(1)
                if y > 400:
                    if x < 600:
                        temppos1.append((x-35)//94)
                    else:
                        temppos1.append((x-45)//94)
                else:
                    if x < 600:
                        temppos1.append(11 - (x-35)//94)
                    else:
                        temppos1.append(11 - (x-45)//94)


            elif event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                temppos2.append(0) if y > 400 else temppos2.append(1)
                if y > 400:
                    temppos2.append((x-45)//92)
                else:
                    temppos2.append(11 -(x-45)//92)
                if board.check_move(temppos1[0], temppos1[1], temppos2[0], temppos2[1], cdice):
                    board.move_piece(temppos1[0], temppos1[1], temppos2[0], temppos2[1], cdice[1])
                    
                    if len(cdice[1]) == 0:
                        board.movenumber += 1
                        board.movesfromhead = 0
                    requests.get(f"https://lledely.pythonanywhere.com/update/{roomid}", json={"state":board.convertfen(board.board), "moven":str(board.movenumber)})
                    if len(cdice[1]) == 0:
                        inf = requests.get(f"https://lledely.pythonanywhere.com/get/{roomid}").json()
                        cdice = bghelper.transform_dice(inf["dice"])
                        
                    

                    
                        
                temppos1 = []
                temppos2 = []
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    inf = requests.get(f"https://lledely.pythonanywhere.com/get/{roomid}").json()
                    board.movenumber += 1
                    board.movesfromhead = 0
                    requests.get(f"https://lledely.pythonanywhere.com/update/{roomid}", json={"state":board.convertfen(board.board), "moven":str(board.movenumber)})
                    cdice = bghelper.transform_dice(inf["dice"])
                    

                    
        
        #if cnt == 0:
        #    requests.get(f"https://lledely.pythonanywhere.com/update/{roomid}", json={"state":board.convertfen(board.board), "prev_move":'1'})    

        my_font = pygame.font.SysFont('Helvetica', 100)
        text_surface = my_font.render(f'{cdice[0][0]} {cdice[0][1]}', False, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(600, 400))
        display.blit(text_surface, text_rect)
        if board.movenumber % 2 == 1:
            bghelper.dropshadow(display, 'w', 50, 450, 410)
        else:
            bghelper.dropshadow(display, 'b', 50, 450, 410)


        my_font = pygame.font.SysFont('Helvetica', 20)
        text_surface = my_font.render(f'Move:', False, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(450, 370))
        display.blit(text_surface, text_rect)
        if board.movenumber < 3:
            text_surface = my_font.render(f'{str(roomid)}', False, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(70, 70))
            display.blit(text_surface, text_rect)
            text_surface = my_font.render(f'Room id:', False, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(70, 50))
            display.blit(text_surface, text_rect)
        
        board.enddeck[0] = board.orientation * (15-board.convertfen(board.board).count(board.orientation))
        board.enddeck[1] = board.returnrevor(board.orientation) * (15-board.convertfen(board.board).count(board.returnrevor(board.orientation)))



        if cnt % 500 == 0:
            print(board.movenumber)
            inf = requests.get(f"https://lledely.pythonanywhere.com/get/{roomid}").json()
            if board.orientation == 'w':
                board.movenumber = int(inf['moven'])
            else:
                board.movenumber = int(inf['moven']) + 1

            
            if cdice[0] != bghelper.transform_dice(inf["dice"])[0]:
                    cdice[0] = bghelper.transform_dice(inf["dice"])[0]
                
            if board.convertfen(inf["state"]) != board.board and not gamejoined:
                board.board = board.convertfen(inf["state"])
            if board.convertfen(inf["state"]) != board.board[::-1] and gamejoined:
                board.board = board.convertfen(inf["state"])

            if board.movenumber % 2 == 1:
                movec = 'w'
            else:
                movec = 'b'
            outcomes = []
            trueboard = board.board[0] + board.board[1]
            for i in range(len(trueboard)):
                if trueboard[i] != '':
                    if trueboard[i][-1] == movec:
                        for s in cdice[1]:
                            outcomes.append(board.check_move(i//12, i%12, (i+s)//12, (i+s)%12, cdice))
            if True not in outcomes:
                print('why')
                board.movenumber += 1
                board.movesfromhead = 0
                requests.get(f"https://lledely.pythonanywhere.com/update/{roomid}", json={"state":board.convertfen(board.board), "moven":str(board.movenumber)})
                cdice = bghelper.transform_dice(inf["dice"])
                        




        board.draw_pieces()
        pygame.display.update()
        cnt += 1
        clock.tick(bghelper.FPS)

if __name__ == '__main__':
    menu()
    pygame.quit()
    sys.exit()
