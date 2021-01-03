import random
import numpy as np

#生成染色体
def Generate_chromosome():
    chromosome = []
    for i in range(3):
        chromosome.append(random.randint(-100, 100) + random.random())
    return chromosome

#杂交
def Crossover(chromosome1, chromosome2):
    chromosome_new = []
    template = [random.randint(0, 1),
                random.randint(0, 1),
                random.randint(0, 1), ]
    for i in range(3):
        if template[i] == 0:
            chromosome_new.append(chromosome1[i])
        else:
            chromosome_new.append(chromosome2[i])
    return chromosome_new

#变异
def Variation(chromosome):
    chromosome_new = chromosome
    pick = random.randint(0, 2)
    chromosome_new[pick] += (random.randint(-100, 100) + random.random()) * 0.1
    if chromosome_new[pick] >= 201:
        chromosome_new[pick] = 201
    elif chromosome_new[pick] <= -199:
        chromosome_new[pick] = -199
    return chromosome_new

#按照环境和模型做出预测
def Predict(chromosome, environment):
    result = environment[0] * chromosome[0] + environment[1] * chromosome[1] + environment[2] * chromosome[2]
    return 0.5 * (1 + np.tanh(result))
