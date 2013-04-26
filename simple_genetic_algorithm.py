from random import randint, random
from math import log
operations = { 10:'-', 11:'+', 12:'/', 13:'*' }
MAX_SIZE=15

def set_operations(val):
	if val<=9:
		return val
	if operations.has_key(val):
		return operations[val]
	return None

def build_expr(genes):
	nums = [set_operations(x) for x in genes]
	nums = [i for i in nums if i!=None]
	prev = None
	out = []
	for item in nums:
		if type(item) != type(prev):
			out.append(item)
		prev = item
	return ' '.join([str(x) for x in out])

def is_viable(genome):
	try:
		return eval(build_expr(genome)) != None
	except:
		return False

def generate(genome_length):
	return [randint(0,MAX_SIZE) for x in xrange(0,genome_length)]

def print_gen(gen_count,genomes,target):
	print '\nGeneration {0} Avg Fitness: {1:.3f}'.format(gen_count,sum([fitness(x,target) for x in genomes])/float(len(genomes)))
	for genome in genomes:
		expr = build_expr(genome)
		print 'Expr: {0:<45} Result: {1:<5} Fit: {2:.3f}'.format(expr,eval(expr),fitness(genome,target))

def build_gen(genome_length,pop_size):
	result = []
	while len(result) < pop_size:
		genome = generate(genome_length)
		if is_viable(genome):
			result.append(genome)
	return result

def fitness(genes,target):
	expr = build_expr(genes)
	return 100/(1+abs(float((target-eval(expr)))))

def roulette(population,count,target):
	out = []
	for n in xrange(count):
		fitnesses = [fitness(x,target) for x in population]
		rel_fitness = [f/float(sum(fitnesses)) for f in fitnesses]
		probs = [sum(rel_fitness[:i+1]) for i in range(len(fitnesses))]
		r = random()
		for (i, individual) in enumerate(population):
			if r <= probs[i]:
				out.append(individual)
				del population[i]
				break
	return out

def mutate(genes,rate):
	out = [(gene if random()>rate else randint(0,MAX_SIZE)) for gene in genes]
	return out

def mate(parents):
	rand = randint(1,len(parents[0])-1)
	choice = randint(0,1)
	if randint(0,1):
		child = parents[choice][:rand]+parents[choice^1][rand:]
	else:
		child = parents[choice][rand:]+parents[choice^1][:rand]
	return child

def regenerate(population,target_size,mutation_rate):
	out = list(population)
	while len(out)<target_size: 
		parents = [population[randint(0,len(population)-1)],population[randint(0,len(population)-1)]]
		child = mutate(mate(parents),mutation_rate)
		if is_viable(child):
			out.append(child)
	return out

def harness(runs,genome_length,pop_size,survivor_count,mutation,target):
	population = build_gen(genome_length,pop_size)
	for i in xrange(runs):
		survivors = roulette(population,survivor_count,target)
		print_gen(i,survivors,target)
		population = regenerate(survivors,pop_size,mutation)
		a = [x for x in population if eval(build_expr(x))==target]
		if len(a)>0:
			break
	print_gen('Complete',population,target)
