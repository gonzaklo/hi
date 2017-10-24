import numpy as np
import random

n_simul = 100
n_bidders = 16
n_demand = 8
markup = 5
error = 5 # equal to markup?
cost_support_inf = 10
cost_support_sup = 100
grid_steps = 20


def bid_function(a, b, c):
	return a + b*c

def bid_calc(c, cap, a, b):
	bid = bid_function(a, b, c)
	if bid > cap:
		bid = cap
	if bid < c:
		bid = c
	return bid

def auction(a, b, a_next, b_next):
	bids = []
	i = 0
	while i < n_bidders:
		c = np.random.random_integers(cost_support_inf,cost_support_sup)
		c_hat = c + np.random.random_integers(-error,error)
		cap = c_hat + markup
		if i == 0:
			bid = bid_calc(c, cap, a_next, b_next)
			profit = bid - c
		else:
			bids.append(bid_calc(c, cap, a, b))
		i = i + 1
	i = 0
	k = 0
	for x in bids:
		if x < bid:
			i = i + 1
		if x == bid:
			k = k + 1
	if i >= n_demand:
		profit = 0
	else:
		if i + k > n_demand:
			profit = profit * float(n_demand - i)/k
	return profit

def optim(a, b):
	prev_profit = 0
	a_step = float(cost_support_sup - cost_support_inf)/grid_steps
	b_step = float (1)/grid_steps
	for aa in range(grid_steps):
		for bb in range(grid_steps):
			a_next = cost_support_inf + aa * a_step
			b_next = bb * b_step
			s_profit = 0
			for k in range(n_simul):
				s_profit = s_profit + auction(a, b, a_next, b_next)
			m_profit = float(s_profit)/n_simul
			if m_profit > prev_profit:
				prev_profit = m_profit
				a_optim = a_next
				b_optim = b_next
	return (a_optim, b_optim)

a = 0
b = 0
a_prev = 50
b_prev = 0.2
err = 100
while err > 1:
	a = a_prev
	b = b_prev
	(a_prev, b_prev) = optim(a, b)
	err = abs(a - a_prev) + abs(b - b_prev)
	print(err)

print (a, b)
