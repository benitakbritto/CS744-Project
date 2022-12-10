'''
    @brief: TODO: Add better desc
    @prereq: bash
    @usage: 
    @authors: Benita, Hemal, Reetuparna
'''

from torch.utils.data import DataLoader, Dataset
import torch
import pandas as pd
import time 
import argparse
from torchvision import transforms

# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("-num-workers",
    help="Number of workers",
    default=0,
    required=False)
parser.add_argument("-batch-size",
    help="Batch size for the dataloader",
    default=256,
    required=False)
parser.add_argument("-input-path",
    help="Path for input data",
    required=True)

class BaselineGraphDataset(Dataset):
    def __init__(self, input_file):
        triples = list()
        with open(input_file, 'r') as f:
            for line in f:
                head, relation, tail = line.strip().split('\t')
                triples.append((head, relation, tail))
        self.dataset = triples

    def __getitem__(self, index):
        return self.dataset[index]
    
    def __len__(self):
        return len(self.dataset)

    @staticmethod
    def collate_fn(data):
        # Important, pass through collate to obtain data in triplet form
        return data


if __name__=='__main__':
    # Example: python baseline_map.py -batch-size 1024 -num-workers 8 -input-path /mnt/data/dataset/fb15k-237/train.txt 

    # Read arguments from command line
    args = parser.parse_args()

    start = time.time()

    dataset = BaselineGraphDataset(args.input_path)

    dataloader = DataLoader(
                    dataset,
                    batch_size = int(args.batch_size), 
                    shuffle=False,
                    collate_fn=BaselineGraphDataset.collate_fn,
                    num_workers=int(args.num_workers))
 
    for _, batch in enumerate(dataloader):
        pass

    
    end = time.time()
    print(f'time to load = {end - start}s')

