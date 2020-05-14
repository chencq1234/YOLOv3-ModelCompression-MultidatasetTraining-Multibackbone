import os

train_img_dir = '/home/chencq/data/yolo_test_data/images'
out_train_txt = '/home/chencq/data/yolo_test_data/train.txt'

out_list = []
for img_name in os.listdir(train_img_dir):
    out_list.append(os.path.join(train_img_dir, img_name))

with open(out_train_txt, 'w') as f:
    strs = '\n'.join(out_list)
    f.write(strs)
print('finished!')