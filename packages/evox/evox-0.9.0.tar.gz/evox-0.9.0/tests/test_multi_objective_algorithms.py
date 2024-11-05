from evox import workflows, algorithms, problems, use_state
from evox.monitors import EvalMonitor
import pytest
import jax
import jax.numpy as jnp


N = 12
M = 3
POP_SIZE = 100
LB = 0
UB = 1
ITER = 10


def run_moea(algorithm, problem=problems.numerical.DTLZ1(m=M)):
    key = jax.random.PRNGKey(42)
    monitor = EvalMonitor()
    workflow = workflows.StdWorkflow(
        algorithm=algorithm,
        problem=problem,
        monitors=[monitor],
    )
    state = workflow.init(key)
    true_pf = problem.pf()

    for i in range(ITER):
        state = workflow.step(state)

    latest_solution, state = use_state(monitor.get_latest_solution)(state)


def test_ibea():
    algorithm = algorithms.IBEA(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_moead():
    algorithm = algorithms.MOEAD(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_nsga2():
    algorithm = algorithms.NSGA2(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_rvea():
    algorithm = algorithms.RVEA(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_nsga3():
    algorithm = algorithms.NSGA3(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_eagmoead():
    algorithm = algorithms.EAGMOEAD(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_hype():
    algorithm = algorithms.HypE(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_moeaddra():
    algorithm = algorithms.MOEADDRA(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_spea2():
    algorithm = algorithms.SPEA2(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_moeadm2m():
    algorithm = algorithms.MOEADM2M(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_knea():
    algorithm = algorithms.KnEA(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_bige():
    algorithm = algorithms.BiGE(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_gde3():
    algorithm = algorithms.GDE3(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_sra():
    algorithm = algorithms.SRA(
        lb=jnp.full(shape=(12,), fill_value=0),
        ub=jnp.full(shape=(12,), fill_value=1),
        n_objs=3,
        pop_size=100,
    )
    run_moea(algorithm)


def test_tdea():
    algorithm = algorithms.TDEA(
        lb=jnp.full(shape=(12,), fill_value=0),
        ub=jnp.full(shape=(12,), fill_value=1),
        n_objs=3,
        pop_size=100,
    )
    run_moea(algorithm)


def test_bce_ibea():
    algorithm = algorithms.BCEIBEA(
        lb=jnp.full(shape=(12,), fill_value=0),
        ub=jnp.full(shape=(12,), fill_value=1),
        n_objs=3,
        pop_size=100,
    )
    run_moea(algorithm)


def test_lmocso():
    algorithm = algorithms.LMOCSO(
        lb=jnp.full(shape=(12,), fill_value=0),
        ub=jnp.full(shape=(12,), fill_value=1),
        n_objs=3,
        pop_size=100,
    )
    run_moea(algorithm)


@pytest.mark.skip(reason="GPJax is unstable at the moment")
def test_im_moea():
    algorithm = algorithms.IMMOEA(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)


def test_rveaa():
    algorithm = algorithms.RVEAa(
        lb=jnp.full(shape=(N,), fill_value=LB),
        ub=jnp.full(shape=(N,), fill_value=UB),
        n_objs=M,
        pop_size=POP_SIZE,
    )
    run_moea(algorithm)
