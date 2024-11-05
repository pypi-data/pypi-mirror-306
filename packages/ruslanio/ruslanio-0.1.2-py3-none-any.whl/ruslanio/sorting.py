import numpy as np
import numba as nb

from .fast_heapq import heapify, heappushpop
from .fast_heapq import argheapify, argheappushpop


@nb.jit(nopython=True)
def topk(seq: np.ndarray, k=10):
    '''
    Returns top-k values of the input array.
    Complexity is O(N * log(k)), where N = len(seq).
    Works only with numpy arrays.

    First time calling this function will be slow because it will compile.

    Equivalent to `np.sort(seq)[-k:][::-1]` or `heapq.nlargest(k, seq)`.
    First option is slow because its complexity is O(N * log(N)).
    Second option is slow because it is pure python.
    This function is fast because it is compiled using numba.jit.
    '''
    topheap = seq[:k].copy()
    heapify(topheap)

    for i in range(k, len(seq)):
        heappushpop(topheap, seq[i])

    return np.sort(topheap)[::-1]


@nb.jit(nopython=True)
def argtopk(seq: np.ndarray, k=10):
    '''
    Works like `ruslanio.sorting.topk`, but returns indeces instead of values.

    Equivalent to `np.argsort(seq)[-k:][::-1]`
    '''
    topheap = argheapify(seq[:k])

    for i in range(k, len(seq)):
        argheappushpop(topheap, seq, i)

    return topheap[np.argsort(seq[topheap])[::-1]]
