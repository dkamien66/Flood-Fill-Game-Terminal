# For 2D array help: https://stackoverflow.com/questions/6667201/how-to-define-a-two-dimensional-array
import random
import numpy as np
import re

class Grid:
    def __init__(self, n):
        # Creates the 2D array for the game
        self.grid = np.array([[random.randint(1, 5) for _ in range(n)] for _ in range(n)])
        # Create a variable to save the total number of elements in this matrix
        self.total_elements = n*n
        # This list contains all of the tiles already filled by the user
        self.filled = []
        # For each iteration the matrix is recursively searched through, this list will reset and modified to to show which ones have been visited in that iteration
        self.visited = []

    def __str__(self):
        return f"{self.grid}"
    
    # This method is called either at the START. It recursively looks for vertically or horizontally adjacent tiles of the same number to be added to the filled list.
    # or
    # This method is called after the select_tile method and recursively looks for vertically or horizontally adjacent tiles of the same number to be added to the filled list.
    def check_fill(self, row, col):
        self.visited.append((row, col))
        if (row, col) not in self.filled:
            self.filled.append((row, col))

        if row > 0:
            if self.grid[row-1][col] == self.grid[row][col] and (row-1, col) not in self.visited:
                self.check_fill(row-1, col)
        if col + 1 < self.grid.shape[1]:
            if self.grid[row][col+1] == self.grid[row][col] and (row, col+1) not in self.visited:
                self.check_fill(row, col+1)
        if row + 1 < self.grid.shape[0]:
            if self.grid[row+1][col] == self.grid[row][col] and (row+1, col) not in self.visited:
                self.check_fill(row+1, col)
        if col > 0:
            if self.grid[row][col-1] == self.grid[row][col] and (row, col-1) not in self.visited:
                self.check_fill(row, col-1)

    # This method changes all currently filled tiles to the selected tile's number.
    # Returns the row and column index of the selected tile.
    def flood_fill(self, row, col):
        for filled_row, filled_col in self.filled:
            self.grid[filled_row][filled_col] = self.grid[row][col]
        return row, col
    
    # This method checks that the user's selected tile is valid to choose from.
    # Returns the row and column index of the selected tile.
    def select_tile(self, row, col):
        # Check the tile is within the range of the grid
        if 0 <= row < self.grid.shape[0] and 0 <= col < self.grid.shape[1]:
            # Check the tile has not already been filled
            if (row, col) not in self.filled:
                # Check the tile is vertically or horizontally adjacent to a filled tile
                    # 1. Same row but different column
                    # OR
                    # 2. Same column but different row
                for filled_row, filled_col in self.filled:
                    if (row == filled_row and abs(col-filled_col) == 1) or (col == filled_col and abs(row-filled_row) == 1):
                        return self.flood_fill(row, col)
                # After checking ALL filled tiles are not adjacent to the selected tile, then let user know error
                raise ValueError("Selected tile is not vertically or horizontally adjacent to a filled tile!")
            else:
                raise ValueError("Selected tile has already been filled!")
        else:
            raise ValueError("Selected tile is not in grid range!")
            

def main():
    while True:
        grid_length = int(input("WELCOME TO FLOOD FILL! How long would you like the grid to be? "))
        if grid_length > 0:
            break
    
    grid = Grid(grid_length)
    print(grid)

    while True:
        try:
            start_tile = input("Type in a starting point: ")
            if match := re.search(r"^\((\d+), (\d+)\)$", start_tile.strip()):
                grid.check_fill(int(match.group(1)), int(match.group(2)))
                grid.visited = []
            else:
                raise ValueError("Type tile location as (x, y)!")
        except ValueError as e:
            print(e, "\n")
            pass
        else:
            break

    while True:
        print(grid, "\n")
        if len(grid.filled) == grid.total_elements:
            print("END. GOODBYE.")
            break
        try:
            print(grid.filled)
            user_tile = input("What tile would you like to fill? ")
            if matches := re.search(r"^\((\d+), (\d+)\)$", user_tile.strip()):
                selected_row, selected_col = grid.select_tile(int(matches.group(1)), int(matches.group(2)))
            else:
                raise ValueError("Type tile location as (x, y)!")
        except ValueError as e:
            print(e, "\n")
            pass
        else:
            grid.check_fill(selected_row, selected_col)
            grid.visited = []


main()