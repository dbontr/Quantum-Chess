import pygame as p
import ChessEngine

WIDTH = HEIGHT = 512
SQ_SIZE = HEIGHT // 8
MAX_FPS = 15
IMAGES = {}
COLOR1 = (235, 236, 208)
COLOR2 = (115, 149, 82)
COLOR3 = 'yellow'
COLOR4 = 'yellow'
COLOR5 = 'red'
ANIMATE = True

'''
Initialize a global dict of images
'''
def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR", "bp", "wR", "wN", "wB", "wQ", "wK", "wB", "wK", "wR", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("assets/pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        # can now load image by using IMAGES["wp"] for white pawn, etc.

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
    validMoves = gs.getValidMoves()
    moveMade = False # flag variable for when a move is made
    animate = False # flag variable for when to animate
    loadImages()
    running = True
    sqSelected = () # tuple of square selected coords
    playerClicks = [] # 2 tuples of clicks coords
    gameOver =  False

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver:
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
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            # key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo with 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r: # reset with 'r'
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False


        if moveMade:
            if ANIMATE and animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        drawGameState(screen, gs, validMoves, sqSelected)
        if gs.checkmate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins by checkmate')
            else:
                drawText(screen, 'White wins by checkmate')
        elif gs.stalemate:
            gameOver = True
            drawText(screen, 'Stalemate')
        clock.tick(MAX_FPS)
        p.display.flip()
'''
Highlight square selected and moves for piece selected
'''
def hightlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): # sqSelected is a piece that can be moved
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # transparent = 0, opaque = 255 
            s.fill(p.Color(COLOR3))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            s.fill(p.Color(COLOR4))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))

'''
Responsible for all graphics
'''
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    hightlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)


'''
Draws squares on board
'''
def drawBoard(screen): #top left square always light
    global colors
    colors = [p.Color(COLOR1), p.Color(COLOR2)]
    for r in range(8):
        for c in range(8):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
    

'''
Draws pieces using current gamestatex
'''
def drawPieces(screen, board):
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

'''
Animating a move
'''
def animateMove(move, screen, board, clock):
    global colors
    coords = [] # list of coords that animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 5
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount
        drawBoard(screen)
        drawPieces(screen, board)
        color =  colors[(move.endRow + move.endCol) % 2] # erases piece from ending square
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != '--': # draws captured piece onto rect
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE)) # draw moving piece
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject1 = font.render(text, 0, p.Color("White"))
    textLocation = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH/2 - textObject1.get_width()/2, HEIGHT/2 - textObject1.get_height()/2)
    textObject2 = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject2, textLocation.move(2, 2))
    screen.blit(textObject2, textLocation.move(-2, 2))
    screen.blit(textObject2, textLocation.move(2, -2))
    screen.blit(textObject2, textLocation.move(-2, -2))
    screen.blit(textObject1, textLocation)

if __name__ == "__main__":
    main()