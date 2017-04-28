''' This file defines arithmetic functions over real numbers.
    A real number is a convergent sequence of rational numbers.
    A rational number is a python fraction, as defined in the fraction class.

    A note on error handling:
    In the rare case that computation of a member of a sequence throws a
    ZeroDivisionError, Fraction(0,1) is used instead. This number is arbitrary,
    as the sequence will converge to it's limit anyways.
'''

from fractions import Fraction as fr
from math import factorial as fact
from math import gcd

# If a and b are real numbers, a->L and b->M, then add(a, b)->L+M
def add(a, b):
    def c(n):
        try:
            return a(n) + b(n)
        except ZeroDivisionError:
            return fr(0,1)
    return c

# If a and b are real numbers, a->L and b->M, then sub(a, b)->L-M
def sub(a, b):
    def c(n):
        try:
            return a(n) - b(n)
        except ZeroDivisionError:
            return fr(0,1)
    return c

# If a and b are real numbers, a->L and b->M, then mul(a, b)->LM
def mul(a, b):
    def c(n):
        try:
            return a(n) * b(n)
        except ZeroDivisionError:
            return fr(0,1)
    return c

# If a and b are real numbers, a->L and b->M, and M != 0, then div(a, b)->L/M
def div(a, b):
    def c(n):
        try:
            return a(n) / b(n)
        except ZeroDivisionError:
            return fr(0,1)
    return c

# If r is a real number, r -> L, then sine(r) -> sin(L)
def sine(r):
    def Q(n):
        return sineQ(r(n), fr(1,n))
    return Q
    
# If x is a rational number and eps is a positive rational, then
# |sineQ(x, eps) - sin(x)| < eps
def sineQ(x, eps):
    n = R(x, eps)
    print("n: ", n)
    print("eps: ", eps)
    print("x: ", x)
    return P(n, x)

# If x is a rational number and eps is a positive rational, R(x, eps) returns an
# n to be used for P(n, x) st |P(n, x) - sin(x)| < eps
def R(x, eps):
    n = 0
    R = 2 #Something always greater than eps
    while (R >= eps):
        R = fr(x.numerator**n+1, \
                (x.denominator**(n+1)) * fact(n+1))
        n += 1
    return n
    
# If x is a rational and n is a positive int, sinP(n, x) is the summation
# from k=0 to n of (sine^k(0)*(x**k)) / k!
def P(n, x):
    PSum = fr(0,1)
    for k in range(0, n):
        PSum += fr(x.numerator**k * sinDeriv(k), \
                   x.denominator**k * fact(k))
    return PSum
   
# if n is a nonnegative integer, sinDeriv returns the nth derivative of sin(0)
def sinDeriv(n):
    return [0, 1, 0, -1][n%4]
