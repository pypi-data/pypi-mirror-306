import numpy as np
from typing import Iterable, Set


def multiple_union(set_list: Iterable[Set]):
    final_set = set()
    for cur_set in set_list:
        final_set = final_set.union(cur_set)
    return final_set


def invert_non_zeros(array):
    out = np.array(array, dtype=float)
    non_zero_mask = array != 0
    out[non_zero_mask] = 1. / out[non_zero_mask]
    return out
