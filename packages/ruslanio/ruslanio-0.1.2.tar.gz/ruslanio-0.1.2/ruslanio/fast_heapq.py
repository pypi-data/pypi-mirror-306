'''
Functions copied from python heapq, but decorated with numba.njit.
Also added arg- versions of these functions, to use in argtopk
'''

import numpy as np
import numba as nb


@nb.jit(nopython=True)
def _siftdown(heap, startpos, pos):
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if newitem < parent:
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem


@nb.jit(nopython=True)
def _siftup(heap, pos):
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    # Bubble up the smaller child until hitting a leaf.
    childpos = 2*pos + 1    # leftmost child position
    while childpos < endpos:
        # Set childpos to index of smaller child.
        rightpos = childpos + 1
        if rightpos < endpos and not heap[childpos] < heap[rightpos]:
            childpos = rightpos
        # Move the smaller child up.
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2*pos + 1
    # The leaf at pos is empty now.  Put newitem there, and bubble it up
    # to its final resting place (by sifting its parents down).
    heap[pos] = newitem
    _siftdown(heap, startpos, pos)


@nb.jit(nopython=True)
def heappush(heap, item):
    """Push item onto heap, maintaining the heap invariant."""
    heap.append(item)
    _siftdown(heap, 0, len(heap)-1)


@nb.jit(nopython=True)
def heappop(heap):
    """Pop the smallest item off the heap, maintaining the heap invariant."""
    lastelt = heap.pop()    # raises appropriate IndexError if heap is empty
    if heap:
        returnitem = heap[0]
        heap[0] = lastelt
        _siftup(heap, 0)
        return returnitem
    return lastelt


@nb.jit(nopython=True)
def heapreplace(heap, item):
    """Pop and return the current smallest value, and add the new item.

    This is more efficient than heappop() followed by heappush(), and can be
    more appropriate when using a fixed-size heap.  Note that the value
    returned may be larger than item!  That constrains reasonable uses of
    this routine unless written as part of a conditional replacement:

        if item > heap[0]:
            item = heapreplace(heap, item)
    """
    returnitem = heap[0]    # raises appropriate IndexError if heap is empty
    heap[0] = item
    _siftup(heap, 0)
    return returnitem


@nb.jit(nopython=True)
def heappushpop(heap, item):
    """Fast version of a heappush followed by a heappop."""
    if heap[0] < item:
        item, heap[0] = heap[0], item
        _siftup(heap, 0)
    return item


@nb.jit(nopython=True)
def heapify(x):
    """Transform list into a heap, in-place, in O(len(x)) time."""
    n = len(x)
    # Transform bottom-up.  The largest index there's any point to looking at
    # is the largest with a child index in-range, so must have 2*i + 1 < n,
    # or i < (n-1)/2.  If n is even = 2*j, this is (2*j-1)/2 = j-1/2 so
    # j-1 is the largest, which is n//2 - 1.  If n is odd = 2*j+1, this is
    # (2*j+1-1)/2 = j so j-1 is the largest, and that's again n//2-1.
    for i in range(n // 2 - 1, -1, -1):
        _siftup(x, i)


@nb.jit(nopython=True)
def _argsiftdown(argheap, values, startpos, pos):
    newitem = argheap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = argheap[parentpos]
        if values[newitem] < values[parent]:
            argheap[pos] = parent
            pos = parentpos
            continue
        break
    argheap[pos] = newitem


@nb.jit(nopython=True)
def _argsiftup(argheap, values, pos):
    endpos = len(argheap)
    startpos = pos
    newitem = argheap[pos]
    # Bubble up the smaller child until hitting a leaf.
    childpos = 2*pos + 1    # leftmost child position
    while childpos < endpos:
        # Set childpos to index of smaller child.
        rightpos = childpos + 1
        if rightpos < endpos and not values[argheap[childpos]] < values[argheap[rightpos]]:
            childpos = rightpos
        # Move the smaller child up.
        argheap[pos] = argheap[childpos]
        pos = childpos
        childpos = 2*pos + 1
    # The leaf at pos is empty now.  Put newitem there, and bubble it up
    # to its final resting place (by sifting its parents down).
    argheap[pos] = newitem
    _argsiftdown(argheap, values, startpos, pos)


@nb.jit(nopython=True)
def argheappush(argheap, values, item):
    """Push item onto heap, maintaining the heap invariant."""
    argheap.append(item)
    _argsiftdown(argheap, values, 0, len(argheap) - 1)


@nb.jit(nopython=True)
def argheappop(argheap, values):
    """Pop the smallest item off the heap, maintaining the heap invariant."""
    lastelt = argheap.pop()    # raises appropriate IndexError if heap is empty
    if argheap:
        returnitem = argheap[0]
        argheap[0] = lastelt
        _argsiftup(argheap, values, 0)
        return returnitem
    return lastelt


@nb.jit(nopython=True)
def argheapreplace(argheap, values, item):
    """Pop and return the current smallest value, and add the new item.

    This is more efficient than heappop() followed by heappush(), and can be
    more appropriate when using a fixed-size heap.  Note that the value
    returned may be larger than item!  That constrains reasonable uses of
    this routine unless written as part of a conditional replacement:

        if item > heap[0]:
            item = heapreplace(heap, item)
    """
    returnitem = argheap[0]    # raises appropriate IndexError if heap is empty
    argheap[0] = item
    _argsiftup(argheap, values, 0)
    return returnitem


@nb.jit(nopython=True)
def argheappushpop(argheap, values, item):
    """Fast version of a heappush followed by a heappop."""
    if values[argheap[0]] < values[item]:
        item, argheap[0] = argheap[0], item
        _argsiftup(argheap, values, 0)
    return item


@nb.jit(nopython=True)
def argheapify(x):
    """Transform list into a heap, in-place, in O(len(x)) time."""
    n = len(x)
    # Transform bottom-up.  The largest index there's any point to looking at
    # is the largest with a child index in-range, so must have 2*i + 1 < n,
    # or i < (n-1)/2.  If n is even = 2*j, this is (2*j-1)/2 = j-1/2 so
    # j-1 is the largest, which is n//2 - 1.  If n is odd = 2*j+1, this is
    # (2*j+1-1)/2 = j so j-1 is the largest, and that's again n//2-1.
    indices = np.arange(len(x))
    for i in range(n // 2 - 1, -1, -1):
        _argsiftup(indices, x, i)
    return indices
