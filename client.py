import pygame
from network import Network
import pickle

pygame.font.init()

width = 900
height = 700

#rgb colors
background_color = (85,59,8)
system_messages_color = (233,229,205)
button_color = (117,66,14)

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)



win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Client")

class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 200
        self.height = 50

    def Draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), width=0, border_radius=10) # Rounded rect
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, WHITE)
        win.blit(text, (self.x+round(self.width/2)-round(text.get_width()/2), (self.y+round(self.height/2)-round(text.get_height()/2))))

    def Click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x+self.width and self.y <= y1 <= self.y+self.height:
            return True
        return False

def RedrawWindow(win, game, playerNum):
    win.fill(background_color)
    
    if not game.Connected():
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for player...", 1, system_messages_color)
        win.blit(text, (width/2-text.get_width()/2, height/2-text.get_height()/2))
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move:", 1, (0,255,255))
        win.blit(text, (50,200))

        text = font.render("Opponent Move:", 1, (0,255,255))
        win.blit(text, (400,200))

        move1 = game.GetPlayerMove(0)
        move2 = game.GetPlayerMove(1)
        if game.IsBothWent():
            text1 = font.render(move1, 1, BLACK)
            text2 = font.render(move2, 1, BLACK)
        else:
            if game.p1Went and playerNum == 0:
                text1 = font.render(move1, 1, system_messages_color)
            elif game.p1Went:
                text1 = font.render("Locked In", 1, system_messages_color)
            else:
                text1 = font.render("Waiting...", 1, system_messages_color)

            if game.p2Went and playerNum == 1:
                text2 = font.render(move2, 1, system_messages_color)
            elif game.p2Went:
                text2 = font.render("Locked In", 1, system_messages_color)
            else:
                text2 = font.render("Waiting...", 1, system_messages_color)

        if playerNum == 1:
            win.blit(text2, (100,350))
            win.blit(text1, (450,350))
        else:
            win.blit(text1, (100,350))
            win.blit(text2, (450,350))
        


        for btn in buttons:
            btn.Draw(win)
    
    pygame.display.update()


buttons = [Button("Rock", 80, 500, button_color), Button("Paper", 310, 500, button_color), Button("Scissors", 540, 500, button_color)]
def Main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    playerNum = int(n.GetP())
    print("You are player: ", playerNum)

    while run:
        clock.tick(60)
        try:
            game = n.Send("get")
        except:
            run = False
            print("Couldnwt get game")
            break

        if game.IsBothWent():
            RedrawWindow(win, game, playerNum)
            pygame.time.delay(2000)
            try:
                game = n.Send("reset")
            except:
                run = False
                print("Couldnwt get game")
                break
        
            font = pygame.font.SysFont("comicsans", 90)
            if game.Winner() == 1 and playerNum == 1 or game.Winner() == 0 and playerNum == 0:
                text = font.render("You Won!", 1, GREEN)
            elif game.Winner() == -1:
                text = font.render("Tie Game!", 1, WHITE)
            else:
                text = font.render("You Lost:(", 1, RED)
            
            win.fill(background_color)
            win.blit(text, (width/2-text.get_width()/2, height/2-text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn.Click(pos) and game.Connected():
                        if playerNum == 0:
                            if not game.p1Went:
                                n.Send(btn.text)
                        else:
                            if not game.p2Went:
                                n.Send(btn.text)

        RedrawWindow(win, game, playerNum)

def Menu():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill(background_color)

        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!", 1, system_messages_color)
        win.blit(text, (width/3,height/3+40))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False
    Main()

while True:
    Menu()