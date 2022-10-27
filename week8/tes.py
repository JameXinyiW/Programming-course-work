import functools
from memory_profiler import  profile
import time

def count():
    def f(j):
       def g():
            return j
       return g

    fs = []
    for i in range(1,4):
        fs.append(f(i))
    return fs

f1,f2,f3 = count()

