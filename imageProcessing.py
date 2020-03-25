# Name: Omri Ben Tov

import tkinter as tk
from tkinter import *
from tkinter import filedialog
import os
import sys
from PIL import Image, ImageTk
from pathlib import Path
import stat


# This is the main loop of the program. the 'operation' argument is a process function index
def the_process(operation, chosen, targetimagepath,root):
    root.destroy()
    if 0 in operation:
        return rotate_picture(chosen, targetimagepath)
    if 1 in operation :
        return mirrorPicture(chosen, targetimagepath)
    if 2 in operation :
        return edge(chosen, targetimagepath, threshold=20)
    if 3 in  operation :
        return resize(chosen, targetimagepath)
    if 4 in operation:
        return Messi_picture(chosen, targetimagepath)


# In some of the functions i used color image and in some grayscale,
# so the conversion applied in the functions if needed

def rotate_picture(chosen, targetimagepath):
    finalList = []
    new_pic_List = []
    file = 0
    for file in range(len(chosen)):
        photo = Image.open(chosen[file])
        w,h = photo.size
        pixels = photo.load()
        new_pic = photo.copy()
        new_pixels = new_pic.load()
        for i in range(w):
            for j in range(h):
                new_pixels[i , j] = pixels[i , h - j-1]
        file_new_name = chosen[file].split('.')
        finalname = file_new_name[0] + '_processed.' + file_new_name[1] # creates the new file name
        finalList.append(finalname)
        new_pic_List.append(new_pic)
        file = file + 1
    os.chdir(targetimagepath)
    for i in range(len(new_pic_List)):
        for i in range(len(finalList)):
            new_pic_List[i].save(finalList[i])



def mirrorPicture(chosen, targetimagepath):
    finalList = []
    new_pic_List = []
    for file in range(len(chosen)):
        photo = Image.open(chosen[file])
        graypic = photo.convert('L')   # Convert to grayscale
        w,h = graypic.size
        w = w-1
        pixels = graypic.load()
        new_pic  = graypic.copy()
        new_pixels = new_pic.load()
        for i in range(w):
            for j in range(h):
            # Here I copy pixels from the first col of the original image to last one of the new image and repeat
                side = graypic.getpixel((i,j))
                new_pic.putpixel((w,j), side)
            w -= 1

        file_new_name = chosen[file].split('.')
        finalname = file_new_name[0] + '_processed.' + file_new_name[1]
        finalList.append(finalname)
        new_pic_List.append(new_pic)
        file = file + 1
    os.chdir(targetimagepath)
    for i in range(len(new_pic_List)):
        for i in range(len(finalList)):
            new_pic_List[i].save(finalList[i])

def edge(chosen, targetimagepath , threshold):   # Threshold was given by the main process function (20)
    finalList = []
    new_pic_List = []
    for file in range(len(chosen)):
        photo = Image.open(chosen[file])
        graypic = photo.convert('L')
        w, h = graypic.size
        pixels = graypic.load()
        new_pic = graypic.copy()
        new_pixels = new_pic.load()
        for i in range (w-1):
            for j in range (h-1):
                side_margin = abs(pixels[i, j + 1] - pixels[i, j])    # The difference from the pixel to left
                up_margin = abs(pixels[i + 1, j] - pixels[i, j])      # The difference from the pixel above
                if side_margin > threshold:
                    new_pixels[i, j] = 255
                if up_margin > threshold:
                    new_pixels[i, j] = 255
                else:
                    new_pixels[i, j] = 0


        file_new_name = chosen[file].split('.')
        finalname = file_new_name[0] + '_processed.' + file_new_name[1]
        finalList.append(finalname)
        new_pic_List.append(new_pic)
        file = file + 1
    os.chdir(targetimagepath)
    for i in range(len(new_pic_List)):
        for i in range(len(finalList)):
            new_pic_List[i].save(finalList[i])

def resize(chosen,targetimagepath):
    finalList = []
    new_pic_List = []
    for file in range(len(chosen)):
        photo = Image.open(chosen[file])
        graypic = photo.convert('L')
        w, h = graypic.size
        pixels = graypic.load()
        newW = w//2      # setting the size of the new image
        newH = h//2
        new_pic = Image.new('L',(newW,newH))
        new_pixels = new_pic.load()
        for i in range(0, w-1, 2):         # Making a two step to not recalculate the same pixels
            for j in range(0, h-1, 2):
                pixavg = int((pixels[i,j]+pixels[i+1,j]+pixels[i,j+1]+pixels[i+1,j+1])//4)
                new_pixels[(i//2),(j//2)] = pixavg

        file_new_name = chosen[file].split('.')
        finalname = file_new_name[0] + '_processed.' + file_new_name[1]  # creates the new file name
        finalList.append(finalname)
        new_pic_List.append(new_pic)
        file = file + 1
    os.chdir(targetimagepath)
    for i in range(len(new_pic_List)):
        for i in range(len(finalList)):
            new_pic_List[i].save(finalList[i])

# This is the function i invented.
# it creates 8 light blue and white stripes on the image, kind of like a support profile picture on facebook
def Messi_picture(chosen, targetimagepath):
    finalList = []
    new_pic_List = []
    for file in range(len(chosen)):
        photo = Image.open(chosen[file])
        w, h = photo.size
        pixels = photo.load()
        new_pic = photo.copy()
        new_pixels = new_pic.load()
        x = 0
        stripe = w // 8   # This divides the image into stripes of 1/8 of the images width
        while stripe <= w:
            for i in range(x, stripe, 2):
                # Making a 2 step so the image will not turn all blue. one pixel is colored, one isnt and so on...
                for j in range(0, h - 1, 2):
                    new_pixels[i, j] = (0, 150, 220)   # Light blue
            x = x + 2 * (w // 8)
            stripe = stripe + 2 * (w // 8)         # a 2/8 step so there will be place for the white stripes
            i = 0
            j = 0

        x = w // 8      # The white stripes begin from images width // 8
        stripe = 2 * x
        while stripe <= w:
            for i in range(x, stripe, 2):
                for j in range(0, h - 1, 2):
                    new_pixels[i, j] = (255, 255, 255)
            x = x + 2 * (w // 8)
            stripe = stripe + 2 * (w // 8)

        file_new_name = chosen[file].split('.')
        finalname = file_new_name[0] + '_processed.' + file_new_name[1]  # creates the new file name
        finalList.append(finalname)
        new_pic_List.append(new_pic)
        file = file + 1
    os.chdir(targetimagepath)
    for i in range(len(new_pic_List)):
        for i in range(len(finalList)):
            new_pic_List[i].save(finalList[i])
