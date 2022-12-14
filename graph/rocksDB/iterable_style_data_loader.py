'''
    @brief: Iterable style Data loader
    @prereq: bash
    @usage: from main.py
    @authors: Benita, Hemal, Reetuparna
'''

import math
from time import sleep
from rocksDB.rocksdb_iterator import RocksDBIterator
from torch.utils.data import IterableDataset, DataLoader, get_worker_info

class RocksDBIterableDataset(IterableDataset):
    def __init__(self, start, end, cache_len):
        # assert end > start, "this example code only works with end > start"
        self.start = start
        self.end = end
        self.cache_len = cache_len

    def __iter__(self):
        worker_info = get_worker_info()
        if worker_info is None:  # single-process data loading, return the full iterator
            iter_start = self.start
            iter_end = self.end
        else:  # in a worker process
            # split workload
            per_worker = int(math.ceil((self.end - self.start) / float(worker_info.num_workers)))
            worker_id = worker_info.id
            iter_start = self.start + worker_id * per_worker
            iter_end = min(iter_start + per_worker, self.end)
        return RocksDBIterator(cache_len=self.cache_len, start = iter_start, end = iter_end)

