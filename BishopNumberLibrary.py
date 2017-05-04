''' This file defines arithmetic functions over real numbers with rates of
    convergence, called "Bishop numbers."

    A real number is a convergent sequence of rational numbers.
    A rational number is a python fraction, as defined in the fraction class.    
    A Bishop number is a pair (x, k(eps)) where x is a real number that
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

# If r is a rational number, bish(r) is a Bishop number corresponding to r
def bish(r):
    def x(n): return r
    def k(eps): return 0
    return (x, k)

# If a and b are bishop numbers, a[0]->L at rate a[1] and b[0]->M at rate b[1],
# then addB(a, b)->L+M at rate k'
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

# If a and b are bishop numbers, a[0]->L at rate a[1] and b[0]->M at rate b[1],
# then subB(a, b)->L-M at rate k'
def subB(a, b):
    x, j = a
    y, k = b
    
    def z(n):
        try:
            return a(n) - b(n)
        except ZeroDivisionError:
            return fr(0,1)

    def kPrime(eps):
        return x(n) + y(n)
    
    return (z, kPrime)

# If a and b are bishop numbers, a[0]->L at rate a[1] and b[0]->M at rate b[1],
# then mulB(a, b)->LM at rate k'
def mulB(a, b):
    x, j = a
    y, k = b
    
    def z(n):
        try:
            return a(n) * b(n)
        except ZeroDivisionError:
            return fr(0,1)

    def kPrime(eps):
        #return x(n) + y(n)
    
    return (z, kPrime)

# If a and b are bishop numbers, a[0]->L at rate a[1], b[0]->M at rate b[1], and
# M != 0, then divB(a, b)->L/M at rate k'
def divB(a, b):
    x, j = a
    y, k = b
    
    def z(n):
        try:
            return a(n) / b(n)
        except ZeroDivisionError:
            return fr(0,1)

    def kPrime(eps):
        #return x(n) + y(n)
    
    return (z, kPrime)
