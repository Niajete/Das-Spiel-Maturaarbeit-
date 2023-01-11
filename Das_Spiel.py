import pygame, sys
import numpy as np
from Konstant import *
import Class
pygame.init()


def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font(None, size)

display = pygame.display.set_mode((WIDTH, HEIGHT))

menu_state = "main"

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        action = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action


#Button

onePlayer_img = pygame.image.load("onePlayer.png").convert_alpha()
twoPlayer_img = pygame.image.load("twoPlayer.png").convert_alpha()

onePlayer_button = Button(100, 300, onePlayer_img, 0.3)
twoPlayer_button = Button(350, 300, twoPlayer_img, 0.3)

Einfach_img = pygame.image.load("Einfach.png").convert_alpha()
Schwierig_img = pygame.image.load("Schwierig.png").convert_alpha()
        
Einfach_button = Button(100, 300, Einfach_img, 1)
Schwierig_button = Button(350, 300, Schwierig_img, 1)

class twoPlayer():

        #twoPlayer
    def twoPlayer():
        pygame.display.set_caption("2 Player")
    
        game = Class.Game()
        board = game.board


        #Mainloop
        while True:
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        twoPlayer.twoPlayer()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        main_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos #Von Pixel zu Rows und Cols
                    row = pos[1] // SQSIZE
                    col = pos[0] // SQSIZE

                    if board.empty_sqr(row, col) and game.running:
                        game.make_move(row, col)

                    if game.isover():
                        game.running = False



            pygame.display.update()


class onePlayer:

        #onePlayer
    def onePlayer():
        display.fill("white")
        pygame.display.set_caption("1 Player")
        
        onePlayer_Text = get_font(45).render("Einfach oder schwer?", True, "black")
        onePlayer_Rect = onePlayer_Text.get_rect(center=(300, 30))
        display.blit(onePlayer_Text, onePlayer_Rect)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        main_menu()

            if Einfach_button.draw(display):
                Zwischenschritt2()
            
            if Schwierig_button.draw(display):
                Zwischenschritt3()

            pygame.display.update()

       #Einfach
    def einfach():
        pygame.display.set_caption("Einfach")
        
        game = Class.Game()
        board = game.board
        ai = Class.AI()

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        onePlayer.einfach()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        main_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos #Von Pixel zu Rows und Cols
                    row = pos[1] // SQSIZE
                    col = pos[0] // SQSIZE

                    if board.empty_sqr(row, col) and game.running:
                        game.make_move(row, col)

                    if game.isover():
                        game.running = False

            if game.gamemode == 'ai' and game.player == ai.player and game.running:
                pygame.display.update()

                row, col = ai.eval(board)
                game.make_move(row, col)  



            pygame.display.update()

        #Schwierig
    def Schwierig():
        pygame.display.set_caption("Schwierig")

        game = Class.Game()
        board = game.board
        Minimax = Class.Minimax()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        onePlayer.Schwierig()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        main_menu()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos #Von Pixel zu Rows und Cols
                    row = pos[1] // SQSIZE
                    col = pos[0] // SQSIZE

                    if board.empty_sqr(row, col) and game.running:
                        game.make_move(row, col)

                    if game.isover():
                        game.running = False

            if game.gamemode == 'ai' and game.player == Minimax.player and game.running:
                pygame.display.update()

                row, col = Minimax.eval(board)
                game.make_move(row, col)

                if game.isover():
                    game.running = False


            pygame.display.update()


def Zwischenschritt():
    display.fill(Menu_Color)
    pygame.display.set_caption("Drücke S um fortzufahren")
        
    Zwischenschritt_Text = get_font(45).render("Drücke S um fortzufahren", True, "white")
    Zwischenschritt_Rect = Zwischenschritt_Text.get_rect(center=(300, 300))
    display.blit(Zwischenschritt_Text, Zwischenschritt_Rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    onePlayer.onePlayer()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    main_menu()


        pygame.display.update()

def Zwischenschritt2():
    display.fill(Menu_Color)
    pygame.display.set_caption("Drücke S um fortzufahren")
        
    Zwischenschritt_Text = get_font(45).render("Drücke S um fortzufahren", True, "white")
    Zwischenschritt_Rect = Zwischenschritt_Text.get_rect(center=(300, 300))
    display.blit(Zwischenschritt_Text, Zwischenschritt_Rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    onePlayer.einfach()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    main_menu()


        pygame.display.update()

def Zwischenschritt3():
    display.fill(Menu_Color)
    pygame.display.set_caption("Drücke S um fortzufahren")
        
    Zwischenschritt_Text = get_font(45).render("Drücke S um fortzufahren", True, "white")
    Zwischenschritt_Rect = Zwischenschritt_Text.get_rect(center=(300, 300))
    display.blit(Zwischenschritt_Text, Zwischenschritt_Rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    onePlayer.Schwierig()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    main_menu()


        pygame.display.update()

#Menu
def main_menu():
    pygame.display.set_caption("Menu")
    menu_state = "main"

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if menu_state == "main":
            display.fill(Menu_Color)
            pygame.display.set_caption("Menu")
            Menu_Text = get_font(100).render("Tic Tac Toe", True, "White")
            Menu_Rect = Menu_Text.get_rect(center=(300, 50))
            display.blit(Menu_Text, Menu_Rect)

            if onePlayer_button.draw(display):
                menu_state = "options"

            if twoPlayer_button.draw(display):
                twoPlayer.twoPlayer()

        if menu_state == "options":
            Zwischenschritt()

        pygame.display.update()

#Main loop
open = True
while open:
    display.fill(Menu_Color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           sys.exit()

    if menu_state == "main":
        pygame.display.set_caption("Menu")
        Menu_Text = get_font(100).render("Tic Tac Toe", True, "White")
        Menu_Rect = Menu_Text.get_rect(center=(300, 50))
        display.blit(Menu_Text, Menu_Rect)

        if onePlayer_button.draw(display):
            menu_state = "options"

        if twoPlayer_button.draw(display):
            twoPlayer.twoPlayer()

    if menu_state == "options":
        Zwischenschritt()




    pygame.display.update()





