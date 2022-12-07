import argparse
from pathlib import Path
from tile_db.TileDBIterableDataset import TileDBIterableDataset
from tile_db.TileDBMapDataset import TileDBMapDataset
import time
from torch.utils.data import DataLoader
import tile_db.dump_fast as tile_db_dump
from tile_db.helper import get_dataset_count
from rocksDB.store import RocksDBStore
from rocksDB.map_style_data_loader import RocksDBMapStyleDataset
from rocksDB.iterable_style_data_loader import RocksDBIterableDataset

# Initialize parser
parser = argparse.ArgumentParser()

# Adding  argument
parser.add_argument("-ds", 
    help = "Backend Data Store. rd for RocksDB, ts for TensorStore, td for TileDB", 
    choices=['rd', 'ts', 'td'],
    required=True)
parser.add_argument("-pf",
    help="Number of items to prefetch within dataset",
    default=1,
    required=False)
parser.add_argument("-input-file",
    help="Path to the input file stored in the filesystem",
    required=True)
parser.add_argument("-input-rows-per-key",
    default=1,
    help="Storing a batch of input rows under a single key",
    required=False)
parser.add_argument("-type", 
    help = "Type of dataloader. m for map style and i for iterable style.", 
    choices=['m', 'i'],
    required=True)
parser.add_argument("-num-workers",
    help="Number of workers",
    default=0,
    required=False)
parser.add_argument("-batch-size",
    help="Batch size for the dataloader",
    default=256,
    required=False)

# Read arguments from command line
args = parser.parse_args()

dataset = None
dataloader = None

start = None
end = None

if args.ds == 'rd':
    # Store data in rocks db
    start = time.time()

    store = RocksDBStore(args.input_file, int(args.input_rows_per_key))
    store.store_data()
    store.store_metadata()
    
    end = time.time()

    total_rows = store.get_total_input_rows()
    store.cleanup()

    # Set Dataloader
    # Example: python main.py -ds rd -input-file /mnt/data/dataset/fb15k-237/train.txt -input-rows-per-key 256 -type m -batch-size 256 
    if args.type == 'm':
        dataset = RocksDBMapStyleDataset()
        dataloader = DataLoader(
            dataset,
            batch_size=int(args.batch_size),
            shuffle=False, 
            num_workers=int(args.num_workers)
        )
    # Example: python main.py -ds rd -input-file /mnt/data/dataset/fb15k-237/train.txt -type i -pf 256
    elif args.type == 'i':
        dataset = RocksDBIterableDataset(cache_len=int(args.pf), start=0, end=int(total_rows))
        dataloader = DataLoader(dataset=dataset, num_workers=0)
elif args.ds == 'td':
    # dump to db
    root_dir = str(Path(args.input_file).parent)

    # switch to input file name from args
    dataset_uri = args.input_file
    tile_uri = root_dir + "fb15k-237.tldb"

    start = time.time()
    tile_db_dump.dump_to_db(tile_uri=tile_uri, dataset_uri=dataset_uri)
    end = time.time()

    print(f'{args.ds} Store time = {end - start} s')

    # prepare dataset and dataloader
    if args.type == 'm':
        dataset = TileDBIterableDataset(cache_len=int(args.pf), start=0, end=get_dataset_count(tile_uri=tile_uri), tile_uri=tile_uri)
    elif args.type == 'i':
        dataset = TileDBMapDataset(size=get_dataset_count(), tile_uri=tile_uri)

    dataloader = DataLoader(dataset=dataset, batch_size=int(args.batch_size))
else:
    raise NotImplementedError("Not implemented")


print(f'{args.ds} Write = {end - start} s')

# Call dataloader
start = time.time()

for batch_idx, data in enumerate(dataloader):
    i = batch_idx

end = time.time()
print(f'{args.ds} Dataloader time = {end - start} s')