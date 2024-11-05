import pytest
import numpy as np

from ruslanio.sorting import topk, argtopk


def topk_np_simple(seq, k):
    return np.sort(seq)[-k:][::-1]

def argtopk_np_simple(seq, k):
    return np.argsort(seq)[-k:][::-1]


Ns = [1, 10, 100, 1000]
ks = [1, 2, 3, 10, 20, 30]

test_data = [
    (np.random.random(N), k)
    for k in ks
    for N in Ns
]

@pytest.mark.parametrize("seq,k", test_data)
def test_topk(seq, k):
    ref = topk_np_simple(seq, k)
    res = topk(seq, k)
    assert (ref == res).all()


@pytest.mark.parametrize("seq,k", test_data)
def test_argtopk(seq, k):
    ref = argtopk_np_simple(seq, k)
    res = argtopk(seq, k)
    assert (seq[ref] == seq[res]).all()
