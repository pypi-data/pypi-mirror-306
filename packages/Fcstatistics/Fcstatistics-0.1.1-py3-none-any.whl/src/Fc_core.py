# ECHC 통계 라이브러리
def Mean(x):
    return float(sum(x) / len(x))

def MVar(x):
    return sum(map(lambda a: (a - Mean(x)) ** 2, x)) / len(x)

# prior_A: A 사건의 사전 확률
# prior_A_2: A_2 사건의 사전 확률
# B_A: B 사건이 일어났을 때의 A 사건의 우도
# B_A_2: B 사건이 일어났을 때의 A_2 사건의 우도
def bayes_theorem(prior_A, prior_A_2, B_A, B_A_2): 
    # A 사건의 사후확률
    posterior_A = (prior_A * B_A) / (prior_A * B_A + prior_A_2 * B_A_2)
    # A_2 사건의 사후확률
    posterior_A_2 = 1 - posterior_A
    return posterior_A, posterior_A_2

# 'n': 전체 수, 'k': 특정 수
def bi_coefficient(n, k):
    if k == 0 or k == n:
        return 1
    return bi_coefficient(n - 1, k - 1) + bi_coefficient(n - 1, k)