from .Individual import Individual
from .Node import Node

# 
# By using this file, you are agreeing to this product's EULA
#
# This product can be obtained in https://github.com/jespb/Python-StdGP
#
# Copyright ©2019-2022 J. E. Batista
#

def double_tournament(rng, population, n, Sf, Sp, Switch):
	'''	. If Switch is False, the function runs Sf fitness tournaments, followed by 1 tournament with Sp individuals chosen at random from the Sf winners, 
        with the winner determined by the formula 1/(1+size(individual)).. 
	
       If Switch is True, the function performs Sp parsimony tournaments followed by a single tournament with Sf individuals, selecting the winner based on the fittest accuracy measure,

       An error is raised if we get incompatible values for Sf and Sp, so it is ensured that Sf is less than Sp when Switch is True and Sp is less than Sf when Switch is False.
 '''
	best=None
	fittest=[]
	smallest=[]
	if Switch == False and Sf >= Sp:
    # If Switch is False, the function runs Sf fitness tournaments, followed by 1 tournament with Sp individuals
		for _ in range(Sf):
			fittest.append(fitness_tournament(rng, population,n))
		for _ in range(Sp):
			competitor = rng.choice(fittest)
			competitor_size = competitor.size
			competitor_fitness = 1 / (1 + competitor_size)
			if best is None or competitor_fitness > best[1]:
				best = (competitor, competitor_fitness)
			elif competitor_fitness == best[1]:
				# Randomly choose between the two individuals
				if rng.random() < 0.5:
					best = (competitor, competitor_fitness)
		return best[0]
	elif Switch==True and Sf <= Sp:
    #If Switch is True, the function performs Sp parsimony tournaments followed by a single tournament with Sf individuals,
		for _ in range(Sp):
			smallest.append(parsimony_tournament(rng, population, n))
		for f in range(Sf):
			competitor = rng.choice(smallest)
			competitor_fitness = competitor.fitness
			if best is None or competitor_fitness > best[1]:
				best = (competitor, competitor_fitness)
			elif competitor_fitness == best[1]:
				# Randomly choose between the two individuals
				if rng.random() < 0.5:
					best = (competitor, competitor_fitness)
		return best[0]
	else:
    #An error is raised if we get incompatible Sf and Sp values
		raise Exception('Incompatible values of Sf and Sp')



def parsimony_tournament(rng, population, n):
	'''
	A parsimony tournament selection strategy is implemented that selects n Individuals randomly from a given population,
   calculates their fitness based on the size of their representation, and returns the Individual with the shortest size as the winner of the tournament
	'''
	best = None
	for _ in range(n):
		competitor = rng.choice(population)
		competitor_size = competitor.size
		competitor_fitness = 1 / (1 + competitor_size)
		if best is None or competitor_fitness > best[1]:
			best = (competitor, competitor_fitness)
	return best[0]


def fitness_tournament(rng, population,n):
	'''
	Selects "n" Individuals from the population and return a 
	single Individual.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''

	candidates = [rng.randint(0,len(population)-1) for i in range(n)]
	return population[min(candidates)]


def getElite(population,n):
	'''
	Returns the "n" best Individuals in the population.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	return population[:n]


def getOffspring(rng, population, tournament_size, Sf, Sp, Switch):
	'''
	Genetic Operator: Selects a genetic operator and returns a list with the 
	offspring Individuals. The crossover GOs return two Individuals and the
	mutation GO returns one individual. Individuals over the LIMIT_DEPTH are 
	then excluded, making it possible for this method to return an empty list.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	isCross = rng.random()<0.5

	desc = None

	if isCross:
		desc = STXO(rng, population, tournament_size, Sf, Sp, Switch)
	else:
		desc = STMUT(rng, population, tournament_size, Sf, Sp, Switch)

	return desc


def discardDeep(population, limit):
	ret = []
	for ind in population:
		if ind.getDepth() <= limit:
			ret.append(ind)
	return ret


def STXO(rng, population, tournament_size, Sf, Sp, Switch):
	'''
	Randomly selects one node from each of two individuals; swaps the node and
	sub-nodes; and returns the two new Individuals as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = double_tournament(rng, population, tournament_size, Sf=Sf, Sp=Sp, Switch=Switch)
	ind2 = double_tournament(rng, population, tournament_size, Sf=Sf, Sp=Sp, Switch=Switch)

	h1 = ind1.getHead()
	h2 = ind2.getHead()

	n1 = h1.getRandomNode(rng)
	n2 = h2.getRandomNode(rng)

	n1.swap(n2)

	ret = []
	for h in [h1,h2]:
		i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
		i.copy(h)
		ret.append(i)
	return ret


def STMUT(rng, population, tournament_size, Sf, Sp, Switch):
	'''
	Randomly selects one node from a single individual; swaps the node with a 
	new, node generated using Grow; and returns the new Individual as the offspring.

	Parameters:
	population (list): A list of Individuals, sorted from best to worse.
	'''
	ind1 = double_tournament(rng, population, tournament_size, Sf=Sf, Sp=Sp, Switch=Switch)
	h1 = ind1.getHead()
	n1 = h1.getRandomNode(rng)
	n = Node()
	n.create(rng, ind1.operators, ind1.terminals, ind1.max_depth)
	n1.swap(n)


	ret = []
	i = Individual(ind1.operators, ind1.terminals, ind1.max_depth, ind1.model_name, ind1.fitnessType)
	i.copy(h1)
	ret.append(i)
	return ret
