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
        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 25, 350, (0, 0, 0)), Button("Scissors", 150, 350, (0, 0, 0)),
        Button("Paper", 275, 350, (0, 0, 0))]


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
