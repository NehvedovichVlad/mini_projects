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
        clock.tick(MAX_FPS)
        p.display.flip() # обновляет только часть дисплэя

if __name__ == "__main__":
    main()