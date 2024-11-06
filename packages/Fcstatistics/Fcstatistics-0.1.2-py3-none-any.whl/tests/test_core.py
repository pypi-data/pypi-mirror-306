import pytest
from Fcstatistics.Fc import Mean, MVar, bayes_theorem, bi_coefficient

data = [1, 2, 3, 4, 5]
prior_A = 1/2
prior_A_2 =1/2
B_A = 30/40
B_A_2 = 20/40
n = 10
k = 5


def test_mean():
    result = Mean(data)
    print(f"Mean: {result}")  # 평균값 출력
    assert result == 3.0  # assert를 사용하여 테스트

def test_mvar():
    result = MVar(data)
    print(f"Population Variance: {result}")  # 분산값 출력
    assert pytest.approx(result, 0.01) == 2.0  # 근사값 비교를 위해 pytest.approx 사용

def test_bayes():
    result = bayes_theorem(prior_A, prior_A_2, B_A, B_A_2)
    print(f"Bayes theorem: {result}")  # 분산값 출력

def test_bicoefficient():
    result = bi_coefficient(n, k)
    print(f"Bi CoefficientL: {result}")