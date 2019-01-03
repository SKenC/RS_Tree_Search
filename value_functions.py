import math

def ucb(n_ij, n_i, q):
    return (q / float(n_ij)) + math.sqrt((2.*math.log(n_i))/n_ij)

def rs(n_ij, q, r):
    return n_ij * ((q/n_ij) - r)