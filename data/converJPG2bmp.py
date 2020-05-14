import cv2
import os
import shutil
from pathlib import Path
from tqdm import tqdm
import glob

def convert_images2bmp():
    anno_path = '/data/det/out/Annotations'
    # cv2.imread() jpg at 230 img/s, *.bmp at 400 img/s
    for path in ['/data/det/out/images/']:
        folder = os.sep + Path(path).name
        output = path.replace(folder, folder + 'bmp')
        #if os.path.exists(output):
        #    shutil.rmtree(output)  # delete output folder
        #os.makedirs(output, exists_ok=True)  # make new output folder

        for f in tqdm(glob.glob('%s*.jpg' % path)):
            if not os.path.exists(f.replace('images', 'Annotations').replace('.jpg', '.xml')):
                # print('xml not exists: {}'.format(f.replace('images', 'Annotations').replace('.jpg', '.xml')))
                continue
            save_name = f.replace('.jpg', '.bmp').replace(folder, folder + 'bmp')
            if os.path.exists(save_name):
                img = cv2.imread(save_name)
                if img is not None and len(img.shape) == 3:
                    continue
                
            cv2.imwrite(save_name, cv2.imread(f))

    # for label_path in ['../coco/trainvalno5k.txt', '../coco/5k.txt']:
    #     with open(label_path, 'r') as file:
    #         lines = file.read()
    #     lines = lines.replace('2014/', '2014bmp/').replace('.jpg', '.bmp').replace(
    #         '/Users/glennjocher/PycharmProjects/', '../')
    #     with open(label_path.replace('5k', '5k_bmp'), 'w') as file:
    #         file.write(lines)


def create_folder(path='./new_folder'):
    # Create folder
    if os.path.exists(path):
        shutil.rmtree(path)  # delete output folder
    os.makedirs(path)  # make new output folder


if __name__ == '__main__':
    convert_images2bmp()
