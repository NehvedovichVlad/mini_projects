"""
Этот класс будет обрабатывать пользовательский ввод и отображать информацию о текущем состоянии игры.
"""
import pygame as p

from Chess.Chess import ChessEngine

WIDTH = HEIGHT = 512
DIMENSIONS = 8  # размер шахматной доски 8х8
SQ_SIZE = HEIGHT // DIMENSIONS  # размер квадрата
MAX_FPS = 15
IMAGES = {}

""" 
Загружаем наши картинки фигур. Загрузка будет происходить только один раз в Main
"""


def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


"""
Это основной драйвер для нашего кода и он будет обрабатывать ввод пользователя и обновлять графику 
"""


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()
    running = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
        DrawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()  # обновляет только часть дисплэя


''' Отвечает за всю графику в текущей игре. '''
def DrawGameState(screen, gs):
    drawBoard(screen)  # рисует карту
    drawPieces(screen, gs.board)  # рисует фигуры


def drawBoard(screen):
    colors = [p.Color("light gray"), p.Color("dark green")]
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

''' Верхний левый квадрат будет всегда белый. '''
def drawPieces(screen, board):
    for r in range(DIMENSIONS):
        for c in range(DIMENSIONS):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
