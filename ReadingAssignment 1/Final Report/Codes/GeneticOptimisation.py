'''
Optimization using Genetic Operator
'''
# Imports
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Main Functions
def cal_pop_fitness(equation_inputs, pop):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calculates the sum of products between each input and its corresponding weight.
    fitness = np.sum(pop*equation_inputs, axis=1)
    return fitness

def select_mating_pool(pop, fitness, num_parents):
    # Selecting the best individuals in the current generation as parents for producing the offspring of the next generation.
    parents = np.empty((num_parents, pop.shape[1]))
    for parent_num in range(num_parents):
        max_fitness_idx = np.where(fitness == np.max(fitness))
        max_fitness_idx = max_fitness_idx[0][0]
        parents[parent_num, :] = pop[max_fitness_idx, :]
        fitness[max_fitness_idx] = -99999999999
    return parents
    
def crossover(parents, offspring_size):
    offspring = np.empty(offspring_size)
    # The point at which crossover takes place between two parents. Usually, it is at the center.
    crossover_point = np.uint8(offspring_size[1]/2)

    for k in range(offspring_size[0]):
        # Index of the first parent to mate.
        parent1_idx = k%parents.shape[0]
        # Index of the second parent to mate.
        parent2_idx = (k+1)%parents.shape[0]
        # The new offspring will have its first half of its genes taken from the first parent.
        offspring[k, 0:crossover_point] = parents[parent1_idx, 0:crossover_point]
        # The new offspring will have its second half of its genes taken from the second parent.
        offspring[k, crossover_point:] = parents[parent2_idx, crossover_point:]
    return offspring

def mutation(offspring_crossover, mutated_gene_index=None):
    if mutated_gene_index == None:
        mutated_gene_index = np.random.randint(0, offspring_crossover.shape[1])
    # Mutation changes a single gene in each offspring randomly.
    for idx in range(offspring_crossover.shape[0]):
        # The random mutation to be added to the gene.
        random_mutation = np.random.uniform(-1.0, 1.0, 1)
        offspring_crossover[idx, mutated_gene_index] = offspring_crossover[idx, mutated_gene_index] + random_mutation
    return offspring_crossover

# Driver Code
# Parameters
verbose = False

equation_inputs = [4, -2, 3.5, 5, -11, -4.7, 2.5, 0.1]

num_weights = len(equation_inputs) # Number of the weights we are looking to optimize.

sol_per_pop = 200 # Defining the population size.

pop_size = (sol_per_pop, num_weights) # The population will have sol_per_pop chromosomes where each chromosome has num_weights genes.

num_generations = 5000

num_parents_mating = 100

ncols = 1


new_population = np.random.uniform(low=-4.0, high=4.0, size=pop_size) # Creating the initial population.

print("No of Generations:", num_generations)
print("No of selected parents per generation:", num_parents_mating)
print("\n")

max_fitness_history = []
max_fitness_ingen_history = []
best_chromosome_history = []
best_chromosome_ingen_history = []

max_fitness = None
best_chromosome = None
for generation in tqdm(range(num_generations)):
    # Measuring the fitness of each chromosome in the population.
    fitness = cal_pop_fitness(equation_inputs, new_population)

    # Record History
    max_fitness_ingen_history.append(np.max(fitness))
    best_chromosome_ingen_history.append(list(new_population[np.argmax(fitness)]))

    # Print
    if not max_fitness == None and verbose:
        print("Best result after generation", str(generation - 1) + ":", np.max(fitness))
        print("Improvement in result:", str(np.max(fitness) - max_fitness))

    # Update Best Values
    if max_fitness == None or max_fitness < np.max(fitness):
        max_fitness = np.max(fitness)
        best_chromosome = new_population[np.argmax(fitness)]
    # Record History
    max_fitness_history.append(max_fitness)
    best_chromosome_history.append(list(best_chromosome))

    # Selecting the best parents in the population for mating.
    parents = select_mating_pool(new_population, fitness, num_parents_mating)

    # Generating next generation using crossover.
    offspring_crossover = crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))

    # Adding some variations to the offsrping using mutation.
    offspring_mutation = mutation(offspring_crossover, mutated_gene_index=4)

    # Prints
    if verbose:
        print("Generation:", str(generation + 1), "\n\n")

        print("Fitness Values:\n")
        print(fitness)
        print("\n")

        print("Selected Parents:\n")
        for p in parents:
            print(p)
        print("\n")

        print("Crossover Result:\n")
        for off in offspring_crossover:
            print(off)
        print("\n")

        print("Mutation Result:\n")
        for off in offspring_mutation:
            print(off)
        print("\n\n")

    # Creating the new population based on the parents and offspring.
    new_population[0 : parents.shape[0], :] = parents
    new_population[parents.shape[0] : , :] = offspring_mutation

print("Summary:\n")

# Best Performer Chromosome
print("Best Fitness:", max_fitness)
print("Best Chromosome:", best_chromosome)
print("\n\n")

# Plots
# Best Fitness Per Generation Plot
plt.plot(range(1, num_generations+1), max_fitness_ingen_history)
plt.show()

# Best Chromosome Per Generation Plot
best_chromosome_ingen_history = np.array(best_chromosome_ingen_history)
n_genes = len(best_chromosome)
nrows = int(n_genes / ncols) + 1

gen_range = range(1, num_generations+1)
for gene_index in range(n_genes):
    ax = plt.subplot(nrows, ncols, gene_index+1)
    ax.title.set_text("Gene " + str(gene_index+1) + ": Input: " + str(equation_inputs[gene_index]) + " , Best: " + str(best_chromosome[gene_index]))
    plt.plot(gen_range, best_chromosome_ingen_history[:, gene_index])
plt.show()