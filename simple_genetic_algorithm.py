from random import randint, random
#Max allowed number
MAX_CONST=20
#These 'constants' will be treated as operations
operations = { MAX_CONST+1:'-', MAX_CONST+2:'+', MAX_CONST+3:'/', MAX_CONST+4:'*', MAX_CONST+5:'%' }
MAX_NUM = MAX_CONST+len(operations)

#Turns a genome into an expression
def build_expr(genome):
	nodes = [set_operations(gene) for gene in genome]
	out = []
	prev = None
	#Strip out repeats up-front, eg: '6 6 +' or '* * 9'
	for node in nodes:
		if type(prev) != type(node):
			out.append(node)
		prev = node
	#Return a string that can be evaluated
	return ' '.join([str(x) for x in out])

#Replace gene numbers with constants
def set_operations(val):
	if val<=MAX_CONST:
		return val
	return operations[val]

#Try/Catch to determine if the expression will live
def is_viable(genome):
	try:
		expr = build_expr(genome)
		return eval(expr) != None
	except:
		return False

#Generate a completely random genome
def generate(genome_length):
	y=[randint(0,MAX_NUM) for x in xrange(genome_length)]
	return y

#Initialiazes a full generation of viable genomes
def initialize_generation(genome_length,pop_size):
	result = []
	while len(result) < pop_size:
		genome = generate(genome_length)
		if is_viable(genome):
			result.append(genome)
	return result

#Determines the fitness of genes. The close to the target, the higher the result
def fitness(genes,target):
	expr = build_expr(genes)
	#1+abs() to prevent divide-by-0
	return 100/(1+abs(float((target-eval(expr)))))

#Who survives from each generation? Play a game of roulette
def roulette(population,count,target):
	out = []
	for n in xrange(count):
		#First, allocate a distribution from 0-1.0
		fitnesses = [fitness(x,target) for x in population]
		rel_fitness = [f/float(sum(fitnesses)) for f in fitnesses]
		probs = [sum(rel_fitness[:i+1]) for i in range(len(fitnesses))]
		#Generate a random number and see where it falls in the population
		r = random()
		for (i, individual) in enumerate(population):
			if r <= probs[i]:
				out.append(individual)
				del population[i]
				break
	return out

#Mutate rate percent of genes in a genome
def mutate(genome,rate):
	out = [(gene if random()>rate else randint(0,MAX_NUM)) for gene in genome]
	return out

#Mate two parents. Single pivot, random parent first, random choice from start/end
def mate(parents):
	rand = randint(1,len(parents[0])-1)
	choice = randint(0,1)
	if randint(0,1):
		child = parents[choice][:rand]+parents[choice^1][rand:]
	else:
		child = parents[choice][rand:]+parents[choice^1][:rand]
	return child

#Rebuild population after culling
def regenerate(population,target_size,mutation_rate):
	out = list(population)
	while len(out)<target_size: 
		#Choose random parents from survivors
		parents = [population[randint(0,len(population)-1)],population[randint(0,len(population)-1)]]
		#Crossover and mutate
		child = mutate(mate(parents),mutation_rate)
		#If it survives, keep it
		if is_viable(child):
			out.append(child)
	return out

#Pretty-prints a set of genomes
def print_gen(gen_count,genomes,target):
	print '\nGeneration {0} Avg Fitness: {1:.3f}'.format(gen_count,sum([fitness(x,target) for x in genomes])/float(len(genomes)))
	for genome in genomes:
		expr = build_expr(genome)
		print 'Expr: {0:<45} Result: {1:<5} Fit: {2:.3f}'.format(expr,eval(expr),fitness(genome,target))

'''
	Harness for running the genetic algorithm
	* runs - the max number of generations to run for
	* genome_length - the number of genes (not all will be expressed)
	* pop_size - the number of genomes in the population
	* survivor_count - how many live?
	* mutation_rate - what percent of genes mutate?
	* target - what should the expression evaluate to?
'''
def harness(runs=100,genome_length=40,pop_size=20,survivor_count=5,mutation_rate=.1,target=500):
	population = initialize_generation(genome_length,pop_size)		#Initialize the herd
	for i in xrange(runs):
		survivors = roulette(population,survivor_count,target) 		#Cull the herd!
		print_gen(i,survivors,target)								#Show the slaughter
		population = regenerate(survivors,pop_size,mutation_rate)	#Reproduce
		a = [x for x in population if eval(build_expr(x))==target] 	#On perfection, terminate
		if len(a)>0:
			break
	print_gen('Complete',population,target) 						#Print the final generation

harness()
