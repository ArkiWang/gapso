
from numba import njit, jit
from time import time
from multiprocessing import pool, Pool


def test1() -> None:
    a = [i for i in range(1000)]
    for i in range(1000):
        for j in range(len(a)):
          a[j]*=2
#@jit(nopython = True)
@njit
def test2() -> None:
    a = [i for i in range(1000)]
    for i in range(1000):
        for j in range(len(a)):
          a[j]*=2


def test3():
    a = [i for i in range(1000)]
    with Pool(4) as p:
        for i in range(1000):
            for j in range(len(a)):
                a[j] *= 2


start = time()
test1()
end = time()
print(end - start)
start = time()
test2()
end = time()
print(end - start)
start = time()
test3()
end = time()
print(end - start)