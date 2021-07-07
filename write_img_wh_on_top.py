# This script takes input_img_folder and output_folder_path
# It iterates read images, get its size and write img size at the center of the image.
# Then save to the output folder.
import sys
import os
import cv2
import numpy as np

import math

font = cv2.FONT_HERSHEY_SIMPLEX 
fontScale = 0.7 # per char: w = 18.x,  h = 22
color = (255, 255, 255) 
thickness = 1

def load_imgs_name_in_folder(folder_path):
    image_files = os.listdir(folder_path)
    image_files.sort()
    images = []
    names =[]
    #print(len(image_files))

    for i, image_file in enumerate(image_files):
        #print(i)
        image = cv2.imread(folder_path + os.sep + image_file, cv2.IMREAD_COLOR)
        images.append(image)
        #print(image.shape)
        names.append(image_file)
    return images, names    


def write_text_on_image(img, img_w, text, baseposition,
                        font, fontScale, color, thickness):

    (text_w, text_h), baseline = cv2.getTextSize(text=text, fontFace=font, fontScale=fontScale, thickness=thickness)
    text_h = text_h+baseline

    line_num =  int(math.ceil(text_w/img_w)) # find the number of line needed to write the text 
    text_len = len(text)

    char_width = int(math.ceil(text_w/text_len))

    text_len_per_line = int(math.floor(img_w/char_width)) # the number of character that can fit 1 line

    #print("img_w,text_w,text_len,line_num,text_len_per_line:",img_w,text_w,text_len,line_num,text_len_per_line)
    start =0
    for cutindex in range(line_num):
        end = start + text_len_per_line
        text_line = text[start:end]
        #print(text_line)
        start_x = int((img_w - text_w)*0.5)
        position = (start_x,baseposition[1]+cutindex*text_h)
        img = cv2.putText(img, text_line, position, font,  
                    fontScale, color, thickness, cv2.LINE_AA)   

        start = end

    return img

#def write_images_wh_in_folder(folderpath_read, folderpath_write):
def write_images_wh(imgs, output_imgname_list):
    

    for img,savename in zip(imgs,output_imgname_list):
        print(img.shape) #(356, 490, 3) (height,width,channel)

        #img_wh = np.zeros(img.shape)
        text = str(img.shape[1])+"x"+str(img.shape[0]) + " px"

        center_x = int(img.shape[1]*0.5)
        center_y = int(img.shape[0]*0.5)
        # img = cv2.putText(img, item, position, font,  
        #             fontScale, color, thickness, cv2.LINE_AA)  
        #
        img_wh = write_text_on_image(img, img.shape[1], text, (0,center_y), font, fontScale, color, thickness)

        cv2.imwrite(savename, img_wh)


# conda activate maskrcnn_matterport_gpu   # import cv2
# python write_img_wh_on_top.py ./weights700 ./weights700wh
def main():
    script = sys.argv[0] # combine_img_multi.py

    # folder_to_align_images, aligned_image_name
    folder_read_images = sys.argv[1]
    folder_save_images = sys.argv[2]

    imgs, names = load_imgs_name_in_folder(folder_read_images)	

    # create output folder if not exist
    if not os.path.isdir(folder_save_images):
        os.makedirs(folder_save_images)

    output_imgname_list =  [os.path.join(folder_save_images, f) for f in names]
    write_images_wh(imgs, output_imgname_list)




if __name__ == '__main__':
   main()
