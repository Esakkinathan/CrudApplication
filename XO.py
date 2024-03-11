import pygame
import sys

# Initialize pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 300, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up font
font = pygame.font.SysFont(None, 50)

# Set up board
board = [[' ' for _ in range(3)] for _ in range(3)]

# Function to draw the board
def draw_board():
    screen.fill(WHITE)
    pygame.draw.line(screen, BLACK, (100, 0), (100, 300), 5)
    pygame.draw.line(screen, BLACK, (200, 0), (200, 300), 5)
    pygame.draw.line(screen, BLACK, (0, 100), (300, 100), 5)
    pygame.draw.line(screen, BLACK, (0, 200), (300, 200), 5)

# Function to draw X or O
def draw_xo(row, col, player):
    if player == 'X':
        text = font.render('X', True, BLACK)
    else:
        text = font.render('O', True, BLACK)
    text_rect = text.get_rect(center=(col*100 + 50, row*100 + 50))
    screen.blit(text, text_rect)

# Function to check for a win
def check_win(player):
    # Check rows and columns
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True
    return False

# Main game loop
current_player = 'X'
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            row = y // 100
            col = x // 100
            if board[row][col] == ' ':
                board[row][col] = current_player
                if check_win(current_player):
                    draw_board()
                    draw_xo(row, col, current_player)
                    pygame.display.update()
                    print(f"Player {current_player} wins!")
                    running = False
                elif all(' ' not in row for row in board):
                    draw_board()
                    pygame.display.update()
                    print("It's a tie!")
                    running = False
                else:
                    draw_xo(row, col, current_player)
                    current_player = 'O' if current_player == 'X' else 'X'

    draw_board()
    for row in range(3):
        for col in range(3):
            if board[row][col] != ' ':
                draw_xo(row, col, board[row][col])
    
    pygame.display.update()

pygame.quit()
