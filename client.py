import pygame
from network import Network
pygame.font.init()

width = 470
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

class Button:
    def __init__(self, id, text, x, y):
        self.id = id
        self.text = text
        self.x = x
        self.y = y
        self.color = (255,255,255)
        self.width = 150
        self.height = 150

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("arial", 80)
        text = font.render(self.text, 1, (0,0,0))
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))
        pygame.draw.lines(win, (0,0,0), True, [(self.x, self.y), (self.x + self.width, self.y), (self.x + self.width, self.y+self.height), (self.x, self.y+self.height)])

    def click(self, pos):
        x1, y1 = pos[0], pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False

def redrawWindow(win, game, btns, player, reset_counter):
    win.fill((128,128,128))

    if not(game.connected()):
        font = pygame.font.SysFont("arial", 40)
        text = font.render("Waiting for Player...", 1, (255,0,0))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
    else:
        draw_info(win, game, player)
        for btn in btns:
            if str(btn.id) in game.moves[0]:
                btn.text = 'X'
            if str(btn.id) in game.moves[1]:
                btn.text = 'O'
            btn.draw(win)

        if reset_counter >= 0:
            winner = game.won_player
            if winner in [0,1,30]:
                font = pygame.font.SysFont("arial", 30)
                if (winner == 1 and player == 1) or (winner == 0 and player == 0):
                    text = font.render("You Won!", 1, (0,255,0))
                    color = (0,255,0)
                elif (winner == 1 and player == 0) or (winner == 0 and player == 1):
                    text = font.render("You Lost...", 1, (255, 0, 0))  
                    color = (255,0,0)
                elif winner == 30:
                    text = font.render("Tie!", 1, (0,0,255))
                    color = (128,128,0)
                win.blit(text, (width/2 - text.get_width()/2, 90 + text.get_height()/2)) 

                if color:
                    for btn in btns:
                        if btn.id in game.won_pattern:
                            btn.color = color
                        btn.draw(win)

            font = pygame.font.SysFont("arial", 50)
            text = font.render(f"Next game in {reset_counter}", 1, (0,0,255))
            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
            if reset_counter in [0,1,2]:
                pygame.time.delay(1000)
        else:
            font = pygame.font.SysFont("arial", 30)
            player_turn = "Your Turn" if (not game.p1_moved and player == 0) or (not game.p2_moved and player == 1) else "Opponent's Turn"
            text = font.render(player_turn, 1, (0, 255, 255))
            win.blit(text, (width/2 - text.get_width()/2, 90 + text.get_height()/2))
    pygame.display.update()

def draw_info(win, game, player):
    font = pygame.font.SysFont("arial", 30)
    
    text = font.render("Score", 1, (0, 255, 255))
    win.blit(text, (width/2 - text.get_width()/2,  10))

    font = pygame.font.SysFont("arial", 25)

    _text = "You 'x'" if player == 0 else "You 'o'"
    text = font.render(_text, 1, (0, 255, 255))
    win.blit(text, (width/4 - text.get_width()/2, 50))

    _text = "'x' Opponent" if player == 1 else "'o' Opponent"
    text = font.render(_text, 1, (0, 255, 255))
    win.blit(text, (width*3/4 - text.get_width()/2, 50))

    text = font.render(f"{game.wins[player]} - {game.wins[1 if player == 0 else 0]}", 1, (0, 255, 255))
    win.blit(text, (width/2 - text.get_width()/2,  50))

def get_buttons():
    buttons = [Button(0, "", 10, 150), Button(1, "", 160, 150), Button(2, "", 310, 150),
        Button(3, "", 10, 290), Button(4, "", 160, 290), Button(5, "", 310, 290),
        Button(6, "", 10, 440), Button(7, "", 160, 440), Button(8, "", 310, 440)]
    return buttons

def main():
    run = True
    reset_counter = -1
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.get_player())
    pygame.display.set_caption(f"Client {player}")
    btns = get_buttons()

    while run:
        clock.tick(60)

        try:
            game = n.send("update")
        except:
            run = False
            print("Send 'update' failed")
            break

        if game.check_winner() in [0, 1, 30]:
            if reset_counter >= 0:
                if reset_counter == 0:
                    try:
                        game = n.send("reset")
                    except:
                        run = False
                        print("Send 'reset' failed")
                        break
                reset_counter -= 1
            else:
                reset_counter = 4
        else:
            if not game.game_started:
                reset_counter = -1 #fix one client stucks at 'Next game in 0'
                btns = get_buttons()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for btn in btns:
                        if btn.click(pos) and game.connected():
                            if btn.text == '':
                                if player == 0:
                                    if not game.p1_moved:
                                        n.send(str(btn.id))
                                else:
                                    if not game.p2_moved:
                                        n.send(str(btn.id))


        redrawWindow(win, game, btns, player, reset_counter)

def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("arial", 40)
        text = font.render("Click to start!", 1, (0,0,255))
        win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()

while True:
    menu_screen()