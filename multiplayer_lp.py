import numpy as np
import converters
import solve_lp
import singleplayer_lp

def singleplayer_opt(player):
    inst = singleplayer_lp.gen_instance(*player)
    soln = solve_lp.cvxpy_solve(inst)
    return np.dot(soln, inst[0])

# list of tuples: (Convs_p1, Resources_p1)
# output: variable labels:
def gen_instance(players):
    #TODO MAKE THIS AN IPYNB???
    # variables:
    # u_{p,m}: usage by player p of machine m
    # t_{p1, p2, r}: trade from player p1 to player p2 of resource r
    # t_{p1, p2, m}: trade from player p1 to player p2 of machine m

    # objective:
    # \sum_{p,m} u_{p,m} * v_m
    # constraints:
    # (1): \sum_m u{p,m} * i_{r,m} - \sum_{p2} t_{p2, p1, r} <= s_{p1, r}
    #     (no player overspends their resources)
    # (2): u_{p,m} - \sum_{p2} t_{p2, p1, m} <= s_{p1, m}
    #     (no player overuses their machines)
    # (3): \sum_m u_{p,m}*v_m >= indv_p (best individual score for that player)
    #     (each player gains something from having traded - TODO strengthen?)
    # (4): u_{p,m} >= 0
    #     (players use machines a positive number of times.)

    Np = len(players)
    machines = sorted(set(sum([i[0] for i in players],[])))

    variables = [(P, m) for m in machines for P in range(Np)] + \
        [(P1, P2, r) for r in converters.resource_types for P1 in range(Np) for P2 in range(P1+1,Np)] + \
        [(P1, P2, m) for m in machines for P1 in range(Np) for P2 in range(P1+1,Np)]

    objective = [v[1].output if len(v) == 2 else 0 for v in variables]

    constraint1 = [
        [v[1].inputs.count(r) if len(v) == 2 and v[0] == p else -1 if len(v) == 3 and v[1] == p and v[2] == r else 1 if len(v) == 3 and v[0] == p and v[2] == r else 0 for v in variables] 
        for r in converters.resource_types for p in range(Np)]
    
    limit1 = [players[p][1][r] for r in converters.resource_types for p in range(Np)]

    constraint2 = [[1 if v[0] == p and v[1] == m else -1 if len(v) == 3 and v[1] == p and v[2] == m else 1 if len(v) == 3 and v[0] == p and v[2] == m else 0 for v in variables] for m in machines for p in range(Np)]

    limit2 = [int(m in players[p][0]) for m in machines for p in range(Np)]

    constraint3 = [[-v[1].output if len(v) == 2 and v[0] == p else 0 for v in variables] for p in range(Np)]

    limit3 = [-singleplayer_opt(p) for p in players]

    constraint4 = [[-1 if v == v0 else 0 for v in variables] for v0 in variables if len(v0) == 2]

    limit4 = [0 for v0 in variables if len(v0) == 2]

    return (variables, (np.array(objective), 
            np.matrix(constraint1 + constraint2 + constraint3 + constraint4), 
            np.array(limit1 + limit2 + limit3 + limit4)))

if __name__ == '__main__':
    import instance_gen
    convs = sorted(set(instance_gen.gen_converters(7,7,7)))
    r_p1 = instance_gen.gen_resources(10)
    r_p2 = instance_gen.gen_resources(10)
    (vars,inst) = gen_instance([(convs,r_p1), (convs,r_p2)])



    p1s= solve_lp.cvxpy_solve(singleplayer_lp.gen_instance(convs,r_p1))
    p2s = solve_lp.cvxpy_solve(singleplayer_lp.gen_instance(convs,r_p2))

    soln = solve_lp.cvxpy_solve(inst)

    print(soln)

    print(p1s, p2s)
    
    print("p1 before: ", singleplayer_opt((convs,r_p1)))
    for i,x in enumerate(p1s):
        if x:
            print("Used:", convs[i],x)
    print("p2 before: ", singleplayer_opt((convs,r_p2)))
    for i,x in enumerate(p2s):
        if x:
            print("Used:", convs[i],x)

    scores = [0,0]
    for x,v in zip(soln,vars):
        if len(v) == 2 and x > 0:
            print(v, x)
            scores[v[0]] += v[1].output*x
    
    print(scores, sum(scores))
    

