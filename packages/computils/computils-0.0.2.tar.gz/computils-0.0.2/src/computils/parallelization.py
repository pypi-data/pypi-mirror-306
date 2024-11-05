""" This module contains functionality for parallelization. """

from math import floor
from psutil import cpu_count
from typing import List


class BatchAllocation:
    def __init__(self,
                 batch_id: int,
                 n_cores: int,
                 indices: List[int]):
        """ Initializes a BatchAllocation object.

        :param batch_id: unique number to identify batch.
        :param n_cores: >= 1, number of physical cores allocated to this batch.
        :param indices: contains the indices of the elements allocated to this batch.
        """

        self.batch_id: int = batch_id  #: id number to identify a batch
        self.n_cores: int = n_cores  #: the number of cores allocated to the batch
        self.indices: List[int] = indices  #: the indices allocated to the batch.

    def batch_size(self) -> int:
        """ Returns the number of indices allocated to the batch.

        :return: the number of indices allocated to the batch.
        """
        return len(self.indices)


def get_batch_allocations(n_elements: int,
                          n_cores: int = None) -> List[BatchAllocation]:
    """ Returns an allocation of elements over batches such that the maximum number of elements per core is minimized.

    :param n_elements: the number of elements to be allocated over the cores.
    :param n_cores: optional, number of physical cores to be used for the batch allocations. If None, all physical
        cores are used.
    :return: a list with batch allocations.
    """

    if n_cores is None:
        n_cores = get_n_physical_cores()

    n_batches = min(n_elements, n_cores)
    indices = list(range(n_elements))

    lower_bound_cores_per_batch = floor(n_cores / n_batches)
    lower_bound_elements_per_batch = floor(n_elements / n_batches)
    batch_allocations = []
    for i in range(n_batches):
        indices_for_batch = [indices.pop() for j in range(lower_bound_elements_per_batch)]
        allocation = BatchAllocation(batch_id=i, n_cores=lower_bound_cores_per_batch,
                                     indices=indices_for_batch)
        batch_allocations.append(allocation)

    n_remaining_cores = n_cores - n_batches * lower_bound_cores_per_batch
    while n_remaining_cores > 0:
        batch_index = n_batches - n_remaining_cores
        batch_allocations[batch_index].n_cores += 1
        n_remaining_cores -= 1

    while len(indices) > 0:
        batch_index = n_batches - len(indices)
        batch_allocations[batch_index].indices.append(indices.pop())

    return batch_allocations


def get_n_physical_cores() -> int:
    """ Returns the number of physical cores on your machine.

    :return: the number of physical cores on your machine.
    """
    return cpu_count(logical=False)
