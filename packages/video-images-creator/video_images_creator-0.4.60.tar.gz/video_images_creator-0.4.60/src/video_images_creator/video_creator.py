import subprocess
import cv2
import numpy as np
import os
from pathlib import Path
import shutil
import secrets
import string
import math
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen
import re
import glob
from math import floor
import azure.cognitiveservices.speech as speechsdk
import pkg_resources
import wave
import concurrent.futures
import contextlib
import random 
import requests
from pydub import AudioSegment
from pydub.silence import split_on_silence

feature_images = {} 
second_anim_images = {} 
switch_anim_images = {} 
third_feature_images = {}

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


def add_alpha_channel(img):
    if img.shape[2] == 4:  # Image already has an alpha channel
        return img
    else:  # Add alpha channel to the image
        alpha_channel = np.ones((img.shape[0], img.shape[1], 1), dtype=img.dtype) * 255  # Fully opaque
        return np.concatenate((img, alpha_channel), axis=-1)

def set_transparency(img, opacity):
    # Ensure the image has an alpha channel
    img_with_alpha = add_alpha_channel(img)
    # Adjust the alpha channel to set the desired opacity
    #img_with_alpha[:, :, 3] = img_with_alpha[:, :, 3] * opacity 

    if opacity == 1.0:
        img_with_alpha[:, :, 3] = 255
    else:
        img_with_alpha[:, :, 3] = 128
    return img_with_alpha


def sort_key(filename):
    # Split the filename into its numerical components, assuming the format is "prefix_number_number.extension"
    parts = re.split(r'[_\.]', filename)  # This splits the filename by underscores and the dot before the extension
    # Convert the numerical parts to integers for proper sorting, ignoring the non-numerical parts
    return [int(part) for part in parts if part.isdigit()]


def add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index, total_frames, transparency, device):

    x_coordinate_increement = 0 
    initial_x_coordinate = 0
    feature_images_urls = list(blended_roi_img_url_dict.keys())
    image_file_prefix = "" 
    increement = 650
    use_dict_obj = False


    if total_frames == 180:
        image_file_prefix = "_preview_frames" 

    if len(feature_images_urls) == 5:
        ###
        x_coordinate_increement = 0
        initial_x_coordinate = 335
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "5featureframe.png"))
    elif len(feature_images_urls) == 4:
        initial_x_coordinate = 713
        background_img_url = "https://testkals.s3.amazonaws.com/4featureframe.png"
    elif len(feature_images_urls) == 3: 

        if device == "mobile":
            initial_x_coordinate = 985
            background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "3featureframe.png"))
        else: 
            initial_x_coordinate = 132
            use_dict_obj = True
            increement = 850
            background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "threeframe_web.png"))

    elif len(feature_images_urls) == 2: 
        
        if device == "mobile":
            initial_x_coordinate = 1340
            background_img_url = "https://testkals.s3.amazonaws.com/2featureframe.png" 
        else:
            initial_x_coordinate = 1340
            use_dict_obj = True
            background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "twoframe_web.png")) 

        
    elif len(feature_images_urls) == 1:

        if device == "mobile":
            initial_x_coordinate = 1635
            background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "animaionfeature.png")) 
        else:
            initial_x_coordinate = 1335
            background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "singleanimation_web.png")) 

    else:
        print("Exit?///") 

    max_index = len(feature_images_urls) - 1
    running_index = 0
    
  
    for feature_images_url in feature_images_urls:

        if use_dict_obj == True:
            x_coordinate = blended_roi_img_url_dict[feature_images_url]["x_coordinate"]
        else:
            x_coordinate = initial_x_coordinate + x_coordinate_increement 

        if device == "mobile":
            x, y = x_coordinate + 13, 486
        else:
            x, y = x_coordinate + 13, 737


        blended_roi = blended_roi_img_url_dict[feature_images_url]["blended_roi"]
        h_o = blended_roi_img_url_dict[feature_images_url]["h_o"]
        w_o = blended_roi_img_url_dict[feature_images_url]["w_o"]


        if running_index == 0 or running_index == max_index:
            blended_roi = set_transparency(blended_roi, transparency)
            #background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3] 
            overlay_image = blended_roi[..., :3]  # RGB channels
            mask = blended_roi[..., 3:] / 255.0  # Alpha channel normalized

            background[y:y+h_o, x:x+w_o] = (1.0 - mask) * background[y:y+h_o, x:x+w_o] + mask * overlay_image 

        else:
            blended_roi = set_transparency(blended_roi, transparency)
            background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3]

        running_index = running_index + 1

        x_coordinate_increement = x_coordinate_increement + increement 


    file_name = f'{directory_name}/frame_{current_index}_{total_frames}{image_file_prefix}.jpg' 
    cv2.imwrite(file_name, background)

    current_index_ = current_index

    return ( current_index + 1 )

def create_feature_set_frames_v2(current_index, directory_name, feature_images_urls, device): 


    current_index = add_blank_background_frames(directory_name, current_index)

    temp_feature_images_urls = feature_images_urls[:1]
    feature_images_url = temp_feature_images_urls[0] 

    if device == "mobile":
        initial_x_coordinate = 1635
    else:
        initial_x_coordinate = 1335

    x_coordinate_increement = 0


    x_coordinate = initial_x_coordinate + x_coordinate_increement

    if device == "mobile":
        x, y = x_coordinate + 13, 486
    else:
        x, y = x_coordinate + 13, 737

    # Generate the rounded image 


    overlay = read_image(feature_images_url) 

    if device == "mobile":
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "animaionfeature.png"))
    else:
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "singleanimation_web.png"))


    
    x_coordinate = initial_x_coordinate + x_coordinate_increement 

    if device == "mobile":
        screen_width, screen_height = 545, 1190
        x, y = x_coordinate + 13, 486
    else:
        screen_width, screen_height = 1140,690
        x, y = x_coordinate + 13, 737


    overlay = cv2.resize(overlay, (screen_width, screen_height))
    corner_radius = 30

    mask = create_rounded_mask(overlay, corner_radius)
    # Generate the rounded image
    rounded_image = get_rounded_image_old(overlay, mask)
    h_o, w_o, _ = rounded_image.shape
    blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)
    blended_roi_img_url_dict = {}
    #blended_roi_img_url_dict[feature_images_url] = blended_roi

    dict_obj = { "blended_roi": blended_roi, "h_o": h_o, "w_o": w_o }

    blended_roi_img_url_dict[feature_images_url] = dict_obj


    current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,7, 0.0, device) 

    current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,3, 0.1, device) 

    current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,120, 1.0, device)

    if device == "mobile" :

        if len(feature_images_urls[:3]) >=3 :

            temp_feature_images_urls = feature_images_urls[:3] 
            temp_feature_images_urls[0], temp_feature_images_urls[1] = temp_feature_images_urls[1], temp_feature_images_urls[0] 

            blended_roi_img_url_dict = {} 
            x_coordinate_increement = 0
            background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "3featureframe.png"))

            for feature_images_url in temp_feature_images_urls: 

                initial_x_coordinate = 985
            

                x_coordinate = initial_x_coordinate + x_coordinate_increement

                x, y = x_coordinate + 13, 486
                # Generate the rounded image 


                overlay = read_image(feature_images_url)
            
                
                x_coordinate = initial_x_coordinate + x_coordinate_increement
                screen_width, screen_height = 545, 1190
                x, y = x_coordinate + 13, 486

                overlay = cv2.resize(overlay, (screen_width, screen_height))
                corner_radius = 30


                mask = create_rounded_mask(overlay, corner_radius)
                # Generate the rounded image
                rounded_image = get_rounded_image_old(overlay, mask)
                h_o, w_o, _ = rounded_image.shape
                blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)
                dict_obj = { "blended_roi": blended_roi, "h_o": h_o, "w_o": w_o }
                blended_roi_img_url_dict[feature_images_url] = dict_obj

                x_coordinate_increement = x_coordinate_increement + 650


            current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,7, 0.0, device) 

            current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,3, 0.1, device) 

            current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index, 120, 1.0, device)

        if len(feature_images_urls) >= 5:

            temp_feature_images_urls = feature_images_urls[:5] 
            temp_feature_images_urls[0], temp_feature_images_urls[2] = temp_feature_images_urls[2], temp_feature_images_urls[0]


            x_coordinate_increement = 0
            initial_x_coordinate = 400
            background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "5featureframe.png"))
            blended_roi_img_url_dict = {}


            for feature_images_url in temp_feature_images_urls: 

                initial_x_coordinate = 335
                

                x_coordinate = initial_x_coordinate + x_coordinate_increement

                x, y = x_coordinate + 13, 486
                # Generate the rounded image 


                overlay = read_image(feature_images_url)

                
                x_coordinate = initial_x_coordinate + x_coordinate_increement
                screen_width, screen_height = 545, 1190
                x, y = x_coordinate + 13, 486

                overlay = cv2.resize(overlay, (screen_width, screen_height))
                corner_radius = 30
                mask = create_rounded_mask(overlay, corner_radius)
                # Generate the rounded image
                rounded_image = get_rounded_image_old(overlay, mask)
                h_o, w_o, _ = rounded_image.shape
                blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)
                dict_obj = { "blended_roi": blended_roi, "h_o": h_o, "w_o": w_o }
                blended_roi_img_url_dict[feature_images_url] = dict_obj

                x_coordinate_increement = x_coordinate_increement + 626

            current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,7, 0.0, device) 

            current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,3, 0.1, device) 

            current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,180, 1.0, device) 

    else: 

        #2 frames, in case of web

        temp_feature_images_urls = feature_images_urls[:2] 
        temp_feature_images_urls[0], temp_feature_images_urls[1] = temp_feature_images_urls[1], temp_feature_images_urls[0]

        blended_roi_img_url_dict = {}
        x_coordinate_increement = 850
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "twoframe_web.png"))

        initial_x_coordinate = 132
        x_coordinate = initial_x_coordinate 

        indexx = 0

        x_coordinatess = [740, 1952]

        for feature_images_url in temp_feature_images_urls: 

            x_coordinate = x_coordinatess[indexx] 

            indexx = indexx + 1

        
            #x_coordinate = x_coordinate + x_coordinate_increement

            x, y = x_coordinate + 13, 737
            # Generate the rounded image 


            overlay = read_image(feature_images_url)
        
            
            #x_coordinate = x_coordinate + x_coordinate_increement
            screen_width, screen_height = 1120,690
            x, y = x_coordinate + 13, 737

            overlay = cv2.resize(overlay, (screen_width, screen_height))
            corner_radius = 30 

            mask = create_rounded_mask(overlay, corner_radius)
            # Generate the rounded image
            rounded_image = get_rounded_image_old(overlay, mask)
            h_o, w_o, _ = rounded_image.shape
            #print(h_o, w_o, x_coordinate)
            blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)
            dict_obj = { "blended_roi": blended_roi, "h_o": h_o, "w_o": w_o, "x_coordinate": x_coordinate }
            blended_roi_img_url_dict[feature_images_url] = dict_obj

            #x_coordinate_increement = 1200


        current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,7, 0.0, device) 

        current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,3, 0.1, device) 

        current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,120, 1.0, device) 

        # 3 frames, for web

        temp_feature_images_urls = feature_images_urls[:3] 
        temp_feature_images_urls[0], temp_feature_images_urls[1] = temp_feature_images_urls[1], temp_feature_images_urls[0] 

        blended_roi_img_url_dict = {} 
        x_coordinate_increement = 850
        #background = three_feature_frame

        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "threeframe_web.png"))

        initial_x_coordinate = 132
        x_coordinate = initial_x_coordinate 

        indexx = 0

        x_coordinatess = [130, 1345, 2560]

        for feature_images_url in temp_feature_images_urls: 

            x_coordinate = x_coordinatess[indexx] 

            indexx = indexx + 1

        
            #x_coordinate = x_coordinate + x_coordinate_increement

            x, y = x_coordinate + 13, 737
            # Generate the rounded image 


            overlay = read_image(feature_images_url)
        
            
            #x_coordinate = x_coordinate + x_coordinate_increement
            screen_width, screen_height = 1120,690
            x, y = x_coordinate + 13, 737

            overlay = cv2.resize(overlay, (screen_width, screen_height))
            corner_radius = 30
            mask = create_rounded_mask(overlay, corner_radius) 

            # Generate the rounded image
            rounded_image = get_rounded_image_old(overlay, mask)
            h_o, w_o, _ = rounded_image.shape
            blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)
            dict_obj = { "blended_roi": blended_roi, "h_o": h_o, "w_o": w_o, "x_coordinate": x_coordinate }
            blended_roi_img_url_dict[feature_images_url] = dict_obj

            #x_coordinate_increement = 1200


        current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,7, 0.0, device) 

        current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,3, 0.1, device) 

        current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,120, 1.0, device)



    return current_index


def add_images_in_single_frame(feature_images_url, directory_name, current_index, transparency, frames):
 
    x_coordinate = 1650
    x, y = x_coordinate, 540
    background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "featureframe.png"))


    overlay = read_image(feature_images_url) 
    screen_width, screen_height = 551, 1210
    overlay = cv2.resize(overlay, (screen_width, screen_height)) 
    corner_radius = 30
    mask = create_rounded_mask(overlay, corner_radius)
    rounded_image = get_rounded_image(overlay, mask)
    x, y = 1650, 540
    h_o, w_o, _ = rounded_image.shape 
    blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image) 

    blended_roi = set_transparency(blended_roi, transparency)

    #background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3] 

    overlay_image = blended_roi[..., :3]  # RGB channels
    mask = blended_roi[..., 3:] / 255.0  # Alpha channel normalized
    
    background[y:y+h_o, x:x+w_o] = (1.0 - mask) * background[y:y+h_o, x:x+w_o] + mask * overlay_image
    
    file_name = f'{directory_name}/frame_{current_index}.jpg' 
    cv2.imwrite(file_name, background)

    current_index_ = current_index

    for i in range(1,frames): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1 

    


    return current_index


def add_blank_background_frames(directory_name, current_index):
  
    # background = cv2.imread("features/startfeatureframe.png")
    # file_name = f'{directory_name}/frame_{current_index}.jpg' 
    # cv2.imwrite(file_name, background)


    ending_page_image = cv2.imread(pkg_resources.resource_filename('video_images_creator', "startfeatureframe.png"))

    #create original image with cv2 imwrite
    original_file_name = f'{directory_name}/frame_{current_index}_49.jpg'
    cv2.imwrite(original_file_name, ending_page_image)

    # current_index_ = current_index

    # for i in range(1,50): 
    #     index = i + current_index_
    #     destination = f'{directory_name}/frame_{index}.jpg'
    #     shutil.copyfile(original_file_name, destination)
    #     current_index = current_index + 1

    return ( current_index + 1 )


def add_images_in_frameset(feature_images_urls, directory_name, current_index, total_frames, transparency):
 
    x_coordinate_increement = 0 
    initial_x_coordinate = 0

    if len(feature_images_urls) == 5:
        ###
        x_coordinate_increement = 0
        initial_x_coordinate = 400
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "5featureframe.png"))
    elif len(feature_images_urls) == 4:
        initial_x_coordinate = 713
        background_img_url = "https://testkals.s3.amazonaws.com/4featureframe.png"
    elif len(feature_images_urls) == 3:
        initial_x_coordinate = 1025
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "3featureframe.png"))
    elif len(feature_images_urls) == 2:
        initial_x_coordinate = 1340
        background_img_url = "https://testkals.s3.amazonaws.com/2featureframe.png" 
    elif len(feature_images_urls) == 1:
        initial_x_coordinate = 1650
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "animaionfeature.png"))
    else:
        print("Exit?///") 

    max_index = len(feature_images_urls) - 1
    running_index = 0
    
  
    for feature_images_url in feature_images_urls: 

        x_coordinate = initial_x_coordinate + x_coordinate_increement

        x, y = x_coordinate + 13, 486
        overlay = read_image(feature_images_url) 
        screen_width, screen_height = 545, 1190
        overlay = cv2.resize(overlay, (screen_width, screen_height))
        corner_radius = 30
        mask = create_rounded_mask(overlay, corner_radius)
        # Generate the rounded image
        rounded_image = get_rounded_image(overlay, mask)
        h_o, w_o, _ = rounded_image.shape
        blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)


        if running_index == 0 or running_index == max_index:
            blended_roi = set_transparency(blended_roi, transparency)
            #background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3] 
            overlay_image = blended_roi[..., :3]  # RGB channels
            mask = blended_roi[..., 3:] / 255.0  # Alpha channel normalized

            background[y:y+h_o, x:x+w_o] = (1.0 - mask) * background[y:y+h_o, x:x+w_o] + mask * overlay_image
        else:
            blended_roi = set_transparency(blended_roi, transparency)
            background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3] 

        running_index = running_index + 1

        
        #background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3] 

        #background = overlay_transparent(background, blended_roi, x_coordinate, 650)  # Adjust y-coordinate as needed


        x_coordinate_increement = x_coordinate_increement + 626 


    file_name = f'{directory_name}/frame_{current_index}.jpg' 
    cv2.imwrite(file_name, background)

    current_index_ = current_index

    for i in range(1,total_frames): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    return current_index


def create_starting_frames(current_index, directory_name, ending_page_image, total_frames, image_suffix):

    # if ending_page_image_url == "terminal":
    #     ending_page_image = pkg_resources.resource_filename('video_images_creator', "terminal.png")

    # elif ending_page_image_url == "preterminal":
    #     ending_page_image = pkg_resources.resource_filename('video_images_creator', "preterminal.png")
    # else:
    #     return
    
    #create original image with cv2 imwrite
    if image_suffix != "":
        original_file_name = f'{directory_name}/frame_{current_index}_{total_frames}_{image_suffix}.jpg'
    else:
        original_file_name = f'{directory_name}/frame_{current_index}_{total_frames}.jpg'
    #original_file_name = f'{directory_name}/frame_{current_index}_{total_frames}.jpg'
    cv2.imwrite(original_file_name, ending_page_image)
    # for i in range(1,total_frames): 
    #     index = current_index + i
    #     destination = f'{directory_name}/frame_{index}.jpg'
    #     shutil.copyfile(original_file_name, destination)
    #     #cv2.imwrite(destination, ending_page_image) 

    return (current_index + 1)

def add_images_in_single_frame_V2(feature_images_url, font, directory_name, current_index, feature_title, device):
    first_image = True 
    background = ''

    if device == "mobile":
        x_coordinate = 1590
        screen_width, screen_height = 660, 1419
        x, y = x_coordinate, 370
        corner_radius = 30
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "featureframe.png"))
    else:
        x_coordinate = 855
        screen_width, screen_height = 2130, 1300
        x, y = x_coordinate, 430
        corner_radius = 60
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "singleframe_web.png"))

    overlay = read_image(feature_images_url)
    
    overlay = cv2.resize(overlay, (screen_width, screen_height))  
    
    if first_image == True:
        first_image = False

    
        mask = create_rounded_mask(overlay, corner_radius)
        # Generate the rounded image
        rounded_image = get_rounded_image_old(overlay, mask)


        h_o, w_o, _ = rounded_image.shape 
        blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image) 


        background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3] 

        # line = feature_title

        # pil_image = Image.fromarray(cv2.cvtColor(background, cv2.COLOR_BGR2RGB))
        # draw = ImageDraw.Draw(pil_image)
        
        # #print(x_coordinate) 
        # #print(len(line))
        # if len(line) > 13: 
        #     x_coordinate = int(max((3840 -  ( len(line) * 40 )  ),0) / 2 ) #tradeoff calc
        # #print(x_coordinate)
        # draw.text((x_coordinate, 1910), line.strip(), font=font, fill=(88, 88, 88))  

        # background = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


        file_name = f'{directory_name}/frame_{current_index}_180_feature_frames.jpg' 
        cv2.imwrite(file_name, background)

        # current_index_ = current_index

        # for i in range(1,180): 
        #     index = i + current_index_
        #     destination = f'{directory_name}/frame_{index}.jpg'
        #     shutil.copyfile(file_name, destination)
        #     current_index = current_index + 1 

    


    return (current_index + 1)


def add_feature_frames(feature_images_urls, directory_name, current_index, feature_titles, device):

    index = 0
     # Load the custom font
    font_path = pkg_resources.resource_filename('video_images_creator', 'Rubik-Medium.ttf')
    font_size = 84
    font = ImageFont.truetype(font_path, font_size)
  
    
    for feature_images_url in feature_images_urls:
        current_index = add_images_in_single_frame_V2(feature_images_url, font, directory_name, current_index, feature_titles[index], device) 
        index = index + 1 

    return current_index



def build_v2(feature_images_urls, feature_names):

    ensure_required_directories_existis()
    current_index = 1
    folder_name = generate_random_string(10)  
    directory_name = f'images/{folder_name}'
    os.mkdir(directory_name)
    terminal_image_path = pkg_resources.resource_filename('video_images_creator', "terminal.png")
    terminal_image = cv2.imread(terminal_image_path)

    pre_terminal_image_path = pkg_resources.resource_filename('video_images_creator', "preterminal.png")
    preterminal_image = cv2.imread(pre_terminal_image_path)

    current_running_index = create_starting_frames(current_index, directory_name, terminal_image,400) 
    #feature_images_urls = ["https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/103054602/1a0d1594-1e81-4181-b4bb-92d31f197539.png", "https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/103054583/30188996-01e3-4eab-9a36-552f70d1bb73.png", "https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/130179838/d41999b6-b89d-4f3a-988b-3a3dd85dd986.png", "https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/130179842/d9954a75-b307-4839-b634-f18c4e4b7b1a.png", "https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/40258072/987611d1-19cd-4931-a618-0897aa0d79d1.png", "https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/40258074/b82fae9a-4d79-45e9-a286-dc6f1b92a0c4.png", "https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/40258060/5cc635d6-b63a-4b20-929f-cf12eb178765.png"]
    #feature_titles = ["Splash Screen", "User Profile", "Signup/ Login", "Categories/ Sub-Categories", "Order Summary", "Payment Details", "Order Summary"]

    current_running_index = create_starting_frames(current_running_index, directory_name, preterminal_image, 80)
    current_running_index = create_feature_set_frames_v2(current_running_index, directory_name, feature_images_urls)


    current_running_index = add_feature_frames(feature_images_urls, directory_name, current_running_index, feature_names) 

    current_running_index = create_starting_frames(current_running_index, directory_name, preterminal_image, 60)
    current_running_index = create_starting_frames(current_running_index, directory_name, terminal_image, 180) 



    image_files = sorted([f for f in os.listdir(directory_name) if f.endswith(('.jpg', '.png'))], key=sort_key) 

    temp_text_file = f'{directory_name}/temp_ffmpeg_list.txt'

    total_duration = 0


    with open(temp_text_file, 'w') as file:
        for image in image_files:
            # Extract the number of frames from the filename (assuming it's after the last '_')
            frames = int(image.split('_')[-1].split('.')[0])
            duration = frames / 60  # Calculate duration in seconds
            total_duration = total_duration + duration

            # Write the file command for this image
            file.write(f"file '{os.path.join('', image)}'\n")
            # Write the duration command for this image
            file.write(f"duration {duration}\n")

        # For the concat demuxer, the last file should not have a duration specified
        # So, we add the last file entry again without a duration
        file.write(f"file '{os.path.join('', image_files[-1])}'\n")


    run_ffmpeg_v3(directory_name, folder_name, temp_text_file, total_duration) 
    return flush_video_images(directory_name, folder_name)


def synthesize_speech_with_ssml(intro_text, features_intro_text, feature_descriptions, subscription_key, service_region, output_file):
    """
    Synthesizes speech from SSML input and saves the output as an audio file.

    Parameters:
    - subscription_key (str): Azure Cognitive Services Speech subscription key.
    - service_region (str): Azure service region (e.g., "westus").
    - output_file (str): Output audio file path.
    """
    try:
        #print(intro_text)
        #print(feature_descriptions)
        # Create an instance of a speech config with specified subscription key and service region
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)

        # Set the speech synthesis output format
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm)

        # Create an audio configuration that points to an output audio file
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)

        # Create a speech synthesizer using the configured speech config and audio config
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # Define the SSML with the desired voice, language, and include a break
        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-GB'>
            <voice name='en-GB-SoniaNeural'>
                {intro_text}.
                <break time='500ms'/>
                Over the next few minutes we will walk through the app.
                <break time='200ms'/>
                {features_intro_text}
                <break time='760ms'/> 
                {feature_descriptions}
            </voice>
        </speak>
        """
        # Synthesize the speech from the SSML
        result = synthesizer.speak_ssml_async(ssml).get()

        # Check the result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return 0, "Audio saved successfully."  # Success code and message
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            error_message = f"Speech synthesis canceled: {cancellation_details.reason}"
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    error_message += f" Error details: {cancellation_details.error_details}"
                return 1, error_message  # Error code and message
        return 2, "Synthesis failed for an unknown reason."  # Unexpected error code and message

    except Exception as e:
        return 99, f"An exception occurred: {str(e)}"  # Exception code and message



def convert_to_stereo_48khz_16bit(input_file, output_file):
    """
    Converts an audio file to stereo, with a sample rate of 48 kHz and 16 bits per sample using FFmpeg.

    Parameters:
    - input_file (str): Path to the input audio file.
    - output_file (str): Path where the converted audio file will be saved.

    Returns:
    - None
    """
    # FFmpeg command components
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',
        '-i', f'./{input_file}',  # Input file
        '-ac', '2',
        output_file  # Output file
    ]

    # Run the FFmpeg command
    try:
        subprocess.run(ffmpeg_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during conversion: {e}")


def add_pause_with_pydub(input_filename, output_filename, pause_duration_milliseconds):
    # Load the existing audio file
    try:
        sound = AudioSegment.from_wav(input_filename)
        silence = AudioSegment.silent(duration=pause_duration_milliseconds)
        combined = sound + silence
        combined.export(output_filename, format="wav")
        return True 
    except Exception as e:
        print(f"An error occurred: {e}") 
    return False


def combine_wav_files(output_file, input_files):
    # Open the first file to get the parameters
    with wave.open(input_files[0], 'rb') as wav:
        params = wav.getparams()

    # Open the output file
    with wave.open(output_file, 'wb') as outfile:
        outfile.setparams(params)  # Set the parameters to match the input files

        # Go through each input file and append the audio
        for file in input_files:
            with wave.open(file, 'rb') as infile:
                while True:
                    data = infile.readframes(1024)
                    if not data:
                        break
                    outfile.writeframes(data)

def synthesize_text(speech_obj, subscription_key, service_region, tts_audio_folder):

    text = speech_obj["text"]
    audio_index = speech_obj["audio_index"]
    generate_audio = speech_obj["generate_audio"] 
    audio_blob_url = speech_obj["audio_blob_url"]
    output_file = f"{tts_audio_folder}/{audio_index}.wav"

    if generate_audio is True and len(audio_blob_url) > 0:

        try:
            response = requests.get(audio_blob_url)
            # Check if the request was successful
            if response.status_code == 200:
                # Write the content to a local file
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                    return 0, "Audio saved successfully.", output_file, audio_index, speech_obj["type"], speech_obj["step_feature_count"], speech_obj["is_last_audio_in_step"], speech_obj["animation_type"], text
        except Exception as ep:
            return 99, f"An exception occurred: {str(ep)}", "", "", "", "", "", "", ""
        
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm)
    speech_config.speech_synthesis_voice_name = 'en-GB-SoniaNeural'
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    ssml = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-GB'>
        <voice name='en-GB-SoniaNeural'>
            {text}
        </voice>
    </speak>
    """
    try:
        result = synthesizer.speak_ssml_async(ssml).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # print("Speech synthesized to [{}] for text [{}]".format(output_file, ssml))  
            
            return 0, "Audio saved successfully.", output_file, audio_index, speech_obj["type"], speech_obj["step_feature_count"], speech_obj["is_last_audio_in_step"], speech_obj["animation_type"], text  # Success code and message
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            error_message = f"Speech synthesis canceled: {cancellation_details.reason}"
            #print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    #print("Error details: {}".format(cancellation_details.error_details))
                    error_message += f" Error details: {cancellation_details.error_details}"
                return 1, error_message, "", "", "", "", "", "", ""  # Error code and message
        return 2, "Synthesis failed for an unknown reason.", "", "","","", "", "", ""  # Unexpected error code and message
    except Exception as e:
        return 99, f"An exception occurred: {str(e)}", "", "", "","", "","", ""


def get_wav_duration(filename):
    with contextlib.closing(wave.open(filename, 'r')) as file:
        frames = file.getnframes()
        rate = file.getframerate()
        duration = frames / float(rate)
        return duration


def run_parallel_tts_process(all_speech_objs, subscription_key, service_region, tts_audios_folder, process_mode, design_mode):
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(all_speech_objs)) as executor:
        # Schedule the synthesize_text function to be called for each set of texts
        future_to_text = {executor.submit(synthesize_text, speech_obj, subscription_key, service_region, tts_audios_folder): speech_obj for speech_obj in all_speech_objs}
        for future in concurrent.futures.as_completed(future_to_text):
            text = future_to_text[future]
            try:

                result_code, message, file_name, audio_index, speech_type, set_feature_count, is_last_audio_in_step, animation_type, text = future.result()

                # print("the animation type is :", animation_type)

                if result_code == 0:
                    #succeeded 
                    duration = get_wav_duration(file_name)
                    min_duration = 3.0
                    if speech_type == "project_intro":
                        min_duration = 8.3 
                        if process_mode == "byscript":
                            min_duration = duration
                            if design_mode == 2:
                                if min_duration < 7.0:
                                    pause_required = 7.0 - min_duration 
                                    pause_required = pause_required * 1000
                                    if pause_required:
                                        pause_success = add_pause_with_pydub(file_name, file_name, pause_required)
                                        if pause_success and os.path.exists(file_name) and os.path.getsize(file_name) > 0:
                                            duration = 7.0
                                if min_duration > 7.0:
                                    duration = min_duration
                    if speech_type == "feature_intro":
                        min_duration = 9.5
                    if speech_type == "feature_description" and design_mode == 2 and process_mode == "byscript":
                        # print("the animation type is inside tts parallel : ", animation_type, " and the duration is : ", duration)
                        if animation_type == 1:
                            min_duration = 5.96
                        elif animation_type == 2:
                            min_duration = 6.038 
                        elif animation_type == 3:
                            min_duration = 4.24

                        # if text == "<break time='200ms'/>..":
                        #     min_duration = 3.0
                        
                    if duration > min_duration and speech_type in ["feature_description"] and process_mode == "byscript" and design_mode == 1: 
                        duration = duration / set_feature_count
                    if duration < min_duration and speech_type in ["project_intro", "feature_intro", "feature_description"]:
                        seconds_diff = min_duration - duration
                        milli_seconds_diff = seconds_diff * 1000
                        pause_success = add_pause_with_pydub(file_name, file_name, milli_seconds_diff)
                        if pause_success and os.path.exists(file_name) and os.path.getsize(file_name) > 0:
                            # print("min duraion ", min_duration, " set for text" , text, " for previous duration ", duration)
                            duration = min_duration
                            if speech_type in ["feature_description"] and process_mode == "byscript" and design_mode == 1:
                                duration = 5.0

                    speech_obj = [obj for obj in all_speech_objs if obj["audio_index"] == audio_index ]

                    if speech_obj:
                        speech_obj = speech_obj[0]
                        speech_obj["duration"] = duration
                        speech_obj["filename"] = file_name 


            except Exception as exc:
                print(f'Text {text} generated an exception: {exc}') 
                return {} 
            
    return all_speech_objs


def compute_feature_count_stepwise(feature_desriptions):
    current_count = 0
    current_parent = ""
    parents_to_index_counts = {}
    current_index = 0
    for fd in feature_desriptions:
        if fd != "<break time='200ms'/>..":
            current_parent = fd
            parents_to_index_counts[fd] = [current_index]
        else:
            parents_to_index_counts[current_parent].append(current_index)
        current_index = current_index + 1

    step_counts = []

    for ind in range(len(feature_desriptions)): 

        for key,value in parents_to_index_counts.items():
            if ind in value:
                step_counts.append(len(value)) 
    return step_counts     



def build_with_old_design(build_card_name, feature_descriptions, intro_text, preview_screen_text, process_mode, feature_images_urls, feature_ids, existing_audios, device, preview_feature_image_urls, feature_names, subscription_key, service_region):
    
    ensure_required_directories_existis()
    current_index = 1
    folder_name = generate_random_string(10)  
    directory_name = f'images/{folder_name}/audios'
    os.makedirs(directory_name, exist_ok=True) 

    directory_name = f'images/{folder_name}'
    tts_audios_folder = f'images/{folder_name}/audios'
    tts_output_filename = f'{directory_name}/tts_outfile_name.wav'
    tts_output_2_channel_filename = f'{directory_name}/tts_2_chnl_outfile_name.wav'
    project_intro_text = f"Hey, I am Natasha, We are excited to share with you the prototype for {build_card_name} that we have designed.<break time='500ms'/>"
    feature_intro_text = f"Starting with the {feature_names[0]} users will be able to then interact with {feature_names[1]} and {feature_names[2]} <break time='200ms'/> "
    feature_count_stepwise = compute_feature_count_stepwise(feature_descriptions) 
    #print("feature_count_stepwise ", feature_count_stepwise)


    if process_mode == "byscript":
        project_intro_text = f"{intro_text}<break time='100ms'/>"
        feature_intro_text = f"{preview_screen_text}..<break time='600ms'/>"

    if process_mode == "legacy":
        preview_feature_image_urls = feature_images_urls[:5]


    pattern = r"[\n\r\t]|<p>|<br>|<b>|</p>|</br>|&nbsp;|&#39;"
    feature_desciption_stripped = ""

    for fd in feature_descriptions:
        feature_desciption_stripped = feature_desciption_stripped + " " + re.sub(pattern, '', fd)

    terminal_image_path = pkg_resources.resource_filename('video_images_creator', "terminal.png")
    terminal_image = cv2.imread(terminal_image_path)

    pre_terminal_image_path = pkg_resources.resource_filename('video_images_creator', "preterminal.png")
    preterminal_image = cv2.imread(pre_terminal_image_path)



    terminal_image_frames = 500 
    preterminal_image_frames = 70 
    if process_mode == "byscript":
        terminal_image_frames = 200
        preterminal_image_frames = 35

    current_running_index = 0

    #current_running_index = create_starting_frames(current_index, directory_name, terminal_image, terminal_image_frames, "start_frames") 
    #feature_images_urls = ["https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/103054602/1a0d1594-1e81-4181-b4bb-92d31f197539.png", "https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/103054583/30188996-01e3-4eab-9a36-552f70d1bb73.png", "https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/130179838/d41999b6-b89d-4f3a-988b-3a3dd85dd986.png", "https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/130179842/d9954a75-b307-4839-b634-f18c4e4b7b1a.png", "https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/40258072/987611d1-19cd-4931-a618-0897aa0d79d1.png", "https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/40258074/b82fae9a-4d79-45e9-a286-dc6f1b92a0c4.png", "https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/40258060/5cc635d6-b63a-4b20-929f-cf12eb178765.png"]
    #feature_titles = ["Splash Screen", "User Profile", "Signup/ Login", "Categories/ Sub-Categories", "Order Summary", "Payment Details", "Order Summary"]


    #current_running_index = create_starting_frames(current_running_index, directory_name, preterminal_image, preterminal_image_frames, "")
    current_running_index = create_feature_set_frames_v2(current_running_index, directory_name, preview_feature_image_urls, device)


    current_running_index = add_feature_frames(feature_images_urls, directory_name, current_running_index, feature_names, device)


    #current_running_index = create_starting_frames(current_running_index, directory_name, preterminal_image, 100,"")
    #current_running_index = create_starting_frames(current_running_index, directory_name, terminal_image, 250, "") 


    image_files = sorted([f for f in os.listdir(directory_name) if f.endswith(('.jpg', '.png'))], key=sort_key)  

    all_speech_objs = [] 
    
    
    project_intro_speech_obj = {
        "text": project_intro_text,
        "type": "project_intro",
        "uniq_id": "project_intro",
        "audio_index": 0,
        "generate_audio": True,
        "audio_blob_url": "",
        "step_feature_count": 1,
        "is_last_audio_in_step": False,
        "animation_type": 1
    }

    all_speech_objs.append(project_intro_speech_obj) 


    post_intro_speech_obj = {
        "text": "Over the next few minutes we will walk through the app.<break time='200ms'/>",
        "type": "post_intro",
        "uniq_id": "post_intro",
        "audio_index": 1,
        "generate_audio": True,
        "audio_blob_url": "",
        "step_feature_count": 1,
        "is_last_audio_in_step": False,
        "animation_type": 1
    } 

    if process_mode == "legacy":
        all_speech_objs.append(post_intro_speech_obj) 


    features_intro_speech_obj = {
        "text": feature_intro_text,
        "type": "feature_intro",
        "uniq_id": "feature_intro",
        "audio_index": 2,
        "generate_audio": True,
        "audio_blob_url": "",
        "step_feature_count": 1,
        "is_last_audio_in_step": False,
        "animation_type": 1
    } 

    all_speech_objs.append(features_intro_speech_obj)

    audio_index = 3
    feature_index = 0

    feature_desciption_formatted = []

    for fd in feature_descriptions:
        pattern = r"[\n\r\t]|<p>|<br>|<b>|</p>|</br>|&nbsp;|&#39;"
        feature_desciption_ = re.sub(pattern, '', fd)
        #feature_desciption_ = feature_desciption_.replace("<break time='600ms'/>","")
        feature_desciption_formatted.append(feature_desciption_)
        feature_desciption_speech_obj = {
            "text": feature_desciption_,
            "type": "feature_description",
            "uniq_id": feature_ids[feature_index],
            "audio_index": audio_index,
            "generate_audio": not(existing_audios[feature_index] == ""),
            "audio_blob_url": existing_audios[feature_index],
            "step_feature_count": feature_count_stepwise[feature_index],
            "is_last_audio_in_step": False,
            "animation_type": 1
        }

        audio_index = audio_index + 1
        feature_index = feature_index + 1
        all_speech_objs.append(feature_desciption_speech_obj)

    all_speech_objs = run_parallel_tts_process(all_speech_objs, subscription_key, service_region, tts_audios_folder, process_mode, 1) 

    all_audio_file_names = [item['filename'] for item in all_speech_objs if 'filename' in item]

    combine_wav_files(tts_output_filename, all_audio_file_names)


    temp_text_file = f'{directory_name}/temp_ffmpeg_list.txt'

    total_duration = 0
    current_feature_index = 0 
    total_preview_frames_duration = 0

    # Open a temporary text file to write the file and duration commands for FFmpeg
    with open(temp_text_file, 'w') as file:
        for image in image_files:
            # Extract the number of frames from the filename (assuming it's after the last '_')  

            image_ = image.replace("_feature_frames", "") 
            image_ = image_.replace("_start_frames","")
            image_ = image_.replace("_preview_frames","")
            seconds = 0

            frames = int(image_.split('_')[-1].split('.')[0])
            duration = frames / 60  # Calculate duration in seconds

            if "_feature_frames" in image:
                pattern = r"[\n\r\t]|<p>|<br>|<b>|</p>|</br>|&nbsp;|&#39;" 
                feature_desciption_ = re.sub(pattern, '', feature_descriptions[current_feature_index])  
                #feature_desciption_ = feature_desciption_.replace("<break time='600ms'/>","")
                uniq_id = feature_ids[current_feature_index]

                speech_obj = [obj for obj in all_speech_objs if obj["uniq_id"] == uniq_id ]
                if speech_obj:
                    speech_obj = speech_obj[0]
                    duration = speech_obj["duration"]  

                if process_mode == "byscript":
                    duration = math.ceil(duration)


            if "start_frames" in image:
                speech_obj = [obj for obj in all_speech_objs if obj["uniq_id"] == "project_intro" ]
                if speech_obj:
                    speech_obj = speech_obj[0]
                    duration = speech_obj["duration"]

                if process_mode == "byscript":
                    duration = math.ceil(duration)

            if "_preview_frames" in image:
                speech_obj = [obj for obj in all_speech_objs if obj["uniq_id"] == "feature_intro" ]
                if speech_obj:
                    speech_obj = speech_obj[0] 
                    duration_ = speech_obj["duration"] 
                    #print("the duration of _preview_frames ", duration_, " the duff us ", abs(duration_ - 10.2))
                    if process_mode == "legacy":
                        duration = 5 +  abs(duration_ - 10.2)

          
         
            total_duration = total_duration + duration

            # if "_preview_frames" in image:
            #     total_preview_frames_duration = total_preview_frames_duration + duration

            # Write the file command for this image
            file.write(f"file '{os.path.join('', image)}'\n")

            # Write the duration command for this image
            file.write(f"duration {duration}\n")

            if "_feature_frames" in image:
                current_feature_index = current_feature_index + 1
            #it is a feature frame

    # For the concat demuxer, the last file should not have a duration specified
    # So, we add the last file entry again without a duration
        file.write(f"file '{os.path.join('', image_files[-1])}'\n") 


    convert_to_stereo_48khz_16bit(tts_output_filename, tts_output_2_channel_filename)
    run_ffmpeg_v5(directory_name, folder_name, temp_text_file, tts_output_2_channel_filename, total_duration) 
    return flush_video_images(directory_name, folder_name)


def copy_intro_assets(dst_folder):
    
    src_folder = pkg_resources.resource_filename('video_images_creator', "intro_outro_assets") 
      # Create the destination folder if it doesn't exist
    if not os.path.exists(dst_folder):
        os.makedirs(dst_folder)
    
    # Copy each item from source to destination
    for item in os.listdir(src_folder):
        src_path = os.path.join(src_folder, item)
        dst_path = os.path.join(dst_folder, item)
        
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)

def read_image_resized(image_url, mode=1):

    resp = urlopen(image_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_UNCHANGED) # The image object 

    # # Check if the image has an alpha channel
    # if image.shape[2] == 3:  # If it's a 3-channel image (no alpha)
    #     # Convert to 4-channel
    #     image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    if mode == 1:
         ## for transition animation
        image = cv2.resize(image, (308, 668))  
    elif mode == 2:
        image = cv2.resize(image, (310, 672))
    else:
        image = cv2.resize(image, (306, 663))
       
    return image

def combined_image_op_v2(image_url, corner_radius): 
    if corner_radius == 23:
        mode = 2
    else:
        mode = 1

    overlay = read_image_resized(image_url, mode) 

    if overlay.shape[2] == 4:
        mask = create_rounded_mask_4_channel(overlay, corner_radius) 
    else:
        mask = create_rounded_mask(overlay, corner_radius)

    rounded_image = get_rounded_image(overlay, mask)
    return rounded_image

def create_overlayed_image_transition(input_image, feature_image_urls_, alpha_val, output_filename, enable_second_layer, alpha_val_second_layer, enable_third_layer, alpha_val_third_layer): 

    if alpha_val == 0:
        shutil.copyfile(input_image, output_filename)
        return

    x = 808
    y = 208
    transparency = alpha_val
    second_layer_transparency = alpha_val_second_layer
    third_layer_transparency = alpha_val_third_layer

    #print(list(feature_images.keys()))  

    # Load the background image with alpha channel
    background = cv2.imread(input_image, cv2.IMREAD_UNCHANGED)

    # Load the overlay image with alpha channel
    #overlay = cv2.imread('common_assets/rounded_corners.png', cv2.IMREAD_UNCHANGED)  


    # overlay = read_image_resized(feature_image_urls[0])
    # mask = create_rounded_mask(overlay, 30) 
    # rounded_image = get_rounded_image(overlay, mask) 

    #overlay = combined_image_op_v2(feature_image_urls[0],30)

    #print(feature_image_urls[0]) 

    #overlay = feature_images[feature_image_urls[0]]  

    #print(feature_image_urls)  

    #center image 

    image_url = feature_image_urls_[0]

    if image_url in feature_images.keys() and alpha_val > 0.0:
        overlay_ = feature_images[image_url]
    else:
        overlay_ = combined_image_op_v2(image_url, 30)
        feature_images[image_url] = overlay_ 

    overlay = overlay_.copy()   

    #left image to center image

    image_url = feature_image_urls_[1] 

    if image_url in feature_images.keys():
        second_image_overlay_ = feature_images[image_url]
    else:
        second_image_overlay_ = combined_image_op_v2(image_url, 30)
        feature_images[image_url] = second_image_overlay_ 

    second_image_overlay = second_image_overlay_.copy() 

    #right image to center image 

    image_url = feature_image_urls_[2] 

    if image_url in feature_images.keys():
        third_image_overlay_ = feature_images[image_url]
    else:
        third_image_overlay_ = combined_image_op_v2(image_url, 30)
        feature_images[image_url] = third_image_overlay_ 

    third_image_overlay = third_image_overlay_.copy() 


    image_url = feature_image_urls_[3]

    if image_url in feature_images.keys():
        fourth_image_overlay_ = feature_images[image_url]
    else:
        fourth_image_overlay_ = combined_image_op_v2(image_url, 30)
        feature_images[image_url] = fourth_image_overlay_  

    fourth_image_overlay = fourth_image_overlay_.copy()

    image_url = feature_image_urls_[4]

    if image_url in feature_images.keys():
        fifth_image_overlay_ = feature_images[image_url]
    else:
        fifth_image_overlay_ = combined_image_op_v2(image_url, 30)
        feature_images[image_url] = fifth_image_overlay_ 

    fifth_image_overlay = fifth_image_overlay_.copy()


    #cv2.imwrite("testing.png", overlay)

    #print(type(overlay), type(feature_images[feature_image_urls[0]]), np.array_equal(overlay, feature_images[feature_image_urls[0]]))

    

    #overlay = feature_images[feature_image_urls[0]]

    #overlay = cv2.imread('common_assets/rounded_corners.png', cv2.IMREAD_UNCHANGED)

    # second_layer_overlay = feature_images[feature_image_urls[1]] 
    # third_layer_overlay = feature_images[feature_image_urls[2]]

    # Ensure the overlay image is not larger than the background
    h_o, w_o, _ = overlay.shape

    # print(overlay.shape)  # Should be (height, width, 4)
    # print(transparency)  # Should be between 0 and 1
    # print(second_layer_overlay.shape)
    # print(second_layer_transparency)
    # print(third_layer_overlay.shape)
    # print(third_layer_transparency)

    # Modify the alpha channel of the overlay
    if overlay.shape[2] == 4:  # Check if the overlay has an alpha channel
        overlay[:, :, 3] = (overlay[:, :, 3] * transparency).astype(np.uint8) 
        second_image_overlay[:, :, 3] = (second_image_overlay[:, :, 3] * second_layer_transparency).astype(np.uint8)
        third_image_overlay_[:, :, 3] = (third_image_overlay_[:, :, 3] * second_layer_transparency).astype(np.uint8)
        fourth_image_overlay[:, :, 3] = (fourth_image_overlay[:, :, 3] * third_layer_transparency).astype(np.uint8)
        fifth_image_overlay[:, :, 3] = (fifth_image_overlay[:, :, 3] * third_layer_transparency).astype(np.uint8)


    # if overlay.shape[2] == 4:  # Ensure the overlay has an alpha channel
    #     overlay[:, :, 3] = (overlay[:, :, 3] * np.clip(transparency, 0, 1)).astype(np.uint8)
    #     second_layer_overlay[:, :, 3] = (second_layer_overlay[:, :, 3] * np.clip(second_layer_transparency, 0, 1)).astype(np.uint8)
    #     third_layer_overlay[:, :, 3] = (third_layer_overlay[:, :, 3] * np.clip(third_layer_transparency, 0, 1)).astype(np.uint8)

    #cv2.imshow("testoverlay",overlay) 
    #cv2.waitKey(0)
        

    # Check dimensions to ensure the overlay fits the background
    if y + h_o > background.shape[0] or x + w_o > background.shape[1]:
        raise ValueError("Overlay image exceeds the dimensions of the background image.") 
    
    if overlay.shape[2] == 4:
        alpha_overlay = overlay[:, :, 3] / 255.0
        alpha_background = 1.0 - alpha_overlay
        #print("overlay has case 1")
        #print("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    else:
        #print("overlay has case 2")
        #print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
    # Handle the case where there's no alpha channel
        alpha_overlay = np.ones((overlay.shape[0], overlay.shape[1]), dtype=np.float32)

    # Extract the alpha channel from the overlay
    # alpha_overlay = overlay[:, :, 3] / 255.0  # Normalize alpha to [0, 1]
      # Inverse alpha for the background 

    if second_image_overlay.shape[2] == 4:
        #print("second overlay has case 1")
        second_layer_alpha_overlay = second_image_overlay[:, :, 3] / 255.0
    else:
    # Handle the case where there's no alpha channel
        #print("second overlay has case 2")
        second_layer_alpha_overlay = np.ones((second_image_overlay.shape[0], second_image_overlay.shape[1]), dtype=np.float32)

    #second_layer_alpha_overlay = second_layer_overlay[:, :, 3] / 255.0  # Normalize alpha to [0, 1]
    second_layer_alpha_background = 1.0 - second_layer_alpha_overlay  # Inverse alpha for the background

    if fourth_image_overlay.shape[2] == 4:
        #print("third overlay has case 1")
        third_layer_alpha_overlay = fourth_image_overlay[:, :, 3] / 255.0
    else:
    # Handle the case where there's no alpha channel
        #print("third overlay has case 2")
        third_layer_alpha_overlay = np.ones((fourth_image_overlay.shape[0], fourth_image_overlay.shape[1]), dtype=np.float32)


    #third_layer_alpha_overlay = third_layer_overlay[:, :, 3] / 255.0  # Normalize alpha to [0, 1]
    third_layer_alpha_background = 1.0 - third_layer_alpha_overlay  # Inverse alpha for the background

    # Loop through the RGB channels
    for c in range(0, 3):
        # First layer blend 

        x = 807
        y = 206
        background[y:y+h_o, x:x+w_o, c] = (
            alpha_overlay * overlay[:, :, c] +
            alpha_background * background[y:y+h_o, x:x+w_o, c]
        )

        if enable_second_layer:
            # Second layer, first position
            x = 457
            y = 206
            background[y:y+h_o, x:x+w_o, c] = (
                second_layer_alpha_overlay * second_image_overlay[:, :, c] +
                second_layer_alpha_background * background[y:y+h_o, x:x+w_o, c]
            )

            # Second layer, second position
            x = 1159
            y = 206
            background[y:y+h_o, x:x+w_o, c] = (
                second_layer_alpha_overlay * third_image_overlay[:, :, c] +
                second_layer_alpha_background * background[y:y+h_o, x:x+w_o, c]
            ) 

        if enable_third_layer:
             # Second layer, first position
            x = 109
            y = 206
            background[y:y+h_o, x:x+w_o, c] = (
                third_layer_alpha_overlay * fourth_image_overlay[:, :, c] +
                third_layer_alpha_background * background[y:y+h_o, x:x+w_o, c]
            )

            # Second layer, second position
            x = 1514
            y = 206
            background[y:y+h_o, x:x+w_o, c] = (
                third_layer_alpha_overlay * fifth_image_overlay[:, :, c] +
                third_layer_alpha_background * background[y:y+h_o, x:x+w_o, c]
            ) 



    # Save the final image
    cv2.imwrite(output_filename, background)

def create_feature_set_frames_v3(running_index, frames_file_path, output_directory, feature_image_urls, feature_intro_audio_length): 


    f = open(frames_file_path, "a")
    #assets_path = "transition_assets/*.png" 

    assets_path = pkg_resources.resource_filename('video_images_creator', "transition_assets/*png") 


    assets_path_wo_wildcard = pkg_resources.resource_filename('video_images_creator', "transition_assets") 
    files_list = [f for f in glob.glob(assets_path) ] 
    sorted_list = sorted(files_list, key=lambda x: int(x.split("/")[-1].split(".")[0].split("_")[1]) ) 

    alpha = 0.1
    second_layer_alpha = 0.1
    third_layer_alpha = 0.1
    index = 1
    increement_mode = True
    enable_second_layer = False 
    enable_third_layer = False 

    temp_duration = 0.0

    #feature_images_urls_ = ["https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/56400089/b5383d80b7594ec3.png","https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/56400123/6d9eaea577134226.png","https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/56400125/1ad7960372754e01.png","https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/56400095/bdcd80bfc6f94704.png","https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/56400093/12ebb54b06b14fcc.png"]  

    feature_images_urls_ = feature_image_urls

   

    # for img_url in feature_images_urls:
    #     feature_images[img_url] = combined_image_op_v2(img_url,30) 
    
    # print("LEN OF FEATURE IMAGES !!!!",len(feature_images)) 

    total_def_duration = 0.0
    temp_index = 1

    for file in sorted_list: 

        file_name = f"image_{running_index}.png"
        duration = 1/30.0 
        total_def_duration = total_def_duration + duration 
        print("file name for ", file_name, ' temp index is : ', temp_index)
        if feature_intro_audio_length != -1:
            if feature_intro_audio_length > 4.02 and running_index == 330:
                duration = feature_intro_audio_length - 4.0
                print("duration updated to : ", duration)

        duration = round(duration, 6)

        temp_duration = temp_duration + duration 


        f.write(f"file '{file_name}'\n")
        f.write(f"duration {duration:.6f}\n")

        if file in [f"{assets_path_wo_wildcard}/image_32.png"]:
            enable_second_layer = True 
        if file in [f"{assets_path_wo_wildcard}/image_61.png"]:
            enable_third_layer = True
        if file in [f"{assets_path_wo_wildcard}/image_120.png"]:
            increement_mode = False
        if file in [f"{assets_path_wo_wildcard}/image_1.png", f"{assets_path_wo_wildcard}/image_2.png"]:
            create_overlayed_image_transition(file, feature_images_urls_, 0, f"{output_directory}/image_{running_index}.png", enable_second_layer, 0, enable_third_layer, 0)
        else:
            create_overlayed_image_transition(file, feature_images_urls_, alpha, f"{output_directory}/image_{running_index}.png", enable_second_layer, second_layer_alpha, enable_third_layer, third_layer_alpha)
            if increement_mode == True:
                alpha = alpha + 0.05 
                alpha = min(1.0, alpha) 
                if enable_second_layer:
                    second_layer_alpha = second_layer_alpha + 0.045
                    second_layer_alpha = min(1.0, second_layer_alpha) 
                if enable_third_layer:
                    third_layer_alpha = third_layer_alpha + 0.045
                    third_layer_alpha = min(1.0, third_layer_alpha) 

            else: 
                alpha = alpha - 0.05
                alpha = max(0.2, alpha)
                if enable_second_layer:
                    second_layer_alpha = second_layer_alpha - 0.05
                    second_layer_alpha = max(0.2, second_layer_alpha) 
                if enable_third_layer:
                    third_layer_alpha = third_layer_alpha - 0.05
                    third_layer_alpha = max(0.2, third_layer_alpha) 
        index = index + 1
        running_index = running_index + 1 
        temp_index = temp_index + 1


    duration = 1/30.0

    shutil.copy(f"{assets_path_wo_wildcard}/image_1.png", f"{output_directory}/image_{running_index}.png")  
    file_name = f"image_{running_index}.png"
    f.write(f"file '{file_name}'\n")
    f.write(f"duration {duration:.6f}\n") 

    temp_duration = temp_duration + duration

    print("total_def_duration is add 0.06 ", total_def_duration)



    running_index = running_index + 1

    shutil.copy(f"{assets_path_wo_wildcard}/image_1.png", f"{output_directory}/image_{running_index}.png") 
    file_name = f"image_{running_index}.png"
    f.write(f"file '{file_name}'\n")
    f.write(f"duration {duration:.6f}\n") 

    temp_duration = temp_duration + duration 

    running_index = running_index + 1 


    f.close()
    return (running_index, temp_duration) 

def cv2_put_text_with_custom_font(img, text, position, font_path, font_size, font_color, max_width):
    # Convert the image to RGB (OpenCV uses BGR)
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    
    # Load the custom font
    font = ImageFont.truetype(font_path, font_size)
    
    # Create a draw object
    draw = ImageDraw.Draw(img_pil) 

    lines = []
    space_split_strs = text.split(" ")
    current_str = "" 
    for word in space_split_strs:
        if len(current_str + " " + word) < max_width:
            current_str = current_str + " " + word
        else:
            #current_str = current_str + " " + word
            lines.append(current_str.strip()) 
            current_str = word

    lines.append(current_str.strip())
    
    for line in lines:
        draw.text(position, line, font=font, fill=font_color)
        position = (position[0], position[1] + 51)

   
    
    # Convert back to BGR for OpenCV
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR) 

def create_overlayed_second_animation(input_image, alpha_val, output_filename, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, image_url, anim_mode):
    
    background = cv2.imread(input_image, cv2.IMREAD_UNCHANGED) 
    #font_path = "features/segoe-ui-symbol.ttf" 

    font_path = pkg_resources.resource_filename('video_images_creator', 'Segoe-UI-Symbol.ttf')

    if alpha_val == 0.0: 
        
        #puts "BLANK TEXT : ", 
        input_image = cv2_put_text_with_custom_font(background, text, (200,380), font_path, 45, (255,255,255), 35) 
        cv2.imwrite(output_filename, input_image) 
        #shutil.copyfile(input_image, output_filename)
        return
    
    # Load the background image with alpha channel
     
    # Load the overlay image with alpha channel 

    if anim_mode == 1:
        overlay_ = second_anim_images[image_url] 
    else:
        overlay_ = switch_anim_images[image_url]

    overlay = overlay_.copy()

    # cv2.imshow("tyyty", overlay) 

    # cv2.waitKey(0)


    #overlay = cv2.imread('common_assets/framed.png', cv2.IMREAD_UNCHANGED)
    
    # Resize the overlay image
    h_o, w_o = overlay.shape[:2]
    new_h_o = int(h_o * scale_factor_y)
    new_w_o = int(w_o * scale_factor_x)
    overlay_resized = cv2.resize(overlay, (new_w_o, new_h_o), interpolation=cv2.INTER_LINEAR)
    
    # # Crop the overlay image
    # if crop_width is None:
    #     crop_width = overlay_resized.shape[1] - crop_x
    # if crop_height is None:
    #     crop_height = overlay_resized.shape[0] - crop_y
    
    # overlay_cropped = overlay_resized[crop_y:crop_y+crop_height, crop_x:crop_x+crop_width] 

    overlay_cropped = overlay_resized
    
    # Ensure the overlay fits within the background
    h_o, w_o = overlay_cropped.shape[:2]
    if y + h_o > background.shape[0]:
        h_o = background.shape[0] - y
        overlay_cropped = overlay_cropped[:h_o, :, :]
    if x + w_o > background.shape[1]:
        w_o = background.shape[1] - x
        overlay_cropped = overlay_cropped[:, :w_o, :]
    
    # Separate the color and alpha channels
    if overlay_cropped.shape[2] == 4:
        overlay_colors = overlay_cropped[:, :, :3]
        overlay_alpha = overlay_cropped[:, :, 3] / 255.0 * alpha_val
    else:
        overlay_colors = overlay_cropped
        overlay_alpha = np.ones((h_o, w_o)) * alpha_val
    
    # Extract the region of interest from the background
    roi = background[y:y+h_o, x:x+w_o]
    
    # Ensure roi and overlay_colors have the same shape
    roi = roi[:overlay_colors.shape[0], :overlay_colors.shape[1]]
    
    # Create a mask of the overlay
    overlay_mask = np.dstack([overlay_alpha] * 3)
    
    # Blend the overlay with the background
    blended = np.where(overlay_mask, 
                       (overlay_colors.astype(float) * overlay_mask + 
                        roi.astype(float) * (1 - overlay_mask)).astype(np.uint8),
                       roi)
    
    # Apply the blended image to the background
    background[y:y+h_o, x:x+w_o] = blended 

    font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    org = (50, 50)

    # fontScale
    fontScale = 1
    
    # Blue color in BGR
    color = (255, 0, 0)

    # Line thickness of 2 px
    thickness = 2 

    

# # img_with_text = cv2_put_text_with_custom_font(
# #     img,
# #     "Hello, Segoe UI Symbol! ☺",
# #     (x, y),
# #     font_path,
# #     36,
# #     (255, 255, 255)  # White color
# # ) 

    background = cv2_put_text_with_custom_font(background, text, (200,380), font_path, 45, (255,255,255), 35)

    
    # Using cv2.putText() method
    #background = cv2.putText(background, f"{output_filename} {x} {y} {scale_factor_x} {scale_factor_y} {alpha_val}", org, font, fontScale, color, thickness, cv2.LINE_AA)
    
    # Save the final image 
  
    cv2.imwrite(output_filename, background)

def build_first_feature_animation(output_directory, running_index, frames_file_path, image_url, continuation_mode, current_text, residual_time):


    initial_running_index = running_index

    if continuation_mode == False:
        initial_running_index = 0 
    else:
        initial_running_index = running_index 


    x = 1200
    y = 210
    scale_factor_x = 1.0
    scale_factor_y = 1.0
    crop_x = 0
    crop_y = 0
    crop_width = None
    crop_height = None
    f_name = pkg_resources.resource_filename('video_images_creator', "background_new_design.png") 
    temp_index = 0
    alpha_val = 0.1
    total_duration_in_step = 0.0

    destination_folder = output_directory
    f = open(frames_file_path, 'a') 
    overlay_ = combined_image_with_border_op_v2(image_url, 25, 1)
    overlay = overlay_.copy()
    second_anim_images[image_url] = overlay

    text = ""
    index_t = 0 

    temp_duration = 0.0

    for index in range(1,150):

        destination = f"{destination_folder}/image_{running_index}_20.png"
        file = f"image_{running_index}_20.png"
        duration = 0.04 
        y = int(y - 0.1)
        y = max(y,60)
        scale_factor_x = scale_factor_x + 0.0015
        scale_factor_y = scale_factor_y + 0.0015
        scale_factor_x = min(scale_factor_x, 1.6) 
        scale_factor_y = min(scale_factor_y, 1.6)
        alpha_val = alpha_val + 0.01
        if index > 50 and index < 100:
            alpha_val = alpha_val + 0.06
            alpha_val = min(alpha_val, 1.0)
        if index > 100 and index < 145:
            alpha_val = alpha_val - 0.06
            alpha_val = max(alpha_val, 0.0) 
        if index > 141:
            alpha_val = alpha_val - 0.09

        # if index == 64:
        #     duration = 2.0
        # else:
        #     duration = 0.04 

        if residual_time > 0.0 and index == 64:
            duration = duration + residual_time

        # print("duration = ", duration, " for index ", index, " and running_index ", running_index)

        alpha_val = min(alpha_val, 1.0) 
        alpha_val = max(alpha_val, 0.0)
        duration = round(duration, 6) 


        f.write(f"file '{file}'\n")
        f.write(f"duration {duration:.6f}\n")  

        temp_duration = temp_duration + duration

        text = current_text[:initial_running_index]

        create_overlayed_second_animation(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, image_url, 1) 

        running_index = running_index + 1

        initial_running_index = initial_running_index + 1

    #print("duration of first animation is ", temp_duration)
         


    f.close()

    return (running_index, temp_duration) 


def fast_overlay(background_path, overlay, position=(13, 13)):
    # Read the background and overlay images, keeping the alpha channel if present
    background = cv2.imread(background_path, cv2.IMREAD_UNCHANGED)
    #overlay = cv2.imread(overlay_path, cv2.IMREAD_UNCHANGED)

    # Resize the background to the specified size
    background = cv2.resize(background, (334, 689))

    # Get dimensions of overlay image
    h, w = overlay.shape[:2]

    # Extract the region of interest (ROI) from the background
    x, y = position
    roi = background[y:y+h, x:x+w]

    # Split the overlay into its color and alpha channels
    if overlay.shape[2] == 4:
        overlay_img = overlay[:, :, :3]  # Get the RGB channels
        mask = overlay[:, :, 3] / 255.0  # Get the alpha channel and normalize to [0, 1]
    else:
        overlay_img = overlay
        mask = np.ones((h, w), dtype=np.float32)  # No alpha, so use a mask of 1s

    # If the background has an alpha channel, split it
    if background.shape[2] == 4:
        roi_img = roi[:, :, :3]
        roi_alpha = roi[:, :, 3] / 255.0
    else:
        roi_img = roi
        roi_alpha = np.ones((h, w), dtype=np.float32)

    # Combine the overlay and background images
    combined_alpha = mask + roi_alpha * (1 - mask)
    for c in range(0, 3):
        roi_img[:, :, c] = (1 - mask) * roi_img[:, :, c] + mask * overlay_img[:, :, c]

    # Reassemble the final image with the combined alpha
    if background.shape[2] == 4:
        background[y:y+h, x:x+w] = np.dstack([roi_img, combined_alpha * 255])
    else:
        background[y:y+h, x:x+w] = roi_img

    return background

def create_rounded_mask_4_channel(image, corner_radius):
    # Create an empty mask with 4 channels (RGBA)
    mask = np.zeros_like(image, dtype=np.uint8)

    # Set the alpha channel (4th channel) to be fully transparent (0) initially
    mask[:, :, 3] = 0

    # Draw white ellipses at the corners to define the rounded corners in the alpha channel
    cv2.ellipse(mask, (corner_radius, corner_radius), (corner_radius, corner_radius), 180, 0, 90, (255, 255, 255, 255), -1)
    cv2.ellipse(mask, (image.shape[1] - corner_radius, corner_radius), (corner_radius, corner_radius), 270, 0, 90, (255, 255, 255, 255), -1)
    cv2.ellipse(mask, (corner_radius, image.shape[0] - corner_radius), (corner_radius, corner_radius), 90, 0, 90, (255, 255, 255, 255), -1)
    cv2.ellipse(mask, (image.shape[1] - corner_radius, image.shape[0] - corner_radius), (corner_radius, corner_radius), 0, 0, 90, (255, 255, 255, 255), -1)

    # Draw rectangles to fill the interior parts of the mask in the alpha channel
    cv2.rectangle(mask, (corner_radius, 0), (image.shape[1] - corner_radius, image.shape[0]), (255, 255, 255, 255), -1)
    cv2.rectangle(mask, (0, corner_radius), (image.shape[1], image.shape[0] - corner_radius), (255, 255, 255, 255), -1)

    # The first three channels (R, G, B) can remain black or any value, as the alpha channel dictates transparency.
    return mask

def combined_image_with_border_op_v2(image_url, corner_radius, type):

    overlay = read_image_resized(image_url,2)   
    if overlay.shape[2] == 4:
        mask = create_rounded_mask_4_channel(overlay, corner_radius) 
    else:
        mask = create_rounded_mask(overlay, corner_radius)
    rounded_image = get_rounded_image(overlay, mask)
    #border_image = cv2.imread("common_assets/border.png", cv2.IMREAD_UNCHANGED) 
    #print("will do overlayyyy!!!!")

    border_path = pkg_resources.resource_filename('video_images_creator', "device_border.png")

    rounded_bordered_image = fast_overlay(border_path, rounded_image)
    return rounded_bordered_image

def build_feature_switch_anim(output_directory, running_index, temp_text_file, image_url, continuation_mode, current_text, residual_time):

    destination_folder = output_directory 

    # print("the current text ... ", current_text, " current index ", running_index, "continuation mode: ", continuation_mode)

    if continuation_mode == False:
        initial_running_index = 0
    else:
        initial_running_index = running_index 


    index = 1
    alpha_val = 1.0
    x = 1380
    y = 205
    scale_factor_x = 1.0
    scale_factor_y = 1.0
    crop_x = 0
    crop_y = 0
    crop_width = None
    crop_height = None
    f_name = pkg_resources.resource_filename('video_images_creator', "background_new_design.png")
    temp_index = 0
    alpha_val = 0.05

    # cv2.imshow("testing", mask) 
    # cv2.waitKey(0)
    overlay_ = combined_image_with_border_op_v2(image_url, 25, 2)
    overlay = overlay_.copy()
    switch_anim_images[image_url] = overlay  

    temp_duration = 0.0


    #right to left movement

    f = open(temp_text_file,'a') 

    current_t_index = running_index

    ### the switch frames #######

    for index in range(1,50):
        destination = f"{destination_folder}/image_{running_index}_20.png"
        file = f"image_{running_index}_20.png"
        duration = 0.002
        alpha_val = alpha_val + 0.01
        x = x - 2
        # if index % 2 == 0:
        #     alpha_val = alpha_val + 0.03
        #     x = x - 4 
        # if index % 4 == 0:
        #     alpha_val = alpha_val + 0.03
        #     # scale_factor_x = scale_factor_x - 0.01 
        #     # scale_factor_y = scale_factor_y - 0.01
        alpha_val = min(alpha_val, 1.0)

        # if continuation_mode == False:
        #     text_index = ( ( initial_running_index + running_index ) % initial_running_index ) + 1

        # else:
        #     text_index = ( ( initial_running_index + running_index ) ) + 1 

        text = current_text[:initial_running_index]
        
       
    
        create_overlayed_second_animation(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, image_url, 2)
        f.write(f"file '{file}'\n") 
        duration = round(duration, 6)
        f.write(f"duration {duration:.6f}\n") 

        temp_duration = temp_duration + duration

        for i in range(10):
            running_index = running_index + 1 
            #create more copies for smoother transition 

            n_destination =  f"{destination_folder}/image_{running_index}_20.png" 
            file = f"image_{running_index}_20.png"
            shutil.copy(destination, n_destination)
            f.write(f"file '{file}'\n")
            f.write(f"duration {duration:.6f}\n")
            temp_duration = temp_duration + duration 

        initial_running_index = initial_running_index + 1

    #print("temp duration for switch animation is : ", temp_duration)  

    

        
    temp_index = running_index


    #grow to dim 

    alpha_val = 1.0 
    temp_index = temp_index + 1 
    dim_index = 0
    for index in range(temp_index, (temp_index + 60)):
        destination = f"{destination_folder}/image_{running_index}_20.png"
        file = f"image_{running_index}_20.png"
        dim_index = dim_index + 1
        duration = 0.04
        # if dim_index == 2:
        #     duration = 2.0
            
        # else:
        #     duration = 0.04

        if residual_time > 0.0 and dim_index == 1:
             duration = duration + residual_time
             #print("added residual time in switch animation ", " time:  ", residual_time, " at index  ", running_index)

        duration = round(duration, 6) 
        temp_duration = temp_duration + duration 

        
    
        f.write(f"file '{file}'\n")
        f.write(f"duration {duration:.6f}\n")


        # if continuation_mode == False:
        #     text_index = ( ( initial_running_index + running_index ) % initial_running_index ) + 1 
        # else:
        #     text_index = ( ( initial_running_index + running_index ) ) + 1  

        text = current_text[:initial_running_index]
        
        
        if dim_index == 1:
            
            create_overlayed_second_animation(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, image_url, 2) 

            for temp_i in range(64):

                running_index = running_index + 1 
                destination = f"{destination_folder}/image_{running_index}_20.png"
                file = f"image_{running_index}_20.png"
                initial_running_index = initial_running_index + 1
                duration = 0.04

                f.write(f"file '{file}'\n")
                f.write(f"duration {duration:.6f}\n") 
                temp_duration = temp_duration + duration 

                text = current_text[:initial_running_index]
                create_overlayed_second_animation(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, image_url, 2) 


        else:
            create_overlayed_second_animation(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, image_url, 2) 





        #print("index : ", running_index, ' file ', file, 'alpha_val ', alpha_val, 'dim_index', dim_index)
        create_overlayed_second_animation(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, image_url, 2) 

        scale_factor_x = scale_factor_x + 0.02
        scale_factor_y = scale_factor_y + 0.02 
        scale_factor_x = min(scale_factor_x, 1.6) 
        scale_factor_y = min(scale_factor_y, 1.6)
        alpha_val = alpha_val - 0.03 
        if index > 50:
            alpha_val = alpha_val - 0.06 
        alpha_val = max(alpha_val, 0.0) 
    
        x = x - 2
        y = y - 4
        #x = min(x, 1100)
        y = max(y, 0)

        running_index = running_index + 1 
        initial_running_index = initial_running_index + 1

    return (running_index, temp_duration)

def create_overlayed_third_anim(input_image, alpha_val, output_filename, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, image_url):
    if alpha_val == 0:
        shutil.copyfile(input_image, output_filename)
        return

    # Load the background image with alpha channel
    #background = cv2.imread(input_image, cv2.IMREAD_UNCHANGED) 

    f_name = pkg_resources.resource_filename('video_images_creator', "background_new_design.png") 
    background = cv2.imread(f_name, cv2.IMREAD_UNCHANGED)

    # if image_url in third_feature_images.keys() and alpha_val > 0.0:
    #     overlay_ = third_feature_images[image_url]
    # else:
    #     overlay_ = combined_image_op_v2(image_url, 23)
    #     third_feature_images[image_url] = overlay_  


    if image_url in third_feature_images.keys() and alpha_val > 0.0:
        overlay_ = third_feature_images[image_url]
    else:
        overlay_ = combined_image_with_border_op_v2(image_url, 25, 3)
        third_feature_images[image_url] = overlay_
       

    overlay = overlay_.copy()   
    
    # Load the overlay image with alpha channel
    #overlay = cv2.imread('common_assets/rounded_corners_2.png', cv2.IMREAD_UNCHANGED)
    
    # Resize the overlay image
    h_o, w_o = overlay.shape[:2]
    new_h_o = int(h_o * scale_factor_y)
    new_w_o = int(w_o * scale_factor_x)
    overlay_resized = cv2.resize(overlay, (new_w_o, new_h_o), interpolation=cv2.INTER_LINEAR)
    
    # Crop the overlay image
    # if crop_width is None:
    #     crop_width = overlay_resized.shape[1] - crop_x
    # if crop_height is None:
    #     crop_height = overlay_resized.shape[0] - crop_y
    
    # overlay_cropped = overlay_resized[crop_y:crop_y+crop_height, crop_x:crop_x+crop_width]

    overlay_cropped = overlay_resized
    
    # Ensure the overlay fits within the background
    h_o, w_o = overlay_cropped.shape[:2]
    if y + h_o > background.shape[0]:
        h_o = background.shape[0] - y
        overlay_cropped = overlay_cropped[:h_o, :, :]
    if x + w_o > background.shape[1]:
        w_o = background.shape[1] - x
        overlay_cropped = overlay_cropped[:, :w_o, :]
    
    # Separate the color and alpha channels
    if overlay_cropped.shape[2] == 4:
        overlay_colors = overlay_cropped[:, :, :3]
        overlay_alpha = overlay_cropped[:, :, 3] / 255.0 * alpha_val
    else:
        overlay_colors = overlay_cropped
        overlay_alpha = np.ones((h_o, w_o)) * alpha_val
    
    # Extract the region of interest from the background
    roi = background[y:y+h_o, x:x+w_o]
    
    # Ensure roi and overlay_colors have the same shape
    roi = roi[:overlay_colors.shape[0], :overlay_colors.shape[1]]
    
    # Create a mask of the overlay
    overlay_mask = np.dstack([overlay_alpha] * 3)
    
    # Blend the overlay with the background
    blended = np.where(overlay_mask, 
                       (overlay_colors.astype(float) * overlay_mask + 
                        roi.astype(float) * (1 - overlay_mask)).astype(np.uint8),
                       roi)
    
    # Apply the blended image to the background
    background[y:y+h_o, x:x+w_o] = blended 

    font = cv2.FONT_HERSHEY_SIMPLEX

    # org
    org = (50, 50)

    # fontScale
    fontScale = 1
    
    # Blue color in BGR
    color = (255, 0, 0)

    # Line thickness of 2 px
    thickness = 1
    
    # Using cv2.putText() metho

    font_path = pkg_resources.resource_filename('video_images_creator', 'Segoe-UI-Symbol.ttf')

    background = cv2_put_text_with_custom_font(background, text, (200,380), font_path, 45, (255,255,255), 35)
    #background = cv2.putText(background, output_filename, org, font, fontScale, color, thickness, cv2.LINE_AA)
    
    # Save the final image
    cv2.imwrite(output_filename, background)


def build_third_animation(output_directory, running_index, temp_text_file, feature_image_url, continuation_mode, current_text, residual_time): 

    third_anim_assets_folder = src_folder = pkg_resources.resource_filename('video_images_creator', "third_anim_assets/*.png")

    files_list = [f for f in glob.glob(third_anim_assets_folder) ]  
    destination_folder = output_directory

    f = open(temp_text_file,'a') 
    sorted_list = sorted(files_list, key=lambda x: int(x.split("/")[-1].split(".")[0].split("_")[1]) )

    initial_running_index = running_index

    if continuation_mode == False:
        initial_running_index = 0 
    else:
        initial_running_index = running_index

    index = 1
    alpha_val = 1.0
    x = 600
    y = -1
    scale_factor_x = 4.7
    scale_factor_y = 1.63 

    temp_duration = 0.0


    for f_name in sorted_list:
        
        # count = int(f_name.split("/")[2].split("_")[2].split(".")[0]) 
        #count = int(f_name.split("/")[1].split("_")[2].split(".")[0]) 
        count = int(f_name.split("/")[-1].split("_")[-1].split(".")[0])
        pre_count = int(f_name.split("/")[-1].split("_")[1])

        text = current_text[:initial_running_index]
            
     
        destination = f"{destination_folder}/image_{running_index}_{count}.png"
        file = f"image_{running_index}_{count}.png"
        # if index == 18:
        #     duration = 0.6
        # elif index < 18:
        #     duration = 0.038
        # elif index == 56:
        #     duration = 0.3
        # else:
        #     duration = 0.01 

        # if residual_time > 0.0 and index == 18: 
        #     duration = max(duration, residual_time)

        duration = 0.04

        if residual_time > 0.0 and index == 18:
            duration = duration + residual_time
            #print("residual_time_added_in_third_animation ..... ", duration, " at file ", file)
        #print("file : ", file, 'index : ', index, ' duration: ', duration) 
        duration = round(duration, 6)

        f.write(f"file '{file}'\n")
        f.write(f"duration {duration:.6f}\n")  

        temp_duration = temp_duration + duration
        
        if f_name.endswith(tuple(["third_anim_assets/image_1_1.png", "third_anim_assets/image_2_1.png", "third_anim_assets/image_3_1.png", "third_anim_assets/image_4_1.png", "third_anim_assets/image_5_1.png", "third_anim_assets/image_56_5.png"])):
            shutil.copy(f_name, destination)
        else:
            if f_name.endswith("third_anim_assets/image_6_1.png"): 
                x = 490
                y = 0
                scale_factor_x = 5
                scale_factor_y = 3
                crop_x = 0
                crop_y = 0
                crop_height = 1100
                crop_width = 1600 
                alpha_val = 0.1
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url) 
            elif f_name.endswith("third_anim_assets/image_7_1.png"):
                x = 692
                y = 0
                scale_factor_x = 5
                scale_factor_y = 3
                crop_x = 0
                crop_y = 0
                crop_height = 1080 
                alpha_val = 0.1
                crop_width = 1250
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url)
            elif f_name.endswith("third_anim_assets/image_8_1.png"):
                x = 830
                y = 0
                scale_factor_x = 5
                scale_factor_y = 3
                crop_x = 0
                crop_y = 0
                crop_height = 1080 
                alpha_val = 0.1
                crop_width = 1090
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url)
            elif f_name.endswith("third_anim_assets/image_9_1.png"):
                x = 920
                y = 0
                scale_factor_x = 3.12
                scale_factor_y = 3
                crop_x = 0
                crop_y = 0
                crop_height = 1100
                alpha_val = 0.4
                crop_width = 1200
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url)
            elif f_name.endswith("third_anim_assets/image_10_1.png"):
                x = 976
                y = 74
                scale_factor_x = 2.67
                scale_factor_y = 2.67
                crop_x = 0
                crop_y = 0
                crop_height = 1000
                alpha_val = 0.4
                crop_width = 1000
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url)
            elif f_name.endswith("third_anim_assets/image_11_1.png"):
                x = 1022
                y = 138
                scale_factor_x = 2.37
                scale_factor_y = 2.37
                crop_x = 0
                crop_y = 0
                crop_height = 950
                alpha_val = 0.4
                crop_width = 800
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url)
            elif f_name.endswith("third_anim_assets/image_12_1.png"):
                x = 1053
                y = 183
                scale_factor_x = 2.17
                scale_factor_y = 2.17
                crop_x = 0
                crop_y = 0
                crop_height = 900
                alpha_val = 0.6
                crop_width = 800
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url) 
            elif f_name.endswith("third_anim_assets/image_13_1.png"):
                x = 1073
                y = 213
                scale_factor_x = 2.04
                scale_factor_y = 2.04
                crop_x = 0
                crop_y = 0
                crop_height = 900
                alpha_val = 0.6
                crop_width = 800
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url) 
            elif f_name.endswith("third_anim_assets/image_14_1.png"):
                x = 1082
                y = 233
                scale_factor_x = 2
                scale_factor_y = 2
                crop_x = 0
                crop_y = 0
                crop_height = 850 
                alpha_val = 0.6
                crop_width = 750
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url)
            elif f_name.endswith("third_anim_assets/image_15_1.png"):
                x = 1091
                y = 250
                scale_factor_x = 1.92
                scale_factor_y = 1.92
                crop_x = 0
                crop_y = 0
                crop_height = 850
                alpha_val = 0.8
                crop_width = 600
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url)
            elif f_name.endswith("third_anim_assets/image_16_1.png"):
                x = 1100
                y = 252
                scale_factor_x = 1.86
                scale_factor_y = 1.86
                crop_x = 0
                crop_y = 0
                crop_height = 850
                alpha_val = 1.0
                crop_width = 600
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url)
            elif f_name.endswith("third_anim_assets/image_17_1.png"):
                x = 1110
                y = 258
                scale_factor_x = 1.8
                scale_factor_y = 1.8
                crop_x = 0
                crop_y = 0
                crop_height = 850 
                alpha_val = 1.0
                crop_width = 600
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url)
            elif f_name.endswith(tuple(["third_anim_assets/image_18_1.png", "third_anim_assets/image_19_1.png", "third_anim_assets/image_20_1.png"])):
                x = 1110
                y = 265
                scale_factor_x = 1.8
                scale_factor_y = 1.8
                crop_x = 0
                crop_y = 0
                crop_height = 850
                alpha_val = 1.0
                crop_width = 600
                if f_name.endswith("third_anim_assets/image_18_1.png"):
                    create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url)     

                    for temp_i in range(50):
                        index = index + 1
                        running_index = running_index + 1
                        initial_running_index = initial_running_index + 1


                        destination = f"{destination_folder}/image_{running_index}_{count}.png"
                        #destination = f"{destination_folder}/image_{running_index}.png"
                        file = f"image_{running_index}_{count}.png"
                        duration = 0.04
                        temp_duration = temp_duration + 0.04
                        f.write(f"file '{file}'\n")
                        f.write(f"duration {duration:.6f}\n")
                        text = current_text[:initial_running_index]   
                        create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url)     

                else:
                    create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url)      
            elif f_name.endswith("third_anim_assets/image_21_1.png"): 
                x = 1110
                y = 265
                scale_factor_x = 1.8
                scale_factor_y = 1.8
                crop_x = 0
                crop_y = 0
                crop_height = 850
                alpha_val = 1.0
                crop_width = 600
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url) 
            else:  
                x = 1110
                y = 265
                scale_factor_x = 1.8
                scale_factor_y = 1.8
                crop_x = 0
                crop_y = 0
                crop_height = 850
                if pre_count >= 46:
                    alpha_val = alpha_val - 0.2
                    alpha_val = max(alpha_val, 0.1)
                crop_width = 600
                create_overlayed_third_anim(f_name, alpha_val, destination, x, y, scale_factor_x, scale_factor_y, crop_x, crop_y, crop_width, crop_height, text, feature_image_url)
        index = index + 1
        running_index = running_index + 1 
        initial_running_index = initial_running_index + 1 

    f.close 
    return (running_index, temp_duration) 

def add_feature_frames_v2(current_running_index, temp_text_file, directory, feature_images_urls, feature_desciption, feature_speech_objs,  total_intitial_audio_duration, total_intitial_video_duration):


    index = 0

    #feature_images_urls = feature_images_urls[:6] 
    index = 1 
    continuation_mode = False 
    prev_text = ""

    show_first_feature_anim = False
    show_switch_feature_anim = False 
    show_third_feature_anim = False
    current_step_duration = 0.0
    animation_no = 1 
    current_total_duration = total_intitial_video_duration
    current_total_audio_duration = total_intitial_audio_duration
    added_previous_residual_time = False
    first_anim_default_duration = 5.96
    switch_feature_default_duraion = 6.038
    third_anim_default_duration = 4.24

    for feature_images_url in feature_images_urls:  

        current_text = feature_desciption[index - 1] 
        feature_speech_obj = feature_speech_objs[index - 1]
        residual_time = -1
        #print(feature_speech_obj) 
        total_audio_duration_in_step = feature_speech_obj["total_audio_duration_in_step"]
        is_last_audio_in_step = feature_speech_obj["is_last_audio_in_step"] 
        current_total_audio_duration = current_total_audio_duration + feature_speech_obj['duration'] 
        animation_no = feature_speech_obj['animation_type'] 
        audio_index = feature_speech_obj['audio_index']


        if current_text == "<break time='200ms'/>..":
            continuation_mode = True 
            current_text = prev_text
        else:
            continuation_mode = False
            current_step_duration = 0.0

        if continuation_mode == False:

            # if index > 1:
            #     animation_no = random.choice([1,2,3])
                

            if animation_no == 1:
                show_first_feature_anim = True
                show_switch_feature_anim = False 
                show_third_feature_anim = False

            elif animation_no == 2:
                show_first_feature_anim = False
                show_switch_feature_anim = True 
                show_third_feature_anim = False 

            else:
                show_first_feature_anim = False 
                show_switch_feature_anim = False 
                show_third_feature_anim = True


        #print("processing index is : ", index, " animation no is ", animation_no, " continuation mode is ", continuation_mode, ' text is ', feature_speech_obj['text'])

        if show_first_feature_anim == True:

            #current_step_duration = current_step_duration + first_anim_default_duration
          

            residual_time = 0.0

            if is_last_audio_in_step:

                temp_current_total_duration = current_total_duration

                #print("the total_audio_duration_in_step in this step was :", total_audio_duration_in_step," all together audio duraion is ", current_total_audio_duration , " all together video duration will be ", temp_current_total_duration + first_anim_default_duration, ' the audio index is : ', audio_index, ' 1st anim  added', first_anim_default_duration ) 

                if ( temp_current_total_duration + first_anim_default_duration ) < current_total_audio_duration:

                    temp_current_total_duration = temp_current_total_duration + first_anim_default_duration
                    residual_time = abs( current_total_audio_duration - temp_current_total_duration )
                    print("in the first anim step, the residual time is  ", residual_time, " current_step_duration ", current_step_duration, " total_audio_duration_in_step ", total_audio_duration_in_step)





            # if is_last_audio_in_step and ( current_step_duration <  total_audio_duration_in_step )
            #     residual_time = abs(( current_total_duration + 5.96  ) - current_total_audio_duration)
            #     print("found residual for build_first_feature_animation", residual_time, ' total_audio_duration_in_step ', current_total_audio_duration , ' current_step_duration ', ( current_total_duration + + 5.96  ) )

            (current_running_index, duration_added) = build_first_feature_animation(directory, current_running_index, temp_text_file, feature_images_url, continuation_mode, current_text, residual_time)
            show_switch_feature_anim = True
            show_first_feature_anim = False
            show_third_feature_anim = False  
            #print("first feature animation duration : ", duration_added)

            current_total_duration = current_total_duration + duration_added 
            
            
        elif show_switch_feature_anim == True:

            #current_step_duration = current_step_duration + switch_feature_default_duraion
            #current_step_duration = current_step_duration + 0.3
            residual_time = 0.0
            # if is_last_audio_in_step and ( current_total_duration + 5.44  ) < current_total_audio_duration:
            #     residual_time = abs(( current_total_duration + 5.44  ) - current_total_audio_duration)
            #     print("found residual for build_feature_switch_anim", residual_time, ' total_audio_duration_in_step ', current_total_audio_duration, ' current_step_duration ', ( current_total_duration + 5.44 ) )


            if is_last_audio_in_step:

                temp_current_total_duration = current_total_duration 

                #print("the total_audio_duration_in_step in this step was :", total_audio_duration_in_step," all together audio duraion is ", current_total_audio_duration , " all together video duration will be ", temp_current_total_duration + switch_feature_default_duraion, ' the audio index is : ', audio_index, ' switch anim  added', switch_feature_default_duraion )

                if ( temp_current_total_duration + switch_feature_default_duraion ) < current_total_audio_duration:

                    temp_current_total_duration = temp_current_total_duration + switch_feature_default_duraion
                    residual_time = abs( current_total_audio_duration - temp_current_total_duration )
                    print("in the switch anim step, the residual time is  ", residual_time, " current_step_duration ", current_step_duration, " total_audio_duration_in_step ", total_audio_duration_in_step)

            (current_running_index, duration_added) = build_feature_switch_anim(directory, current_running_index, temp_text_file, feature_images_url, continuation_mode, current_text, residual_time) 
            show_third_feature_anim = True 
            show_switch_feature_anim = False 
            show_first_feature_anim = False
            #print("switch feature animation duration : ", duration_added) 

            current_total_duration = current_total_duration + duration_added 
            
           
        elif show_third_feature_anim == True: 

            residual_time = 0.0 
            #current_step_duration = current_step_duration +  third_anim_default_duration
            #current_step_duration = current_step_duration + 0.3

            # if is_last_audio_in_step and ( current_total_duration + 4.12  ) < current_total_audio_duration:
            #     residual_time = abs(( current_total_duration + 4.12  ) - current_total_audio_duration)
            #     print("found residual for build_third_animation", residual_time, ' total_audio_duration_in_step ', current_total_audio_duration, ' current_step_duration ', ( current_total_duration + 4.12 ) )


            if is_last_audio_in_step: 

                ## check if default duration is less than audio track length 

                temp_current_total_duration = current_total_duration

                #print("the total_audio_duration_in_step in this step was :", total_audio_duration_in_step," all together audio duraion is ", current_total_audio_duration , " all together video duration will be ", temp_current_total_duration + third_anim_default_duration, ' the audio index is : ', audio_index, ' 3rd anim  added', third_anim_default_duration )

                if ( temp_current_total_duration + third_anim_default_duration ) < current_total_audio_duration:

                    temp_current_total_duration = temp_current_total_duration + third_anim_default_duration
                    residual_time = abs( current_total_audio_duration - temp_current_total_duration )
                    print("in the third anim step, the residual time is  ", residual_time, " current_step_duration ", current_step_duration, " total_audio_duration_in_step ", total_audio_duration_in_step)




                # residual_time = abs( current_step_duration - total_audio_duration_in_step)

                # if added_previous_residual_time == False:
                #     residual_time = residual_time + 0.33
                #     added_previous_residual_time = True
                #     print("the added_previous_residual_time time was adedd !!!!")
                # print("total_audio_duration_in_step ", total_audio_duration_in_step, "current step duration : ", current_step_duration)
                
             
                
                # if residual_time > 0.1 and current_step_duration < total_audio_duration_in_step:
                #     print("found residual for build_first_feature_animation", residual_time, ' total_audio_duration_in_step ', total_audio_duration_in_step , ' current_step_duration ', ( current_step_duration  ) )

            (current_running_index, duration_added) = build_third_animation(directory, current_running_index, temp_text_file, feature_images_url, continuation_mode, current_text, residual_time) 
            show_first_feature_anim = True 
            show_switch_feature_anim = False 
            show_third_feature_anim = False
            #print("third feature animation duration : ", duration_added) 

            current_total_duration = current_total_duration + duration_added 
           

        index = index + 1

        if continuation_mode is False:
            prev_text = current_text 

        #print("current video duration is : ", current_total_duration, ' current audio duration is ', current_total_audio_duration)


        #prev_text = current_text if continuation_mode is False else ""

    return current_running_index  

def copy_outro_assets(dst_folder, current_index, frames_txt_file):

    src_folder = pkg_resources.resource_filename('video_images_creator', "intro_outro_assets")   
    f = open(frames_txt_file, 'a')

    files_list = [f for f in glob.glob(f"{src_folder}/*.png") ]  

    sorted_list = sorted(files_list, key=lambda x: int( x.split("/")[-1].split("_")[1]  ) ) 

    for file in sorted_list:
        count = file.split("/")[-1].split("_")[2].split(".")[0]
        file_name = f"image_{current_index}_{count}.png" 
        file_name_w_dst = f"{dst_folder}/{file_name}"
        duration = 0.015 
        if "image_1_5.png" in file:
            duration = 0.166667 
        if "image_175_34.png" in file:
            duration = 1.133333
        if "image_176_99.png" in file:
            duration = 3.300000
        shutil.copy(file, file_name_w_dst)
        f.write(f"file '{file_name}'\n")
        f.write(f"duration {duration:.6f}\n") 
        current_index = current_index + 1 

    f.write(f"file '{file_name}'\n")
    f.close()
    return current_index 

def build_speech_objects(z):
    
    local_duration = 0
    for i in range(len(z)):
        if z[i]['type'] == 'feature_description':
            
            if z[i]['text'] != "<break time='200ms'/>..":
                local_duration = 0

            local_duration = local_duration + z[i]['duration']
            z[i]['total_audio_duration_in_step'] = local_duration
            if (i + 1) < len(z) and z[i+1]['text'] != "<break time='200ms'/>.." and z[i]['text'] == "<break time='200ms'/>.." :
                z[i]['is_last_audio_in_step'] = True
            elif i + 1 >= len(z) and z[i]['text'] == "<break time='200ms'/>..":
                z[i]['is_last_audio_in_step'] = True 
            else:
                z[i]['is_last_audio_in_step'] = False 
        else:
            z[i]['is_last_audio_in_step'] = False 
            z[i]['total_audio_duration_in_step'] = 1.0
    return z

def modify_last_duration(file_path, new_duration, new_file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the last occurrence of 'duration' and replace the value
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith('duration'):
            lines[i] = f'duration {new_duration}\n'
            break

    # Write the modified lines back to the file
    with open(new_file_path, 'w') as file:
        file.writelines(lines)

def build_with_new_design(build_card_name, feature_descriptions, intro_text, preview_screen_text, process_mode, feature_images_urls, feature_ids, existing_audios, device, preview_feature_image_urls, feature_names, subscription_key, service_region):
    
    ensure_required_directories_existis()
    current_index = 1
    folder_name = generate_random_string(10)  
    directory_name = f'images/{folder_name}/audios'
    os.makedirs(directory_name, exist_ok=True) 

    directory_name = f'images/{folder_name}'
    tts_audios_folder = f'images/{folder_name}/audios'
    tts_output_filename = f'{directory_name}/tts_outfile_name.wav'
    tts_output_2_channel_filename = f'{directory_name}/tts_2_chnl_outfile_name.wav'
    project_intro_text = f"Hey, I am Natasha, We are excited to share with you the prototype for {build_card_name} that we have designed.<break time='500ms'/>"
    feature_intro_text = f"Starting with the {feature_names[0]} users will be able to then interact with {feature_names[1]} and {feature_names[2]} <break time='200ms'/> "
    feature_count_stepwise = compute_feature_count_stepwise(feature_descriptions) 
    #print("feature_count_stepwise ", feature_count_stepwise)


    if process_mode == "byscript":
        project_intro_text = f"{intro_text}<break time='100ms'/>"
        feature_intro_text = f"{preview_screen_text}..<break time='600ms'/>"

    if process_mode == "legacy":
        preview_feature_image_urls = feature_images_urls[:5]


    pattern = r"[\n\r\t]|<p>|<br>|<b>|</p>|</br>|&nbsp;|&#39;"
    feature_desciption_stripped = ""

    for fd in feature_descriptions:
        feature_desciption_stripped = feature_desciption_stripped + " " + re.sub(pattern, '', fd)

    # terminal_image_path = pkg_resources.resource_filename('video_images_creator', "terminal.png")
    # terminal_image = cv2.imread(terminal_image_path)

    # pre_terminal_image_path = pkg_resources.resource_filename('video_images_creator', "preterminal.png")
    # preterminal_image = cv2.imread(pre_terminal_image_path)



    terminal_image_frames = 500 
    preterminal_image_frames = 70 
    if process_mode == "byscript":
        terminal_image_frames = 200
        preterminal_image_frames = 35


    #image_files = sorted([f for f in os.listdir(directory_name) if f.endswith(('.jpg', '.png'))], key=sort_key)  

    all_speech_objs = [] 
    
    
    project_intro_speech_obj = {
        "text": project_intro_text,
        "type": "project_intro",
        "uniq_id": "project_intro",
        "audio_index": 0,
        "generate_audio": True,
        "audio_blob_url": "",
        "step_feature_count": 1,
        "is_last_audio_in_step": False,
        "animation_type": 1
    }

    all_speech_objs.append(project_intro_speech_obj) 


    post_intro_speech_obj = {
        "text": "Over the next few minutes we will walk through the app.<break time='200ms'/>",
        "type": "post_intro",
        "uniq_id": "post_intro",
        "audio_index": 1,
        "generate_audio": True,
        "audio_blob_url": "",
        "step_feature_count": 1,
        "is_last_audio_in_step": False,
        "animation_type": 1
    } 

    if process_mode == "legacy":
        all_speech_objs.append(post_intro_speech_obj) 


    features_intro_speech_obj = {
        "text": feature_intro_text,
        "type": "feature_intro",
        "uniq_id": "feature_intro",
        "audio_index": 2,
        "generate_audio": True,
        "audio_blob_url": "",
        "step_feature_count": 1,
        "is_last_audio_in_step": False,
        "animation_type": 1
    } 

    all_speech_objs.append(features_intro_speech_obj)

    audio_index = 3
    feature_index = 0

    feature_desciption_formatted = [] 

    feature_desciption_index = 0
    animation_type = 1

    for fd in feature_descriptions:
        pattern = r"[\n\r\t]|<p>|<br>|<b>|</p>|</br>|&nbsp;|&#39;"
        feature_desciption_ = re.sub(pattern, '', fd)
        is_last_audio_in_step = False
        continuation_mode = False 
        #feature_desciption_ = feature_desciption_.replace("<break time='600ms'/>","") 

        if fd == "<break time='200ms'/>..":
            continuation_mode = True

        if feature_desciption_index + 1 < len(feature_descriptions) and feature_descriptions[feature_desciption_index + 1 ] != "<break time='200ms'/>.." and feature_descriptions[feature_desciption_index] == "<break time='200ms'/>..":
            is_last_audio_in_step = True 
        elif feature_desciption_index + 1 >= len(feature_descriptions) and feature_descriptions[feature_desciption_index] == "<break time='200ms'/>..":
            is_last_audio_in_step = True 
        else:
            is_last_audio_in_step = False

        #print("the continuation_mode ", continuation_mode, " feature_desciption_index ", feature_desciption_index, "description ", fd)

        if continuation_mode == False:
            if feature_desciption_index == 0:
                animation_type = 1
            else:
                animation_type = random.choice([1,2,3])
        else:
            if animation_type == 1:
                animation_type = 2
            elif animation_type == 2:
                animation_type = 3
            elif animation_type == 3:
                animation_type = 1

        #print("animation type will be ", animation_type)

        feature_desciption_formatted.append(feature_desciption_)
        feature_desciption_speech_obj = {
            "text": feature_desciption_,
            "type": "feature_description",
            "uniq_id": feature_ids[feature_index],
            "audio_index": audio_index,
            "generate_audio": not(existing_audios[feature_index] == ""),
            "audio_blob_url": existing_audios[feature_index],
            "step_feature_count": feature_count_stepwise[feature_index],
            "is_last_audio_in_step": is_last_audio_in_step,
            "animation_type": animation_type
        }

        audio_index = audio_index + 1
        feature_index = feature_index + 1
        all_speech_objs.append(feature_desciption_speech_obj)  

        feature_desciption_index = feature_desciption_index + 1

    #print("the prev speech obj: ", all_speech_objs)

    all_speech_objs = run_parallel_tts_process(all_speech_objs, subscription_key, service_region, tts_audios_folder, process_mode, 2) 

    all_audio_file_names = [item['filename'] for item in all_speech_objs if 'filename' in item]

    combine_wav_files(tts_output_filename, all_audio_file_names) 

    all_speech_objs = build_speech_objects(all_speech_objs)

    print(all_speech_objs)

    feature_speech_objs = all_speech_objs[2:] ### we skip intro and feature intro 

    #print("the audio length off ")

    #project_intro_audio_length = feature_speech_objs[0]['']

    feature_intro_audio_length = -1

    try:
        feature_intro_audio_length = [k for k in all_speech_objs if k['type'] == 'feature_intro'][0]['duration']
    except:
        print("exception occured !!!") 


 


    temp_text_file = f'{directory_name}/temp_ffmpeg_list.txt' 

    copy_intro_assets(directory_name) 

    current_running_index = 212

    (current_running_index, video_duration) = create_feature_set_frames_v3(current_running_index, temp_text_file, directory_name, preview_feature_image_urls, feature_intro_audio_length) 

    intro_audio_duration = all_speech_objs[0]['duration']
    total_intitial_audio_duration = sum(obj['duration'] for obj in all_speech_objs[:2])
    extra_residual_in_intro_frames = 0.0

    if intro_audio_duration > 7.0:
        extra_residual_in_intro_frames = intro_audio_duration - 7.0

    if extra_residual_in_intro_frames > 0.0:
        new_duration = 7.16 + extra_residual_in_intro_frames
        modify_last_duration(temp_text_file, new_duration, temp_text_file)


    total_intitial_video_duration = video_duration + 7.16 + extra_residual_in_intro_frames

    # print("the initial total video_duration is", total_intitial_video_duration, ' total audio duration is ', 16.5) 


    current_running_index = add_feature_frames_v2(current_running_index, temp_text_file, directory_name, feature_images_urls, feature_descriptions, feature_speech_objs, total_intitial_audio_duration, total_intitial_video_duration) 

    copy_outro_assets(directory_name, current_running_index, temp_text_file) 


    convert_to_stereo_48khz_16bit(tts_output_filename, tts_output_2_channel_filename)
    run_ffmpeg_v6(temp_text_file, tts_output_2_channel_filename, folder_name) 
    return flush_video_images(directory_name, folder_name)


def run_ffmpeg_v6(temp_text_file, tts_output_2_channel_filename, uniq_code):

    thanks_audio_path = pkg_resources.resource_filename('video_images_creator', 'thanks.wav')
    background_audio_path = pkg_resources.resource_filename('video_images_creator', 'background_music.wav') 

    # jpg_files = glob.glob(os.path.join(directory_name, '*.jpg'))
    # number_of_jpg_files = len(jpg_files) 
    # #delay_for_thanks = floor( number_of_jpg_files / 60 ) * 1000

    # delay_for_thanks = ( floor( total_duration - 3.0 ) ) * 1000

    # delay_for_thanks = delay_for_thanks + 14000


    video_creation_with_audio_command = [
    "ffmpeg",
    "-y",
    "-f", "concat",  # Use the concat demuxer
    "-safe", "0",  # Allow use of absolute paths
    "-i", temp_text_file,  # Input video list
    "-i", tts_output_2_channel_filename,  # Main audio (synthesized speech)
    "-stream_loop", "-1",  # Loop the background audio indefinitely
    "-i", background_audio_path,  # Background audio
    "-filter_complex", "[2:a]volume=0.35[aud2];[1:a][aud2]amix=inputs=2:duration=first[aout]",  # Mix audio and set background volume
    "-pix_fmt", "yuv420p",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-vsync", "vfr",
    "-c:a", "aac",
    "-map", "0:v:0",  # Map video from the first input
    "-map", "[aout]",  # Map the mixed audio
    f"outputs/output_{uniq_code}.mp4"  # Output video with audio
]

    subprocess.run(video_creation_with_audio_command)

    


def build_v3(process_dict):

    feature_images_urls = process_dict["image_urls"] 
    feature_names = process_dict["feature_names"] 
    feature_descriptions = process_dict["feature_desciptions"] 
    feature_ids = process_dict["feature_ids"]
    existing_audios = process_dict["audio_script_blob_urls"] 
    build_card_name = process_dict["project_name"] 
    subscription_key = process_dict["subscription_key"]
    service_region = process_dict["service_region"] 
    intro_text = process_dict["intro_text"]
    preview_screen_text = process_dict["preview_screen_text"]
    preview_feature_image_urls = process_dict["preview_feature_image_urls"]  
    process_mode = process_dict["process_mode"]
    device = process_dict["device"]
    new_design_flow = False 

    
    if device is None:
        device = "mobile"

    if process_mode is None:
        process_mode = "legacy"

    if device == "mobile" and process_mode == "byscript":
        new_design_flow = True

    #print("new_design_flow", new_design_flow)

    if new_design_flow: 
        return build_with_new_design(build_card_name, feature_descriptions, intro_text, preview_screen_text, process_mode, feature_images_urls, feature_ids, existing_audios, device, preview_feature_image_urls, feature_names, subscription_key, service_region)
    else:
        return build_with_old_design(build_card_name, feature_descriptions, intro_text, preview_screen_text, process_mode, feature_images_urls, feature_ids, existing_audios, device, preview_feature_image_urls, feature_names, subscription_key, service_region) 

    

   


        



        


   

    








def build(image_file_paths, feature_names, project_name, logo_url):
    ensure_required_directories_existis()
    current_index = 0
    folder_name = generate_random_string(10)  
    directory_name = f'images/{folder_name}' 
    bg_image_path = pkg_resources.resource_filename('video_images_creator', "builderbackground.png") 
    bg_img = cv2.imread(bg_image_path) 
  
  
    os.mkdir(directory_name) 
    put_project_name(bg_img, project_name, directory_name, logo_url)
    for index in range(len(image_file_paths) - 1):
        if index % 2 == 0:
            current_index = create_right_to_left_movement(image_file_paths[index + 1], image_file_paths[index], current_index, directory_name, project_name, feature_names[index], feature_names[index + 1], bg_img) 
        else:
            current_index = create_left_to_right_movement(image_file_paths[index], image_file_paths[index + 1], current_index, directory_name, project_name, feature_names[index], feature_names[index+1], bg_img) 
        #print("done for feature index ", index)

    create_ending_frames(current_index, directory_name, ending_page_image) 
    #print("done with creation of ending frames")
    run_ffmpeg(directory_name, folder_name) 
    return flush_video_images(directory_name, folder_name) 

def put_project_name(bg_image, project_name, directory_name, logo_url): 

    project_name_x = 80
    logo_to_be_added = False
    # if logo_url:
    #     logo = read_image(logo_url)
    #     logo_height, logo_width, _ = logo.shape
    #     new_logo_width = min(logo_width, 130)
    #     new_logo_height = min(logo_height, 130)
    #     #logo = cv2.resize(logo, (new_logo_width, new_logo_height))  
    #     logo = logo[0:new_logo_height, 0:new_logo_width]
    #     logo_to_be_added = True
    #     if new_logo_width == 130:
    #         project_name_x = 150
    #     else:
    #         project_name_x = project_name_x + int(( 130 - new_logo_width ) * 1.9 )
    
    pil_image = Image.fromarray(cv2.cvtColor(bg_image, cv2.COLOR_BGR2RGB)) 
    draw = ImageDraw.Draw(pil_image)
    font_path = pkg_resources.resource_filename('video_images_creator', 'Rubik-Medium.ttf')
    font_size = 27
    font = ImageFont.truetype(font_path, font_size) 
    draw.text((project_name_x, 40), project_name, font=font, fill=(255, 255, 255)) 
    bg_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    if logo_to_be_added:
        bg_image[20:20+new_logo_height, 10:10+new_logo_width] = logo
    #bg_image[20:20+new_logo_height, 10:10+new_logo_width] = logo
    # Save and return the modified image
    cv2.imwrite(f'{directory_name}/bg_img.jpg', bg_image)   

    image_path = pkg_resources.resource_filename('video_images_creator', "combined_left.jpg")
    bg_image = cv2.imread(image_path)
    pil_image = Image.fromarray(cv2.cvtColor(bg_image, cv2.COLOR_BGR2RGB))   
    draw = ImageDraw.Draw(pil_image)
    draw.text((project_name_x, 40), project_name, font=font, fill=(255, 255, 255))  
    bg_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR) 
    if logo_to_be_added:
        bg_image[20:20+new_logo_height, 10:10+new_logo_width] = logo
    #bg_image[20:20+new_logo_height, 10:10+new_logo_width] = logo
    # Save and return the modified image
    cv2.imwrite(f'{directory_name}/combined_left_new.jpg', bg_image)   

    image_path = pkg_resources.resource_filename('video_images_creator', "combined_right.jpg")
    bg_image = cv2.imread(image_path)
    pil_image = Image.fromarray(cv2.cvtColor(bg_image, cv2.COLOR_BGR2RGB))   
    draw = ImageDraw.Draw(pil_image)
    draw.text((project_name_x, 40), project_name, font=font, fill=(255, 255, 255)) 
    bg_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR) 
    if logo_to_be_added:
        bg_image[20:20+new_logo_height, 10:10+new_logo_width] = logo
    #bg_image[20:20+new_logo_height, 10:10+new_logo_width] = logo
    # Save and return the modified image
    cv2.imwrite(f'{directory_name}/combined_right_new.jpg', bg_image) 
    
def create_ending_frames(current_index, directory_name, ending_page_image):
    for i in range(110): 
        index = current_index + i
        destination = f'{directory_name}/frame_{index}.jpg'
        #shutil.copyfile(img1, destination)
        cv2.imwrite(destination, ending_page_image)


def create_left_to_right_movement(left_image_file_path, right_image_file_path, current_index_, directory_name, project_name, left_screen_name, right_screen_name, bg_img):

    #create images  

    #print("inside left to right movement method")

    left_image_file_name = left_image_file_path
    right_image_file_name = right_image_file_path

    parent_current_index = current_index_
    left_image = build_screen_optimised(left_image_file_name, f'{directory_name}/combined_left_image_{current_index_}.jpg', 455, directory_name, 'left')
    right_image = build_screen_optimised(right_image_file_name, f'{directory_name}/combined_right_image_{current_index_}.jpg', 1179, directory_name, 'right')  

    #print("built parent screens")

    put_text(f'{directory_name}/combined_left_image_with_name_{current_index_}.jpg', left_image, left_screen_name, project_name, 455) 
    put_text(f'{directory_name}/combined_right_image_with_name_{current_index_}.jpg', right_image, right_screen_name, project_name, 1179) 

    #print("added texts")

    # left_image_with_name = build_screen(left_image_file_name, f'{directory_name}/combined_left_image_with_name_{current_index_}.jpg', 455, left_screen_name, True)
    # right_image_with_name = build_screen(right_image_file_name, f'{directory_name}/combined_right_image_with_name_{current_index_}.jpg', 1179, right_screen_name, True) 




    img1 = cv2.imread(left_image)
    img2 = cv2.imread(right_image) 

    #bg_img = read_image("https://builderbuckets.blob.core.windows.net/builder-now-beta/builderbackground.png")





    #these are for feature transitions 
    start_point = np.array([455, 218])  
    end_point = np.array([1179, 218])   


    obj_width = 305
    obj_height = 643


    #  #create 40 copies of image with names
    # current_index = current_index_

    # file_name =  f'combined_left_image_with_name${parent_current_index}.jpg'
    # for i in range(40): 
    #     index = i + current_index_
    #     destination = f'./images/frame_{index}.jpg'
    #     shutil.copyfile(file_name, destination)
    #     current_index = current_index + 1



    #create 20 copies of image without names
    current_index = current_index_

    #create 20 copies of img1

    file_name = f'{directory_name}/combined_left_image_{parent_current_index}.jpg'
    for i in range(20): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    num_frames = 70
    
    #print("added images for left without text")



    temp_current_index = current_index 

    bg_img = cv2.imread(f'{directory_name}/bg_img.jpg')

    for i in range(num_frames):
        t = i / float(num_frames)  

        
        position = (1 - t) * start_point + t * end_point  

        
        img = bg_img.copy()

        
        box1 = img1[int(start_point[1]):int(start_point[1] + obj_height), int(start_point[0]):int(start_point[0] + obj_width)]
        box2 = img2[int(end_point[1]):int(end_point[1] + obj_height), int(end_point[0]):int(end_point[0] + obj_width)] 


        # corner_radius = 30
        # mask = create_rounded_mask(box1, corner_radius)

        # # Generate the rounded image
        # box1 = get_rounded_image(box1, mask) 


        # corner_radius = 30
        # mask = create_rounded_mask(box2, corner_radius)

        # # Generate the rounded image 

        # box2 = get_rounded_image(box2, mask)

        
        transition_obj = (1 - t) * box1 + t * box2 


        transition_obj_h, transition_obj_w, _ = transition_obj.shape

        ch = min(transition_obj_h, int(position[1] + obj_height ) - int(position[1])) 
        cw = min(int(position[0] + obj_width) - int(position[0]), transition_obj_w) 

        img[int(position[1]): int(position[1]) + ch, int(position[0]): int(position[0]) + cw] = transition_obj 

        
        # transition_obj = refined_alpha_blend( img[int(position[1]): int(position[1]) + ch, int(position[0]): int(position[0]) + cw], transition_obj)
        # img[int(position[1]): int(position[1]) + ch, int(position[0]): int(position[0]) + cw] = transition_obj[:, :, :3]  # Only take BGR channels, ignore alpha 

        #frame_index = 76 + i + 2 

        frame_index = temp_current_index + i 
        
        cv2.imwrite(f'{directory_name}/frame_{frame_index}.jpg', img)  

        current_index = current_index + 1



    #create 20 copies of imgage without name 

    #print("created the intermediatory frames")

    current_index_ = current_index

    file_name =  f'{directory_name}/combined_right_image_{parent_current_index}.jpg'
    for i in range(20): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination) 
        current_index = current_index + 1

    current_index_ = current_index


    #print("added images for right")

    file_name =  f'{directory_name}/combined_right_image_with_name_{parent_current_index}.jpg'
    for i in range(40): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    #print("added images for right with name")

   

   

    return current_index


def filter_text(html_str):
    cleaned_text = re.sub(r'<style.*?>.*?</style>|<.*?>', '', html_str, flags=re.DOTALL)

    # Replace HTML entities with their associated characters
    cleaned_text = cleaned_text.replace('&nbsp;', ' ')
    cleaned_text = cleaned_text.replace('\r\n', ' ')  # Replace newline characters with a space
    cleaned_text = cleaned_text.replace('\t', ' ') 

    return cleaned_text


def put_text(combine_file_name, background, sceen_name, project_name, x_coordinate): 

    #print("### put text start")
    background = cv2.imread(background)
    pil_image = Image.fromarray(cv2.cvtColor(background, cv2.COLOR_BGR2RGB)) 
    #print("got pil image")



    #sceen_name = filter_text(sceen_name)
        
    # Load the custom font
    font_path = pkg_resources.resource_filename('video_images_creator', 'Rubik-Medium.ttf')
    title_font_path = pkg_resources.resource_filename('video_images_creator', 'Rubik-Bold.ttf')
    font_size = 59
    font = ImageFont.truetype(title_font_path, font_size)
    draw = ImageDraw.Draw(pil_image) 

    #print("loaded fonts")
    
    max_width = 450  # The maximum width for text 
    y = background.shape[0] - 600
    if x_coordinate != 455:
        lines = []
        words = sceen_name.split()
        #print("words are ", words)
        while words:
            line = ''
            #print("arg1", int(draw.textlength(line + words[0], font=font)), "- max_Width", max_width) 

            if int(draw.textlength(words[0], font=font)) > max_width:
                # Handle words that are too long
                # For now, we'll just append it to lines and continue
                lines.append(words.pop(0))
                continue
            while words and int(draw.textlength(line + words[0], font=font)) <= max_width: 
                #print("inside pop")
                line += (words.pop(0) + ' ')
            lines.append(line) 

        
        
        # Limit to 3 lines
        lines = lines[:3] 
        
        apply_indent = False 
        for i, line in enumerate(lines):
            x = x_coordinate - 450 
            line = line.strip()
            if ( x + len(line) ) >= 740 or apply_indent:
                apply_indent = True 
                x = x - 25
            draw.text((x, y + i*font_size), line.strip(), font=font, fill=(255, 255, 255))  
            #print("added text on right with row",i+1)
    else:
        x = x_coordinate + 350
        draw.text((x, y), sceen_name, font=font, fill=(255, 255, 255))  
        #print("added text on left")


    #add project name
    # if project_name:
    #     font_size = 27
    #     font = ImageFont.truetype(font_path, font_size) 
    #     draw.text((80, 40), project_name, font=font, fill=(255, 255, 255))

    # #add description
    # font_size = 30 
    # font_path = 'features/Rubik-Light.ttf'
    # font = ImageFont.truetype(font_path, font_size)
    # max_width = 580
    # lines = []
    # words = description.split()
    # while words:
    #     line = ''
    #     while words and int(draw.textlength(line + words[0], font=font)) <= max_width:
    #         line += (words.pop(0) + ' ')
    #     lines.append(line)
    
    # # Limit to 3 lines
    # lines = lines[:7]
    
    # y = background.shape[0] - 650
    # for i, line in enumerate(lines):
    #     if x_coordinate == 455:
    #         x = x_coordinate + 335
    #     else:
    #         x = x_coordinate - 600
    #     draw.text((x, y + i*font_size), line.strip(), font=font, fill=(255, 255, 255)) 



    background = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Save and return the modified image
    cv2.imwrite(combine_file_name, background) 

    #print("###put text end")



def create_right_to_left_movement(left_image_file_path, right_image_file_path, current_index_, directory_name, project_name, right_screen_name, left_screen_name, bg_img):
    #create images
    left_image_file_name = left_image_file_path
    right_image_file_name = right_image_file_path


    #print("inside left to right movement method")

    #images with no feature name
    parent_current_index = current_index_
    left_image = build_screen_optimised(left_image_file_name, f'{directory_name}/combined_left_image_{current_index_}.jpg', 455, directory_name, 'left')
    right_image = build_screen_optimised(right_image_file_name, f'{directory_name}/combined_right_image_{current_index_}.jpg', 1179, directory_name, 'right') 

    #print("created parent screens")

    #images with feature names
    put_text(f'{directory_name}/combined_left_image_with_name_{current_index_}.jpg', left_image, left_screen_name, project_name, 455) 
    put_text(f'{directory_name}/combined_right_image_with_name_{current_index_}.jpg', right_image, right_screen_name, project_name, 1179) 
    # left_image_with_name = build_screen(left_image_file_name, f'{directory_name}/combined_left_image_with_name_{current_index_}.jpg', 455, left_screen_name, True)
    # right_image_with_name = build_screen(right_image_file_name, f'{directory_name}/combined_right_image_with_name_{current_index_}.jpg', 1179, right_screen_name, True) 

      


    img1 = cv2.imread(left_image)
    img2 = cv2.imread(right_image) 

    #bg_img = read_image("https://builderbuckets.blob.core.windows.net/builder-now-beta/builderbackground.png")

    #these are for feature transitions 
    start_point = np.array([1179, 218])  
    end_point = np.array([455, 218])


    obj_width = 305
    obj_height = 643


    #create 40 copies of image with names
    current_index = current_index_

    file_name =  f'{directory_name}/combined_right_image_with_name_{parent_current_index}.jpg'
    for i in range(40): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    #print("added images for right with names")

    #create 20 copies of image without names
    current_index_ = current_index
    file_name =  f'{directory_name}/combined_right_image_{parent_current_index}.jpg'
    for i in range(20): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    num_frames = 70 



    temp_current_index = current_index 

    bg_img = cv2.imread(f'{directory_name}/bg_img.jpg')

    for i in range(0,num_frames):
        t = i / float(num_frames)  
        
        # Get current position 
        position = (1 - t) * start_point + t * end_point  
        
        # Create a copy of the background
        img = bg_img.copy()

        # Define object from img2
        box1 = img2[int(start_point[1]):int(start_point[1] + obj_height), int(start_point[0]):int(start_point[0] + obj_width)]
        # Define object from img1
        box2 = img1[int(end_point[1]):int(end_point[1] + obj_height), int(end_point[0]):int(end_point[0] + obj_width)]
        
        # If the transition is at the start, take the object from img2, otherwise take it from img1
        # if t <= 0.5:
        #     transition_obj = box1
        # else:
        #     transition_obj = box2  

        # corner_radius = 30
        # mask = create_rounded_mask(box1, corner_radius)

        # # Generate the rounded image
        # box1 = get_rounded_image(box1, mask)


        # corner_radius = 30
        # mask = create_rounded_mask(box2, corner_radius)

        # # Generate the rounded image
        # box2 = get_rounded_image(box2, mask)

        transition_obj = (1 - t) * box1 + t * box2

        transition_obj_h, transition_obj_w, _ = transition_obj.shape

        ch = min(transition_obj_h, int(position[1] + obj_height ) - int(position[1])) 
        cw = min(int(position[0] + obj_width) - int(position[0]), transition_obj_w) 
        
        # Add object to the current image
        img[int(position[1]): int(position[1]) + ch, int(position[0]): int(position[0]) + cw] = transition_obj

        # transition_obj = refined_alpha_blend( img[int(position[1]): int(position[1]) + ch, int(position[0]): int(position[0]) + cw], transition_obj)
        # img[int(position[1]): int(position[1]) + ch, int(position[0]): int(position[0]) + cw] = transition_obj[:, :, :3]  # Only take BGR channels, ignore alpha 

        #frame_index = 76 + i + 2 

        frame_index = temp_current_index + i 
        
        cv2.imwrite(f'{directory_name}/frame_{frame_index}.jpg', img)  

        current_index = current_index + 1



    current_index_ = current_index

    #print("added intermediatory frames")

    #create 25 copies of imgage without names

    file_name = f'{directory_name}/combined_left_image_{parent_current_index}.jpg'
    for i in range(25): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination) 
        current_index = current_index + 1


    #print("added images for left")



    #create 40 copies of image with names
    current_index_ = current_index

    file_name =  f'{directory_name}/combined_left_image_with_name_{parent_current_index}.jpg'
    for i in range(40): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    #print("added images for left with names")


    
  
    


   

    return current_index


def refined_alpha_blend(roi, overlay):
    # Extract the alpha channel and normalize it
    alpha = overlay[:, :, 3] / 255.0
    inverse_alpha = 1.0 - alpha

    # Ensure both images have 4 channels
    if roi.shape[2] == 3:
        roi = np.dstack([roi, np.ones((roi.shape[0], roi.shape[1]), dtype="uint8") * 255])

    # Premultiply RGB channels with the alpha
    overlay_premul = overlay.copy()
    roi_premul = roi.copy()
    for c in range(3):
        overlay_premul[:, :, c] = overlay_premul[:, :, c] * alpha
        roi_premul[:, :, c] = roi_premul[:, :, c] * inverse_alpha

    # Blend the premultiplied images
    blended = overlay_premul + roi_premul
    blended[:, :, 3] = overlay[:, :, 3]  # Set the alpha channel

    return blended

def get_rounded_image_old(image, mask):
    # Separate the color and alpha channels from the mask
    mask_color = mask[:, :, :3]
    mask_alpha = mask[:, :, 3] if mask.shape[2] == 4 else None

    # Apply the mask to get the rounded image
    rounded_img = cv2.bitwise_and(image, mask_color)
    
    # If the image doesn't already have an alpha channel, add one
    if image.shape[2] == 3:
        rounded_img = np.dstack([rounded_img, mask_alpha if mask_alpha is not None else mask_color[:, :, 0]])
    
    return rounded_img

def get_rounded_image(image, mask):
    # Check if the mask has 4 channels (RGBA)
    if mask.shape[2] == 4:
        # Separate the color (RGB) and alpha channels
        mask_color = mask[:, :, :3]
        mask_alpha = mask[:, :, 3]
    else:
        # If the mask only has 3 channels (RGB), no alpha channel
        mask_color = mask
        mask_alpha = None

    # Apply the mask to get the rounded image (compatible with both 3- and 4-channel images)
    if image.shape[2] == 4:
        # If the image has an alpha channel, keep the alpha in the final image
        image_color = image[:, :, :3]
        image_alpha = image[:, :, 3]
    else:
        # If the image doesn't have an alpha channel, treat it as RGB
        image_color = image
        image_alpha = None

    # Perform bitwise AND between image_color and mask_color
    rounded_img_color = cv2.bitwise_and(image_color, mask_color)

    # Combine color with alpha channels if needed
    if image_alpha is not None:
        if mask_alpha is not None:
            # Merge the color result and the product of image and mask alphas
            combined_alpha = cv2.bitwise_and(image_alpha, mask_alpha)
        else:
            # Use the image's own alpha if the mask has none
            combined_alpha = image_alpha
        rounded_img = np.dstack([rounded_img_color, combined_alpha])
    else:
        # If the image didn't have an alpha, add the mask's alpha or one channel as alpha
        if mask_alpha is not None:
            rounded_img = np.dstack([rounded_img_color, mask_alpha])
        else:
            # Default to using the mask's first channel as alpha if no true alpha is present
            rounded_img = np.dstack([rounded_img_color, mask_color[:, :, 0]])

    return rounded_img
    

def create_rounded_mask(image, corner_radius):
    mask = np.zeros_like(image)
    
    # Draw 4 ellipses at the corners to make them rounded
    cv2.ellipse(mask, (corner_radius, corner_radius), (corner_radius, corner_radius), 180, 0, 90, (255,255,255), -1)
    cv2.ellipse(mask, (image.shape[1] - corner_radius, corner_radius), (corner_radius, corner_radius), 270, 0, 90, (255,255,255), -1)
    cv2.ellipse(mask, (corner_radius, image.shape[0] - corner_radius), (corner_radius, corner_radius), 90, 0, 90, (255,255,255), -1)
    cv2.ellipse(mask, (image.shape[1] - corner_radius, image.shape[0] - corner_radius), (corner_radius, corner_radius), 0, 0, 90, (255,255,255), -1)
    
    # Draw the rectangles to fill the interior parts
    cv2.rectangle(mask, (corner_radius, 0), (image.shape[1] - corner_radius, image.shape[0]), (255, 255, 255), -1)
    cv2.rectangle(mask, (0, corner_radius), (image.shape[1], image.shape[0] - corner_radius), (255, 255, 255), -1)
    
    return mask


def build_screen(screen_file, combine_file_name, x_coordinate, sceen_name, text_to_be_added):

    # Load the images
    background = read_image("https://builderbuckets.blob.core.windows.net/builder-now-beta/builderbackground.png")
    overlay = read_image(screen_file)
    mobile = read_image("https://builderbuckets.blob.core.windows.net/builder-now-beta/310x640-with-border-radius.png")

    # Resize overlay to fit inside the mobile screen
    # Assuming the visible screen area dimensions are (280, 520) for the mobile image
    screen_width, screen_height = 284, 609
    overlay = cv2.resize(overlay, (screen_width, screen_height))
    
    # Ensure mobile has an alpha channel
    if mobile.shape[2] < 4:
        mobile = np.dstack([mobile, np.ones((mobile.shape[0], mobile.shape[1]), dtype="uint8") * 255])

    # Overlay the mobile image onto the background
    m_x, m_y, m_w, m_h = x_coordinate, 150, mobile.shape[1], mobile.shape[0]
    roi = background[m_y:m_y+m_h, m_x:m_x+m_w]
    img_blend = cv2.addWeighted(roi, 1, mobile[:, :, 0:3], 1, 0)
    background[m_y:m_y+m_h, m_x:m_x+m_w, 0:3] = img_blend * (mobile[:, :, 3:] / 255.0) + background[m_y:m_y+m_h, m_x:m_x+m_w, 0:3] * (1 - mobile[:, :, 3:] / 255.0)
    
    # Overlay the screen onto the background
    # Assuming the top-left corner of the visible screen area is at position (15, 60) for the mobile image 

    corner_radius = 30
    mask = create_rounded_mask(overlay, corner_radius)

    # Generate the rounded image
    rounded_image = get_rounded_image(overlay, mask) 

    x, y = x_coordinate + 13, 150 + 15
    h_o, w_o, _ = rounded_image.shape  

    # Overlay the rounded image onto the background
    m_x, m_y, m_w, m_h = x_coordinate, 150, rounded_image.shape[1], rounded_image.shape[0]  

    if rounded_image.shape[2] < 4:
        rounded_image = np.dstack([rounded_image, np.ones((rounded_image.shape[0], rounded_image.shape[1]), dtype="uint8") * 255])


    roi = background[y:y+h_o, x:x+w_o]  

    alpha = rounded_image[:, :, 3] / 255.0
    inverse_alpha = 1.0 - alpha  


    blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)
    background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3]  # Only take BGR channels, ignore alpha


    if text_to_be_added:
        # Convert OpenCV image to Pillow format
        pil_image = Image.fromarray(cv2.cvtColor(background, cv2.COLOR_BGR2RGB))
        
        # Load the custom font
        font_path = pkg_resources.resource_filename('video_images_creator', 'Rubik-Medium.ttf')
        font_size = 47
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(pil_image)
        
        max_width = 455  # The maximum width for text
        lines = []
        words = sceen_name.split()
        while words:
            line = ''
            while words and int(draw.textlength(line + words[0], font=font)) <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line)
        
        # Limit to 3 lines
        lines = lines[:3]
        
        y = background.shape[0] - 600
        for i, line in enumerate(lines):
            if x_coordinate == 455:
                x = x_coordinate + 350
            else:
                x = x_coordinate - 400  
            draw.text((x, y + i*font_size), line.strip(), font=font, fill=(255, 255, 255))

        background = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Save and return the modified image
    cv2.imwrite(combine_file_name, background)
    return combine_file_name


def build_screen_optimised(screen_file, combine_file_name, x_coordinate, directory_name, position):
    overlay = read_image(screen_file) 
    screen_width, screen_height = 284, 615
    x, y = x_coordinate + 13, 220 + 15
   
    overlay = cv2.resize(overlay, (screen_width, screen_height))


    if position == 'left':
        background = cv2.imread(f'{directory_name}/combined_left_new.jpg') 
    else:
        background = cv2.imread(f'{directory_name}/combined_right_new.jpg')

    # if position == 'left': 
    #     image_path = pkg_resources.resource_filename('video_images_creator', "combined_left_new.jpg")
    #     background = cv2.imread(image_path) 
    # else:
    #     image_path = pkg_resources.resource_filename('video_images_creator', "combined_right_new.jpg")
    #     background = cv2.imread(image_path)

    corner_radius = 30
    mask = create_rounded_mask(overlay, corner_radius)

    # Generate the rounded image
    rounded_image = get_rounded_image(overlay, mask)
    h_o, w_o, _ = rounded_image.shape 
    blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)
    background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3]  # Only take BGR channels, ignore alpha 

    cv2.imwrite(combine_file_name, background)

    return combine_file_name

def run_ffmpeg_v3(directory_name, uniq_code, temp_text_file, total_duration):
     
    main_audio_path = pkg_resources.resource_filename('video_images_creator', 'audionew.wav') 
    thanks_audio_path = pkg_resources.resource_filename('video_images_creator', 'thanks.wav') 


    jpg_files = glob.glob(os.path.join(directory_name, '*.jpg'))
    number_of_jpg_files = len(jpg_files) 
    #delay_for_thanks = floor( number_of_jpg_files / 60 ) * 1000

    delay_for_thanks = ( floor( total_duration - 3.0 ) ) * 1000

    ffmpeg_command = [
    "ffmpeg",
    "-f", "concat",   # Use the concat demuxer
    "-safe", "0",     # Allow use of absolute paths
    "-i", temp_text_file,  # Specify the input text file
    "-i", main_audio_path,
    "-i", thanks_audio_path,
    "-filter_complex", f"[2:a]adelay={delay_for_thanks}|{delay_for_thanks}[a2];[1:a][a2]amix=inputs=2:duration=longest[aout]",
    "-map", "0:v",  # Map video from the first input (image sequence)
    "-map", "[aout]",  # Map the audio output from the filtergraph
    "-vsync", "vfr",  # Use variable frame rate to avoid frame duplication,
    "-pix_fmt", "yuv420p",
    "-color_primaries", "bt709",
    "-color_trc", "bt709",
    "-colorspace", "bt709",
    "-shortest",
    f"outputs/output_{uniq_code}.mp4"      # Specify the output video file 
    ]

    #print("the delay is", delay_for_thanks)

    #print(ffmpeg_command)

    subprocess.run(ffmpeg_command) 


def run_ffmpeg_v5(directory_name, uniq_code, temp_text_file, tts_output_2_channel_filename, total_duration):

    main_audio_path = pkg_resources.resource_filename('video_images_creator', 'audionew.wav') 
    thanks_audio_path = pkg_resources.resource_filename('video_images_creator', 'thanks.wav')
    background_audio_path = pkg_resources.resource_filename('video_images_creator', 'background_music.wav') 
    intro_outro_video = pkg_resources.resource_filename('video_images_creator', 'intro_outro_v6.mp4')

    jpg_files = glob.glob(os.path.join(directory_name, '*.jpg'))
    number_of_jpg_files = len(jpg_files) 
    #delay_for_thanks = floor( number_of_jpg_files / 60 ) * 1000

    delay_for_thanks = ( floor( total_duration - 3.0 ) ) * 1000

    delay_for_thanks = delay_for_thanks + 14000


    #step 1 create base video

    video_creation_command = [
    "ffmpeg",
    "-y",
    "-f", "concat",  # Use the concat demuxer
    "-safe", "0",  # Allow use of absolute paths
    "-i", temp_text_file,  # Specify the input text file for video
    "-fflags", "+genpts",
    "-pix_fmt", "yuv420p",
    "-color_primaries", "bt709",
    "-color_trc", "bt709",
    "-colorspace", "bt709",
     "-vsync", "vfr", 
    "-preset", "fast",
    f"{directory_name}/base_video.mp4"   # Specify a temporary output video file
    ]
    

    subprocess.run(video_creation_command)
    
    #step 2 , concat video with intro and outro video 

    concat_command = [
        "ffmpeg",
        "-y",
        "-i", intro_outro_video,
        "-i", f"{directory_name}/base_video.mp4",
        "-i", intro_outro_video,
        "-filter_complex", "[0:v]fps=25[v0];[2:v]fps=25[v2];[v0][1:v][v2]concat=n=3:v=1:a=0[outv]",
        "-map", "[outv]",
        "-vsync", "vfr",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-tune", "fastdecode",
        f"{directory_name}/concated_video.mp4"
    ]

    
    subprocess.run(concat_command) 

    #step 3, add audio track to concatenated video 


    audio_addition_command = [
    "ffmpeg",
    "-y",
    "-i", f"{directory_name}/concated_video.mp4",  # Input the temporary video file
    "-i", tts_output_2_channel_filename,  # First audio input
    "-stream_loop", "-1", "-i", background_audio_path,  # Loop this audio file
    "-i", thanks_audio_path,  # Third audio input
    "-filter_complex",
    "[2:a]volume=0.35[looped];"  # Lower the volume of the looped audio
    f"[3:a]adelay={delay_for_thanks}|{delay_for_thanks}[a3];"  # Delay 'thanks.wav'
    "[1:a][looped][a3]amix=inputs=3:duration=longest[aout]",  # Mix all audio inputs
    "-map", "0:v",  # Map video from the first input (created video)
    "-map", "[aout]",  # Map the audio output from the filtergraph
    "-shortest",  # Stop encoding when the shortest input stream ends
    "-c:v", "copy",  # Copy the video stream without re-encoding
    "-c:a", "aac",  # Encode the audio to AAC (efficient and widely supported
    "-vsync", "vfr",
    f"outputs/output_{uniq_code}.mp4"  # Specify the final output video file
    ]


    subprocess.run(audio_addition_command)









def run_ffmpeg_v4(directory_name, uniq_code, temp_text_file, tts_output_2_channel_filename, total_duration):
     
    main_audio_path = pkg_resources.resource_filename('video_images_creator', 'audionew.wav') 
    thanks_audio_path = pkg_resources.resource_filename('video_images_creator', 'thanks.wav')
    background_audio_path = pkg_resources.resource_filename('video_images_creator', 'background_music.wav') 



    jpg_files = glob.glob(os.path.join(directory_name, '*.jpg'))
    number_of_jpg_files = len(jpg_files) 
    #delay_for_thanks = floor( number_of_jpg_files / 60 ) * 1000

    delay_for_thanks = ( floor( total_duration - 3.0 ) ) * 1000

    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-f", "concat",  # Use the concat demuxer
        "-safe", "0",  # Allow use of absolute paths
        "-i", temp_text_file,  # Specify the input text file for video
        "-i", tts_output_2_channel_filename,  # First audio input
        "-stream_loop", "-1", "-i", background_audio_path,  # Loop this audio file
        "-i", thanks_audio_path,  # Third audio input
        "-filter_complex",
        "[2:a]volume=0.35[looped];"  # Lower the volume of the looped audio
        f"[3:a]adelay={delay_for_thanks}|{delay_for_thanks}[a3];"  # Delay 'thanks.wav'
        "[1:a][looped][a3]amix=inputs=3:duration=longest[aout]",  # Mix all audio inputs
        "-map", "0:v",  # Map video from the first input (image sequence)
        "-map", "[aout]",  # Map the audio output from the filtergraph
        "-vsync", "vfr",  # Use variable frame rate to avoid frame duplication
        "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-colorspace", "bt709",
        "-shortest",  # Stop encoding when the shortest input stream ends
        f"outputs/output_{uniq_code}.mp4"  # Specify the output video file 
    ]


    #print("the delay is", delay_for_thanks)

    #print(ffmpeg_command)

    subprocess.run(ffmpeg_command)


def run_ffmpeg_v2(directory_name, uniq_code):
    main_audio_path = pkg_resources.resource_filename('video_images_creator', 'audionew.wav') 
    thanks_audio_path = pkg_resources.resource_filename('video_images_creator', 'thanks.wav') 

    jpg_files = glob.glob(os.path.join(directory_name, '*.jpg'))
    number_of_jpg_files = len(jpg_files) 
    #delay_for_thanks = floor( number_of_jpg_files / 60 ) * 1000

    delay_for_thanks = ( floor( number_of_jpg_files / 60 ) - 2 ) * 1000

    # print(f"ffmpeg -v verbose -y -framerate 60 -i {directory_name}/frame_%d.jpg  -i {main_audio_path} -i {thanks_audio_path} -filter_complex '[2:a]adelay={delay_for_thanks}|{delay_for_thanks}[a2];[1:a][a2]amix=inputs=2:duration=longest[aout]' -map 0:v -map '[aout]' -c:v libx264 -crf 18 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -r 60 -c:a aac -strict experimental -shortest outputs/output_{uniq_code}.mp4")

    os.system(f"ffmpeg -v verbose -y -framerate 60 -i {directory_name}/frame_%d.jpg  -i {main_audio_path} -i {thanks_audio_path} -filter_complex '[2:a]adelay={delay_for_thanks}|{delay_for_thanks}[a2];[1:a][a2]amix=inputs=2:duration=longest[aout]' -map 0:v -map '[aout]' -c:v libx264 -preset ultrafast -crf 18 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -r 60 -c:a aac -strict experimental -shortest outputs/output_{uniq_code}.mp4")



def run_ffmpeg(directory_name, uniq_code): 
    
    audio_path = pkg_resources.resource_filename('video_images_creator', 'instantvideoaudio.wav') 
    os.system(f"ffmpeg -v verbose -y -framerate 60 -i {directory_name}/frame_%d.jpg -i {audio_path} -c:v libx264 -crf 18 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -r 60 -c:a aac -strict experimental -shortest outputs/output_{uniq_code}.mp4")


def flush_video_images(diretory_name, folder_name):
    try:
        #return f"outputs/output_{folder_name}.mp4"
        # Use shutil.rmtree() to remove the entire folder and its contents
        #shutil.rmtree(diretory_name)
        #print(f"Folder '{diretory_name}' and its contents have been deleted.")
        return f"outputs/output_{folder_name}.mp4"
    except Exception as e:
        #print(f"An error occurred: {e}")
        return f"outputs/output_{folder_name}.mp4"

def read_image(image_url):
    resp = urlopen(image_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR) # The image object
    return image 

def ensure_required_directories_existis():
    if not os.path.exists("images"):
        try:
            os.mkdir("images")
        except Exception as e:
            print("Exception occured", e)
    if not os.path.exists("outputs"):
        try:
            os.mkdir("outputs")
        except Exception as e:
            print("Exception occured..", e)


if __name__ == "__main__": 
    project_name = "Design Process"
    image_file_paths = ["video_images_creator/features/launch.png", "video_images_creator/features/first.png","video_images_creator/features/second.png", "video_images_creator/features/third.png", "video_images_creator/features/fourth.png", "video_images_creator/features/fifth.png"] 
    feature_names = ["Splash Screen", "Search", "Dashboard", "Settings", "Profile/Bio", "Analytics" ]
    #image_file_paths = ["video_images_creator/features/launch.png", "video_images_creator/features/first.png", "video_images_creator/features/second.png"]

    build(image_file_paths, feature_names, project_name)