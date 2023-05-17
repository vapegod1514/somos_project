import numpy as np
import gc
import fractions
from math import gcd
import random

from sympy import Matrix

def make_science(p, q, n, alpha, betta, S_positive):

    def print_matrix(numpy_matrix):
        print(numpy_matrix)
        return


    # S_positive = [
    #     fractions.Fraction(1, 1),
    #     fractions.Fraction(2, 1),
    #     fractions.Fraction(1, 1),
    #     fractions.Fraction(198, 1),
    #     fractions.Fraction(3465, 1111),
    #     fractions.Fraction(228, 1488),
    # ]

    # p = 3
    # q = 1
    # n = 6
    #
    # alpha = fractions.Fraction(1, 1)
    # betta = fractions.Fraction(2, 1)


    assert min(p, q) <= n/2
    assert len(S_positive) == n

    S_negative = [x for x in S_positive[::-1]]
    for _ in range(n-1):
        k = len(S_negative)-n
        S_negative.append((alpha*S_negative[k+p]*S_negative[k+n-p] + betta*S_negative[k+q]*S_negative[k+n-q])/S_negative[k])
    S_negative = S_negative[-n:]


    def find_s_bigger(m):
        if S_positive[m - n] == 0:
            # print(S_positive)
            # print(S_negative)
            assert False
        s_m = (alpha * S_positive[m - p] * S_positive[m - n + p] + betta * S_positive[m - q] * S_positive[m - n + q]) / S_positive[m - n]
        S_positive.append(s_m)
        return s_m


    def find_s_smaller(m):
        if S_negative[-(m + n)] == 0:
            # print(S_positive)
            # print(S_negative)
            assert False
        s_m = (alpha * S_negative[-(m + p)] * S_negative[-(m + n-p)] + betta * S_negative[-(m + q)] * S_negative[-(m + n-q)]) / S_negative[-(m + n)]
        S_negative.append(s_m)
        return s_m


    def make_matrix_positions(n):
        position_matrix = [[(q, w) for q in range(-n, n + 1)] for w in range(-n, n + 1)]
        # print(position_matrix)
        return position_matrix


    def make_numpy_matrix_0(position_matrix):
        somos_matrix = []
        for row in position_matrix:
            somos_row = []
            for elem in row:
                m = elem[0]
                n = elem[1]
                if m - n >= 0:
                    while m - n > len(S_positive) - 1:
                        find_s_bigger(len(S_positive))
                    somos_elem = S_positive[m - n]
                else:
                    while -(m - n) > len(S_negative) - 1:
                        find_s_smaller(-len(S_negative))
                    somos_elem = S_negative[-(m - n)]
                if m + n >= 0:
                    while m + n > len(S_positive) - 1:
                        find_s_bigger(len(S_positive))
                    somos_elem_ = S_positive[m + n]
                else:
                    while -(m + n) > len(S_negative) - 1:
                        find_s_smaller(-len(S_negative))
                    somos_elem_ = S_negative[-(m + n)]
                somos_row.append(somos_elem * somos_elem_)
            somos_matrix.append(somos_row)
        return Matrix(somos_matrix)

    ranks = []

    dim = 0
    while dim <= 500:
        dim += 1
        position_matrix_ = make_matrix_positions(dim)
        numpy_somos_matrix_ = make_numpy_matrix_0(position_matrix_)
        rank = numpy_somos_matrix_.rank() # calc_rank(numpy_somos_matrix_)
        ranks.append(rank)
        print(rank)
        all_good = False
        if len(ranks) > 10:
            all_good = True
            for i in range(len(ranks) - 1, len(ranks) - 6, -1):
                if rank != ranks[i]:
                    all_good = False
        if all_good:
            return True

    # print(ranks)
    return False


for dummy in range(100000):
    n = 9
    for p in range(2, n // 2):
        for q in range(1, p):
            if gcd(q, p) == 1 and gcd(n, q) == 1 and gcd(n, p):
                first_members = [fractions.Fraction(random.randint(1, 100), 1) for _ in range(n)]

                print(first_members, end='\t')
                alpha = fractions.Fraction(random.randint(1, 10), 1)
                betta = fractions.Fraction(random.randint(1, 10), 1)
                print('alpha = ', alpha, 'betta =', betta, 'p=', p, 'q=', q)

                print(make_science(p, q, n, alpha, betta, first_members))
                gc.collect()
