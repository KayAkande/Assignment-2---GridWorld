# -*- coding: utf-8 -*-
"""
COSC-4117EL: Assignment 2 Problem Domain

This code provides a basic and interactive grid world environment where a robot can navigate using the arrow keys. The robot encounters walls that block movement, gold that gives positive rewards, and traps that give negative rewards. The game ends when the robot reaches its goal. The robot's score reflects the rewards it collects and penalties it incurs.
"""

import pygame
import numpy as np
import random
import time

# Constants for our display
GRID_SIZE = 5  # Easily change this value
CELL_SIZE = 60  # Adjust this based on your display preferences
SCREEN_WIDTH = GRID_SIZE * CELL_SIZE
SCREEN_HEIGHT = GRID_SIZE * CELL_SIZE
GOLD_REWARD = 10
TRAP_PENALTY = -10
GOAL_REWARD = 100  # Reward for reaching the goal
ROBOT_COLOR = (0, 128, 255)
GOAL_COLOR = (0, 255, 0)
WALL_COLOR = (0, 0, 0)
EMPTY_COLOR = (255, 255, 255)
GOLD_COLOR = (255, 255, 0)  # Yellow
TRAP_COLOR = (255, 0, 0)    # Red

ITERATIONAMOUNT = 100
DELAY = 1

random.seed(100)

class GridWorld:
    def __init__(self, size=GRID_SIZE):
        self.size = size
        self.grid = np.zeros((size, size))
        self.rewards = np.zeros((size, size))  # Added to keep track of rewards separately
        
        # Randomly select start and goal positions
        self.start = (random.randint(0, size-1), random.randint(0, size-1))
        self.goal = (random.randint(0, size-1), random.randint(0, size-1))
        
        self.robot_pos = self.start
        self.score = 0
        self.generate_walls_traps_gold()
        
        # Assign a high value for the goal state
        self.rewards[self.goal] = GOAL_REWARD

    def generate_walls_traps_gold(self):
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) != self.start and (i, j) != self.goal:
                    rand_num = random.random()
                    if rand_num < 0.1:  # 10% chance for a wall
                        self.grid[i][j] = np.inf
                    elif rand_num < 0.2:  # 10% chance for gold
                        self.rewards[i][j] = GOLD_REWARD
                    elif rand_num < 0.3:  # 10% chance for a trap
                        self.rewards[i][j] = TRAP_PENALTY

def move(self, direction):
    """Move the robot in a given direction."""
    x, y = self.robot_pos
    new_x, new_y = x, y

    # Check the direction and make the move if there is no wall
    if direction == "up" and x > 0 and self.grid[x-1][y] != np.inf:
        new_x = x - 1
    elif direction == "down" and x < self.size-1 and self.grid[x+1][y] != np.inf:
        new_x = x + 1
    elif direction == "left" and y > 0 and self.grid[x][y-1] != np.inf:
        new_y = y - 1
    elif direction == "right" and y < self.size-1 and self.grid[x][y+1] != np.inf:
        new_y = y + 1

    # Update the robot's position
    self.robot_pos = (new_x, new_y)

    # Calculate the reward (or penalty) for the new position
    reward = self.rewards[new_x][new_y]

    # Apply a step penalty (if there is no trap or gold, this would be -1)
    self.score += reward - 1

    # Clear the reward or penalty from the cell after it's been collected or triggered
    if self.rewards[new_x][new_y] != 0:
        self.rewards[new_x][new_y] = 0

    # If the cell had a wall, the robot's position would not change
    # Hence, no reward or penalty would be collected in that case

    return reward

    
    def display(self):
        """Print a text-based representation of the grid world (useful for debugging)."""
        for i in range(self.size):
            row = ''
            for j in range(self.size):
                if (i, j) == self.robot_pos:
                    row += 'R '
                elif self.grid[i][j] == np.inf:
                    row += '# '
                else:
                    row += '. '
            print(row)


def setup_pygame():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Grid World")
    clock = pygame.time.Clock()
    return screen, clock

def draw_grid(world, screen):
    """Render the grid, robot, and goal on the screen."""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # Determine cell color based on its value
            color = EMPTY_COLOR
            if world.grid[i][j] == np.inf:
                color = WALL_COLOR
            elif world.rewards[i][j] == GOLD_REWARD:  # Gold
                color = GOLD_COLOR
            elif world.rewards[i][j] == TRAP_PENALTY:  # Trap
                color = TRAP_COLOR

            pygame.draw.rect(screen, color, pygame.Rect(j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Drawing the robot and goal on top of the grid
    pygame.draw.circle(screen, ROBOT_COLOR, 
                       (int((world.robot_pos[1] + 0.5) * CELL_SIZE), int((world.robot_pos[0] + 0.5) * CELL_SIZE)), 
                       int(CELL_SIZE/3))
    pygame.draw.circle(screen, GOAL_COLOR, 
                       (int((world.goal[1] + 0.5) * CELL_SIZE), int((world.goal[0] + 0.5) * CELL_SIZE)), 
                       int(CELL_SIZE/3))

    # Drawing the grid lines
    for i in range(GRID_SIZE):
        pygame.draw.line(screen, (200, 200, 200), (i * CELL_SIZE, 0), (i * CELL_SIZE, SCREEN_HEIGHT))
        pygame.draw.line(screen, (200, 200, 200), (0, i * CELL_SIZE), (SCREEN_WIDTH, i * CELL_SIZE))

def randomMovement ():
    randomNum = random.randint(1, 4)
    if (randomNum == 1):
        return "up";
    elif (randomNum == 2):
        return "down";
    elif (randomNum == 3):
        return "left";
    elif (randomNum == 4):
        return "right";



def generateValueFunction(world):
    livingReward = -0.04  # Small negative reward to encourage shortest path
    gamma = 0.9  # Discount factor

    # Initialize values for all states to be zero
    valueArray = np.zeros((GRID_SIZE, GRID_SIZE))
    
    # Assign the goal state a high initial value
    valueArray[world.goal] = GOAL_REWARD
    
    for iteration in range(ITERATIONAMOUNT):
        newValueArray = np.copy(valueArray)

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if world.grid[i][j] == np.inf:  # Skip walls
                    continue

                # Check for the reward or penalty of the current state
                stateReward = world.rewards[i][j]

                # Calculate the value of each possible action from this state
                up = newValueArray[i-1][j] if i > 0 else -np.inf
                down = newValueArray[i+1][j] if i < GRID_SIZE - 1 else -np.inf
                left = newValueArray[i][j-1] if j > 0 else -np.inf
                right = newValueArray[i][j+1] if j < GRID_SIZE - 1 else -np.inf

                # Choose the best action (highest value)
                bestValue = max(up, down, left, right)

                # Update the state's value in the new value array
                newValueArray[i][j] = stateReward + livingReward + gamma * bestValue

        valueArray = newValueArray

    return valueArray


def main():
    """Main loop"""
    screen, clock = setup_pygame()
    world = GridWorld()


##################################################
    print(generateValueFunction(world));
##################################################

    running = True
    time_to_move = time.time() + DELAY  # Set the initial time to move

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if time.time() >= time_to_move:
           # world.move("down") #*************************
           # time_to_move = time.time() + DELAY  # Update the time to move

           # print(f"Current Score: {world.score}")

            if world.robot_pos == world.goal:
                print("Robot reached the goal!")
                print(f"Final Score: {world.score}")
                running = False

        screen.fill(EMPTY_COLOR)
        draw_grid(world, screen)
        pygame.display.flip()
        clock.tick(10)  # FPS



    pygame.quit()


if __name__ == "__main__":
    main()
