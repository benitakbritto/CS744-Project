'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: python <filename>
    @authors: Benita, Hemal, Reetuparna
'''

import tensorstore as ts
import tensor_store.constants as constants

class TensorStoreImageIterator():
    
    def __init__(self, cache_len, start, end):
        
        self.db = ts.open({
            'driver': 'n5',
            'kvstore': {
                'driver': 'file',
                'path': constants.PATH_TO_KV_STORE ,
            }
        }).result()

        # cache stores
        self.image = []

        self.curr_idx = start
        self.end_idx = end
        # idx after which we need to fetch from DB
        self.last_exclusive_idx = start - 1
        
        # items to fetch in one shot, don't overfetch
        # import pdb; pdb.set_trace()
        self.cache_len = min(cache_len, end - start + 1)


    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_idx >= self.end_idx:
            # print('raising ex:', self.curr_idx)
            raise StopIteration

        # pre-fetch
        elif self.curr_idx >= self.last_exclusive_idx:
            # print('fetching:', self.curr_idx)
            
            # find last index to fetch(exclusive)
            self.last_exclusive_idx = min(self.curr_idx + self.cache_len, self.end_idx)

            # bulk fetch
            data = self.db[self.curr_idx : self.last_exclusive_idx, : ].read().result()
            # cache store
            self.image = data
                
        # find the relative index within cache data
        relative_idx = self.curr_idx % len(self.image)
        
        # advance to next index
        self.curr_idx = self.curr_idx + 1

        return self.image[relative_idx]