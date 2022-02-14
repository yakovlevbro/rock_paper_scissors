import os

import pygame
from network import Network

pygame.font.init()

width = 400
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Клиент")

rock_image = pygame.image.load(
    os.path.join('images', 'rock.png')
)
paper_image = pygame.image.load(
    os.path.join('images', 'paper.png')
)
scissors_image = pygame.image.load(
    os.path.join('images', 'scissors.png')
)

rock = pygame.transform.scale(rock_image, (100, 100))
paper = pygame.transform.scale(paper_image, (100, 100))
scissors = pygame.transform.scale(scissors_image, (100, 100))


class Button:
    def __init__(self, text, x, y, color, image):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 100
        self.height = 100
        self.image = image

    def draw(self, win):
        win.blit(self.image, (self.x, self.y, self.width, self.height))

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
        move4 = game.get_player_move(3)
        move5 = game.get_player_move(4)
        if game.all_went():
            text1 = font.render(move1, True, (0, 0, 0))
            text2 = font.render(move2, True, (0, 0, 0))
            text3 = font.render(move3, True, (0, 0, 0))
            text4 = font.render(move4, True, (0, 0, 0))
            text5 = font.render(move5, True, (0, 0, 0))
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

            if game.p4_went and p == 3:
                text4 = font.render(move4, True, (0, 0, 0))
            elif game.p4_went:
                text4 = font.render("Выбрал", True, (0, 0, 0))
            else:
                text4 = font.render("Ждем...", True, (0, 0, 0))

            if game.p5_went and p == 4:
                text5 = font.render(move5, True, (0, 0, 0))
            elif game.p5_went:
                text5 = font.render("Выбрал", True, (0, 0, 0))
            else:
                text5 = font.render("Ждем...", True, (0, 0, 0))

        if p == 1:
            win.blit(text2, (170, 80))
            win.blit(text1, (100, 240))
            win.blit(text3, (240, 240))
            win.blit(text4, (100, 280))
            win.blit(text5, (240, 280))
        elif p == 2:
            win.blit(text3, (170, 80))
            win.blit(text1, (100, 240))
            win.blit(text2, (240, 240))
            win.blit(text4, (100, 280))
            win.blit(text5, (240, 280))
        elif p == 3:
            win.blit(text4, (170, 80))
            win.blit(text1, (100, 240))
            win.blit(text2, (240, 240))
            win.blit(text3, (100, 280))
            win.blit(text5, (240, 280))
        elif p == 4:
            win.blit(text5, (170, 80))
            win.blit(text1, (100, 240))
            win.blit(text2, (240, 240))
            win.blit(text3, (100, 280))
            win.blit(text4, (240, 280))
        else:
            win.blit(text1, (170, 80))
            win.blit(text2, (100, 240))
            win.blit(text3, (240, 240))
            win.blit(text4, (100, 280))
            win.blit(text5, (240, 280))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Камень", 25, 350, (0, 0, 0), rock), Button("Ножницы", 150, 350, (0, 0, 0), scissors),
        Button("Бумага", 275, 350, (0, 0, 0), paper)]


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

            font = pygame.font.SysFont("comicsans", 50)
            if game.winner() == -1:
                text = font.render("Ничья!", True, (0, 0, 0))
            elif player in game.winner():
                text = font.render("Вы победили!", True, (0, 0, 0))
            else:
                text = font.render("Вы проиграли...", True, (0, 0, 0))

            win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))

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
                                n.send(btn.text)
                        elif player == 1:
                            if not game.p2_went:
                                n.send(btn.text)
                        elif player == 2:
                            if not game.p3_went:
                                n.send(btn.text)
                        elif player == 3:
                            if not game.p4_went:
                                n.send(btn.text)
                        elif player == 4:
                            if not game.p5_went:
                                n.send(btn.text)

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
