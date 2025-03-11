import pygame
import sys

# Initialize pygame
pygame.init()

# Screen size and board settings
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 5  # Thickness of grid lines
BOARD_ROWS, BOARD_COLS = 3, 3  # 3x3 board size
SQUARE_SIZE = WIDTH // BOARD_COLS  # Size of each square

# Colors used in the game
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Initialize display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")
screen.fill(WHITE)

# Initialize game board with None (empty positions)
board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
current_player = "X"  # Player "X" starts first

# Function to draw the grid lines
def draw_grid():
    for row in range(1, BOARD_ROWS):
        pygame.draw.line(screen, BLACK, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
    for col in range(1, BOARD_COLS):
        pygame.draw.line(screen, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Function to draw "X" and "O" marks on the board
def draw_marks():
    font = pygame.font.Font(None, 100)  # Font size
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col]:
                text = font.render(board[row][col], True, RED)
                screen.blit(text, (col * SQUARE_SIZE + 30, row * SQUARE_SIZE + 20))

# Function to check if there is a winner
def check_winner():
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]
    
    # Check columns
    for col in range(BOARD_COLS):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None:
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    
    return None

# Function to get available empty cells on the board
def get_empty_cells():
    return [(r, c) for r in range(BOARD_ROWS) for c in range(BOARD_COLS) if board[r][c] is None]

# Function to reset the board for a new game
def reset_board():
    global board, current_player
    board = [[None] * BOARD_COLS for _ in range(BOARD_ROWS)]
    current_player = "X"

# Minimax algorithm to find the best move for AI
def minimax(is_maximizing):
    winner = check_winner()
    if winner == "X":
        return -1
    elif winner == "O":
        return 1
    elif not get_empty_cells():
        return 0  # Draw
    
    if is_maximizing:
        best_score = -float("inf")
        for row, col in get_empty_cells():
            board[row][col] = "O"
            score = minimax(False)
            board[row][col] = None
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for row, col in get_empty_cells():
            board[row][col] = "X"
            score = minimax(True)
            board[row][col] = None
            best_score = min(score, best_score)
        return best_score

# AI selects the best move
def agent_move():
    best_score = -float("inf")
    best_move = None
    for row, col in get_empty_cells():
        board[row][col] = "O"
        score = minimax(False)
        board[row][col] = None
        if score > best_score:
            best_score = score
            best_move = (row, col)
    
    if best_move:
        row, col = best_move
        board[row][col] = "O"

# Main game loop
def main():
    global current_player
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN and current_player == "X":
                x, y = event.pos
                row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
                if board[row][col] is None:
                    board[row][col] = "X"
                    winner = check_winner()
                    if winner:
                        print(f"Player {winner} wins!")
                        pygame.time.delay(2000)
                        reset_board()
                        continue
                    if not get_empty_cells():
                        print("It's a draw!")
                        pygame.time.delay(2000)
                        reset_board()
                        continue
                    current_player = "O"
                    pygame.time.delay(500)
                    agent_move()
                    winner = check_winner()
                    if winner:
                        print(f"Player {winner} wins!")
                        pygame.time.delay(2000)
                        reset_board()
                        continue
                    if not get_empty_cells():
                        print("It's a draw!")
                        pygame.time.delay(2000)
                        reset_board()
                        continue
                    current_player = "X"
        
        screen.fill(WHITE)
        draw_grid()
        draw_marks()
        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    main()
