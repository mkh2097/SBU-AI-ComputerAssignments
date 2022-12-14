# -*- coding: utf-8 -*-
"""FinalChess.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1SlACxvYkKKIBvftuGmKdV_joW4e5gv2N
"""

import numpy as np

def initialize(queen_number=8, pop_number=40):
  init_population = np.zeros((pop_number,queen_number))
  init_population = [np.random.permutation(queen_number)+1 for _ in range(pop_number)]
  return init_population

import numpy as np
def evaluate(person):
    score = 0
    for first_row, first_col in enumerate(person, start=1):
      for second_row, second_col in enumerate(person[first_row:(len(person))], start=first_row+1):
        if abs(first_col-second_col) == abs(first_row-second_row) or second_col == first_col:
          score += 1
    return score

def select(population, scores):
  scores = np.array(scores)
  population = np.array(population)

  indexes = np.argsort(scores)
  sorted_list = population[indexes]

  print("best_score:", evaluate(sorted_list[0]))

  return sorted_list[0:10]

def mutate(child):
  child_mut = child.copy() 
  for i in range(len(child)):
    if np.random.rand() < 0.2:
      index = np.random.randint(0, len(child))
      child_mut[index] = np.random.randint(1, len(child)+1)
  return child_mut

def crossover(parent_1, parent_2):
  child_1, child_2 = parent_1.copy(), parent_2.copy()
  if np.random.rand() < 0.95:
    split_point = np.random.randint(1, len(child_1)-2)
    child_1 = np.append(parent_1[:split_point], parent_2[split_point:])
    child_2 = np.append(parent_2[:split_point], parent_1[split_point:])
  return [child_1, child_2]

def genetic_algorithm(queen_number=8,max_gen=100000):
  population = initialize(queen_number)
  gen_counter = 0
  while gen_counter < max_gen:
    if evaluate(population[0])  == 0:
      break
    gen_counter += 1
    print("GEN:", gen_counter)
    scores = [evaluate(person) for person in population]    
    population = select(population, scores)
    np.random.shuffle(population)
    children = np.empty(0)
    for i in range(0, 10, 2):
      parent_1, parent_2 = population[i], population[i+1]
      for child in crossover(parent_1, parent_2):
        child = mutate(child)
        population = np.vstack((population, child))
    population = population.tolist()
  # print("Gen:", gen_counter)
  return np.array(population[0])

import matplotlib.pyplot as plt
import matplotlib.cm as cm
def plotCheckBoard(sol):
   
    def checkerboard(shape):
        return np.indices(shape).sum(axis=0) % 2

    sol = sol -1
    size = len(sol)
    color = 0.5
    board = checkerboard((size,size)).astype('float64')
    # board = board.astype('float64')
    for i in range(size):
        board[int(sol[i]), i] = color

    fig, ax = plt.subplots()
    ax.imshow(board, cmap=plt.cm.CMRmap, interpolation='nearest')
    plt.show()

if __name__ == "__main__":
    best_fit = genetic_algorithm(queen_number=12)
    print("Final Results:")
    for row, col in enumerate(best_fit):
      print("(", row+1, ",", col, ")")
    plotCheckBoard(best_fit)