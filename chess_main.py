"""
This is the main driver file. It is responsible for handling user input and displaying current GameState object
"""
import pygame as p
import chess_engine

p.init()
WIDTH = HEIGHT = 512  # 400 is another option
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}

'''
Initialize a global dictionary of images. This will be called exactly once in the main! It is its own method (not in the main)
so we are flexible
'''


def loadImages():
    pieces = ["wP", "wR", "wN", "wB", "wK",
              "wQ", "bP", "bR", "bN", "bB", "bK", "bQ"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load(
            "pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))  # load pictures into IMAGES dictionary
    # pygame.image.load() function returns us a Surface with the ball data
    # Note: we can access an image by saying 'IMAGES['wp']'
    # we also scale the images so it fits the square nicely


'''
The main driver for the code. It handles user inpute and updates the graphics.
'''


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    # creates a new Surface object that represents the actual displayed graphics. Any drawing you do to this Surface will become visible on the monitor.
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chess_engine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable for when a move is made, in order to change validMoves
    # print(gs.board)
    loadImages()  # only do this once, before the while loop

    # starting here, program is inizalized and ready to run
    # inside an infinite loop we check if a QUIT event has happened. If so, we exit the programm
    running = True
    # no square is selected initially, keeps track of LAST click of user (row, col)
    sqSelected = ()
    # keeeps track of player clicks (two tuples: [(6,4), (4,4)]), for example
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # MOUSE HANDLERS
            elif e.type == p.MOUSEBUTTONDOWN:  # this does not include "dragging" pieces!!
                location = p.mouse.get_pos()  # (x, y) location of mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if sqSelected == (row, col):  # the user clicked the same square twice!
                    sqSelected = ()  # de-select
                    playerClicks = []  # clear player clicks
                else:
                    sqSelected = (row, col)
                    # append for 1st and 2nd clicks
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:  # after 2 different clicks
                    move = chess_engine.Move(
                        playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    # makeMove is a method within the GameState class, that's why we must use gs.makeMove
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True

                    sqSelected = ()  # reset user clicks
                    playerClicks = []
            # KEY HANDLERS
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo move when 'z' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()
    # This makes everything we have drawn on the screen Surface become visible
    # This buffering makes sure we only see completely drawn frames on the screen.
    # Without it, the user would see the half completed parts of the screen as they are being created.


'''
Responsible for all the graphics within a current game state.
'''


def drawGameState(screen, gs):
    # order in which we call is important! First draw the board, then the pieces!!
    drawBoard(screen)  # draw squares on the board
    # add in piece highlighting for move suggestions (later)
    drawPieces(screen, gs.board)  # draw pieces on top of those squares


'''
Draw the squares on the board. The top left square is always light (no matter the perspective)
'''


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            # sum of tuple of coordinates of white squares are always even! (0,0), (0,2), (1,1),...
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(
                c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
Draw the pieces on the board using the urrent GameState.board
'''


def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":  # not empty square
                screen.blit(IMAGES[piece], p.Rect(
                    c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()
