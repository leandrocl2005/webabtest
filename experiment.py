from scipy.stats import beta
import numpy as np

from math import lgamma
from numba import jit

#defining the functions used
@jit
def h(a, b, c, d):
    num = lgamma(a + c) + lgamma(b + d) + lgamma(a + b) + lgamma(c + d)
    den = lgamma(a) + lgamma(b) + lgamma(c) + lgamma(d) + lgamma(a + b + c + d)
    return np.exp(num - den)

@jit
def g0(a, b, c):    
    return np.exp(lgamma(a + b) + lgamma(a + c) - (lgamma(a + b + c) + lgamma(a)))

@jit
def hiter(a, b, c, d):
    while d > 1:
        d -= 1
        yield h(a, b, c, d) / d

def g(a, b, c, d):
    return g0(a, b, c) + sum(hiter(a, b, c, d))

def calc_prob_between(beta1, beta2):
    return g(beta1.args[0], beta1.args[1], beta2.args[0], beta2.args[1])


class Experiment:

	def __init__(self, pA, pB, cA, cB):
		self.pA = pA
		self.pB = pB
		self.cA = cA
		self.cB = cB
		self.crA = cA/pA
		self.crB = cB/pA

	@property
	def beta_C(self):
		a_C = self.cA + 1
		b_C = self.pA - self.cA + 1
		return beta(a_C, b_C)

	@property
	def beta_T(self):
		a_T = self.cB + 1
		b_T = self.pB - self.cB + 1
		return beta(a_T, b_T)

	@property
	def lift(self):
		return (self.beta_T.mean()-self.beta_C.mean())/self.beta_C.mean()

	@property
	def prob(self):
		return calc_prob_between(self.beta_T, self.beta_C)
	

	def serialize(self):
		return {
			'rate A': "{:.0f}".format(100*self.crA),
			'rate B': "{:.0f}".format(100*self.crB),
			'lift': "{:.0f}".format(100*self.lift),
			'prob': int(round(100*self.prob,0))
		}