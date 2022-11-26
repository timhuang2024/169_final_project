#this module contains various approximate integer LP solvers.
import numpy as np
import cvxpy as cp


def cvxpy_solve(instance):
    R, A, b = instance
    x = cp.Variable(len(R), integer = True)
    objective = cp.Maximize(x * R)
    constraint = A@x <= b
    problem = cp.Problem(objective, [constraint, 0 <= x])

    problem.solve()

    return x.value


if __name__ == '__main__':
    import instance_gen
    import singleplayer_lp
    convs = instance_gen.gen_converters(7,7,7)
    ress = instance_gen.gen_resources(10)

    inst = singleplayer_lp.gen_instance(convs,ress)
    

    solution = cvxpy_solve(inst)
    print(ress)
    print(solution)
    for i,x in enumerate(solution):
        if x:
            print("Used:", convs[i])
    print("Score:",np.dot(solution, inst[0]))