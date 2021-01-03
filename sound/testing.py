import numpy as np


# --------------------------------------------
# 激活函数
# 当derive为True时，是对sigmoid函数求一阶导数后的函数，f'=y*(1-y)
def f_sigmoid(x, derive=False):
    if not derive:
        return 1 / (1 + np.exp(-x))
    else:
        return x * (1 - x)  # 这里的x实际上是f(x)


# --------------------------------------------

# 学习的样本，3个维度，共4个样本，因此是3x4的矩阵
X = np.array([[1, 1, 1],
              [1, 1, 2],
              [1, 2, 2],])
# 预期输出，即监督值
Y = np.array([[0, 0],
              [0, 1],
              [1, 0]])
# Weights
np.random.seed(3)
# 4 x 3 ，说明隐藏层有3个结点，但是包括1个偏置
W = 2 * np.random.random((3, 3)) - 1
print('\nW=\n', W)
#
Bias1 = np.ones((4, 3)) * 0.1
print('Bias1=\n', Bias1)
# 把Bias1要扩展成5x3，因为有5个样本，有3个隐含层节点

# 4 x 1 ，说明输出层有1个结点，包含了偏置之后，维度增加1
V = 2 * np.random.random((3, 2)) - 1
print('\nV=\n', V)
Bias2 = np.ones((4, 2)) * 0.1  # 输出层偏置，设置为
print('Bias2=\n', Bias2)

# 学习的速率
learn_rate = 0.95

# 为隐含层的输入增加偏置向量
'''Bias_S = (2 * np.random.random((3, 1)) - 1).dot(np.array([[1, 1, 1]]))
print('Bias_S =\n', Bias_S)'''

MAX_LEARN_COUNT = 6000
nLearn_Count = 0
while nLearn_Count < MAX_LEARN_COUNT:
    # --------------------------------------------
    # 隐含层的结点总输入
    S = np.dot(X, W) + Bias1
    B = f_sigmoid(S)
    # --------------------------------------------
    # 输出层的计算
    L = np.dot(B, V) + Bias2
    C = f_sigmoid(L)
    # --------------------------------------------
    Diff = Y - C  # Diff是监督值与实际输出之间的误差，5x1 矩阵
    # print('\nCost=\n', Diff)
    zDiff = np.mean(np.abs(Diff))  # np.abs()把矩阵的元素逐个求绝对值，保存回原来的位置
    print('绝对误差值 zDiff={0}'.format(zDiff))

    Delta_C = Diff * f_sigmoid(C, True)
    ##print('#Delta_C=\n', Delta_C)  # Delta_C记录了

    Delta_V = np.dot(B.T, Delta_C)  # B相当于是输出层的输入，把每个节点的5次训练产生的delta_V累积了
    Delta_Bias2 = Delta_C.sum(axis=0)  # 按列求和，把每个输出节点的每个样本训练后的效果都累积下来
    ##print('Delta_Bias2=', Delta_Bias2)
    # print('Delta_V=\n', Delta_V)  # 记录了5次训练的Delta_V, 5x4 矩阵
    V = V + learn_rate * Delta_V
    Bias2 = Bias2 + learn_rate * Delta_Bias2
    ##print('调整后V=\n', V)
    # print('调整后Bias2=\n', Bias2)

    # 计算隐含层的权的调整
    Delta_B = np.dot(Delta_C, V.T) * f_sigmoid(B, derive=True)
    ##print('中间 Delta_B=\n', Delta_B)
    Delta_Bias1 = Delta_B.sum(axis=0)
    # print('Delta_Bias1=\n', Delta_Bias1)
    Delta_W = np.dot(X.T, Delta_B)  # 把多个样本的每个节点的偏差累积
    Bias1 = Bias1 + learn_rate * Delta_Bias1
    W = W + learn_rate * Delta_W

    # print('Delta_W=\n', Delta_W)
    nLearn_Count += 1


