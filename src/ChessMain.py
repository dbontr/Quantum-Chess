import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
COLOR1 = "white"
COLOR2 = "gray"

'''
Initialize a global dict of images
'''
def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bp", "wR", "wN", "wB", "wQ", "wK", "wB", "wK", "wR", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("assets/pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        # Can now load image by using IMAGES["wp"] for white pawn, etc.

'''
The main driver for code
'''

def main():
    p.display.set_caption("Quantum Chess")
    p.display.set_icon(p.image.load("assets/icon.png"))
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages()

    running = True
    sqSelected = () # tuple of square selected coords
    playerClicks = [] # 2 tuples of clicks coords
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # return tuple of coords
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = ()
                    playerClicks = []

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

'''
Responsible for all graphics
'''
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

'''
draws squares on board
'''
def drawBoard(screen): #top left square always light
    colors = [p.Color(COLOR1), p.Color(COLOR2)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    

'''
draws pieces using current gamestatex
'''
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()