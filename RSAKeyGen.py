#!/usr/bin/env python

import requests
from random import randrange, randint
from fractions import gcd


class RSAKeyGen(object):
    """
    Generate RSA Key pair using random numbers generated from Random.org
    """

    def __init__(self, url, params=None):
        self.url = url
        self.params = params or {"num": 960,
                                 "min": 0,
                                 "max": 2 ** 16 - 1,
                                 "col": 1,
                                 "base": 2,
                                 "format": "plain",
                                 "rnd": "new"
                                 }
        self.random_nums = []
        self.p = None
        self.q = None
        self.N = None
        self.lcm = None
        self.e = None
        self.d = None
        self.public = None
        self.private = None

    def get_random(self):
        """ Query random.org and generate a list of random numbers """
        request = requests.get(self.url, params=self.params)
        res = request.text.split()
        tmp = []
        while res:
            tmp.append(res.pop())
            if len(tmp) == 64:
                number = "".join(tmp)
                self.random_nums.append(int(number, 2))
                tmp = []

    # Adapted from Rosetta code
    def is_prime(self, guess, no_of_checks=10):
        """Checks whether the guess is prime
            using Miller Rabin Primality test """
        if guess == 2:
            return True
        if not guess & 1:
            return False

        def check(a, s, d, n):
            x = pow(a, d, n)
            if x == 1:
                return True
            for _ in range(s - 1):
                if x == n - 1:
                    return True
                x = pow(x, 2, n)
            return x == n - 1

        s = 0
        d = guess - 1

        while d % 2 == 0:
            d >>= 1
            s += 1

        for _ in range(no_of_checks):
            a = randrange(2, guess - 1)
            if not check(a, s, d, guess):
                return False
        return True

    def generate_primes(self):
        p = self.random_nums.pop()
        while not self.is_prime(p) and p.bit_length() < 1024:
            p = self.random_nums.pop()
        q = self.random_nums.pop()
        while not self.is_prime(q) and q.bit_length() < 1024:
            q = self.random_nums.pop()
        self.p = p
        self.q = q
        print "p: ", p
        print "q: ", q

    def totient(self):
        self.N = self.p * self.q
        print "N: ", self.N

    def coprimeTotient(self, lcm):
        while True:
            i = randint(0, lcm)
            if gcd(i, lcm) == 1:
                return i

    # Adapted from Rosetta Code
    def xgcd(self, b, n):
        x0, x1, y0, y1 = 1, 0, 0, 1
        while n != 0:
            q, b, n = b // n, n, b % n
            x0, x1 = x1, x0 - q * x1
            y0, y1 = y1, y0 - q * y1
        return b, x0, y0

    def mulinv(self, b, n):
        g, x, _ = self.xgcd(b, n)
        if g == 1:
            return x % n

    def generate_keys(self):
        self.get_random()
        self.generate_primes()
        self.totient()
        self.lcm = self.N // gcd(self.p, self.q)
        self.e = self.coprimeTotient(self.lcm)
        self.d = self.mulinv(self.e, self.lcm)
        print "e: ", self.e
        print "d: ", self.d
        self.public = (self.N, self.e)
        self.private = (self.N, self.d)
        return self.public, self.private


if __name__ == "__main__":
    gen = RSAKeyGen(url='https://www.random.org/integers')
    public, private = gen.generate_keys()
    print "Public Key: ", public
    print "Private Key: ", private
