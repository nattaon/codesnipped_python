# run this to concate image in horizontal or vertical direction

# conda activate maskrcnn_matterport_gpu

# python combine_img_multi.py ./logs/concatimg_allaug100-500 -horizontal ./logs/val_gt_all_class ./logs/allaug_0100 ./logs/allaug_0200 ./logs/allaug_0300 ./logs/allaug_0400 ./logs/allaug_0500

# python combine_img_multi.py ./logs/concatimg_allaug600-1000 -horizontal ./logs/val_gt_some_class ./logs/allaug_0600 ./logs/allaug_0700 ./logs/allaug_0800 ./logs/allaug_0900 ./logs/allaug_1000

# python combine_img_multi.py ./logs/concatimg_allaugmentation -vertical ./logs/concatimg_allaug100-500 ./logs/concatimg_allaug600-1000




import sys
import os
import cv2
import numpy as np

def load_filenames_imgs_in_folder(folder_path):
    image_files = os.listdir(folder_path)
    image_files.sort()
    images = []
    for i, image_file in enumerate(image_files):
        image = cv2.imread(folder_path + os.sep + image_file, cv2.IMREAD_COLOR)
        images.append(image)
    return image_files, images

def load_imgs_in_folder(folder_path):
    image_files = os.listdir(folder_path)
    image_files.sort()
    images = []
    for i, image_file in enumerate(image_files):
        image = cv2.imread(folder_path + os.sep + image_file, cv2.IMREAD_COLOR)
        images.append(image)
    return images

def concat_2_img_array_horizontal(imgs_A, imgs_B):
    if len(imgs_A)!=len(imgs_B):
        print("Error! images numbers is not equal")
        return

    im_concat = []
    for i in range(len(imgs_A)):

        # padding 0 if both img height not match
        if imgs_A[i].shape[0] > imgs_B[i].shape[0]:
            temp_b = np.zeros(imgs_A[i].shape)
            temp_b[:imgs_B[i].shape[0], :imgs_B[i].shape[1]] = imgs_B[i]
            imgs_B[i]=temp_b

        elif imgs_A[i].shape[0] < imgs_B[i].shape[0]:
            temp_a = np.zeros(imgs_B[i].shape)
            temp_a[:imgs_A[i].shape[0], :imgs_A[i].shape[1]] = imgs_A[i]
            imgs_A[i]=temp_a

   


        im_AB = np.concatenate([imgs_A[i], imgs_B[i]], 1)
        im_concat.append(im_AB)
    return im_concat

def concat_2_img_array_vertical(imgs_A, imgs_B):
    if len(imgs_A)!=len(imgs_B):
        print("Error! images numbers is not equal")
        return

    im_concat = []
    for i in range(len(imgs_A)):
        # padding 0 if both img width not match
        if imgs_A[i].shape[1] > imgs_B[i].shape[1]:
            temp_b = np.zeros(imgs_A[i].shape)
            temp_b[:imgs_B[i].shape[0],:imgs_B[i].shape[1]] = imgs_B[i]
            imgs_B[i]=temp_b
        elif imgs_A[i].shape[1] < imgs_B[i].shape[1]:
            temp_a = np.zeros(imgs_B[i].shape)
            temp_a[:imgs_A[i].shape[0],:imgs_A[i].shape[1]] = imgs_A[i]
            imgs_A[i]=temp_a

        im_AB = np.concatenate([imgs_A[i], imgs_B[i]], 0)
        im_concat.append(im_AB)
    return im_concat


def concate_img_list_horizontal( list_imgdata, concat_path):
    if not os.path.isdir(concat_path):
        os.makedirs(concat_path)   

    list_imgname, imgs_CC = load_filenames_imgs_in_folder(list_imgdata[0])
    #print(len(imgs_CC))
    #print(imgs_CC[0].shape)
    for foldername in list_imgdata[1:]:
        #print('foldername = %s' % (foldername))
        #imgs_i = []
        imgs_i = load_imgs_in_folder(foldername)
        
        #print(len(imgs_i))
        #print(imgs_i[0].shape)

        imgs_CC = concat_2_img_array_horizontal(imgs_CC, imgs_i)
    
    for i, img in enumerate(imgs_CC):
        path_concat = os.path.join(concat_path, list_imgname[i])
        #print(i, path_concat)
        cv2.imwrite(path_concat, img)
	

def main():
    script = sys.argv[0] # combine_img_multi.py



    output_concat_img_folder = sys.argv[1] 
    concat_direction = sys.argv[2]
    first_img_folder = sys.argv[3]
    #label_img_folder = sys.argv[2]
    # = sys.argv[3]

    remain_folder_names = sys.argv[4:] # ./trainingData226/predicted_smp_t70_100ep

    img_name_list = os.listdir(first_img_folder)
    img_name_list.sort()
    print('number of images = %d' % (len(img_name_list)))

    # create output folder if not exist
    if not os.path.isdir(output_concat_img_folder): os.makedirs(output_concat_img_folder)

    print('output at = %s' % (output_concat_img_folder))


    print('foldername = %s' % (first_img_folder))
    imgs_CC = load_imgs_in_folder(first_img_folder)

    if concat_direction == '-horizontal':  
        # concat remaining img
        for foldername in remain_folder_names:
            print('foldername = %s' % (foldername))
            #imgs_i = []
            imgs_i = load_imgs_in_folder(foldername)
            imgs_CC = concat_2_img_array_horizontal(imgs_CC, imgs_i)

    elif concat_direction == '-vertical':       
        # concat remaining img
        for foldername in remain_folder_names:
            print('foldername = %s' % (foldername))
            #imgs_i = []
            imgs_i = load_imgs_in_folder(foldername)
            imgs_CC = concat_2_img_array_vertical(imgs_CC, imgs_i)

    for i, img in enumerate(imgs_CC):
        path_concat = os.path.join(output_concat_img_folder, img_name_list[i])
        cv2.imwrite(path_concat, img)


if __name__ == '__main__':
   main()
