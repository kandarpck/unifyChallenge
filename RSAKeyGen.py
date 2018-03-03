#!/usr/bin/env python

import requests
from random import randrange
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

    def generate_rsa_key_pairs(self):
        p = self.random_nums.pop()
        while not self.is_prime(p) and p.bit_length() < 1024:
            p = self.random_nums.pop()
        q = self.random_nums.pop()
        while not self.is_prime(q) and q.bit_length() < 1024:
            q = self.random_nums.pop()
        self.p = p
        self.q = q

    def totient(self):
        self.N = self.p * self.q
        self.lcm = self.N // gcd(self.p, self.q)


    def generate_keys(self):
        self.generate_keys()
        self.totient()


if __name__ == "__main__":
    gen = RSAKeyGen(url='https://www.random.org/integers')
    gen.get_random()
    gen.generate_keys()
