from random import randint
from math import floor
import pygame

class Board():
    def __init__(self, height=10, width=10):
        self.height = height
        self.width = width
        self.board = self.create_board(height, width)

    def create_board(self, height, width):
        """Generate a NxN board for simulation"""
        board = []
        # Add columns
        for _ in range(height):
            board.append([])
            for _ in range(width):
                board[-1].append(None)
        return board
    
    def populate_board(self, weight=0.8):
        """Generate random positions for trees"""
        total_trees = floor((self.height * self.width) * weight)

        for _ in range(total_trees):
            added = False
            # Create a random index for the tree
            while added == False:
                spot = self.get_random_spot()
                if not self.board[spot['x']][spot['y']]:
                    self.board[spot['x']][spot['y']] = 1  # Tree
                    added = True

    def get_random_spot(self):
        """Pick a random index in a 2D NxN array"""
        return {'x': randint(0,self.height-1), 'y': randint(0,self.width-1)}

    def lightning(self, real_spot=None):
        """Simulate lightning"""
        spot = self.get_random_spot() if real_spot == None else real_spot
        cf = coin_flip(weight=0.5)

        if self.board[spot['x']][spot['y']] and cf:
            self.board[spot['x']][spot['y']] = 0
            for neighbor in filter_pixels(self.height, self.width, get_indices(kernel=(3,3), height_index=spot['x'], width_index=spot['y'])):
                if neighbor != spot:
                    self.lightning(neighbor)
    
    def grow(self):
        """Simulate growth after fire"""
        for x, col in enumerate(self.board):
            for y, tree in enumerate(col):
                # Bias towards growth
                if tree != 1 and coin_flip(weight=0.8):
                    self.board[x][y] = 1


    def pretty_print(self):
        """Print the board in a visually appealing manner"""
        for row in self.board:
            print(str(row).center(60))


pygame.init()
WHITE = (255,255,255)
GREEN = (0,255,0)
FIRE = (255,15,0)
BG = (0, 0, 0)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def draw_grid(positions):
    for position in positions:
        col, row, color =  position
        top_left = (col*TILE_SIZE, row*TILE_SIZE)
        pygame.draw.rect(screen, color, (*top_left, TILE_SIZE, TILE_SIZE))


    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, WHITE, (0, row*TILE_SIZE), (WIDTH, row*TILE_SIZE))
    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, WHITE, (col*TILE_SIZE, 0), (col*TILE_SIZE, HEIGHT))


def main():
    running = True

    board = Board(40, 40)
    board.populate_board()

    positions = set()
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            for col_index, col in enumerate(board.board):
                for row_index, value in enumerate(col):
                    col_index = col_index
                    row_index = row_index
                    color = BG
                    if value == 0:
                        color = FIRE
                    elif value == 1:
                        color = GREEN

                    position = (col_index, row_index, color)
                    print(position)
                    positions.add(position)
                    
            
        screen.fill(BG)
        # Grid lines on top of background
        draw_grid(positions)
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()



def get_indices(kernel: tuple[int], height_index: int, width_index: int) -> list[list[int]]:
    """Find all neighboring pixels within the kernel size"""
    box_blur_values = []
    # Define the starting point, the middle of the range
    starting_spot_height_middle = floor(kernel[0] / 2)
    starting_spot_width_middle = floor(kernel[1] / 2)

    for height in range (kernel[0]):
        for width in range(kernel[1]):
            box_blur_values.append({'x': height_index-(starting_spot_height_middle-height), 'y': width_index-(starting_spot_width_middle-width)})
    return box_blur_values

def filter_pixels(height, width, box_blur_values: list[list[int]]) -> list[list[int]]:
   """Filter out indexes not in image, Grab pixels from image"""
   filtered_values = list(filter(lambda pixel: (pixel["x"] < height) and (pixel["y"] < width) and (pixel['x'] >= 0) and (pixel['y'] >= 0), box_blur_values))
   return filtered_values

# class Tree():
#     def __init__(self):
#         pass

def coin_flip(weight=0.5) -> bool:
    """Simulate a coin flip for probability of power law"""
    number = randint(1,100)
    return True if number >= floor(100*weight) else False

# game_board = Board()
# game_board.populate_board()
# game_board.pretty_print()
# print("Fires")
# game_board.lightning()
# game_board.pretty_print()
# game_board.grow()
# print("Regrowth")
# game_board.pretty_print()

# while True:
#     game_board.pretty_print()
#     print("Fires")
#     game_board.lightning()
#     game_board.pretty_print()
#     game_board.grow()
#     print("Regrowth")



# def create_board(height=100, width=100) -> list[list[int]]:
#     """Generate a nxn board upon which I'll create the simulated forest"""
#     board = []
#     # Add columns
#     for _ in range(height):
#         board.append([])
#         for _ in range(width):
#             board[-1].append(None)
#     return board

# board = create_board()


# def populate_board(height: int, width: int, weight: float, board=create_board()) -> list[list]:
#     """Generate random positions for trees"""
#     total_trees = (((height + width) / 2) * weight)

#     for _ in range(total_trees):
#         added = False
#         # Create a random index for the tree
#         while added == False:
#             height_index = randint(height)
#             width_index = randint(width)
#             if board[height_index][width_index]:
#                 board[height_index][width_index] = 1  # Tree
    
#     return board

# board = populate_board(board)

