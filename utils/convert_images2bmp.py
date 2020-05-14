import os
import glob
import tqdm
import cv2

def convert_images2bmp():
    # cv2.imread() jpg at 230 img/s, *.bmp at 400 img/s
    out_dir = ['/disk/ADAS/DidiData/yoloDiDi/yoloBMP/images_jpg/trainBMP',
               '/disk/ADAS/DidiData/yoloDiDi/yoloBMP/images_jpg/testBMP']
    for idx, img_dir in enumerate(['/disk/ADAS/DidiData/yoloDiDi/yoloBMP/images_jpg/train',
                                   '/disk/ADAS/DidiData/yoloDiDi/yoloBMP/images_jpg/test']):
        # folder = os.sep + Path(path).name
        # output = path.replace(folder, folder + 'bmp')
        # if os.path.exists(output):
        #     shutil.rmtree(output)  # delete output folder
        os.makedirs(out_dir[idx], exist_ok=True)  # make new output folder

        for f in tqdm(glob.glob('%s*.jpg' % img_dir)):
            save_name = f.replace('.jpg', '.bmp')
            cv2.imwrite(save_name, cv2.imread(f))

    for label_path in ['../coco/trainvalno5k.txt', '../coco/5k.txt']:
        with open(label_path, 'r') as file:
            lines = file.read()
        lines = lines.replace('2014/', '2014bmp/').replace('.jpg', '.bmp').replace(
            '/Users/glennjocher/PycharmProjects/', '../')
        with open(label_path.replace('5k', '5k_bmp'), 'w') as file:
            file.write(lines)


if __name__ == '__main__':
    convert_images2bmp()
