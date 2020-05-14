from PIL import Image
import numpy as np
import datum_pb2
import lmdb
import os
import cv2
import os

def array_to_datum(arr, label=None):
    assert arr.ndim == 3
    assert arr.dtype == np.uint8
    # assert label is not None

    datum = datum_pb2.Datum()
    datum.width, datum.height, datum.channels = arr.shape
    datum.data = arr.tostring()
    # datum.label = label
    return datum


def preprocess(img):
    # TODO put your code here
    return np.asarray(img, dtype=np.uint8)


def save_to_lmdb(save_path, imgs_dir, img_paths):
    """
    :param save_path: lmdb path(dir, not file)
    :param imgs: img path and label list
    """
    db = lmdb.open(save_path, map_size=1024**4)
    # db = lmdb.open(save_path)
    # db = lmdb.open(save_path)
    # txn = db.begin(write=True)

    count = 0
    for idx, img_path in enumerate(img_paths):
        # TODO put your code here
        # split = img_path.split()
        # assert len(split) == 2
        # label = int(split[1])
        img_id = idx
        # img = Image.open(img_path).convert('RGB')
        # img = preprocess(img)
        img = cv2.imread(img_path.replace('\n', ''))
        datum_img = array_to_datum(img)
        with db.begin(write=True) as txn:
            txn.put('{:0>8d}'.format(img_id).encode(), datum_img.SerializeToString())
            # txn.put('{}'.format(img_id).encode(), datum_img.SerializeToString())
            # key = str(img_id).encode()
            # image_array = np.ascontiguousarray(img, dtype=np.uint8)
            # txn.put(key, image_array)
            count += 1
            # txn.commit()
        if count % 1000 == 0:
            print('processed %d images' % count)
            # break

    # print('num_samples: ', count)
    # txn.put('num_samples'.encode(), str(count).encode())

    db.close()

def datum_to_array(datum):
    return np.fromstring(datum.data, dtype=np.uint8).reshape(datum.width, datum.height, datum.channels)


def test_get(lmdb_path):
    db = lmdb.open(lmdb_path, readonly=True)
    datum = datum_pb2.Datum()
    res = []

    with db.begin() as lmdb_txn:
        for i in range(100):
            value = lmdb_txn.get('{:0>8d}'.format(i).encode())
            datum.ParseFromString(value)
            img = datum_to_array(datum)
            res.append(img)
    # print(np.array(res).shape)

def save_shelve(save_path_dir, img_paths):
    os.makedirs(save_path_dir, exist_ok=True)
    import shelve
    for idx, img_path in enumerate(img_paths):
        img = cv2.imread(os.path.join(img_path.replace('\n', '')))
        with shelve.open(os.path.join(save_path_dir, str(idx))) as fs:
            fs['res'] = img
        if idx % 1000==0:
            print(idx)
if __name__ == '__main__':
    import json
    # split = 'train'
    split = 'test'
    img_dir = '/data/det/out/yoloDiDi/images/{}'.format(split)
    save_path = '/data/det/out/yoloDiDi/img73184_lmdb_{}'.format(split)
    save_shelve_path = '/data/det/out/yoloDiDi/img73184_shelve_{}'.format(split)
    print(save_path)
    with open('/data/det/out/yoloDiDi/{}.txt'.format(split), 'r', encoding='utf-8') as f:
        lines = f.readlines()

    save_to_lmdb(save_path, img_dir, lines)
    # save_shelve(save_shelve_path, lines)
    # test_get(save_path)