from concurrent.futures import ProcessPoolExecutor
import multiprocessing
import tiledb
import torchvision
from torch.utils.data import DataLoader
import torchvision.transforms as transforms
import numpy as np

def create_tiledb_schema(rows_count, tile_uri, np_tuple_type):

    # Create the dimension, inclusive of both end
    d1 = tiledb.Dim(domain=(0, rows_count - 1), tile=2, dtype=np.int32)

    # Create a domain using the two dimensions
    dom = tiledb.Domain(d1)

    # Create a dummy attr, required
    # np_tuple_type = ','.join('f4' for _ in range(0, cols_count))
    im_attr = tiledb.Attr(name="im", dtype=np.dtype(np_tuple_type))
    label_attr = tiledb.Attr(name="label", dtype=np.int8)

    # Create the array schema, setting `sparse=False` to indicate a dense array
    schema = tiledb.ArraySchema(domain=dom, attrs=[im_attr, label_attr])

    tiledb.DenseArray.create(tile_uri, schema, overwrite=True)

    # print('TileDB schema created')

def write_to_tldb(row_start, row_end, im_data, label_data, tile_uri):
    with tiledb.DenseArray(tile_uri, mode='w') as A:
        A[row_start:row_end] = {'im': im_data, 'label': label_data}
    
    # print(f'from:{row_start} to {row_end} is written')
    

def dump_to_db(root_dir, tile_uri):
    # pytorch params
    batch_size = 256
    max_workers = 8

    transform = transforms.Compose([transforms.ToTensor()])
    trainset = torchvision.datasets.CIFAR100(root=root_dir, train=True,
                                            download=True, transform=transform)

    image_len = 3*32*32
    np_tuple_type = ','.join('f4' for _ in range(0, 3 * 32* 32))

    create_tiledb_schema(rows_count=len(trainset), np_tuple_type=np_tuple_type, tile_uri=tile_uri)

    trainloader = DataLoader(trainset, batch_size=batch_size,
                                            shuffle=False, num_workers=max_workers)

    # Setting start method to 'spawn' is required to
    # avoid problems with process global state when spawning via fork.
    # NOTE: *must be inside __main__* or a function.
    if multiprocessing.get_start_method(True) != "spawn":
        multiprocessing.set_start_method("spawn", True)

    i = 0
    tasks = []
    

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        for batch_idx, (images, labels) in enumerate(trainloader):
            size = len(labels)
            # labels = labels.reshape(size, 1)
            images = images.reshape(size, 3*32*32)

            im_data = images.numpy(force=False)
            im_data = np.array([tuple(row) for row in im_data], dtype=np_tuple_type)

            label_data = labels.numpy(force=False)

            # print(f'batch_idx:{batch_idx} is converted')

            task = executor.submit(write_to_tldb, *(i, i + size, im_data, label_data, tile_uri))

            tasks.append(task)

            # next
            i += size

    # print("Task results: ", [t.result() for t in tasks])