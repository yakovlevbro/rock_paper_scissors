import pygame
from network import Network

pygame.font.init()

width = 400
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Клиент")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 100
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 20)
        text = font.render(self.text, True, (255, 255, 255))
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


def redraw_window(win, game, p):
    win.fill((255, 255, 255))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Ожидаем игроков...", True, (0, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        font = pygame.font.SysFont("comicsans", 20)
        text = font.render("Твой ход", True, (0, 0, 0))
        win.blit(text, (150, 40))

        text = font.render("Оппоненты", True, (0, 0, 0))
        win.blit(text, (140, 200))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        move3 = game.get_player_move(2)
        if game.all_went():
            text1 = font.render(move1, True, (0, 0, 0))
            text2 = font.render(move2, True, (0, 0, 0))
            text3 = font.render(move3, True, (0, 0, 0))
        else:
            if game.p1_went and p == 0:
                text1 = font.render(move1, True, (0, 0, 0))
            elif game.p1_went:
                text1 = font.render("Выбрал", True, (0, 0, 0))
            else:
                text1 = font.render("Ждем...", True, (0, 0, 0))

            if game.p2_went and p == 1:
                text2 = font.render(move2, True, (0, 0, 0))
            elif game.p2_went:
                text2 = font.render("Выбрал", True, (0, 0, 0))
            else:
                text2 = font.render("Ждем...", True, (0, 0, 0))

            if game.p3_went and p == 2:
                text3 = font.render(move3, True, (0, 0, 0))
            elif game.p3_went:
                text3 = font.render("Выбрал", True, (0, 0, 0))
            else:
                text3 = font.render("Ждем...", True, (0, 0, 0))

        if p == 1:
            win.blit(text2, (170, 80))
            win.blit(text1, (100, 240))
            win.blit(text3, (240, 240))
        elif p == 2:
            win.blit(text3, (170, 80))
            win.blit(text2, (100, 240))
            win.blit(text1, (240, 240))
        else:
            win.blit(text1, (170, 80))
            win.blit(text2, (100, 240))
            win.blit(text3, (240, 240))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Камень", 25, 350, (0, 0, 0)), Button("Ножницы", 150, 350, (0, 0, 0)),
        Button("Бумага", 275, 350, (0, 0, 0))]


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.get_p())
    print("Игрок №", player)

    while run:
        clock.tick(60)

        try:
            game = n.send("get")
        except:
            run = False
            print("Не удалось получить игру")
            break

        if game.all_went():
            redraw_window(win, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("reset")
            except:
                run = False
                print("Не удалось получить игру")
                break

            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.p1_went:
                                print(btn.text)
                        elif player == 1:
                            if not game.p2_went:
                                print(btn.text)
                        elif player == 2:
                            if not game.p3_went:
                                print(btn.text)

        redraw_window(win, game, player)


def menu_screen():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((255, 255, 255))
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Нажмите для начала", True, (0, 0, 0))
        win.blit(text, (50, 200))
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
