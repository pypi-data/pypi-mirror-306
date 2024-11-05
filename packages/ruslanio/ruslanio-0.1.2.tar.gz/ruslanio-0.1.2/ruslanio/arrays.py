import typing as tp

import numpy as np


def flatten_list(l: tp.Any, times: int = -1):
    # Check exit conditions
    if times == 0:
        return l
    if not isinstance(l, list):
        if times >= 0:
            raise ValueError(f'{type(l)} is not list')
        else:
            return l

    # Flatten recursively
    new_l = []
    for sub_l in l:
        for item in sub_l:
            new_l.append(flatten_list(item, times - 1))
    return new_l


class GenWithLen:
    def __init__(self, gen: tp.Iterable, length: int):
        self.gen = gen
        self.length = length

    def __iter__(self):
        for item in self.gen:
            yield item
    
    def __len__(self):
        return self.length
    
    def len(self):
        return self.length


def help_convolve_sliceable(source: tp.Iterable, kernel: int = 2, stride: int = 1):
    '''
    Generator function to perform a convolution-like operation on a sliceable input iterable.

    Parameters:
    - source (iterable): The input iterable to be processed (sliceable).
    - kernel (int, optional): The size of the sublists to yield (default is 2).
    - stride (int, optional): The step size when moving through the iterable (default is 1).
    
    Yields:
    - Slices: Slices of elements from the source iterable.

    This function takes a sliceable iterable, slices it into sublists of a specified size (kernel)
    with a specified step size (stride) while ensuring that stride is less than or equal to the kernel.
    '''
    assert kernel > 0
    assert stride > 0

    def _interator():
        # Start iterating over the source using slices
        for start in range(0, len(source) - kernel + stride, stride):
            end = start + kernel

            # Ensure that the end index does not exceed the length of the source
            end = min(end, len(source))

            # Yield the current slice
            yield source[start:end]
    
    return GenWithLen(_interator(), (len(source) - kernel + stride) // stride)


def help_convolve(source: tp.Iterable, kernel: int = 2, stride: int = 1):
    '''
    Generator function to perform a convolution-like operation on an input iterable.

    Parameters:
    - source (iterable): The input iterable to be processed.
    - kernel (int, optional): The size of the sublists to yield (default is 2).
    - stride (int, optional): The step size when moving through the iterable (default is 1).
    
    Yields:
    - List: Sublists of elements from the source iterable.

    This function takes an iterable, reads elements from it, and yields sublists of a specified
    size (kernel) with a specified step size (stride) while ensuring that stride is less than
    or equal to the kernel.
    '''

    # Check if stride is less than or equal to the kernel
    assert stride <= kernel
    assert kernel > 0
    assert stride > 0

    # Initialize an empty list to store elements from the source
    current = []

    # Create a generator from the source iterable
    gen = (item for item in source)

    # Infinite loop until a StopIteration exception is raised
    while True:
        try:
            # Get the next item from the generator
            item = next(gen)
        except StopIteration:
            # Break the loop when there are no more items in the generator
            break
        
        # Append the item to the current list
        current.append(item)

        # Check if the current list has reached the specified kernel size
        if len(current) == kernel:
            # Yield the current sublist as a result
            yield current

            # Update `current` to contain the last `kernel - stride` elements
            current = current[stride:]

    # If there are remaining elements in current (fewer than kernel elements), yield them
    # current = current[stride:]
    if len(current) > 0:
        yield current
