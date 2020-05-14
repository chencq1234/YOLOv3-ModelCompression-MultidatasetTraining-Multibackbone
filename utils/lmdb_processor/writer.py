from PIL import Image
import numpy as np
import datum_pb2
import lmdb
import os
import cv2

def array_to_datum(arr, label):
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


def save_to_lmdb(save_path, imgs_dir, imgs_info):
    """
    :param save_path: lmdb path(dir, not file)
    :param imgs: img path and label list
    """
    db = lmdb.open(save_path, map_size=1024 ** 4)
    txn = db.begin(write=True)

    count = 0
    for img_info in imgs_info:
        # TODO put your code here
        # split = img_path.split()
        # assert len(split) == 2
        img_path = os.path.join(imgs_dir, img_info['file_name'])
        # label = int(split[1])
        img_id = img_info['id']
        # img = Image.open(img_path).convert('RGB')
        # img = preprocess(img)
        img = cv2.imread(img_path)
        datum_img = array_to_datum(img, label=None)
        txn.put('{:0>8d}'.format(img_id).encode(), datum_img.SerializeToString())

        count += 1
        if count % 1000 == 0:
            print('processed %d images' % count)

    # print('num_samples: ', count)
    # txn.put('num_samples'.encode(), str(count).encode())
    txn.commit()
    db.close()


if __name__ == '__main__':
    import json
    split = 'train'
    # split = 'test'
    img_dir = '/data-private/nas/my_data/car/COCO69863BDDcar/coco/images/{}'.format(split)
    save_path = '/data-private/nas/my_data/car/COCO69863BDDcar/img_lmdb_{}'.format(split)
    print(save_path)
    with open('/data-private/nas/my_data/car/COCO69863BDDcar/coco/annotations/car_instances_{}.json'.format(split), 'r',
              encoding='utf-8') as f:
        coco_data_dict = json.loads(f.read())

    save_to_lmdb(save_path, img_dir, coco_data_dict['images'])
