'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

from torch.utils.data import DataLoader, IterableDataset, get_worker_info
import math
from tensor_store.TensorStoreImageIterator import TensorStoreImageIterator

class TensorStoreIterableDataset(IterableDataset):

    def __init__(self, db, start, end, cache_len):
        # assert end > start, "this example code only works with end > start"
        self.db = db
        self.start = start
        self.end = end
        self.cache_len = cache_len

    def __iter__(self):
        worker_info = get_worker_info()
        if worker_info is None:  # single-process data loading, return the full iterator
            iter_start = self.start
            iter_end = self.end
        else:  
            # in a worker process
            # split workload
            per_worker = int(math.ceil((self.end - self.start) / float(worker_info.num_workers)))
            worker_id = worker_info.id
            iter_start = self.start + worker_id * per_worker
            iter_end = min(iter_start + per_worker, self.end)
        
        return TensorStoreImageIterator(db = self.db, cache_len = self.cache_len, start = iter_start, end = iter_end)