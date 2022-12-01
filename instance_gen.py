import random
from collections import defaultdict
from converters import *

def gen_resources(amount):
    # generate a random bundle of resources with the chosen value `amount`
    resources = defaultdict(int)
    res_count = {'O':1, 'U':2, 'B':2, 'Y':2, 'G':3, 'W':3, 'R':3}
    for i in range(amount):
        resource = random.choice('OURBGYW')
        resources[resource] += res_count[resource]
    return resources

def gen_converters(n_t1, n_t2, n_t3):
    #sample some number of converters of each tier level
    return sorted(random.sample(t1_converters,n_t1) + random.sample(t2_converters,n_t2) + random.sample(t3_converters,n_t3))
