"""
conway.py 
A simple Python/matplotlib implementation of Conway's Game of Life.
"""

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

ON = 255
OFF = 0
vals = [ON, OFF]

def randomGrid(N):
    """returns a grid of NxN random values"""
    return np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N, N)

def createGrid(N, filename):
    grid = np.zeros((N,N))
    file = open(filename, 'r')
    lines = file.readlines()
    for i, line in enumerate(lines):
        if i > 1:
            coords = line.split(' ')
            x = int(coords[0])
            y = int(coords[1])
            if x >= N or y >= N:
                continue
            grid[x][y] = ON
    return grid

def addGlider(i, j, grid):
    """adds a glider with top left cell at (i, j)"""
    glider = np.array([[0,    0, 255], 
                       [255,  0, 255], 
                       [0,  255, 255]])
    grid[i:i+3, j:j+3] = glider

def update(frameNum, img, grid, N, ax):
    # copy grid since we require 8 neighbors for calculation
    # and we go line by line 
    newGrid = grid.copy()
    #Implement the rules of Conway's Game of Life
    for i in range(N):
        for j in range(N):
 
            # compute 8-neighbor sum
            # using toroidal boundary conditions - x and y wrap around
            # so that the simulaton takes place on a toroidal surface.
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] +
                         grid[(i-1)%N, j] + grid[(i+1)%N, j] +
                         grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
                         grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
 
            # apply Conway's rules
            if grid[i, j]  == ON:
                if (total < 2) or (total > 3):
                    newGrid[i, j] = OFF
            else:
                if total == 3:
                    newGrid[i, j] = ON
    
    # update data
    frameNum += 1
    ax.set_title("Generation = " + str(frameNum))
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img,

# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Runs Conway's Game of Life system.py.")
    #arguments
    parser.add_argument('--size', dest='N', required=False)
    parser.add_argument('--update', dest='update', required=False)
    parser.add_argument('--filename', dest='filename', required=False)
    args = parser.parse_args()
    generations = 10
    if args.filename:
        with open(str(args.filename), 'r') as file:
            lines = file.readlines()
        generations = int(lines[1].split(' ')[0])
    
    # set grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)
        
    # set animation update interval
    updateInterval = 200
    if args.update:
        updateInterval = int(args.update)

    # declare grid
    grid = np.array([])

    if args.filename:
        grid = createGrid(N, args.filename)
    else: # populate grid with random on/off - more off than on
        grid = randomGrid(N)
    # Uncomment lines to see the "glider" demo
    #grid = np.zeros(N*N).reshape(N, N)
    #addGlider(1, 1, grid)

    # set up animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, N, ax),
                                  frames = generations,
                                  interval=updateInterval,
                                  save_count=50)

    plt.show()

# call main
if __name__ == '__main__':
    main()