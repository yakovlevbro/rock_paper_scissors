import pygame
from network import Network

pygame.font.init()

width = 400
height = 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Клиент")


def redraw_window(win, game, p):
    win.fill((255, 255, 255))

    if not (game.connected()):
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Ожидаем игроков...", True, (0, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))

    pygame.display.update()


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
