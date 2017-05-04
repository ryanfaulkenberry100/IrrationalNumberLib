''' This file defines arithmetic functions over real numbers with rates of
    convergence, called measured real numbers

    A real number is a convergent sequence of rational numbers.
    A rational number is a python fraction, as defined in the fraction class.    
    A measured real number is a pair (x, k(eps)) where x is a real number that
        converges to its limit at rate k(eps).
    k(eps) is a function from positive rational numbers to positive integers.
        Where eps is an error bound for a real number, and for every integer
        n > k(eps), |n - L| < eps. In other words, every element x(n) where
        n > k(eps) is approximately L with error bound eps.
        

    Usage example:
        def x(n): return Fraction(1, n)
        def y(n): return Fraction(1, n**2)
        def j(eps): return Fraction(1/eps)
        def k(eps): return Fraction(1/eps**.5)
    
        (a, b) = addB((x, j), (y, k))

        a(n) is equivalent to:
            lambda n: Fraction(1,n) + Fraction(1,n**2)
        b(n) is equivalent to:
            lambda eps: Fraction(1/eps) + Fraction(1/eps**.5)

        We now have the sum of two real numbers, and a function that tells us
        which elements of the resulting real number are within some error bound
        we choose.


    Note:
    The elements of real numbers that throw zero-division errors are
    handled by returning Fraction(0,1), which is arbitrary. If these elements
    aren't taken into account when choosing a k function, the resulting k(eps)
    could be incorrect. Best is to avoid such real numbers altogether, if
    possible.
    
'''

from fractions import Fraction as fr
from math import factorial as fact
from math import gcd
from math import ceil

# For ease of testing
a = (lambda n: 1/n, lambda eps: ceil(1/eps))
b = (lambda n: 1/n**2, lambda eps: ceil((1/eps)**.5))

# If r is a rational number, bish(r) is a measured real number corresponding
# to r
def bish(r):
    def x(n): return r
    def k(eps): return 0
    return (x, k)

# If a and b are measured real numbers, a[0]->L at rate a[1] and b[0]->M at
# rate b[1], then addB(a, b)->L+M at rate k'
def addB(a, b):
    x, j = a
    y, k = b
    
    def z(n):
        try:
            return x(n) + y(n)
        except ZeroDivisionError:
            return fr(0,1)

    def kPrime(eps):
            return j(eps) + k(eps)
        
    return (z, kPrime)

# If a and b are measured real numbers, a[0]->L at rate a[1] and b[0]->M at
# rate b[1], then subB(a, b)->L-M at rate k'
def subB(a, b):
    x, j = a
    y, k = b
    
    def z(n):
        try:
            return x(n) - y(n)
        except ZeroDivisionError:
            return fr(0,1)

    def kPrime(eps): return j(eps) + k(eps)
    
    return (z, kPrime)

# If a and b are measured real numbers, a[0]->L at rate a[1] and b[0]->M at
# rate b[1], then mulB(a, b)->LM at rate k'
def mulB(a, b):
    x, j = a
    y, k = b
    
    def z(n):
        try:
            return x(n) * y(n)
        except ZeroDivisionError:
            return fr(0,1)

    def kPrime(eps): return ceil(x(eps) * y(eps)) # Inefficient (but correct)
    
    return (z, kPrime)

# If a and b are measured real numbers, a[0]->L at rate a[1], b[0]->M at rate
# b[1], and M != 0, then divB(a, b)->L/M at rate k'
def divB(a, b):
    x, j = a
    y, k = b
    
    def z(n):
        try:
            return x(n) / y(n)
        except ZeroDivisionError:
            return fr(0,1)

    def kPrime(eps): return ceil(x(eps) * y(eps)) # Inefficient (but correct)
    
    return (z, kPrime)

# If a is a measured real number and a[0]->L at rate a[1], then sinB(a)->sine(a)
# at rate k', where sine(a) is the true sine of a
def sinB(a):
    x, j = a
    def Q(n): return sinQ(x(n), fr(1,n))
    def kPrime(eps): return j(eps)
    return (Q, kPrime)

# If x is a rational number and eps is a positive rational, then
# |sinQ(x, eps) - sine(x)| < eps, where sine(x) is the true sine of x
def sinQ(q, eps):
    n = R(q, eps)
    return P(n, q)

# If x is a rational number and eps is a positive rational, R(q, eps) returns an
# n to be used for P(n, x) st |P(n, q) - sin(q)| < eps, per Taylor's Theorem
def R(q, eps):
    n = 0
    R = eps + 1 #Something always greater than eps
    while (R >= eps):
        R = q**(n+1) * fr(1, fact(n+1))
        n += 1
    return n

# If q is a rational and n is a positive int, P(n, q) is the summation
# from k=0 to n of (sine^k(0)*(q**k)) / k!, per Taylor's Theorem
def P(n, q):
    PSum = fr(0,1)
    for k in range(0, n):
        PSum += q * fr(sinDeriv(k), fact(k))
    return PSum
    
# if n is a nonnegative integer, sinDeriv returns the nth derivative of sin(0)
def sinDeriv(n):
    return [0, 1, 0, -1][n%4]
