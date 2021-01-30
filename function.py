import random
import numpy as np


# 生成染色体
def Generate_chromosome():
    chromosome = []
    chromosome.append(random.randint(-80, 80) + random.random())
    chromosome.append(random.randint(-280, 30) + random.random())
    chromosome.append(random.randint(-80, 80) + random.random())
    chromosome.append(random.randint(-30, 130) + random.random())
    return chromosome


# 杂交
def Crossover(chromosome1, chromosome2):
    chromosome_new = []
    template = [random.randint(0, 1),
                random.randint(0, 1),
                random.randint(0, 1),
                random.randint(0, 1)]
    for i in range(4):
        if template[i] == 0:
            chromosome_new.append(chromosome1[i])
        else:
            chromosome_new.append(chromosome2[i])
    return chromosome_new

# 变异
def Variation(chromosome):
    chromosome_new = chromosome
    pick = random.randint(0, 3)
    chromosome_new[pick] += random.randint(-10, 10) + random.random()
    if pick == 0:
        if chromosome_new[pick] >= 51:
            chromosome_new[pick] = 50
        elif chromosome_new[pick] <= -51:
            chromosome_new[pick] = -50
    elif pick == 1:
        if chromosome_new[pick] >= 0:
            chromosome_new[pick] = -1
        elif chromosome_new[pick] <= -251:
            chromosome_new[pick] = -250
    elif pick == 2:
        if chromosome_new[pick] >= 51:
            chromosome_new[pick] = 50
        elif chromosome_new[pick] <= -51:
            chromosome_new[pick] = -50
    else:
        if chromosome_new[pick] >= 101:
            chromosome_new[pick] = 100
        elif chromosome_new[pick] <= 0:
            chromosome_new[pick] = 1
    return chromosome_new


# 按照环境和模型做出预测
def Predict(chromosome, environment):
    result = environment[0] * chromosome[0] + environment[1] * chromosome[1] + environment[2] * chromosome[2] + chromosome[3]
    return 0.5 * (1 + np.tanh(result)*0.5)
